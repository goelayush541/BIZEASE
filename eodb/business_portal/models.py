from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class BusinessProfile(models.Model):
    BUSINESS_TYPES = [
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('service', 'Service'),
        ('it', 'Information Technology'),
        ('hospitality', 'Hospitality'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    date_established = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class GovernmentScheme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    eligibility = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField()
    website_link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ApprovalType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    department = models.CharField(max_length=255)
    processing_time = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    required_documents = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ApprovalApplication(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('additional_info_required', 'Additional Info Required'),
    ]
    
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    approval_type = models.ForeignKey(ApprovalType, on_delete=models.CASCADE)
    application_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    submission_date = models.DateTimeField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_number} - {self.approval_type.name}"

class ApplicationDocument(models.Model):
    DOCUMENT_TYPES = [
        ('pan', 'PAN Card'),
        ('address', 'Address Proof'),
        ('registration', 'Business Registration'),
        ('id', 'ID Proof'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(ApprovalApplication, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document = models.FileField(
        upload_to='application_documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.application_number} - {self.get_document_type_display()}"

class Compliance(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business.business_name} - {self.title}"

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    source = models.CharField(max_length=255)
    source_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DigitalSignature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(ApplicationDocument, on_delete=models.CASCADE)
    signature_image = models.ImageField(upload_to='digital_signatures/')
    signed_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.document.document_type}"