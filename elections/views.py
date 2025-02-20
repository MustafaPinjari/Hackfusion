from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Election, Nomination, Vote
from .forms import NominationForm, NominationAdminForm, ElectionForm

@login_required
def election_list(request):
    active_elections = Election.objects.filter(is_active=True).order_by('-start_date')
    user_nominations = {
        nom.election_id: nom 
        for nom in Nomination.objects.filter(user=request.user)
    }
    return render(request, 'elections/election_list.html', {
        'elections': active_elections,
        'user_nominations': user_nominations
    })

@login_required
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)
    user_nomination = Nomination.objects.filter(election=election, user=request.user).first()
    nominations = Nomination.objects.filter(election=election, status='approved')
    
    context = {
        'election': election,
        'user_nomination': user_nomination,
        'nominations': nominations,
        'can_nominate': election.is_nomination_open() and not user_nomination
    }
    return render(request, 'elections/election_detail.html', context)

@login_required
def register_candidate(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if not election.is_nomination_open():
        messages.error(request, "Nominations are closed for this election.")
        return redirect('elections:detail', pk=election_id)
    
    if Nomination.objects.filter(election=election, user=request.user).exists():
        messages.error(request, "You have already submitted a nomination for this election.")
        return redirect('elections:detail', pk=election_id)
    
    if request.method == 'POST':
        form = NominationForm(request.POST)
        if form.is_valid():
            nomination = form.save(commit=False)
            nomination.user = request.user
            nomination.election = election
            nomination.save()
            messages.success(request, "Your nomination has been submitted successfully!")
            return redirect('elections:detail', pk=election_id)
    else:
        form = NominationForm()
    
    return render(request, 'elections/submit_nomination.html', {
        'form': form,
        'election': election
    })

@login_required
def submit_vote(request, election_id, candidate_id):
    election = get_object_or_404(Election, pk=election_id)
    candidate = get_object_or_404(Nomination, pk=candidate_id, election=election, status='approved')
    
    if not election.is_active:
        messages.error(request, "This election is not active.")
        return redirect('elections:detail', pk=election_id)
    
    if Vote.objects.filter(election=election, user=request.user).exists():
        messages.error(request, "You have already voted in this election.")
        return redirect('elections:detail', pk=election_id)
    
    Vote.objects.create(
        user=request.user,
        election=election,
        candidate=candidate
    )
    
    messages.success(request, "Your vote has been recorded successfully!")
    return redirect('elections:detail', pk=election_id)

@user_passes_test(lambda u: u.is_staff)
def edit_election(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, "Election updated successfully!")
            return redirect('elections:detail', pk=election_id)
    else:
        form = ElectionForm(instance=election)
    
    return render(request, 'elections/election_form.html', {
        'form': form,
        'election': election
    })

@user_passes_test(lambda u: u.is_staff)
def delete_election(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if request.method == 'POST':
        election.delete()
        messages.success(request, "Election deleted successfully!")
        return redirect('elections:list')
    return redirect('elections:detail', pk=election_id)

@login_required
def election_results(request, pk):
    election = get_object_or_404(Election, pk=pk)
    candidates = election.nomination_set.all().order_by('-votes')
    total_votes = Vote.objects.filter(election=election).count()
    return render(request, 'elections/election_results.html', {
        'election': election,
        'candidates': candidates,
        'total_votes': total_votes
    })

@login_required
def submit_nomination(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if not election.is_nomination_open():
        messages.error(request, "Nominations are closed for this election.")
        return redirect('elections:detail', pk=election_id)
    
    if Nomination.objects.filter(election=election, user=request.user).exists():
        messages.error(request, "You have already submitted a nomination for this election.")
        return redirect('elections:detail', pk=election_id)
    
    if request.method == 'POST':
        form = NominationForm(request.POST)
        if form.is_valid():
            nomination = form.save(commit=False)
            nomination.user = request.user
            nomination.election = election
            nomination.save()
            messages.success(request, "Your nomination has been submitted successfully!")
            return redirect('elections:detail', pk=election_id)
    else:
        form = NominationForm()
    
    return render(request, 'elections/submit_nomination.html', {
        'form': form,
        'election': election
    })

@login_required
def manage_nominations(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to manage nominations.")
        return redirect('elections:list')
    
    nominations = Nomination.objects.all().order_by('-created_at')
    return render(request, 'elections/manage_nominations.html', {
        'nominations': nominations
    })

@login_required
def review_nomination(request, nomination_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to review nominations.")
        return redirect('elections:list')
    
    nomination = get_object_or_404(Nomination, pk=nomination_id)
    if request.method == 'POST':
        form = NominationAdminForm(request.POST, instance=nomination)
        if form.is_valid():
            form.save()
            messages.success(request, "Nomination status updated successfully!")
            return redirect('elections:manage_nominations')
    else:
        form = NominationAdminForm(instance=nomination)
    
    return render(request, 'elections/review_nomination.html', {
        'form': form,
        'nomination': nomination
    })

@login_required
def election_edit(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    # Add your edit logic here
    return render(request, 'elections/election_edit.html', {'election': election})

@user_passes_test(lambda u: u.is_staff)
def election_create(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save()
            messages.success(request, 'Election created successfully!')
            return redirect('elections:detail', pk=election.pk)
    else:
        form = ElectionForm()
    
    return render(request, 'elections/election_form.html', {
        'form': form,
        'title': 'Create Election'
    })