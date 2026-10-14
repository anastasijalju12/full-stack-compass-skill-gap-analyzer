from datetime import date, timedelta, timezone

from accounts.models import User
from careers.models import JobAd
from jobs.models import FavoriteCandidate


def my_active_adds(id):
    return JobAd.objects.filter(company_id=id, status='active')

def my_inactive_adds(id):
    return JobAd.objects.filter(company_id=id, status='inactive')

def my_all_ads(id):
    return JobAd.objects.filter(company_id=id)

def my_soon_will_expire_ads(id, num_of_days):
    limit = date.today() + timedelta(days=num_of_days)
    return JobAd.objects.filter(company_id=id, status='active',
                                application_deadline__gte = date.today(),
                                application_deadline__lte = limit)

def my_ads_applications_opened(id):
    return JobAd.objects.filter(company_id=id, status='active',
                                application_deadline__gte = date.today())

def my_ads_applications_closed(id):
    return JobAd.objects.filter(company_id=id, status='active',
                                application_deadline__lt=date.today())

def get_candidates(applications_queryset):
    candidate_ids = applications_queryset.values_list('user_id', flat=True).distinct()
    return User.objects.filter(id__in=candidate_ids)

def mark_favorite_candidates_on_ads(ads, company_id):
    favorite_pairs = set(
        FavoriteCandidate.objects
        .filter(company_id=company_id)
        .values_list("user_id", "job_ad_id")
    )

    application_lists = [
        "accepted_applications",
        "active_applications",
        "denied_applications",
    ]

    for ad in ads:
        for list_name in application_lists:
            applications = getattr(ad, list_name, [])

            for application in applications:
                application.is_favorite_candidate = (
                    application.user_id,
                    ad.id
                ) in favorite_pairs

    return ads

def mark_favorite_candidates(ads, company_id):
    favorite_pairs = set(
        FavoriteCandidate.objects
        .filter(company_id=company_id)
        .values_list("user_id", "job_ad_id")
    )

    for ad in ads:
        for application in getattr(ad, "candidates", []):
            application.is_favorite_candidate = (
                application.user_id,
                ad.id
            ) in favorite_pairs

    return ads