from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint, ComplaintResponse
from .forms import ComplaintForm, ResponseForm
from utils.notifications import send_complaint_notification

@login_required
def complaint_list(request):
    # Fetch complaints for the logged-in user
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})

@login_required
def add_response(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.complaint = complaint
            response.responder = request.user
            response.save()
            messages.success(request, 'Response added successfully!')
            return redirect('complaints:detail', pk=pk)
    else:
        form = ResponseForm()
    
    return render(request, 'complaints/add_response.html', {
        'form': form,
        'complaint': complaint
    })

@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            # Set the user only if the complaint is not anonymous
            if not form.cleaned_data['is_anonymous']:
                complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('accounts:profile')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    responses = complaint.complaintresponse_set.all().order_by('created_at')
    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'responses': responses
    })

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            # Only set the user if the complaint is not anonymous
            if not form.cleaned_data['is_anonymous']:
                complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('accounts:profile')
    return redirect('accounts:profile')