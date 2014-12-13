from lxml import html
import requests
from django.core.management.base import BaseCommand, CommandError
import re
from courses.models import School, Course

DRPS_URL = 'http://www.drps.ed.ac.uk/14-15/dpt/'

class Command(BaseCommand):

    def handle(self, *args, **options):
        schools_index = requests.get(DRPS_URL+'cx_schindex.htm')
        schools_index_tree = html.fromstring(schools_index.text)
        schools_index_nodes = schools_index_tree.xpath('//a[starts-with(@href, "cx_s_su")]')
        for school_index_node in schools_index_nodes:
            print school_index_node.text, school_index_node.attrib['href']
            new_school = School(title=school_index_node.text, url=DRPS_URL+school_index_node.attrib['href'])
            new_school.save()
            school_detail = requests.get(DRPS_URL+school_index_node.attrib['href'])
            school_detail_tree = html.fromstring(school_detail.text)
            schools_detail_nodes = school_detail_tree.xpath('//a[starts-with(@href, "cx_sb")]')
            for school_detail_node in schools_detail_nodes:
                print "-----", school_detail_node.text, school_detail_node.attrib['href']
                course_index = requests.get(DRPS_URL+school_detail_node.attrib['href'])
                course_index_tree = html.fromstring(course_index.text)
                course_code_prefix = re.search("cx_sb_([^\.]+).htm", school_detail_node.attrib['href'])
                if course_code_prefix:
                    prefix = course_code_prefix.groups()[0]
                    course_index_nodes = course_index_tree.xpath(('//a[starts-with(@href, "cx%s")]' % prefix))
                    for course_index_node in course_index_nodes:
                        td_node = course_index_node.getparent()
                        tr_node = td_node.getparent()
                        td_code_node = tr_node.getchildren()[0]
                        print "----------", course_index_node.text, course_index_node.attrib['href'], td_code_node.text
                        new_course = Course(school=new_school, title=course_index_node.text, url=DRPS_URL+course_index_node.attrib['href']
                                            , code=td_code_node.text)
                        new_course.save()