"""
Author: Sofija Nikolic, index: 2023/0603

Custom decorators for protecting views based on the session (role of
user/company/admin), since Django's built-in auth system is not used.
"""

from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def login_required_custom(view_func):
    """Requires that someone (any role) is logged in (user, company or admin)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('role'):
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """Requires that the logged-in role is one of the given roles.

    Example: @role_required('company')
             @role_required('user', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = request.session.get('role')
            if not role:
                messages.error(request, "You must be logged in to access this page.")
                return redirect('login')
            if role not in allowed_roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
