"""
Author: Milica Pavlovic, student ID: 2023/0148

URL paths for the administration app.
"""

from django.urls import path

from . import views


app_name = 'administration'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-account/', views.create_account, name='create_account'),

    path(
        'company-requests/',
        views.company_requests,
        name='company_requests',
    ),
    path(
        'company-requests/<int:company_id>/approve/',
        views.approve_company,
        name='approve_company',
    ),
    path(
        'company-requests/<int:company_id>/reject/',
        views.reject_company,
        name='reject_company',
    ),
    path(
        'company-requests/<int:company_id>/keep-pending/',
        views.keep_company_pending,
        name='keep_company_pending',
    ),

    path('moderation/', views.moderation, name='moderation'),
    path(
    'moderation/<int:job_ad_id>/remove/',
    views.remove_job_ad,
    name='remove_job_ad',
),
path(
    'moderation/<int:job_ad_id>/mark-outdated/',
    views.mark_job_ad_outdated,
    name='mark_job_ad_outdated',
),
path(
    'moderation/<int:job_ad_id>/keep-active/',
    views.keep_job_ad_active,
    name='keep_job_ad_active',
),
    path('manage-accounts/', views.manage_accounts, name='manage_accounts'),
    path(
    'manage-accounts/user/<int:user_id>/edit/',
    views.update_user_account,
    name='update_user_account',
),
path(
    'manage-accounts/company/<int:company_id>/edit/',
    views.update_company_account,
    name='update_company_account',
),
path(
    'manage-accounts/user/<int:user_id>/role/',
    views.change_user_role,
    name='change_user_role',
),
path(
    'manage-accounts/user/<int:user_id>/delete/',
    views.delete_user_account,
    name='delete_user_account',
),
path(
    'manage-accounts/company/<int:company_id>/delete/',
    views.delete_company_account,
    name='delete_company_account',
),
    path('manage-careers/', views.manage_careers, name='manage_careers'),
    path(
    'manage-careers/create/',
    views.create_career,
    name='create_career',
),
path(
    'manage-careers/<int:career_id>/update/',
    views.update_career,
    name='update_career',
),
path(
    'manage-careers/<int:career_id>/delete/',
    views.delete_career,
    name='delete_career',
),
]