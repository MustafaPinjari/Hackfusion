from django.contrib import admin
from .models import Facility, Course, Event, LibraryResource, CareerService, SupportService, ExtracurricularActivity, Alumni, TransportFacility

# Register your models here.
@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'description')  # Customize the fields to display

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'credits', 'department')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'sponsor', 'budget', 'expenses')

@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'resource_type', 'availability')

@admin.register(CareerService)
class CareerServiceAdmin(admin.ModelAdmin):
    list_display = ('description',)

@admin.register(SupportService)
class SupportServiceAdmin(admin.ModelAdmin):
    list_display = ('description',)

@admin.register(ExtracurricularActivity)
class ExtracurricularActivityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'graduation_year', 'linkedin_profile')

@admin.register(TransportFacility)
class TransportFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'description')