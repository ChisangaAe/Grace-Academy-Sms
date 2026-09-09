from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User
from .forms import TeacherRegistrationForm, SignUpForm
from students.models import Student
from academics.models import Classroom, Subject


# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

def user_login(request):
    """Handles authentication and routes users based on approval and allocation status."""
    if request.user.is_authenticated:
        if not request.user.is_approved and not request.user.is_superuser:
            return redirect('pending_allocation')
        if not request.user.is_allocated:
            return redirect('pending_allocation')
        return redirect('dashboard')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)
            
            # Check approval status first
            if not user.is_approved and not user.is_superuser:
                messages.warning(request, "Your account is pending superadmin approval.")
                return redirect('pending_allocation')

            # Check allocation status
            if not user.is_allocated:
                messages.info(request, "Your account is approved but awaiting class/subject allocation.")
                return redirect('pending_allocation')

            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


def user_logout(request):
    """Logs out the user and redirects to login."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


def register_teacher(request):
    """Allows new teachers to submit registration requests."""
    if request.user.is_authenticated:
        if not request.user.is_approved and not request.user.is_superuser:
            return redirect('pending_allocation')
        if not request.user.is_allocated:
            return redirect('pending_allocation')
        return redirect('dashboard')

    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'TEACHER'
            user.is_approved = False  # Requires Superadmin/Principal approval
            user.save()
            form.save_m2m()  # Save secondary subjects if selected

            messages.success(
                request,
                "Account request submitted! Please wait for approval from the superadmin before logging in."
            )
            return redirect('login')
    else:
        form = TeacherRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def signup_view(request):
    """General User Signup view requiring superadmin approval."""
    if request.user.is_authenticated:
        if not request.user.is_approved and not request.user.is_superuser:
            return redirect('pending_allocation')
        if not request.user.is_allocated:
            return redirect('pending_allocation')
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Explicitly require superadmin approval
            user.save()

            messages.success(
                request,
                f"Account created for {user.username}! Your account is pending superadmin approval."
            )
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


# ==========================================
# DASHBOARD & APPROVAL WORKFLOW
# ==========================================

@login_required
def dashboard(request):
    """Central Dashboard summarizing key school statistics & pending approvals."""
    # Block unapproved or unallocated users (except superusers)
    if not request.user.is_approved and not request.user.is_superuser:
        messages.warning(request, "Your account is awaiting approval from the superadmin.")
        return redirect('pending_allocation')

    if not request.user.is_allocated:
        return redirect('pending_allocation')

    total_students = Student.objects.count()
    total_classrooms = Classroom.objects.count()
    total_subjects = Subject.objects.count()
    total_teachers = User.objects.filter(role='TEACHER', is_approved=True).count()

    # Pending teacher account approvals for review
    pending_approvals = User.objects.filter(is_approved=False).exclude(is_superuser=True)

    context = {
        'total_students': total_students,
        'total_classrooms': total_classrooms,
        'total_subjects': total_subjects,
        'total_teachers': total_teachers,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def pending_allocation_view(request):
    """Holding page displayed to users awaiting approval or allocation."""
    # Auto-redirect to dashboard if superuser or fully approved & allocated
    if request.user.is_superuser or (request.user.is_approved and request.user.is_allocated):
        return redirect('dashboard')

    return render(request, 'accounts/pending_allocation.html')


@login_required
def approve_user(request, pk):
    """Action view for Superadmin / IT Tech to approve a pending teacher/user account."""
    if not getattr(request.user, 'is_admin_user', False) and not request.user.is_superuser:
        messages.error(request, "You do not have authorization to perform this action.")
        return redirect('dashboard')

    user = get_object_or_404(User, pk=pk)
    user.is_approved = True
    user.is_active = True
    user.save()

    messages.success(request, f"Account for {user.get_full_name() or user.username} has been approved.")
    return redirect('dashboard')


@login_required
def reject_user(request, pk):
    """Action view for Superadmin / IT Tech to reject/delete a pending registration."""
    if not getattr(request.user, 'is_admin_user', False) and not request.user.is_superuser:
        messages.error(request, "You do not have authorization to perform this action.")
        return redirect('dashboard')

    user = get_object_or_404(User, pk=pk)
    username = user.get_full_name() or user.username
    user.delete()

    messages.warning(request, f"Registration request for {username} was rejected and removed.")
    return redirect('dashboard')