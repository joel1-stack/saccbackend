"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'SACCO Nova Digital Ecosystem',
        'version': '2.0',
        'description': 'Complete SACCO management platform with trust, automation & intelligence',
        'core_endpoints': {
            'auth': '/api/auth/',
            'dashboard': '/api/dashboard/',
            'accounts': '/api/accounts/',
            'loans': '/api/loans/',
            'transactions': '/api/transactions/',
            'members': '/api/members/',
        },
        'ecosystem_endpoints': {
            'guarantors': '/api/guarantors/',
            'shares': '/api/shares/',
            'notifications': '/api/notifications/',
            'reporting': '/api/reporting/',
            'integrations': '/api/integrations/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/dashboard/', views.dashboard_summary, name='dashboard-summary'),
    # Core SACCO APIs
    path('api/auth/', include('authentication.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/loans/', include('loans.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/members/', include('members.urls')),
    # Advanced SACCO Ecosystem APIs
    path('api/guarantors/', include('guarantors.urls')),
    path('api/shares/', include('shares.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reporting/', include('reporting.urls')),
    path('api/integrations/', include('integrations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
