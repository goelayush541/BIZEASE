from django.urls import path, include
from django.contrib.auth import views as auth_views
from business_portal import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Business Profile
    path('profile/', views.business_profile, name='business_profile'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Approvals
    path('approvals/', views.approval_types, name='approval_types'),
    path('approvals/create/<int:type_id>/', views.create_application, name='create_application'),
    path('approvals/<int:application_id>/', views.application_details, name='application_details'),
    path('approvals/<int:application_id>/upload/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/sign/', views.add_signature, name='add_signature'),
    
    # Government Schemes
    path('schemes/', views.government_schemes, name='government_schemes'),
    path('schemes/<int:scheme_id>/', views.scheme_details, name='scheme_details'),
    
    # Compliances
    path('compliances/', views.compliances, name='compliances'),
    path('compliances/<int:compliance_id>/complete/', views.mark_compliance_complete, name='mark_compliance_complete'),
    
    # News
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    
    # API
    path('api/status/<str:application_number>/', views.api_application_status, name='api_application_status'),
]