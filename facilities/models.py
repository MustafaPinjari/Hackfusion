from django.db import models
from accounts.models import User

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='facilities/', null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    syllabus = models.TextField()
    credits = models.IntegerField()
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    sponsor = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class LibraryResource(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    pdf_url = models.URLField(blank=True, null=True)  # Add this line for PDF URL

    def __str__(self):
        return self.title

class CareerService(models.Model):
    description = models.TextField()

    def __str__(self):
        return "Career Services"

class SupportService(models.Model):
    description = models.TextField()

    def __str__(self):
        return "Support Services"

class ExtracurricularActivity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Alumni(models.Model):
    name = models.CharField(max_length=200)
    graduation_year = models.IntegerField()
    linkedin_profile = models.URLField(blank=True)

    def __str__(self):
        return self.name

class TransportFacility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='transport/', null=True, blank=True)

    def __str__(self):
        return self.name