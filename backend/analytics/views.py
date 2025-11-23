"""
API Views for the Analytics application.

This module handles CSV file uploads, data processing, and provides
endpoints for retrieving summaries and download history.
"""

import pandas as pd
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset
from .serializers import DatasetSerializer


# Required columns for CSV validation
REQUIRED_COLUMNS = {
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature'
}

# Maximum number of datasets to keep
MAX_DATASETS = 5


class UploadCSV(APIView):
    """
    Handle CSV file uploads.
    
    Validates the CSV file structure, processes the data to generate
    summary statistics, and stores the dataset. Maintains only the
    most recent MAX_DATASETS datasets.
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        """
        Process CSV file upload.
        
        Args:
            request: HTTP request containing the CSV file
            format: Optional format parameter
            
        Returns:
            Response with dataset data on success, or error message on failure
        """
        # Get uploaded file
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read and validate CSV
            dataframe = pd.read_csv(csv_file)
            
            # Validate required columns
            if not REQUIRED_COLUMNS.issubset(set(dataframe.columns)):
                return Response({
                    'error': 'CSV missing required columns',
                    'required': list(REQUIRED_COLUMNS),
                    'found': list(dataframe.columns)
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate summary statistics
            summary = self._calculate_summary(dataframe)
            
            # Save dataset
            dataset = Dataset.objects.create(
                file=csv_file,
                summary=summary,
                original_filename=getattr(csv_file, 'name', 'uploaded.csv')
            )
            
            # Maintain only the most recent datasets
            self._cleanup_old_datasets()
            
            # Return serialized response
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except pd.errors.EmptyDataError:
            return Response(
                {'error': 'CSV file is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except pd.errors.ParserError as e:
            return Response(
                {'error': f'Invalid CSV format: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Processing error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _calculate_summary(self, dataframe):
        """
        Calculate summary statistics from the dataframe.
        
        Args:
            dataframe: pandas DataFrame containing the CSV data
            
        Returns:
            dict: Summary statistics including total count, averages, and type distribution
        """
        total_count = len(dataframe)
        
        # Calculate averages for numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        averages = dataframe[numeric_columns].mean().to_dict()
        
        # Calculate type distribution
        type_distribution = dataframe['Type'].value_counts().to_dict()
        
        return {
            'total_count': int(total_count),
            'averages': {key: float(value) for key, value in averages.items()},
            'type_distribution': type_distribution
        }
    
    def _cleanup_old_datasets(self):
        """
        Remove old datasets, keeping only the most recent MAX_DATASETS.
        """
        while Dataset.objects.count() > MAX_DATASETS:
            oldest = Dataset.objects.earliest('uploaded_at')
            # Delete associated file
            if oldest.file:
                oldest.file.delete(save=False)
            oldest.delete()


class HistoryList(APIView):
    """
    Retrieve list of all uploaded datasets.
    
    Returns datasets ordered by upload date (most recent first).
    """
    
    def get(self, request, format=None):
        """
        Get all datasets.
        
        Args:
            request: HTTP request
            format: Optional format parameter
            
        Returns:
            Response with list of all datasets
        """
        datasets = Dataset.objects.all().order_by('-uploaded_at')
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DatasetDownload(APIView):
    """
    Download a specific dataset file.
    
    Allows users to download previously uploaded CSV files.
    """
    
    def get(self, request, pk, format=None):
        """
        Download dataset file by primary key.
        
        Args:
            request: HTTP request
            pk: Primary key of the dataset
            format: Optional format parameter
            
        Returns:
            FileResponse with the CSV file, or error message if not found
        """
        try:
            dataset = Dataset.objects.get(pk=pk)
            
            if not dataset.file:
                return Response(
                    {'error': 'File not found for this dataset'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Return file as download
            filename = dataset.original_filename or 'dataset.csv'
            return FileResponse(
                dataset.file.open(), 
                as_attachment=True, 
                filename=filename
            )
            
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class LatestSummary(APIView):
    """
    Retrieve the latest dataset summary.
    
    Returns summary statistics for the most recently uploaded dataset.
    """
    
    def get(self, request, format=None):
        """
        Get latest dataset summary.
        
        Args:
            request: HTTP request
            format: Optional format parameter
            
        Returns:
            Response with latest summary data, or error if no datasets exist
        """
        try:
            latest_dataset = Dataset.objects.latest('uploaded_at')
            
            return Response({
                'summary': latest_dataset.summary,
                'uploaded_at': latest_dataset.uploaded_at,
                'original_filename': latest_dataset.original_filename
            }, status=status.HTTP_200_OK)
            
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'No datasets found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
