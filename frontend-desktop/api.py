"""
API Client Module

Handles all HTTP requests to the backend API.
Provides functions for uploading files, retrieving summaries, and history.
"""

import requests
import os

# Backend API base URL
BASE = 'http://localhost:8000/api/'

def upload_csv(filepath, auth=None):
    """Upload a CSV file to the backend"""
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'text/csv')}
        resp = requests.post(BASE + 'upload/', files=files, auth=auth)
        resp.raise_for_status()
    return resp.json()

def get_latest_summary(auth=None):
    """Get the latest dataset summary"""
    resp = requests.get(BASE + 'summary/latest/', auth=auth)
    resp.raise_for_status()
    return resp.json()

def get_history(auth=None):
    """Get upload history"""
    resp = requests.get(BASE + 'history/', auth=auth)
    resp.raise_for_status()
    return resp.json()
