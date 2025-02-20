from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Facility, Booking
from .forms import BookingForm

@login_required
def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'facilities/facility_list.html', {'facilities': facilities})

@login_required
def book_facility(request, facility_id):
    facility = Facility.objects.get(id=facility_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.facility = facility
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('facilities:list')
    else:
        form = BookingForm()
    return render(request, 'facilities/book_facility.html', {
        'form': form,
        'facility': facility
    })

# Add this missing view function
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'facilities/my_bookings.html', {'bookings': bookings})