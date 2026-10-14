from django.contrib import messages
from django.db.models import Aggregate, CharField, Value, Prefetch, Model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date
from django.db.models import Q, Count
from django.views.decorators.http import require_POST

import jobs.helper_functions.helper_functions as hf
from jobs.forms import AddJobAdForm, ApplyForJobForm

from jobs.models import (JobAd, Application, Career,
                         User, Company, JobAdSkill, Skill,
                         FavoriteCandidate)

# Create your views here.

class GroupConcat(Aggregate):
    function = "GROUP_CONCAT"
    template = "%(function)s(DISTINCT %(expressions)s SEPARATOR ', ')"
    output_field = CharField()

def company_main(request):
    context = {}
    my_id = request.session['company_id']
    #my_id = 1

    # forms on page
    context["form"] = AddJobAdForm()

    active_ads = hf.my_active_adds(my_id)
    # setting company name - welcome message
    context["company_name"] = Company.objects.get(id=my_id).name
    # setting number of active ads
    context["active_ads_num"] = len(active_ads)

    # setting number of candidates who applied today
    today = date.today()
    recent_candidates = hf.get_candidates(
        Application.objects.filter(
            applied_at__date=today,
            job_ad_id__company_id=my_id
        )
    )
    context["new_candidates_num"] = len(recent_candidates)

    # getting all active ads with number of applications
    active_ads_with_num = active_ads.annotate(num_candidates=Count('application'))
    context["active_ads_with_num"] = active_ads_with_num

    # setting number of (current) candidates - applied for active ads
    chosen_applications = Application.objects.filter(job_ad_id__in=active_ads)
    context["candidates_num"] = len(hf.get_candidates(chosen_applications))

    # setting number of ads whose deadline is soon
    context["ads_expires_soon_num"] = len(hf.my_soon_will_expire_ads(my_id, 7))

    # more details about clients that applied today
    recent_candidates_with_adds = (recent_candidates
    .filter(application__job_ad__company_id=my_id)
    .annotate(
        adds=GroupConcat('application__job_ad__name')
    ).distinct())
    context["recent_candidates"] = recent_candidates_with_adds

    # active ads and lists of their candidates
    active_ads_with_cands = active_ads.prefetch_related(
        Prefetch(
            'application_set',
            queryset=Application.objects.exclude(status="withdrawn"),
            to_attr='candidates'
        )
    )

    active_ads_with_cands = list(active_ads_with_cands)
    hf.mark_favorite_candidates(active_ads_with_cands, my_id)

    context["active_ads_with_cands"] = active_ads_with_cands

    context['skills'] = Skill.objects.all()

    return render(request, 'company_main.html', context)

def add_job_ad(request):
    if request.method == 'POST':
        form = AddJobAdForm(request.POST)

        if JobAd.objects.filter(name=request.POST.get('name')).exists():
            messages.error(request, 'A job ad with the same name already exists.')
            return redirect(request.META.get('HTTP_REFERER', 'company_main'))

        if form.is_valid():
            ad = form.save(commit=False)
            ad.status = 'pending'
            ad.company_id = request.session['company_id']
            #ad.company_id = 1
            ad.save()

            selected_skill_ids = request.POST.getlist("skills")

            for skill_id in selected_skill_ids:
                level = request.POST.get(f"skill_level_{skill_id}")

                JobAdSkill.objects.create(
                    job_ad=ad,
                    skill_id=skill_id,
                    required_level=level
                )

            messages.success(request, 'The request has been sent successfully and is waiting for administrator approval.')
            return redirect(request.META.get('HTTP_REFERER', 'company_main'))
        else:
            messages.error(request, 'The entered data is not valid. Please try again.')
            return redirect(request.META.get('HTTP_REFERER', 'company_main'))

    return redirect(request.META.get('HTTP_REFERER', 'company_main'))

@require_POST
def update_job_ad(request, ad_id):
    ad = JobAd.objects.get(id=ad_id)
    form = AddJobAdForm(request.POST, instance=ad)

    if form.is_valid():
        form.save()

        JobAdSkill.objects.filter(job_ad=ad).delete()

        selected_skill_ids = request.POST.getlist("skills")

        for skill_id in selected_skill_ids:
            level = request.POST.get(f"skill_level_{skill_id}")

            JobAdSkill.objects.create(
                job_ad=ad,
                skill_id=skill_id,
                required_level=level
            )

        messages.success(request, "The job ad has been updated successfully.")
    else:
        messages.error(request, "An error occurred while updating the job ad.")

    return redirect("company_ads")

@require_POST
def delete_job_ad(request, ad_id):
    ad = JobAd.objects.get(id=ad_id)

    ad.delete()

    messages.success(request, "The job ad has been deleted successfully.")

    return redirect("company_ads")

def company_ads(request):
    context = {}

    my_id = request.session['company_id']
    #my_id = 1

    context['form'] = AddJobAdForm()
    context['skills'] = Skill.objects.all()
    context['logo_path'] = Company.objects.get(id=my_id).logo_path

    ads = hf.my_all_ads(my_id).prefetch_related(
        Prefetch(
            'application_set',
            queryset=Application.objects
                .filter(status='accepted')
                .select_related('user'),
            to_attr='accepted_applications'
        ),
        Prefetch(
            'application_set',
            queryset=Application.objects
                .filter(status='active')
                .select_related('user'),
            to_attr='active_applications'
        ),
        Prefetch(
            'application_set',
            queryset=Application.objects
                .filter(status='denied')
                .select_related('user'),
            to_attr='denied_applications'
        ),
        Prefetch(
            'application_set',
            queryset=JobAdSkill.objects
                .filter(job_ad_id__company_id=my_id)
                .select_related("skill"),
            to_attr='required_skills'
        )
    )

    ads = list(ads)

    hf.mark_favorite_candidates_on_ads(ads, my_id)

    context['ads'] = ads

    return render(request, 'company_ads.html', context)

@require_POST
def change_application_status(request, application_id):
    application = Application.objects.get(id=application_id)
    new_status = request.POST.get('status')
    allowed_statuses = ['active', 'accepted', 'denied']

    if new_status in allowed_statuses:
        application.status = new_status
        application.save()

    # if request is AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "ok": True,
            "new_status": application.status,
            "new_status_display": application.get_status_display(),
            "message": "The status has been updated successfully."
        })
    return redirect('company_ads')

def job_ads_candidate_view(request):
    context = {}
    context['ads'] = JobAd.objects.filter(status='active')
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.filter(id=user_id).first()
        default_data = {
            'first_last_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'contact_number': user.contact,
            'education': "npr. ETF Beograd",
            'skills': [],
            'cover_message': "",
        }
        context['form'] = ApplyForJobForm(initial=default_data)
    else:
        context['form'] = ApplyForJobForm()

    return render(request, 'job_ads_candidate_view.html', context)

def apply_for_job(request):
    user_id = request.session['user_id']
    #user_id = 1
    if request.method == 'POST':
        job_ad_id = request.POST.get("ad_id")

        if Application.objects.filter(user_id=user_id, job_ad_id=job_ad_id).exists():
            messages.error(request, 'You have already applied for this job ad.')
            return redirect(request.META.get('HTTP_REFERER', 'job_ads_candidate_view'))

        form = ApplyForJobForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True, user_id=user_id, job_ad_id=job_ad_id)
            messages.success(request, 'Your application has been submitted successfully.')
        else:
            print("FORM ERRORS:", form.errors.as_data())
            messages.error(request, 'The entered data is not valid. Please try again.')
    return redirect(request.META.get('HTTP_REFERER', 'job_ads_candidate_view'))

def careers(request):
    careers = Career.objects.all().order_by("name")

    context = {
        "careers": careers
    }

    return render(request, "careers.html", context)


def career_details(request, career_id):
    career = Career.objects.get(id=career_id)

    context = {
        "career": career
    }

    return render(request, "career_details.html", context)

@require_POST
def toggle_favorite_candidate(request):
    #my_id = request.session['company_id']
    my_id = 1
    from django.conf import settings
    from django.db import connection

    print("DJANGO DATABASE NAME:", settings.DATABASES["default"]["NAME"])
    print("DJANGO DB HOST:", settings.DATABASES["default"].get("HOST"))
    print("DJANGO DB USER:", settings.DATABASES["default"].get("USER"))
    print("REAL DATABASE:", connection.settings_dict["NAME"])

    user_id = request.POST.get("user_id")
    job_ad_id = request.POST.get("job_ad_id")

    print("DJANGO TABLE:", FavoriteCandidate._meta.db_table)
    print("USER:", user_id)
    print("JOB AD:", job_ad_id)

    if not user_id or not job_ad_id:
        return JsonResponse({
            "ok": False,
            "error": "Missing user_id or job_ad_id."
        }, status=400)

    job_ad = JobAd.objects.get(
        id=job_ad_id,
        company_id=my_id
    )

    favorite = FavoriteCandidate.objects.filter(
        company_id=my_id,
        user_id=user_id,
        job_ad_id=job_ad.id
    ).first()

    if favorite:
        print("Found an existing favorite, deleting it.")
        favorite.delete()
        is_favorite = False
    else:
        print("No favorite exists, creating it.")
        FavoriteCandidate.objects.create(
            company_id=my_id,
            user_id=user_id,
            job_ad_id=job_ad.id
        )
        is_favorite = True

    exists_after = FavoriteCandidate.objects.filter(
        company_id=my_id,
        user_id=user_id,
        job_ad_id=job_ad.id
    ).exists()

    count_after = FavoriteCandidate.objects.filter(
        company_id=my_id,
        user_id=user_id,
        job_ad_id=job_ad.id
    ).count()

    print("IS_FAVORITE:", is_favorite)
    print("EXISTS AFTER:", exists_after)
    print("COUNT POSLE:", count_after)

    return JsonResponse({
        "ok": True,
        "is_favorite": is_favorite,
        "exists_after": exists_after,
        "count_after": count_after,
        "user_id": int(user_id),
        "job_ad_id": int(job_ad.id),
    })


def companies(request):
    companies = Company.objects.filter(status="active").order_by("name")
    context = {
        "companies": companies,
    }

    return render(request, "companies.html", context)