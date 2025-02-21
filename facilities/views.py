from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Facility, Booking, Course, Event, LibraryResource, CareerService, SupportService, ExtracurricularActivity, Alumni, TransportFacility
from .forms import BookingForm

@login_required
def facility_list(request):
    facilities = Facility.objects.all()
    courses = Course.objects.all()
    events = Event.objects.all()
    library_resources = LibraryResource.objects.all()
    career_services = CareerService.objects.all()
    support_services = SupportService.objects.all()
    extracurricular_activities = ExtracurricularActivity.objects.all()
    alumni = Alumni.objects.all()

    context = {
        'facilities': facilities,
        'courses': courses,
        'events': events,
        'library_resources': library_resources,
        'career_services': career_services,
        'support_services': support_services,
        'extracurricular_activities': extracurricular_activities,
        'alumni': alumni,
    }
    
    return render(request, 'facilities/facility_list.html', context)

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

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'facilities/course_list.html', {'courses': courses})

@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'facilities/event_list.html', {'events': events})

@login_required
def library_resources(request):
    resources = LibraryResource.objects.all()
    return render(request, 'facilities/library_resources.html', {'resources': resources})

@login_required
def career_services(request):
    services = CareerService.objects.all()
    return render(request, 'facilities/career_services.html', {'services': services})

@login_required
def support_services(request):
    services = SupportService.objects.all()
    return render(request, 'facilities/support_services.html', {'services': services})

@login_required
def extracurricular_activities(request):
    activities = ExtracurricularActivity.objects.all()
    return render(request, 'facilities/extracurricular_activities.html', {'activities': activities})

@login_required
def alumni_network(request):
    alumni = Alumni.objects.all()
    return render(request, 'facilities/alumni_network.html', {'alumni': alumni})

@login_required
def transport_facilities(request):
    transport_facilities = TransportFacility.objects.all()
    return render(request, 'facilities/transport_facilities.html', {'transport_facilities': transport_facilities})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'facilities/event_detail.html', {'event': event})