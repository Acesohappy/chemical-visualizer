/**
 * Upload Form Component
 * 
 * Handles CSV file uploads to the backend API.
 * Displays upload status and error messages.
 */

import React, { useState } from 'react';
import api from './api';

/**
 * UploadForm Component
 * 
 * @param {Function} onUploadSuccess - Callback function called after successful upload
 */
export default function UploadForm({ onUploadSuccess }) {
  // Component state
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  
  /**
   * Handle form submission
   * Uploads the selected CSV file to the backend
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate file selection
    if (!file) {
      setMessage('Please choose a file');
      return;
    }
    
    setLoading(true);
    setMessage('');
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // Upload file
      await api.post('upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      // Success
      setMessage('Uploaded successfully!');
      setFile(null);
      
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = '';
      }
      
      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess();
      }
      
    } catch (err) {
      // Handle errors
      const errorData = err.response?.data;
      let errorMessage = 'Upload failed';
      
      if (errorData) {
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData.error) {
          errorMessage = errorData.error;
        } else {
          errorMessage = JSON.stringify(errorData);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  /**
   * Handle file selection
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setMessage(''); // Clear previous messages
  };
  
  /**
   * Determine message CSS class based on content
   */
  const getMessageClass = () => {
    return message.toLowerCase().includes('success') 
      ? 'success-msg' 
      : 'error-msg';
  };
  
  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <div className="file-input-wrapper">
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleFileChange}
          disabled={loading}
        />
      </div>
      
      <button 
        type="submit" 
        disabled={loading || !file}
      >
        {loading ? 'Uploading...' : 'Upload CSV'}
      </button>
      
      {message && (
        <p className={getMessageClass()}>
          {message}
        </p>
      )}
    </form>
  );
}
