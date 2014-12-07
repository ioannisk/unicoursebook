from django.db import models
from datetime import datetime

# model to describe university courses


class School(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, default='',
                               help_text='Please enter the url of the School\'s home page')

    def __str__(self):
        return self.title


class Course(models.Model):
    LEVEL_07 = '07'
    LEVEL_08 = '08'
    LEVEL_09 = '09'
    LEVEL_10 = '10'
    LEVEL_CHOICES = (
        (LEVEL_07, '7'),
        (LEVEL_08, '8'),
        (LEVEL_09, '9'),
        (LEVEL_10, '10'),
    )
    SEMESTER_1 = '1'
    SEMESTER_2 = '2'
    SEMESTER_CHOICES = (
        (SEMESTER_1, '1'),
        (SEMESTER_2, '2'),
    )
    school = models.ForeignKey(School)
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_08)
    url = models.URLField(blank=True, default='',
                               help_text='Please enter the url of the course\'s home page')
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

    def __str__(self):
        return '%s (%s)' % (self.title, self.code)


# model to describe feedback on courses
class CourseFeedback(models.Model):
    CHOICE_4 = 'Strongly Agree'
    CHOICE_3 = 'Agree'
    CHOICE_2 = 'Disagree'
    CHOICE_1 = 'Strongly Disagree'
    CHOICE_0 = 'N/A'
    RATING_CHOICES = (
        (0, CHOICE_0),
        (1, CHOICE_1),
        (2, CHOICE_2),
        (3, CHOICE_3),
        (4, CHOICE_4),
    )
    course = models.ForeignKey(Course)
    comment = models.CharField(max_length=1000, default='', blank=True)
    r_course_difficulty = models.IntegerField(choices=RATING_CHOICES, default=0, verbose_name='The course is easy')
    r_course_organization = models.IntegerField(choices=RATING_CHOICES, default=0,
                                                verbose_name='The course is well organized')
    r_tutor_presentation = models.IntegerField(choices=RATING_CHOICES, default=0,
                                               verbose_name='The tutor presentation skills are good')
    r_tutor_support = models.IntegerField(choices=RATING_CHOICES, default=0,
                                          verbose_name='The tutor is helpful with students')
    r_recommendation = models.IntegerField(choices=RATING_CHOICES, default=0, verbose_name='I recommend this course')
    submission_date = models.DateTimeField(default=datetime.now)
    # administrator can mark inappropriate comments as visible=FALSE, so end users don't see them
    visible = models.BooleanField(default=True)



    def __str__(self):
        return '%s (%d)' % (self.comment, self.score())

    def score(self):
        return (self.r_course_difficulty + self.r_course_organization
                + self.r_tutor_presentation + self.r_tutor_support
                + self.r_recommendation) / 5

    class Meta:
        # set default ordering (eg in admin) to most recent first
        ordering = ['-submission_date']


class FeedbackVotes(models.Model):
    CHOICE_1 = 'Like'
    CHOICE_2 = 'Dislike'
    CHOICE_3 = 'Inappropriate'
    VOTE_CHOICES = (
        ('PLUS', CHOICE_1),
        ('MINUS', CHOICE_2),
        ('FLAG', CHOICE_3),
    )
    course_feedback = models.ForeignKey(CourseFeedback)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, default='')