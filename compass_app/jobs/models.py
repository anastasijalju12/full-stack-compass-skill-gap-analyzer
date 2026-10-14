import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from careers.models import JobAd, Application, Career, JobAdSkill, Skill
from accounts.models import Company, User


class FavoriteCandidate(models.Model):
    pk = models.CompositePrimaryKey('company_id', 'user_id', 'job_ad_id')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'favorite_candidate'