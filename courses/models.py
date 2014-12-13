from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# model to describe university courses


class School(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, default='',
                               help_text='Please enter the url of the School\'s home page')

    def __str__(self):
        return self.title


class Course(models.Model):
    school = models.ForeignKey(School)
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, default='',
                               help_text='Please enter the url of the course\'s home page')


    def __str__(self):
        return '%s (%s)' % (self.title, self.code)

    def score(self):
        course_feedbacks = self.coursefeedback_set.all()
        total_score = 0.0
        total_feedbacks = 0.0
        for feedback in course_feedbacks.iterator():    # iterator improves performance
            total_score += feedback.score()
            total_feedbacks += 1
        return total_score/total_feedbacks if total_feedbacks > 0 else 0

# model to describe feedback on courses
class CourseFeedback(models.Model):
    CHOICE_4 = 5
    CHOICE_3 = 2
    CHOICE_2 = -2
    CHOICE_1 = -5
    CHOICE_0 = 0
    RATING_CHOICES = (
        (CHOICE_0, 'N/A'),
        (CHOICE_1, 'Strongly Disagree'),
        (CHOICE_2, 'Disagree'),
        (CHOICE_3, 'Agree'),
        (CHOICE_4, 'Strongly Agree'),
    )
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    comment = models.TextField(max_length=1000, default='', blank=True)
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
        return (25*self.r_course_difficulty + 10*self.r_course_organization
                + 25*self.r_tutor_presentation + 10*self.r_tutor_support
                + 30*self.r_recommendation) / 100

    class Meta:
        # set default ordering (eg in admin) to most recent first
        ordering = ['-submission_date']
        # allow 1 feedback on a course per user
        unique_together = (("course", "user"),)


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


#Model to describe users
class UserProfile(models.Model):

    # this line will link UserProfile to a User model
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username