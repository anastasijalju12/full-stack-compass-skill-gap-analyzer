"""
Author: Milica Pavlovic, student ID: 2023/0148

Views for the administration module:
dashboard, account management, company registrations, and moderation.
"""
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from accounts.models import Administrator,User, Company
from careers.models import Career, CareerSkill, JobAd, Skill
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from decimal import Decimal, InvalidOperation
from django.db import transaction
from accounts.forms import (
    CompanyRegistrationForm,
    UserRegistrationForm,
)

from accounts.decorators import role_required

@role_required('admin')
def dashboard(request):
    """Displays the administration dashboard and system statistics.

    Returns:
        HttpResponse: Rendered administration home page with counts for
        pending company requests, job ads awaiting review, active accounts,
        and careers.
    """

    pending_companies_count = Company.objects.filter(status='pending').count()
    pending_job_ads_count = JobAd.objects.filter(status='pending').count()

    active_accounts_count = (
        User.objects.filter(status='active').count()
        + Company.objects.filter(status='active').count()
    )

    careers_count = Career.objects.count()

    context = {
        'pending_companies_count': pending_companies_count,
        'pending_job_ads_count': pending_job_ads_count,
        'active_accounts_count': active_accounts_count,
        'careers_count': careers_count,
    }

    return render(request, 'administration/dashboard.html', context)

@role_required('admin')
def create_account(request):
    """Allows an administrator to create a user or company account.

    Uses the existing registration forms from the accounts application.
    Accounts created by an administrator are activated immediately.
    """

    selected_type = request.GET.get('type', 'user')

    user_form = UserRegistrationForm(prefix='user')
    company_form = CompanyRegistrationForm(prefix='company')

    if request.method == 'POST':
        selected_type = request.POST.get('account_type', 'user')

        if selected_type == 'user':
            user_form = UserRegistrationForm(
                request.POST,
                prefix='user',
            )

            if user_form.is_valid():
                username = user_form.cleaned_data['username']
                email = user_form.cleaned_data['email']

                if Company.objects.filter(username=username).exists():
                    user_form.add_error(
                        'username',
                        'This username is already used by a company.',
                    )

                if Company.objects.filter(email=email).exists():
                    user_form.add_error(
                        'email',
                        'An account with this email address already exists.',
                    )

                if not user_form.errors:
                    user = User.objects.create(
                        first_name=user_form.cleaned_data['first_name'],
                        last_name=user_form.cleaned_data['last_name'],
                        username=username,
                        email=email,
                        contact=user_form.cleaned_data.get('contact'),
                        password=make_password(
                            user_form.cleaned_data['password']
                        ),
                        status='active',
                        role='user',
                    )

                    messages.success(
                        request,
                        (
                            f'The user account for “'
                            f'{user.first_name} {user.last_name}” '
                            f'was created successfully.'
                        ),
                    )

                    create_account_url = reverse(
                        'administration:create_account'
                    )

                    return redirect(
                        f'{create_account_url}?type=user'
                    )

        elif selected_type == 'company':
            company_form = CompanyRegistrationForm(
                request.POST,
                prefix='company',
            )

            if company_form.is_valid():
                username = company_form.cleaned_data['username']
                email = company_form.cleaned_data['email']

                if User.objects.filter(username=username).exists():
                    company_form.add_error(
                        'username',
                        'This username is already used by another account.',
                    )

                if User.objects.filter(email=email).exists():
                    company_form.add_error(
                        'email',
                        'An account with this email address already exists.',
                    )

                if not company_form.errors:
                    company = Company.objects.create(
                        name=company_form.cleaned_data['name'],
                        username=username,
                        email=email,
                        industry=company_form.cleaned_data.get('industry'),
                        contact=company_form.cleaned_data.get('contact'),
                        description=company_form.cleaned_data.get(
                            'description'
                        ),
                        password=make_password(
                            company_form.cleaned_data['password']
                        ),
                        status='active',
                        rejection_reason=None,
                    )

                    messages.success(
                        request,
                        (
                            f'The company account for “{company.name}” '
                            f'was created and activated successfully.'
                        ),
                    )

                    create_account_url = reverse(
                        'administration:create_account'
                    )

                    return redirect(
                        f'{create_account_url}?type=company'
                    )

        else:
            messages.error(
                request,
                'An unknown account type was selected.',
            )
            selected_type = 'user'

    users = User.objects.order_by(
        'first_name',
        'last_name',
    )

    companies = Company.objects.order_by('name')

    context = {
        'user_form': user_form,
        'company_form': company_form,
        'selected_type': selected_type,
        'users': users,
        'companies': companies,
    }

    return render(
        request,
        'administration/create_account.html',
        context,
    )

@role_required('admin')
def company_requests(request):
    """Displays company registration requests and the decision history.

    The company being reviewed is selected through the ``company`` GET parameter.
    Applications with the ``pending`` status are shown as unprocessed, while
    approved and rejected companies are shown in the decision history.
    """

    pending_companies = Company.objects.filter(
        status='pending'
    ).order_by('name')

    processed_companies = Company.objects.exclude(
        status='pending'
    ).order_by('name')

    selected_company = None
    selected_company_id = request.GET.get('company')

    if selected_company_id:
        selected_company = get_object_or_404(
            Company,
            pk=selected_company_id,
        )

    context = {
        'pending_companies': pending_companies,
        'processed_companies': processed_companies,
        'selected_company': selected_company,
    }

    return render(
        request,
        'administration/company_requests.html',
        context,
    )
@require_POST
@role_required('admin')
def approve_company(request, company_id):
    """Approves a company registration and activates its account."""

    company = get_object_or_404(Company, pk=company_id)

    company.status = 'active'
    company.rejection_reason = None
    company.save(
        update_fields=['status', 'rejection_reason']
    )

    messages.success(
        request,
        f'The registration for “{company.name}” was approved successfully.',
    )

    return redirect('administration:company_requests')


@require_POST
@role_required('admin')
def reject_company(request, company_id):
    """Rejects a company registration and requires a rejection reason."""

    company = get_object_or_404(Company, pk=company_id)
    rejection_reason = request.POST.get(
        'rejection_reason',
        '',
    ).strip()

    if not rejection_reason:
        messages.error(
            request,
            'You must enter a reason for rejecting the registration.',
        )

        company_requests_url = reverse(
            'administration:company_requests'
        )

        return redirect(
            f'{company_requests_url}?company={company.id}'
        )

    company.status = 'rejected'
    company.rejection_reason = rejection_reason
    company.save(
        update_fields=['status', 'rejection_reason']
    )

    messages.success(
        request,
        f'The registration for “{company.name}” was rejected.',
    )

    return redirect('administration:company_requests')


@require_POST
@role_required('admin')
def keep_company_pending(request, company_id):
    """Keeps a company application in the pending state."""

    company = get_object_or_404(Company, pk=company_id)

    company.status = 'pending'
    company.rejection_reason = None
    company.save(
        update_fields=['status', 'rejection_reason']
    )

    messages.info(
        request,
        f'The application for “{company.name}” remains pending.',
    )

    company_requests_url = reverse(
        'administration:company_requests'
    )

    return redirect(
        f'{company_requests_url}?company={company.id}'
    )

@role_required('admin')
def moderation(request):
    """Displays job ads for review and the moderation history.

    Active and pending job ads can be reviewed and moderated.
    Inactive job ads are shown in the moderation history.
    """

    ads_for_review = (
        JobAd.objects
        .filter(status__in=['pending', 'active'])
        .select_related('company')
        .order_by('application_deadline', 'name')
    )

    moderated_ads = (
        JobAd.objects
        .filter(status='inactive')
        .select_related('company')
        .order_by('-updated_at', 'name')
    )

    selected_ad = None
    selected_ad_id = request.GET.get('ad')

    if selected_ad_id:
        selected_ad = get_object_or_404(
            JobAd.objects.select_related('company'),
            pk=selected_ad_id,
        )

    context = {
        'ads_for_review': ads_for_review,
        'moderated_ads': moderated_ads,
        'selected_ad': selected_ad,
        'today': timezone.localdate(),
    }

    return render(
        request,
        'administration/moderation.html',
        context,
    )
@require_POST
@role_required('admin')
def remove_job_ad(request, job_ad_id):
    """Removes a job ad from public listings."""

    job_ad = get_object_or_404(JobAd, pk=job_ad_id)
    admin_note = request.POST.get('admin_note', '').strip()

    if not admin_note:
        messages.error(
            request,
            'You must enter a reason for removing the job ad.'
        )
        return redirect(
            f"{reverse('administration:moderation')}?ad={job_ad.id}"
        )

    job_ad.status = 'inactive'
    job_ad.removal_reason = admin_note
    job_ad.updated_at = timezone.now()

    job_ad.save(
        update_fields=[
            'status',
            'removal_reason',
            'updated_at',
        ]
    )

    messages.success(
        request,
        f'The job ad “{job_ad.name}” was removed from public listings.',
    )

    return redirect('administration:moderation')
@require_POST
@role_required('admin')
def mark_job_ad_outdated(request, job_ad_id):
    """Marks a job ad as outdated and removes it from public listings."""

    job_ad = get_object_or_404(JobAd, pk=job_ad_id)
    admin_note = request.POST.get('admin_note', '').strip()

    removal_reason = 'Outdated job ad.'

    if admin_note:
        removal_reason = f'{removal_reason} {admin_note}'

    job_ad.status = 'inactive'
    job_ad.removal_reason = removal_reason
    job_ad.updated_at = timezone.now()

    job_ad.save(
        update_fields=[
            'status',
            'removal_reason',
            'updated_at',
        ]
    )

    messages.success(
        request,
        f'The job ad “{job_ad.name}” was marked as outdated.',
    )

    return redirect('administration:moderation')
@require_POST
@role_required('admin')
def keep_job_ad_active(request, job_ad_id):
    """Keeps a job ad active and visible to users."""

    job_ad = get_object_or_404(JobAd, pk=job_ad_id)

    job_ad.status = 'active'
    job_ad.removal_reason = None
    job_ad.updated_at = timezone.now()

    job_ad.save(
        update_fields=[
            'status',
            'removal_reason',
            'updated_at',
        ]
    )

    messages.success(
        request,
        f'The job ad “{job_ad.name}” remains active and visible to users.',
    )

    moderation_url = reverse('administration:moderation')

    return redirect(
        f'{moderation_url}?ad={job_ad.id}'
    )
def _selected_account_url(account_type, account_id):
    """Builds the page URL with the selected account restored."""

    base_url = reverse('administration:manage_accounts')

    return f'{base_url}?type={account_type}&id={account_id}'

@role_required('admin')
def manage_accounts(request):
    """Displays user and company accounts and the selected account."""

    users = User.objects.order_by(
        'first_name',
        'last_name',
    )

    companies = Company.objects.order_by('name')

    selected_type = request.GET.get('type')
    selected_id = request.GET.get('id')

    selected_user = None
    selected_company = None

    if selected_type == 'user' and selected_id:
        selected_user = get_object_or_404(
            User,
            pk=selected_id,
        )

    elif selected_type == 'company' and selected_id:
        selected_company = get_object_or_404(
            Company,
            pk=selected_id,
        )

    context = {
        'users': users,
        'companies': companies,
        'selected_type': selected_type,
        'selected_user': selected_user,
        'selected_company': selected_company,
        'logged_admin_id': request.session.get('user_id'),
    }

    return render(
        request,
        'administration/manage_accounts.html',
        context,
    )
@require_POST
@role_required('admin')
def update_user_account(request, user_id):
    """Updates basic user account details."""

    user = get_object_or_404(User, pk=user_id)

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    username = request.POST.get('username', '').strip()
    contact = request.POST.get('contact', '').strip()

    redirect_url = _selected_account_url('user', user.id)

    if not first_name or not last_name or not email or not username:
        messages.error(
            request,
            'First name, last name, email, and username are required.',
        )
        return redirect(redirect_url)

    try:
        validate_email(email)
    except ValidationError:
        messages.error(
            request,
            'The entered email address is invalid.',
        )
        return redirect(redirect_url)

    username_exists = (
        User.objects
        .exclude(pk=user.id)
        .filter(username=username)
        .exists()
        or Company.objects.filter(username=username).exists()
    )

    if username_exists:
        messages.error(
            request,
            'This username already exists in the system.',
        )
        return redirect(redirect_url)

    email_exists = (
        User.objects
        .exclude(pk=user.id)
        .filter(email=email)
        .exists()
        or Company.objects.filter(email=email).exists()
    )

    if email_exists:
        messages.error(
            request,
            'This email address already exists in the system.',
        )
        return redirect(redirect_url)

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.username = username
    user.contact = contact or None

    user.save(
        update_fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'contact',
        ]
    )

    messages.success(
        request,
        (
            f'The account details for “{user.first_name} '
            f'{user.last_name}” were updated successfully.'
        ),
    )

    return redirect(redirect_url)
@require_POST
@role_required('admin')
def update_company_account(request, company_id):
    """Updates basic company account details."""

    company = get_object_or_404(Company, pk=company_id)

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    username = request.POST.get('username', '').strip()
    industry = request.POST.get('industry', '').strip()
    contact = request.POST.get('contact', '').strip()
    description = request.POST.get('description', '').strip()

    redirect_url = _selected_account_url(
        'company',
        company.id,
    )

    if not name or not email or not username:
        messages.error(
            request,
            'Company name, email, and username are required.',
        )
        return redirect(redirect_url)

    try:
        validate_email(email)
    except ValidationError:
        messages.error(
            request,
            'The entered email address is invalid.',
        )
        return redirect(redirect_url)

    username_exists = (
        Company.objects
        .exclude(pk=company.id)
        .filter(username=username)
        .exists()
        or User.objects.filter(username=username).exists()
    )

    if username_exists:
        messages.error(
            request,
            'This username already exists in the system.',
        )
        return redirect(redirect_url)

    email_exists = (
        Company.objects
        .exclude(pk=company.id)
        .filter(email=email)
        .exists()
        or User.objects.filter(email=email).exists()
    )

    if email_exists:
        messages.error(
            request,
            'This email address already exists in the system.',
        )
        return redirect(redirect_url)

    company.name = name
    company.email = email
    company.username = username
    company.industry = industry or None
    company.contact = contact or None
    company.description = description or None

    company.save(
        update_fields=[
            'name',
            'email',
            'username',
            'industry',
            'contact',
            'description',
        ]
    )

    messages.success(
        request,
        f'The company details for “{company.name}” were updated successfully.',
    )

    return redirect(redirect_url)
@require_POST
@role_required('admin')
def change_user_role(request, user_id):
    """Changes a user role between user and admin."""

    user = get_object_or_404(User, pk=user_id)
    new_role = request.POST.get('new_role', '').strip()

    redirect_url = _selected_account_url('user', user.id)

    if new_role not in {'user', 'admin'}:
        messages.error(
            request,
            'The selected user role is not allowed.',
        )
        return redirect(redirect_url)

    if user.role == new_role:
        messages.error(
            request,
            'The new role must be different from the current role.',
        )
        return redirect(redirect_url)

    logged_admin_id = request.session.get('user_id')

    if user.id == logged_admin_id and new_role != 'admin':
        messages.error(
            request,
            'You cannot remove the administrator role from the account you are currently using.',
        )
        return redirect(redirect_url)

    with transaction.atomic():
        old_role = user.role
        user.role = new_role
        user.save(update_fields=['role'])

        if new_role == 'admin':
            administrator_exists = Administrator.objects.filter(
                user=user
            ).exists()

            if not administrator_exists:
                Administrator.objects.create(
                    user=user,
                    access_level='standard',
                    assigned_date=timezone.localdate(),
                )

        else:
            Administrator.objects.filter(user=user).delete()

    messages.success(
        request,
        (
            f'The role for “{user.first_name} {user.last_name}” '
            f'was changed from {old_role} to {new_role}.'
        ),
    )

    return redirect(redirect_url)
@require_POST
@role_required('admin')
def delete_user_account(request, user_id):
    """Permanently deletes a user account."""

    user = get_object_or_404(User, pk=user_id)

    if user.id == request.session.get('user_id'):
        messages.error(
            request,
            'You cannot delete the account you are currently using.',
        )

        return redirect(
            _selected_account_url('user', user.id)
        )

    full_name = f'{user.first_name} {user.last_name}'
    user.delete()

    messages.success(
        request,
        f'The account “{full_name}” was deleted successfully.',
    )

    return redirect('administration:manage_accounts')
@require_POST
@role_required('admin')
def delete_company_account(request, company_id):
    """Permanently deletes a company account."""

    company = get_object_or_404(
        Company,
        pk=company_id,
    )

    company_name = company.name
    company.delete()

    messages.success(
        request,
        f'The company account “{company_name}” was deleted successfully.',
    )

    return redirect('administration:manage_accounts')

def _parse_career_skills(raw_value):
    """Parses a textual skill list into CareerSkill data.

    Supported formats:

    Python, SQL, Git

    or, in detail, one skill per line:

    Python | 5 | 1.00
    SQL | 4 | 0.80

    The second value is the required level from 1 to 5, and the third is the weight.
    When omitted, level 3 and weight 1.00 are used.
    """

    raw_value = raw_value.strip()

    if not raw_value:
        return None, 'You must enter at least one required skill.'

    entries = []

    for line in raw_value.replace('\r', '').split('\n'):
        line = line.strip()

        if not line:
            continue

        if '|' in line:
            entries.append(line)
        else:
            entries.extend(
                item.strip()
                for item in line.split(',')
                if item.strip()
            )

    parsed_skills = []
    used_names = set()

    for entry in entries:
        parts = [
            part.strip()
            for part in entry.split('|')
        ]

        if len(parts) > 3:
            return None, (
                f'The skill “{entry}” is not entered correctly. '
                f'Use the format: name | level | weight.'
            )

        skill_name = parts[0]

        if not skill_name:
            return None, 'The skill name cannot be empty.'

        if len(skill_name) > 100:
            return None, (
                f'The skill name “{skill_name}” exceeds 100 characters.'
            )

        normalized_name = skill_name.lower()

        if normalized_name in used_names:
            return None, (
                f'The skill “{skill_name}” was entered more than once.'
            )

        used_names.add(normalized_name)

        required_level = 3

        if len(parts) >= 2 and parts[1]:
            try:
                required_level = int(parts[1])
            except ValueError:
                return None, (
                    f'The level for “{skill_name}” must be an integer.'
                )

        if required_level < 1 or required_level > 5:
            return None, (
                f'The level for “{skill_name}” must be between 1 and 5.'
            )

        weight = Decimal('1.00')

        if len(parts) == 3 and parts[2]:
            try:
                weight = Decimal(
                    parts[2].replace(',', '.')
                )
            except InvalidOperation:
                return None, (
                    f'The weight for “{skill_name}” is invalid.'
                )

        if weight <= Decimal('0') or weight > Decimal('9.99'):
            return None, (
                f'The weight for “{skill_name}” must be '
                f'greater than 0 and no more than 9.99.'
            )

        if weight.quantize(Decimal('0.01')) != weight:
            return None, (
                f'The weight for “{skill_name}” can have '
                f'at most two decimal places.'
            )

        parsed_skills.append(
            {
                'name': skill_name,
                'required_level': required_level,
                'weight': weight,
            }
        )

    if not parsed_skills:
        return None, 'You must enter at least one required skill.'

    return parsed_skills, None
def _replace_career_skills(career, parsed_skills):
    """Replaces the required skills associated with a career."""

    CareerSkill.objects.filter(career=career).delete()

    for skill_data in parsed_skills:
        skill = (
            Skill.objects
            .filter(name__iexact=skill_data['name'])
            .order_by('id')
            .first()
        )

        if skill is None:
            skill = Skill.objects.create(
                name=skill_data['name'],
            )

        CareerSkill.objects.create(
            career=career,
            skill=skill,
            required_level=skill_data['required_level'],
            weight=skill_data['weight'],
        )
@role_required('admin')
def manage_careers(request):
    """Displays careers and allows an administrator to select one for editing."""

    careers = (
        Career.objects
        .prefetch_related('career_skills__skill')
        .order_by('name')
    )

    selected_career = None
    selected_skills_text = ''

    selected_career_id = request.GET.get('career')

    if selected_career_id:
        selected_career = get_object_or_404(
            Career,
            pk=selected_career_id,
        )

        career_skills = (
            CareerSkill.objects
            .filter(career=selected_career)
            .select_related('skill')
            .order_by('skill__name')
        )

        selected_skills_text = '\n'.join(
            (
                f'{career_skill.skill.name} | '
                f'{career_skill.required_level} | '
                f'{career_skill.weight}'
            )
            for career_skill in career_skills
        )

    context = {
        'careers': careers,
        'selected_career': selected_career,
        'selected_skills_text': selected_skills_text,
        'new_career_selected': request.GET.get('new') == '1',
    }

    return render(
        request,
        'administration/manage_careers.html',
        context,
    )
@require_POST
@role_required('admin')
def create_career(request):
    """Creates a new career with required skills."""

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    skills_text = request.POST.get('skills', '').strip()

    if not name or not description:
        messages.error(
            request,
            'Career name and description are required.',
        )

        return redirect(
            f"{reverse('administration:manage_careers')}?new=1"
        )

    if len(name) > 150:
        messages.error(
            request,
            'The career name can contain at most 150 characters.',
        )

        return redirect(
            f"{reverse('administration:manage_careers')}?new=1"
        )

    if Career.objects.filter(name__iexact=name).exists():
        messages.error(
            request,
            'A career with this name already exists.',
        )

        return redirect(
            f"{reverse('administration:manage_careers')}?new=1"
        )

    parsed_skills, skills_error = _parse_career_skills(
        skills_text
    )

    if skills_error:
        messages.error(request, skills_error)

        return redirect(
            f"{reverse('administration:manage_careers')}?new=1"
        )

    with transaction.atomic():
        career = Career.objects.create(
            name=name,
            description=description,
        )

        _replace_career_skills(
            career,
            parsed_skills,
        )

    messages.success(
        request,
        f'The career “{career.name}” was added successfully.',
    )

    manage_url = reverse(
        'administration:manage_careers'
    )

    return redirect(
        f'{manage_url}?career={career.id}'
    )
@require_POST
@role_required('admin')
def update_career(request, career_id):
    """Updates an existing career and its required skills."""

    career = get_object_or_404(
        Career,
        pk=career_id,
    )

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    skills_text = request.POST.get('skills', '').strip()

    manage_url = reverse(
        'administration:manage_careers'
    )

    redirect_url = (
        f'{manage_url}?career={career.id}'
    )

    if not name or not description:
        messages.error(
            request,
            'Career name and description are required.',
        )
        return redirect(redirect_url)

    if len(name) > 150:
        messages.error(
            request,
            'The career name can contain at most 150 characters.',
        )
        return redirect(redirect_url)

    duplicate_exists = (
        Career.objects
        .exclude(pk=career.id)
        .filter(name__iexact=name)
        .exists()
    )

    if duplicate_exists:
        messages.error(
            request,
            'Another career with this name already exists.',
        )
        return redirect(redirect_url)

    parsed_skills, skills_error = _parse_career_skills(
        skills_text
    )

    if skills_error:
        messages.error(request, skills_error)
        return redirect(redirect_url)

    with transaction.atomic():
        career.name = name
        career.description = description

        career.save(
            update_fields=[
                'name',
                'description',
            ]
        )

        _replace_career_skills(
            career,
            parsed_skills,
        )

    messages.success(
        request,
        f'The career “{career.name}” was updated successfully.',
    )

    return redirect(redirect_url)
@require_POST
@role_required('admin')
def delete_career(request, career_id):
    """Deletes a career and its required-skill relationships."""

    career = get_object_or_404(
        Career,
        pk=career_id,
    )

    career_name = career.name
    career.delete()

    messages.success(
        request,
        f'The career “{career_name}” was deleted successfully.',
    )

    return redirect(
        'administration:manage_careers'
    )