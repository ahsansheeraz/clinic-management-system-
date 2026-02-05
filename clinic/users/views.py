from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required

# ---------------------------
# LOGIN VIEW
# ---------------------------

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Safe role name
            role_name = user.role.name.lower() if user.role else None
            print("Logged in user:", user.email, "Role:", role_name)  # Debug

            # Role-based redirection
            if role_name in ['superuser', 'admin']:
                return redirect('/admin/')
            elif role_name == 'doctor':
                return redirect('users:doctor_dashboard')
            elif role_name in ['call_agent', 'fdo']:
                return redirect('users:staff_dashboard')
            else:
                # fallback if role not defined
                return redirect('users:login')

    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('users:login')

# ---------------------------
# DASHBOARDS
# ---------------------------
@login_required
def doctor_dashboard(request):
    """
    Doctor's personal dashboard.
    Only accessible by users with role = 'doctor'.
    """
    return render(request, 'users/doctor_dashboard.html')


@login_required
def staff_dashboard(request):
    """
    Staff dashboard for Call Agent / FDO.
    Only accessible by users with role = 'call_agent' or 'fdo'.
    """
    return render(request, 'users/staff_dashboard.html')
