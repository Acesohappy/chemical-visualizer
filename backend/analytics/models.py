"""
Database models for the Analytics application.

This module defines the Dataset model which stores uploaded CSV files
and their computed summary statistics.
"""

from django.db import models


class Dataset(models.Model):
    """
    Model representing an uploaded CSV dataset.
    
    Stores the uploaded file, metadata, and computed summary statistics.
    """
    
    file = models.FileField(
        upload_to='uploads/',
        help_text='The uploaded CSV file'
    )
    
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the file was uploaded'
    )
    
    summary = models.JSONField(
        null=True,
        blank=True,
        help_text='Computed summary statistics (counts, averages, distributions)'
    )
    
    original_filename = models.CharField(
        max_length=255,
        blank=True,
        help_text='Original filename of the uploaded file'
    )
    
    preview_html = models.TextField(
        blank=True,
        help_text='Optional HTML preview of the dataset'
    )
    
    class Meta:
        """Metadata for the Dataset model."""
        ordering = ['-uploaded_at']
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
    
    def __str__(self):
        """String representation of the dataset."""
        return f"{self.original_filename or 'Unknown'} @ {self.uploaded_at}"
