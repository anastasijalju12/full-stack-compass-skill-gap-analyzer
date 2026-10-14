from django.db import models
from django.db.models.functions import Now

from accounts.models import User, Company
from decimal import Decimal


class Career(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'career'


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'skill'


class CareerSkill(models.Model):
    pk = models.CompositePrimaryKey('career_id', 'skill_id')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="career_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.IntegerField()
    weight = models.DecimalField(max_digits=3, decimal_places=2, db_default=Decimal('1.00'))

    class Meta:
        managed = True
        db_table = 'career_skill'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(required_level__gte=1) & models.Q(required_level__lte=5),
                name='career_skill_level_chk',
            ),
        ]


class UserSkill(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'skill_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_skill'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(level__gte=1) & models.Q(level__lte=5),
                name='user_skill_level_chk',
            ),
        ]


class Resource(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=500, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'resource'

    def __str__(self):
        return self.name


class CareerProject(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'career_project'


class JobAd(models.Model):
    TYPE_CHOICES = [
        ('internship', 'internship'),
        ('junior', 'junior'),
    ]
    STATUS_CHOICES = [
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('pending', 'pending'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    location = models.CharField(max_length=150, blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, db_default=Now())
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=True, null=True, db_default='pending')
    removal_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'job_ad'


class JobAdSkill(models.Model):
    pk = models.CompositePrimaryKey('job_ad_id', 'skill_id')
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'job_ad_skill'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(required_level__gte=1) & models.Q(required_level__lte=5),
                name='job_ad_skill_level_chk',
            ),
        ]

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

CUSTOM_CV_PATH = os.path.join(settings.BASE_DIR, 'jobs', 'media', 'cvs')


class Application(models.Model):
    STATUS_CHOICES = [
        ('active', 'aktivna'),
        ('withdrawn', 'povučena'),
        ('accepted', 'prihvaćena'),
        ('denied', 'odbijena')
    ]
    cv_storage = FileSystemStorage(location=CUSTOM_CV_PATH, base_url='/custom-cvs/')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(db_default=Now())
    cv_path = models.FileField(blank=True, null=True, storage=cv_storage, upload_to='')
    skills = models.CharField(max_length=500, blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    cover_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, db_default='active')


    class Meta:
        managed = True
        db_table = 'application'
        unique_together = (('user', 'job_ad'),)


class FavoriteCareer(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'career_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'favorite_career'


class FavoriteJobAd(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'job_ad_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'favorite_job_ad'

