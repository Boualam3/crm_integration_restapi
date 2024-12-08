"""
URL configuration for HubspotApiIntegration project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authapp.urls")),
    path("api/crm/", include("crm_integration.urls")),
]
