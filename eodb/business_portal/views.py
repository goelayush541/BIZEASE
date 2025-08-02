from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import random
import string

from .models import (
    BusinessProfile, GovernmentScheme, ApprovalType,
    ApprovalApplication, ApplicationDocument, Compliance,
    NewsArticle, DigitalSignature
)
from .forms import (
    UserRegistrationForm, BusinessProfileForm,
    ApprovalApplicationForm, ApplicationDocumentForm,
    ComplianceForm, DigitalSignatureForm
)
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'business_portal/login.html'  # Your custom template
    redirect_authenticated_user = True

def home(request):
    schemes = GovernmentScheme.objects.filter(is_active=True).order_by('-created_at')[:3]
    news = NewsArticle.objects.filter(is_active=True).order_by('-publish_date')[:3]
    return render(request, 'business_portal/home.html', {
        'schemes': schemes,
        'news': news
    })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'Account created successfully! Please complete your business profile.')
            return redirect('business_profile')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'business_portal/register.html', {'user_form': user_form})

@login_required
def business_profile(request):
    try:
        profile = request.user.businessprofile
    except BusinessProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Business profile updated successfully!')
            return redirect('dashboard')
    else:
        form = BusinessProfileForm(instance=profile)
    
    return render(request, 'business_portal/business_profile.html', {'form': form})

@login_required
def dashboard(request):
    try:
        business = request.user.businessprofile
    except BusinessProfile.DoesNotExist:
        return redirect('business_profile')
    
    applications = ApprovalApplication.objects.filter(business=business).order_by('-created_at')[:5]
    compliances = Compliance.objects.filter(business=business, is_completed=False).order_by('due_date')[:5]
    
    # Check for due compliances and send reminders
    due_soon = Compliance.objects.filter(
        business=business,
        is_completed=False,
        due_date__lte=datetime.now().date() + timedelta(days=7),
        reminder_sent=False
    )
    
    for compliance in due_soon:
        send_mail(
            f'Compliance Reminder: {compliance.title}',
            f'Your compliance "{compliance.title}" is due on {compliance.due_date}. Please complete it on time.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=True,
        )
        compliance.reminder_sent = True
        compliance.save()
    
    return render(request, 'business_portal/dashboard.html', {
        'business': business,
        'applications': applications,
        'compliances': compliances,
    })

@login_required
def approval_types(request):
    types = ApprovalType.objects.filter(is_active=True)
    return render(request, 'business_portal/approval_types.html', {'approval_types': types})

@login_required
def create_application(request, type_id):
    approval_type = get_object_or_404(ApprovalType, pk=type_id)
    business = get_object_or_404(BusinessProfile, user=request.user)
    
    if request.method == 'POST':
        form = ApprovalApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.business = business
            application.approval_type = approval_type
            application.application_number = generate_application_number()
            application.save()
            messages.success(request, 'Application created successfully! Please upload required documents.')
            return redirect('application_details', application_id=application.id)
    else:
        form = ApprovalApplicationForm(initial={'approval_type': approval_type})
    
    return render(request, 'business_portal/create_application.html', {
        'form': form,
        'approval_type': approval_type,
    })

def generate_application_number():
    prefix = "APP"
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{random_str}"

@login_required
def application_details(request, application_id):
    application = get_object_or_404(ApprovalApplication, pk=application_id, business__user=request.user)
    documents = ApplicationDocument.objects.filter(application=application)
    
    if request.method == 'POST' and 'submit_application' in request.POST:
        if documents.count() < 1:
            messages.error(request, 'Please upload at least one document before submitting.')
        else:
            application.status = 'submitted'
            application.submission_date = datetime.now()
            application.save()
            
            send_mail(
                'Application Submitted Successfully',
                f'Your application {application.application_number} for {application.approval_type.name} has been submitted successfully.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard')
    
    document_form = ApplicationDocumentForm()
    
    return render(request, 'business_portal/application_details.html', {
        'application': application,
        'documents': documents,
        'document_form': document_form,
    })

@login_required
def upload_document(request, application_id):
    application = get_object_or_404(ApprovalApplication, pk=application_id, business__user=request.user)
    
    if request.method == 'POST':
        form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            
            if document.document.name.lower().endswith('.pdf'):
                document.is_verified = True
                document.verification_notes = "Automatically verified as PDF"
                document.save()
            
            messages.success(request, 'Document uploaded successfully!')
            return redirect('application_details', application_id=application.id)
    
    return redirect('application_details', application_id=application.id)

@login_required
def add_signature(request, document_id):
    document = get_object_or_404(ApplicationDocument, pk=document_id, application__business__user=request.user)
    
    if request.method == 'POST':
        form = DigitalSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.user = request.user
            signature.document = document
            signature.save()
            
            document.is_verified = True
            document.verification_notes = "Document signed by user"
            document.save()
            
            messages.success(request, 'Digital signature added successfully!')
            return redirect('application_details', application_id=document.application.id)
    else:
        form = DigitalSignatureForm()
    
    return render(request, 'business_portal/add_signature.html', {
        'form': form,
        'document': document,
    })

@login_required
def government_schemes(request):
    schemes = GovernmentScheme.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'business_portal/government_schemes.html', {'schemes': schemes})

@login_required
def scheme_details(request, scheme_id):
    scheme = get_object_or_404(GovernmentScheme, pk=scheme_id)
    return render(request, 'business_portal/scheme_details.html', {'scheme': scheme})

@login_required
def compliances(request):
    business = get_object_or_404(BusinessProfile, user=request.user)
    compliances = Compliance.objects.filter(business=business).order_by('-due_date')
    
    if request.method == 'POST':
        form = ComplianceForm(request.POST)
        if form.is_valid():
            compliance = form.save(commit=False)
            compliance.business = business
            compliance.save()
            messages.success(request, 'Compliance added successfully!')
            return redirect('compliances')
    else:
        form = ComplianceForm()
    
    return render(request, 'business_portal/compliances.html', {
        'compliances': compliances,
        'form': form,
    })

@login_required
def mark_compliance_complete(request, compliance_id):
    compliance = get_object_or_404(Compliance, pk=compliance_id, business__user=request.user)
    if not compliance.is_completed:
        compliance.is_completed = True
        compliance.completed_date = datetime.now().date()
        compliance.save()
        messages.success(request, 'Compliance marked as completed!')
    return redirect('compliances')

@login_required
def news(request):
    news_articles = NewsArticle.objects.filter(is_active=True).order_by('-publish_date')
    return render(request, 'business_portal/news.html', {'news_articles': news_articles})

@login_required
def news_detail(request, news_id):
    article = get_object_or_404(NewsArticle, pk=news_id)
    return render(request, 'business_portal/news_detail.html', {'article': article})

@csrf_exempt
def api_application_status(request, application_number):
    if request.method == 'GET':
        try:
            application = ApprovalApplication.objects.get(application_number=application_number)
            data = {
                'application_number': application.application_number,
                'approval_type': application.approval_type.name,
                'status': application.status,
                'submission_date': application.submission_date.strftime('%Y-%m-%d %H:%M:%S') if application.submission_date else None,
                'approval_date': application.approval_date.strftime('%Y-%m-%d %H:%M:%S') if application.approval_date else None,
            }
            return JsonResponse(data)
        except ApprovalApplication.DoesNotExist:
            return JsonResponse({'error': 'Application not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)