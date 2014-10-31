from django.db import models


class Course(models.Model):
    LEVEL_07 = '07'
    LEVEL_08 = '08'
    LEVEL_09 = '09'
    LEVEL_CHOICES = (
        (LEVEL_07, '7'),
        (LEVEL_08, '8'),
        (LEVEL_09, '9'),
    )
    SEMESTER_1 = '1'
    SEMESTER_2 = '2'
    SEMESTER_CHOICES = (
        (SEMESTER_1, '1'),
        (SEMESTER_2, '2'),
    )
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_08)
    drps_url = models.URLField(blank=True, default='',
                               verbose_name='DRPS url',
                               help_text='Please enter the url of the course\'s DRPS page')
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)


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
    r_course_difficulty = models.IntegerField(choices=RATING_CHOICES, default=0)
    r_course_organization = models.IntegerField(choices=RATING_CHOICES, default=0)
    r_tutor_presentation = models.IntegerField(choices=RATING_CHOICES, default=0)
    r_tutor_support = models.IntegerField(choices=RATING_CHOICES, default=0)
    r_recommendation = models.IntegerField(choices=RATING_CHOICES, default=0)
    visible = models.BooleanField(default=True)
    #todo add user info


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
    #todo add user info