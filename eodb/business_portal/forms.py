from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    BusinessProfile, ApprovalApplication, 
    ApplicationDocument, Compliance, DigitalSignature
)
from django.core.validators import FileExtensionValidator

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_established': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class ApprovalApplicationForm(forms.ModelForm):
    class Meta:
        model = ApprovalApplication
        fields = ['approval_type', 'notes']
        widgets = {
            'approval_type': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional notes...'
            }),
        }

class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['document_type', 'document']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ComplianceForm(forms.ModelForm):
    class Meta:
        model = Compliance
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class DigitalSignatureForm(forms.ModelForm):
    class Meta:
        model = DigitalSignature
        fields = ['signature_image']
        widgets = {
            'signature_image': forms.FileInput(attrs={'class': 'form-control'}),
        }