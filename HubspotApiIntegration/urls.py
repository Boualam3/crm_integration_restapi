"""
URL configuration for HubspotApiIntegration project.
"""
from django.http import HttpResponse
from django.contrib import admin
from django.urls import include, path


def health_check(request):
    return HttpResponse("OK", content_type="text/plain")


urlpatterns = [
    path("/", health_check),
    path("admin/", admin.site.urls),
    path("api/auth/", include("authapp.urls")),
    path("api/crm/", include("crm_integration.urls")),
]
