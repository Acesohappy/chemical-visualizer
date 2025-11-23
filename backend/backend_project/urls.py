"""
Main URL configuration for the backend project.

This module defines the root URL patterns and includes
app-specific URL configurations.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Include analytics app URLs
    path('api/', include('analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
