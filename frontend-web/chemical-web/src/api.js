/**
 * API Configuration
 * 
 * Axios instance configured with base URL for backend API.
 * All API requests should use this instance.
 */

import axios from 'axios';

// Base URL for the backend API
const BASE_URL = 'http://localhost:8000/api/';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor (for adding auth tokens, etc.)
api.interceptors.request.use(
  (config) => {
    // Add any default headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (for handling errors globally)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors here if needed
    return Promise.reject(error);
  }
);

export default api;
