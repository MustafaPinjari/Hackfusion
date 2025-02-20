from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Count
from .forms import UserRegistrationForm, UserUpdateForm
from elections.models import Election, Nomination
from complaints.models import Complaint
from facilities.models import Booking
from .models import User
from django.utils import timezone

@login_required
def dashboard(request):
    context = {
        'active_elections': Election.objects.filter(is_active=True),
        'user_bookings': Booking.objects.filter(user=request.user).order_by('-start_time')[:5],
        'recent_complaints': Complaint.objects.filter(user=request.user).order_by('-created_at')[:5],
    }
    
    # Add role-specific data
    if request.user.role in ['admin', 'faculty']:
        context.update({
            'total_students': User.objects.filter(role='student').count(),
            'department_stats': User.objects.filter(role='student').values('department').annotate(count=Count('id')),
            'pending_complaints': Complaint.objects.filter(status='pending').count(),
            'facility_usage': Booking.objects.values('facility__name').annotate(count=Count('id'))
        })
    
    return render(request, 'accounts/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get active elections and user nominations
    active_elections = Election.objects.filter(
        is_active=True,
        nomination_end_date__gte=timezone.now()
    ).order_by('nomination_end_date')
    
    user_nominations = {
        nom.election_id: nom 
        for nom in Nomination.objects.filter(user=request.user)
    }
    
    context = {
        'form': form,
        'recent_activities': get_user_activities(request.user),
        'active_elections': active_elections,
        'user_nominations': user_nominations,
    }
    return render(request, 'accounts/profile.html', context)

def get_user_activities(user):
    """Get recent activities for the user across all modules"""
    activities = []
    
    try:
        # Add elections activity - check if Vote model exists
        from elections.models import Vote
        activities.extend(Election.objects.filter(vote__user=user).distinct().order_by('-created_at')[:5])
    except (ImportError, AttributeError):
        # Skip if Vote model or related field doesn't exist
        pass

    try:
        # Add complaints activity
        activities.extend(Complaint.objects.filter(user=user).order_by('-created_at')[:5])
    except Exception:
        pass

    try:
        # Add bookings activity
        activities.extend(Booking.objects.filter(user=user).order_by('-created_at')[:5])
    except Exception:
        pass
    
    # Filter out activities without created_at and sort
    valid_activities = [a for a in activities if hasattr(a, 'created_at')]
    return sorted(valid_activities, key=lambda x: x.created_at, reverse=True)[:10]