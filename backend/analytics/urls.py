"""
URL configuration for the Analytics application.

Defines the API endpoints for uploading, retrieving, and downloading datasets.
"""

from django.urls import path
from .views import (
    UploadCSV,
    HistoryList,
    DatasetDownload,
    LatestSummary
)

app_name = 'analytics'

urlpatterns = [
    # Upload endpoint
    path('upload/', UploadCSV.as_view(), name='upload'),
    
    # History endpoint
    path('history/', HistoryList.as_view(), name='history'),
    
    # Latest summary endpoint
    path('summary/latest/', LatestSummary.as_view(), name='latest_summary'),
    
    # Download endpoint
    path('dataset/<int:pk>/download/', DatasetDownload.as_view(), name='download'),
]
