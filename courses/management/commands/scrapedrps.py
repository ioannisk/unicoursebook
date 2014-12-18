from lxml import html
import requests
from django.core.management.base import BaseCommand, CommandError
import re
from courses.models import School, Course

DRPS_URL = 'http://www.drps.ed.ac.uk/14-15/dpt/'


class Command(BaseCommand):
    def handle(self, *args, **options):
        # getting the DRPS page which list all the schools
        schools_index = requests.get(DRPS_URL + 'cx_schindex.htm')
        schools_index_tree = html.fromstring(schools_index.text)
        # After view-page-source we notice that school links share cx_s_su start
        schools_index_nodes = schools_index_tree.xpath('//a[starts-with(@href, "cx_s_su")]')
        for school_index_node in schools_index_nodes:
            school_title = re.search("^([^\(]+)", school_index_node.text).groups()[0]
            school_url = DRPS_URL + school_index_node.attrib['href']
            print school_title, school_index_node.attrib['href']
            old_school_set = School.objects.filter(title=school_title)
            # if school already exists update its URL
            if old_school_set:
                current_school = old_school_set.first()
                current_school.url = school_url
            else:
                current_school = School(title=school_title, url=school_url)
            current_school.save()
            school_detail = requests.get(school_url)
            school_detail_tree = html.fromstring(school_detail.text)
            # After view-page-source we notice that school subschools links share cx_sb start
            schools_detail_nodes = school_detail_tree.xpath('//a[starts-with(@href, "cx_sb")]')
            for school_detail_node in schools_detail_nodes:
                print "-----", school_detail_node.text, school_detail_node.attrib['href']
                course_index = requests.get(DRPS_URL + school_detail_node.attrib['href'])
                course_index_tree = html.fromstring(course_index.text)
                # After view-page-source we notice that school courses links pattern can be found by
                # looking at the schools url and extracting its initials with regex.
                course_code_prefix = re.search("cx_sb_([^\.]+).htm", school_detail_node.attrib['href'])
                if course_code_prefix:
                    prefix = course_code_prefix.groups()[0]
                    course_index_nodes = course_index_tree.xpath(('//a[starts-with(@href, "cx%s")]' % prefix))
                    for course_index_node in course_index_nodes:
                        td_node = course_index_node.getparent()
                        tr_node = td_node.getparent()
                        td_code_node = tr_node.getchildren()[0]
                        course_title = course_index_node.text
                        course_url = DRPS_URL + course_index_node.attrib['href']
                        course_code = td_code_node.text
                        old_course_set = Course.objects.filter(school=current_school, title=course_title)
                        if old_course_set:
                            current_course = old_course_set.first()
                            current_course.url = course_url
                            current_course.code = course_code
                            course_status = "OLD"
                        else:
                            current_course = Course(school=current_school, title=course_title, url=course_url,
                                                    code=course_code)
                            course_status = "NEW"
                        print "----------", course_status, course_title, course_index_node.attrib['href'], course_code
                        current_course.save()