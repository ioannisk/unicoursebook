from django.db import models

# Create your models here.

class Courses(models.Model):
    LEVEL_07 = '07'
    LEVEL_08 = '08'
    LEVEL_09 = '09'
    LEVEL_CHOICES = (
        (LEVEL_07, '7')
        (LEVEL_08, '8')
        (LEVEL_09, '9')
    )
    SEMESTER_1 = '1'
    SEMESTER_2 = '2'
    SEMESTER_CHOICES = (
        (SEMESTER_1, '1')
        (SEMESTER_2, '2')
    )
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_08)
    drps_url = models.URLField
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

