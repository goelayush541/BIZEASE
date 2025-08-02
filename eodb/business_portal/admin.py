from django.contrib import admin
from .models import (
    BusinessProfile, GovernmentScheme, ApprovalType,
    ApprovalApplication, ApplicationDocument, Compliance,
    NewsArticle, DigitalSignature
)

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_type', 'registration_number', 'contact_person')
    search_fields = ('business_name', 'registration_number')

@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(ApprovalType)
class ApprovalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'processing_time', 'fees', 'is_active')
    list_filter = ('department', 'is_active')

@admin.register(ApprovalApplication)
class ApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'business', 'approval_type', 'status', 'submission_date')
    list_filter = ('status', 'approval_type')
    search_fields = ('application_number', 'business__business_name')

@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'is_verified', 'uploaded_at')
    list_filter = ('is_verified', 'document_type')

@admin.register(Compliance)
class ComplianceAdmin(admin.ModelAdmin):
    list_display = ('business', 'title', 'due_date', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('title', 'business__business_name')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')

@admin.register(DigitalSignature)
class DigitalSignatureAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'signed_at', 'is_valid')
    list_filter = ('is_valid',)