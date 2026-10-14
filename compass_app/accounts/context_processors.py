"""
Author: Sofija Nikolic, index: 2023/0603

Context processor that automatically injects the role of the
logged-in user/company (user_role) into the context of every
template, based on the session data.
"""

from .models import User, Company


def role_context(request):
    """Returns context with the role and name of the currently logged-in entity.

    Reads the role from the session (request.session['role']) and,
    depending on it, fetches the corresponding user or company from
    the database so their name can be displayed in the navbar.
    Registered in settings.py as a global context processor, so it's
    available in all templates.

    Returns: dict with the keys 'user_role' and 'current_display_name'.
    """
    role = request.session.get('role')

    context = {
        'user_role': role,
        'current_display_name': None,
    }

    if role in ('user', 'admin'):
        user_id = request.session.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            context['current_display_name'] = user.first_name
        else:
            context['user_role'] = None

    elif role == 'company':
        company_id = request.session.get('company_id')
        company = Company.objects.filter(id=company_id).first()
        if company:
            context['current_display_name'] = company.name
        else:
            context['user_role'] = None

    return context
