from django.urls import path

from jobs.views import company_main, add_job_ad, job_ads_candidate_view
from jobs.views import company_ads
from jobs.views import change_application_status
from jobs.views import job_ads_candidate_view
from jobs.views import apply_for_job
from jobs.views import career_details
from jobs.views import careers
from jobs.views import delete_job_ad, update_job_ad
from jobs.views import toggle_favorite_candidate
from jobs.views import companies

urlpatterns = [
    path('company/', company_main, name='company_main'),
    path('company/ads/', company_ads, name='company_ads'),
    path('add-job-ad/', add_job_ad, name='add_job_ad'),
    path(
        "applications/<int:application_id>/status/",
        change_application_status,
        name="change_application_status"
    ),

    path('user/ads/', job_ads_candidate_view, name='job_ads_candidate_view'),

    path('apply-for-job/', apply_for_job, name='apply_for_job'),

    path("careers/", careers, name="careers"),
    path("careers/<int:career_id>/", career_details, name="career_details"),

path("company-ads/<int:ad_id>/update/", update_job_ad, name="update_job_ad"),
path("company-ads/<int:ad_id>/delete/", delete_job_ad, name="delete_job_ad"),

path(
    "favorite-candidate/toggle/",
    toggle_favorite_candidate,
    name="toggle_favorite_candidate"
),

path("companies/", companies, name="companies")
]