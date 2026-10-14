from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from accounts.decorators import login_required_custom
from django.contrib.auth import login, logout
from django.http import JsonResponse


from django.http import FileResponse
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from .models import Skill, Career, JobAd, Resource, CareerProject, FavoriteCareer, FavoriteJobAd
from accounts.models import User

def get_current_user(request):
    return User.objects.filter(id=request.session.get('user_id')).first()




def level_to_label(level):
    if level <= 2:
        return 'beginner'
    elif level <= 4:
        return 'intermediate'
    else:
        return 'advanced'

@login_required_custom
def toggle_favourite(request):
    current_user = get_current_user(request)
    if request.method=="POST":
        favourite_type = request.POST.get('type')
        element_id = request.POST.get('id')

        if favourite_type == "career":
            is_favourite = FavoriteCareer.objects.filter(user=current_user, career_id=element_id).exists()
            if is_favourite:
                FavoriteCareer.objects.filter(user=current_user, career_id=element_id).delete()
                is_favourite=False
            else:
                FavoriteCareer.objects.create(user=current_user, career_id=element_id)
                is_favourite=True
            return JsonResponse({'success': True, 'is_favourite': is_favourite})
        
        if favourite_type == "job":
            is_favourite = FavoriteJobAd.objects.filter(user=current_user, job_ad_id=element_id).exists()
            if is_favourite:
                FavoriteJobAd.objects.filter(user=current_user, job_ad_id=element_id).delete()
                is_favourite=False
            else:
                FavoriteJobAd.objects.create(user=current_user, job_ad_id=element_id)
                is_favourite=True

            return JsonResponse({'success': True, 'is_favourite': is_favourite})

        return JsonResponse({'success': False, 'error': 'Invalid type'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required_custom
def favourites(request):
    current_user = get_current_user(request)

    favourite_careers = FavoriteCareer.objects.filter(user=current_user).select_related('career')
    favourite_job_ads = FavoriteJobAd.objects.filter(user=current_user).select_related('job_ad', 'job_ad__company')

    context = {
        'favourite_careers': favourite_careers,
        'favourite_job_ads': favourite_job_ads,
    }
    return render(request, 'careers/favourites.html', context)

@login_required_custom
def download_project(request, project_id):
    project = CareerProject.objects.filter(id=project_id).first()

    if not project:
        messages.error(request, "This project could not be found.")
        return redirect('skill_match')

    if not project.file_path:
        messages.error(request, "The file is not available for download. Please try again later.")
        return redirect('skill_match')

    file_path = Path(settings.MEDIA_ROOT) / project.file_path

    if not file_path.exists():
        messages.error(request, "The file could not be found on the server. Please try again later.")
        return redirect('skill_match')

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_path.name)
    

@login_required_custom
def skill_match(request):

    combined_matching=[] #contains 'type','match_percentage', plus career/job_ad specific data

    show_careers=True
    show_jobs=True

    #loading 
    if request.method=="POST":
        current_user = get_current_user(request)
        favorited_career_ids = FavoriteCareer.objects.filter(user=current_user).values_list('career_id', flat=True)
        favorited_job_ad_ids = FavoriteJobAd.objects.filter(user=current_user).values_list('job_ad_id', flat=True)


        show_careers = 'show_careers' in request.POST
        show_jobs = 'show_jobs' in request.POST

        user_selected_skills={}
        for key, value in request.POST.items():
            if key.startswith("skill-"):
                id=int(key.replace('skill-',''))
                user_selected_skills[id] = int(value)

        
        if show_careers:
            for career in Career.objects.prefetch_related('career_skills__skill'):
                career_skills=list(career.career_skills.all())

                if not career_skills:
                    continue

                number_of_skills=sum(1 for cs in career_skills)
                career_match=0
                skill_matching=[]
                
                for cs in career_skills:
                    user_level=user_selected_skills.get(cs.skill_id,0)
                    career_level=cs.required_level
                    matching_percent=min(user_level,career_level)/career_level
                    career_match+=matching_percent/number_of_skills
                    gap = max(0, career_level - user_level)
                    labeled_level=level_to_label(career_level)
                    skill_matching.append({
                        'skill_name': cs.skill.name,
                        'user_level': user_level,
                        'career_level': career_level,
                        'user_level_percentage':round(user_level / 5 * 100),
                        'career_level_percentage':round(career_level / 5 * 100),
                        'gap': gap,
                        'missing_skills_resources': list(Resource.objects.filter(skill_id=cs.skill_id, level=labeled_level)) if user_level < career_level else []
                    })

                    
                    

                
                career_match_percentage=round(career_match * 100)
                has_missing_resources = any(skill["missing_skills_resources"] for skill in skill_matching)
                combined_matching.append({
                    'type':'career',
                    'match_percentage':career_match_percentage,
                    'career':career,
                    'skills_match':skill_matching,
                    'has_missing_resources':has_missing_resources,
                    'projects': list(CareerProject.objects.filter(career=career)),
                    'is_favorited': career.id in favorited_career_ids
                })

        if show_jobs:
            for job_ad in JobAd.objects.filter(status='active').prefetch_related('jobadskill_set__skill', 'company'):
                job_ad_skills=list(job_ad.jobadskill_set.all())

                if not job_ad_skills:
                    continue

                number_of_skills=sum(1 for jas in job_ad_skills)
                job_match=0
                skill_matching=[]
                for jas in job_ad_skills:
                    user_level=user_selected_skills.get(jas.skill_id,0)
                    career_level=jas.required_level
                    matching_percent=min(user_level,career_level)/career_level
                    job_match+=matching_percent/number_of_skills
                    labeled_level=level_to_label(career_level)

                    skill_matching.append({
                        'skill_name': jas.skill.name,
                        'user_level': user_level,
                        'career_level': career_level,
                        'user_level_percentage':round(user_level / 5 * 100),
                        'career_level_percentage':round(career_level / 5 * 100),
                        'gap': max(0, career_level - user_level),
                        'missing_skills_resources': list(Resource.objects.filter(skill_id=jas.skill_id,level=labeled_level)) if user_level < career_level else []
                    })

                job_match_percentage=round(job_match * 100)
                has_missing_resources = any(skill["missing_skills_resources"] for skill in skill_matching)

                combined_matching.append({
                    'type':'job',
                    'match_percentage':job_match_percentage,
                    'job_ad':job_ad,
                    'skills_match':skill_matching,
                    'has_missing_resources': has_missing_resources,
                    'is_favorited': job_ad.id in favorited_job_ad_ids
                })

        combined_matching.sort(key=lambda x: x['match_percentage'],reverse=True)


    context={
        'skills':Skill.objects.all().order_by('name'),
        'combined_matching':combined_matching,
        'show_careers':show_careers,
        'show_jobs':show_jobs
    }

    return render(request,'careers/skill_match.html',context)

def index(request):
    """Root path of the application.

        If the user is logged in, redirects them to the list of all quizzes,
        otherwise to the login page.
        """
    if request.user.is_authenticated:
        return redirect('home_user')
    return redirect('login')

def registration_view(request):
    """Registers a new user.

       Uses Django's built-in UserCreationForm. After a successful
       registration the user is logged in automatically and taken to the list of quizzes.
       """
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home_user')
    else:
        form=UserCreationForm()
    return render(request,'careers/registration.html',{'form':form})

def logout_view(request):
    """Logs out the current user and returns them to the login page."""
    logout(request)
    return redirect("login")


def home_user(request):
    return render(request,'careers/home_user.html',{})