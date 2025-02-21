from django.db import models
from django.conf import settings
from accounts.models import User
from django.core.exceptions import ValidationError

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.title

    def get_user_display(self):
        return "Anonymous" if self.is_anonymous else self.user.get_full_name()

    def clean(self):
        # Only validate if the complaint is being created (not updated)
        if not self.pk:  # New complaint
            if self.status == 'resolved' and not self.user:
                raise ValidationError("A user must be assigned to resolve the complaint.")
        # Allow existing complaints to be updated without requiring a user

class ComplaintResponse(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)