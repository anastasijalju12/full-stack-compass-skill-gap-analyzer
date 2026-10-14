"""
Author: Sofija Nikolic, index: 2023/0603

View functions for the accounts app: login and logout (user and
company), registration, password reset, subscription, role-protected
pages, and static public pages.
"""

import uuid
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Avg

from .forms import (
    LoginForm,
    UserRegistrationForm,
    CompanyRegistrationForm,
    ForgotPasswordForm,
    SetNewPasswordForm,
    UserProfileForm,
    CompanyProfileForm,
)
from .models import User, Company, PasswordReset, Subscription
from .decorators import role_required, login_required_custom
from careers.models import Career, JobAd

RESET_TOKEN_VALID_HOURS = 1


def home(request):
    """Displays the home page after login/logout."""
    return render(request, 'accounts/home.html')


def public_index(request):
    """Displays the public home (marketing) page, available to everyone.

    Combines data from the careers (Career) and jobs (JobAd, Company)
    apps to show an overview of careers, current job ads, and
    companies. Supports simple filtering of job ads by industry,
    engagement type, and required skill level via GET parameters
    ('oblast', 'tip', 'nivo').

    Returns: HttpResponse - the rendered home page with data.
    """
    careers = Career.objects.all()[:3]
    companies = Company.objects.filter(status='active')[:3]

    job_ads = JobAd.objects.filter(status='active').select_related('company')

    industries = (
        Company.objects.filter(status='active')
        .exclude(industry__isnull=True)
        .exclude(industry__exact='')
        .values_list('industry', flat=True)
        .distinct()
    )

    selected_industry = request.GET.get('oblast', '')
    selected_type = request.GET.get('tip', '')
    selected_level = request.GET.get('nivo', '')
    filtering = bool(selected_industry or selected_type or selected_level)

    filtered_job_ads = job_ads.annotate(avg_skill_level=Avg('jobadskill__required_level'))
    if selected_industry:
        filtered_job_ads = filtered_job_ads.filter(company__industry=selected_industry)
    if selected_type:
        filtered_job_ads = filtered_job_ads.filter(type=selected_type)
    if selected_level == 'beginner':
        filtered_job_ads = filtered_job_ads.filter(avg_skill_level__lte=2)
    elif selected_level == 'intermediate':
        filtered_job_ads = filtered_job_ads.filter(avg_skill_level__gt=2, avg_skill_level__lte=4)

    context = {
        'careers': careers,
        'job_ads': job_ads[:3],
        'companies': companies,
        'industries': industries,
        'selected_industry': selected_industry,
        'selected_type': selected_type,
        'selected_level': selected_level,
        'filtering': filtering,
        'filtered_job_ads': filtered_job_ads[:6] if filtering else None,
    }
    return render(request, 'accounts/public_index.html', context)


def about_us(request):
    """Displays the static 'About Us' page, available to everyone."""
    return render(request, 'accounts/about_us.html')


def payment_view(request):
    """Displays the registration payment page (simulation).

    Expects the registration data to already be stored in the session
    via register_user/register_company. If it doesn't exist (e.g. the
    user opened this page directly), redirects to the registration
    choice page.

    Returns: HttpResponse - the rendered payment page or a redirect.
    """
    pending = request.session.get('pending_registration')
    if not pending:
        messages.error(request, "You need to fill out the registration form first.")
        return redirect('registration_choice')

    return render(request, 'accounts/payment.html', {'is_company': pending['type'] == 'company'})


def payment_process(request):
    """Processes the payment simulation and creates the account on success.

    If the payment succeeds: creates a User (status 'active', logged
    in immediately) or a Company (status 'pending', awaiting admin
    approval) based on the data stored in the session, and creates the
    corresponding Subscription record. If the payment fails, the data
    stays in the session so the user can try again.

    Returns: HttpResponse - the payment success/failure page.
    """
    pending = request.session.get('pending_registration')
    if not pending:
        messages.error(request, "You need to fill out the registration form first.")
        return redirect('registration_choice')

    if request.method != "POST":
        return redirect('payment')

    action = request.POST.get('action', 'success')

    if action == 'fail':
        return render(request, 'accounts/payment_fail.html')

    if pending['type'] == 'user':
        user = User.objects.create(
            first_name=pending['first_name'],
            last_name=pending['last_name'],
            username=pending['username'],
            email=pending['email'],
            contact=pending['contact'],
            password=pending['password'],
            status='active',
            role='user',
        )
        Subscription.objects.create(user=user, amount=Decimal('10.00'), status='success')

        del request.session['pending_registration']
        request.session['role'] = user.role
        request.session['user_id'] = user.id

        return render(request, 'accounts/payment_success.html', {'is_company': False})

    else:
        company = Company.objects.create(
            name=pending['name'],
            username=pending['username'],
            email=pending['email'],
            industry=pending['industry'],
            contact=pending['contact'],
            description=pending['description'],
            password=pending['password'],
            status='pending',
        )
        Subscription.objects.create(company=company, amount=Decimal('10.00'), status='success')

        del request.session['pending_registration']

        return render(request, 'accounts/payment_success.html', {'is_company': True})


def payment_cancel(request):
    """Cancels the registration/payment flow.

    Deletes the temporary registration data from the session without
    creating an account.

    Returns: HttpResponse - the rendered cancellation page.
    """
    request.session.pop('pending_registration', None)
    return render(request, 'accounts/payment_cancelled.html')


def login_view(request):
    """Handles login for a user or a company (dual login).

    First checks whether the username matches someone in the User
    table (regular users and administrators), then in the Company
    table. If the password matches, stores the role and id in the
    session and redirects to the home page.

    Returns: HttpResponse - the rendered login page or a redirect to 'home'.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # first check users (user + admin are in the same table)
            user = User.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                request.session['role'] = user.role  # 'user' or 'admin'
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome, {user.first_name}!")
                return redirect('home')

            # then check companies
            company = Company.objects.filter(username=username).first()
            if company and check_password(password, company.password):
                if company.status == 'pending':
                    messages.warning(request, "Your account has not been approved by the administrator yet.")
                    return redirect('login')
                if company.status == 'rejected':
                    reason = company.rejection_reason or "No reason provided."
                    messages.error(request, f"Your registration request was rejected. Reason: {reason}")
                    return redirect('login')

                request.session['role'] = 'company'
                request.session['company_id'] = company.id
                messages.success(request, f"Welcome, {company.name}!")
                return redirect('home')

            messages.error(request, "Incorrect username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def registration_view(request):
    """Displays the registration type selection page (user or company).

    Returns: HttpResponse - the rendered selection page.
    """
    return render(request, 'accounts/registration_choice.html')


def check_username_availability(request):
    """AJAX endpoint - checks whether a username is available.

    Used on the registration page so that the user gets immediate
    feedback, while typing, on whether the desired username is already
    taken, without needing to submit/refresh the whole form.

    Expects a GET parameter 'username'.
    Returns: JsonResponse with an 'available' key (bool).
    """
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': False})

    taken = User.objects.filter(username=username).exists() or Company.objects.filter(username=username).exists()
    return JsonResponse({'available': not taken})


def register_user(request):
    """Accepts data for registering a new user.

    Validates the form (unique username and email, matching
    passwords), hashes the password, and temporarily stores the data
    in the session. The account is NOT created here - it is only
    created after the payment flow completes successfully (see
    payment_view/payment_process).

    Returns: HttpResponse - the rendered form or a redirect to 'payment'.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            request.session['pending_registration'] = {
                'type': 'user',
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'contact': form.cleaned_data['contact'],
                'password': make_password(form.cleaned_data['password']),
            }
            return redirect('payment')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register_user.html', {'form': form})


def register_company(request):
    """Accepts data for registering a new company.

    Validates the form, hashes the password, and temporarily stores
    the data in the session. The account is NOT created here - it is
    created with the 'pending' status (awaiting administrator
    approval) only after the payment flow completes successfully.

    Returns: HttpResponse - the rendered form or a redirect to 'payment'.
    """
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            request.session['pending_registration'] = {
                'type': 'company',
                'name': form.cleaned_data['name'],
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'industry': form.cleaned_data['industry'],
                'contact': form.cleaned_data['contact'],
                'description': form.cleaned_data['description'],
                'password': make_password(form.cleaned_data['password']),
            }
            return redirect('payment')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'accounts/register_company.html', {'form': form})


def logout_view(request):
    """Logs out the currently logged-in user or company.

    Clears all data from the session and redirects to the home page.
    """
    request.session.flush()
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')


@login_required_custom
def profile_view(request):
    """Displays and updates the profile of the logged-in user or company.

    Shows the appropriate form (User or Company) depending on the
    role of the current session, and saves changes upon successful
    validation. The password is not changed here - that goes through
    the separate password reset flow.

    Returns: HttpResponse - the rendered profile page.
    """
    role = request.session.get('role')

    if role == 'company':
        company_id = request.session.get('company_id')
        instance = Company.objects.filter(id=company_id).first()
        form_class = CompanyProfileForm
        template = 'accounts/my_profile_company.html'
    else:
        user_id = request.session.get('user_id')
        instance = User.objects.filter(id=user_id).first()
        form_class = UserProfileForm
        template = 'accounts/my_profile_user.html'

    if not instance:
        messages.error(request, "Account not found.")
        return redirect('home')

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated.")
            return redirect('my_profile')
    else:
        form = form_class(instance=instance)

    return render(request, template, {'form': form})


def forgot_password_view(request):
    """Handles the password reset request.

    Looks up a user or company by the entered email, generates a
    one-time token with an expiration time, stores it in the
    PasswordReset table, and "sends" (prints via the console email
    backend) the reset link. Shows the same message regardless of
    whether the email exists, so as not to reveal whether an email is
    registered in the system.

    Returns: HttpResponse - the rendered form or a redirect to 'login'.
    """
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = User.objects.filter(email=email).first()
            company = None
            if not user:
                company = Company.objects.filter(email=email).first()

            if user or company:
                token = uuid.uuid4().hex
                expires_at = timezone.now() + timedelta(hours=RESET_TOKEN_VALID_HOURS)

                PasswordReset.objects.create(
                    user=user,
                    company=company,
                    token=token,
                    expires_at=expires_at,
                    is_used=False,
                )

                reset_link = request.build_absolute_uri(f'/accounts-app/reset-password/{token}/')
                send_mail(
                    subject="Kompas - Password Reset",
                    message=f"Click the link to reset your password (valid for {RESET_TOKEN_VALID_HOURS}h):\n{reset_link}",
                    from_email=None,
                    recipient_list=[email],
                )

            # same message regardless of whether the email exists (security best practice)
            messages.success(request, "If the email exists in our system, we've sent a password reset link.")
            return redirect('login')
    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password_view(request, token):
    """Handles setting a new password via the token from the email.

    Checks that the token exists, has not already been used, and has
    not expired. If everything is fine, shows the new password form
    and, upon successful validation, updates the password of the
    corresponding user or company and marks the token as used.

    Arguments:
        token (str): the unique password reset token from the link.

    Returns: HttpResponse - the rendered form or a redirect.
    """
    reset_entry = PasswordReset.objects.filter(token=token).first()

    if not reset_entry or reset_entry.is_used or reset_entry.expires_at < timezone.now():
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('forgot_password')

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = make_password(form.cleaned_data['password'])

            if reset_entry.user:
                reset_entry.user.password = new_password
                reset_entry.user.save()
            elif reset_entry.company:
                reset_entry.company.password = new_password
                reset_entry.company.save()

            reset_entry.is_used = True
            reset_entry.save()

            messages.success(request, "Your password has been successfully changed. You can now log in.")
            return redirect('login')
    else:
        form = SetNewPasswordForm()

    return render(request, 'accounts/reset_password.html', {'form': form})


@login_required_custom
def subscription_view(request):
    """Displays the current subscription status and subscription history.

    Available to any logged-in user or company (see
    login_required_custom). Displays the active subscription (status
    'success') if one exists, and a list of all past subscriptions.

    Returns: HttpResponse - the rendered subscription status page.
    """
    role = request.session.get('role')
    user_id = request.session.get('user_id')
    company_id = request.session.get('company_id')

    if role == 'company':
        subscriptions = Subscription.objects.filter(company_id=company_id).order_by('-date')
    else:
        subscriptions = Subscription.objects.filter(user_id=user_id).order_by('-date')

    active_subscription = subscriptions.filter(status='success').first()

    context = {
        'subscriptions': subscriptions,
        'active_subscription': active_subscription,
    }
    return render(request, 'accounts/subscription.html', context)


@login_required_custom
def subscribe_view(request):
    """Creates a new subscription for the logged-in user or company.

    Simulates the payment flow: if action='fail' is sent, creates a
    subscription with the 'failed' status, otherwise 'success'. There
    is no real payment system, this is a simulation for demonstrating
    the flow.

    Returns: HttpResponse - a redirect to 'subscription_view'.
    """
    if request.method == "POST":
        role = request.session.get('role')
        user_id = request.session.get('user_id')
        company_id = request.session.get('company_id')

        action = request.POST.get('action', 'success')
        status = 'failed' if action == 'fail' else 'success'

        Subscription.objects.create(
            user_id=user_id if role != 'company' else None,
            company_id=company_id if role == 'company' else None,
            amount=Decimal('10.00'),
            status=status,
        )

        if status == 'success':
            messages.success(request, "You have successfully subscribed!")
        else:
            messages.error(request, "Payment failed. Please try again.")

    return redirect('subscription_view')


@login_required_custom
def cancel_subscription_view(request, subscription_id):
    """Cancels an existing subscription.

    Checks that the cancelled subscription belongs to the currently
    logged-in user/company before allowing the cancellation.

    Arguments:
        subscription_id (int): the ID of the subscription being cancelled.

    Returns: HttpResponse - a redirect to 'subscription_view'.
    """
    if request.method == "POST":
        role = request.session.get('role')
        user_id = request.session.get('user_id')
        company_id = request.session.get('company_id')

        subscription = Subscription.objects.filter(id=subscription_id).first()

        owns_it = (
            (role == 'company' and subscription and subscription.company_id == company_id) or
            (role != 'company' and subscription and subscription.user_id == user_id)
        )

        if subscription and owns_it:
            subscription.status = 'cancelled'
            subscription.save()
            messages.success(request, "The subscription has been cancelled.")
        else:
            messages.error(request, "Subscription not found.")

    return redirect('subscription_view')
