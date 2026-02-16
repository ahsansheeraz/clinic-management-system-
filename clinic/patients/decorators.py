from django.shortcuts import redirect
from functools import wraps

ALLOWED_ROLES = ['admin', 'superuser', 'call_agent', 'fdo']

def role_required(allowed_roles=ALLOWED_ROLES):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role and request.user.role.name.lower() in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('users:staff_dashboard')  # or show Unauthorized page
        return _wrapped_view
    return decorator
