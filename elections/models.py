from django.db import models
from accounts.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    nomination_end_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Set nomination_end_date to one day before start_date if not set
        if not self.nomination_end_date:
            self.nomination_end_date = self.start_date - timedelta(days=1)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def is_nomination_open(self):
        now = timezone.now()
        return now <= self.nomination_end_date

class Nomination(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    manifesto = models.TextField(help_text="Describe your election agenda and why students should vote for you")
    experience = models.TextField(help_text="Describe your relevant experience")
    achievements = models.TextField(help_text="List your achievements")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'election')

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey('Nomination', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'election')