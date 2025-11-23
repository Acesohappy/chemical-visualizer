"""
Serializers for the Analytics application.

This module defines serializers for converting model instances
to JSON and vice versa for API responses.
"""

from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dataset model.
    
    Serializes all fields of the Dataset model for API responses.
    """
    
    class Meta:
        """Metadata for the serializer."""
        model = Dataset
        fields = '__all__'
        read_only_fields = ['uploaded_at']
