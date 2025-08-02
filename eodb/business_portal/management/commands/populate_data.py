from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from business_portal.models import (
    BusinessProfile, GovernmentScheme, ApprovalType,
    ApprovalApplication, ApplicationDocument, Compliance,
    NewsArticle
)
from datetime import datetime, timedelta
import random
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')
    
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eodb.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
    
        # Create sample business users
        business_users = []
        for i in range(1, 6):
            username = f'business{i}'
            email = f'business{i}@example.com'
        
            # Check if user exists first
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
        
            if created:
                user.set_password(f'business{i}123')
                user.save()
                business_users.append(user)
            
                BusinessProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'business_name': f'Sample Business {i}',
                        'business_type': random.choice(['retail', 'manufacturing', 'service', 'it', 'hospitality']),
                        'registration_number': f'REG{i:03d}',
                        'address': f'{i}00, Sample Street, Delhi',
                        'contact_person': f'Contact Person {i}',
                        'contact_number': f'987654321{i}',
                        'email': email,
                        'date_established': datetime.now() - timedelta(days=random.randint(365, 365*5))
                    }
                )
            else:
                business_users.append(user)

        # Create government schemes
        schemes = [
            {
                'name': 'Delhi Startup Policy',
                'description': 'Financial and infrastructural support for startups in Delhi.',
                'eligibility': 'Startups registered in Delhi with less than 5 years of operation.',
                'benefits': 'Up to ₹10 lakhs funding and incubation support.',
                'application_process': 'Online application with business plan submission.',
                'website_link': 'https://delhi.gov.in/startup',
                'start_date': datetime.now() - timedelta(days=180),
                'end_date': datetime.now() + timedelta(days=180),
            },
            {
                'name': 'MSME Loan Subsidy',
                'description': 'Interest subsidy on loans for MSMEs.',
                'eligibility': 'Registered MSMEs with turnover less than ₹50 crores.',
                'benefits': '5% interest subsidy on term loans.',
                'application_process': 'Apply through portal with required documents.',
                'website_link': 'https://delhi.gov.in/msme',
                'start_date': datetime.now() - timedelta(days=90),
                'end_date': None,
            },
            {
                'name': 'Green Business Incentive',
                'description': 'Incentives for eco-friendly business practices.',
                'eligibility': 'Businesses implementing green initiatives.',
                'benefits': 'Tax rebates and certification.',
                'application_process': 'Submit application with proof of green initiatives.',
                'website_link': 'https://delhi.gov.in/green',
                'start_date': datetime.now() - timedelta(days=60),
                'end_date': datetime.now() + timedelta(days=300),
            },
        ]
        
        for scheme_data in schemes:
            GovernmentScheme.objects.create(**scheme_data)
        
        # Create approval types
        approval_types = [
            {
                'name': 'Trade License',
                'description': 'License required for all businesses operating in Delhi.',
                'department': 'Municipal Corporation of Delhi',
                'processing_time': '7-10 working days',
                'fees': 2000.00,
                'required_documents': '1. Address proof\n2. ID proof\n3. Business registration certificate',
            },
            {
                'name': 'GST Registration',
                'description': 'Mandatory for businesses with turnover above ₹20 lakhs.',
                'department': 'Department of Trade and Taxes',
                'processing_time': '3-5 working days',
                'fees': 0.00,
                'required_documents': '1. PAN\n2. Address proof\n3. Bank details\n4. Business registration',
            },
            {
                'name': 'FSSAI License',
                'description': 'Required for food-related businesses.',
                'department': 'Food Safety and Standards Authority',
                'processing_time': '14-21 working days',
                'fees': 5000.00,
                'required_documents': '1. Food safety plan\n2. Layout plan\n3. List of food products',
            },
        ]
        
        for approval_data in approval_types:
            ApprovalType.objects.create(**approval_data)
        
        # Create sample applications
        statuses = ['draft', 'submitted', 'under_review', 'approved', 'rejected']
        approval_types = ApprovalType.objects.all()
        
        for user in business_users:
            business = BusinessProfile.objects.get(user=user)
            
            for i in range(random.randint(1, 4)):
                approval_type = random.choice(approval_types)
                status = random.choice(statuses)
                
                application = ApprovalApplication.objects.create(
                    business=business,
                    approval_type=approval_type,
                    application_number=f'APP-{user.id}{i}{random.randint(1000,9999)}',
                    status=status,
                    submission_date=datetime.now() - timedelta(days=random.randint(1, 30)) if status != 'draft' else None,
                    approval_date=datetime.now() - timedelta(days=random.randint(1, 10)) if status == 'approved' else None,
                    rejection_reason='Incomplete documentation' if status == 'rejected' else None,
                )
                
                # Add documents to some applications
                if status != 'draft' and random.random() > 0.3:
                    ApplicationDocument.objects.create(
                        application=application,
                        document_type=random.choice(['pan', 'address', 'registration', 'id']),
                        document='dummy.pdf',
                        is_verified=random.choice([True, False]),
                    )
        
        # Create compliances
        compliance_titles = [
            'GST Return Filing',
            'TDS Payment',
            'Professional Tax Payment',
            'Annual Business Return',
            'EPF Payment',
        ]
        
        for user in business_users:
            business = BusinessProfile.objects.get(user=user)
            
            for i in range(random.randint(2, 5)):
                due_date = datetime.now() + timedelta(days=random.randint(1, 60))
                Compliance.objects.create(
                    business=business,
                    title=random.choice(compliance_titles),
                    description=f'Compliance requirement for {business.business_name}',
                    due_date=due_date,
                    is_completed=random.choice([True, False]),
                    completed_date=due_date - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None,
                )
        
        # Create news articles
        news_articles = [
            {
                'title': 'Delhi Government Launches New Business Portal',
                'content': 'The Delhi government has launched a new portal to streamline business registration and approval processes. The portal aims to reduce the time and effort required for businesses to obtain various licenses and approvals.',
                'publish_date': datetime.now() - timedelta(days=2),
                'source': 'Delhi Government',
                'source_url': 'https://delhi.gov.in/news',
            },
            {
                'title': 'Ease of Doing Business Rankings Improve',
                'content': 'Delhi has moved up 5 positions in the national Ease of Doing Business rankings. The improvement is attributed to several reforms implemented by the government.',
                'publish_date': datetime.now() - timedelta(days=5),
                'source': 'Business Today',
                'source_url': 'https://businesstoday.in',
            },
            {
                'title': 'New Subsidy Scheme for Small Businesses',
                'content': 'The government has announced a new subsidy scheme for small businesses affected by the pandemic. The scheme offers financial assistance and tax benefits.',
                'publish_date': datetime.now() - timedelta(days=10),
                'source': 'Economic Times',
                'source_url': 'https://economictimes.indiatimes.com',
            },
        ]
        
        for article_data in news_articles:
            NewsArticle.objects.create(**article_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))