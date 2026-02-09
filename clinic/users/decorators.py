# users/decorators.py

from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to restrict view access based on user role.
    allowed_roles: list of role names as strings, e.g. ['admin', 'call_agent']
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            
            user_role = request.user.role.name.lower() if hasattr(request.user, 'role') and request.user.role else None
            if user_role not in allowed_roles:
                return redirect('users:login')  # Or some "permission denied" page
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
