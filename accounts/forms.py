from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'department', 'phone']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'phone']

class HealthRequestForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['health_requests']  # Assuming health_requests is a text field

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['leave_requests']  # Assuming leave_requests is a text field