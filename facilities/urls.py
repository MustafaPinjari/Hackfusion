from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('', views.facility_list, name='list'),
    path('book/<int:facility_id>/', views.book_facility, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('courses/', views.course_list, name='course_list'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('library/', views.library_resources, name='library_resources'),
    path('career-services/', views.career_services, name='career_services'),
    path('support-services/', views.support_services, name='support_services'),
    path('extracurricular-activities/', views.extracurricular_activities, name='extracurricular_activities'),
    path('alumni-network/', views.alumni_network, name='alumni_network'),
    path('transport-facilities/', views.transport_facilities, name='transport_facilities'),
]