/**
 * Main App Component
 * 
 * Chemical Equipment Data Visualizer - Web Application
 * Displays dashboard with upload functionality, summary statistics,
 * charts, and upload history.
 */

import React, { useState, useEffect } from 'react';
import './App.css';
import UploadForm from './UploadForm';
import TypeDistributionChart from './TypeDistributionChart';
import api from './api';

function App() {
  // State management
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  /**
   * Fetch the latest dataset summary from the API
   */
  const fetchLatestSummary = async () => {
    try {
      const response = await api.get('summary/latest/');
      setSummary(response.data);
      setError('');
    } catch (err) {
      // Only show error if it's not a 404 (no data yet)
      if (err.response?.status !== 404) {
        setError(err.response?.data?.error || 'Failed to fetch summary');
      }
    }
  };

  /**
   * Fetch upload history from the API
   */
  const fetchHistory = async () => {
    try {
      const response = await api.get('history/');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  /**
   * Load data on component mount
   */
  useEffect(() => {
    fetchLatestSummary();
    fetchHistory();
  }, []);

  /**
   * Handle successful file upload
   * Refreshes summary and history data
   */
  const handleUploadSuccess = () => {
    fetchLatestSummary();
    fetchHistory();
  };

  /**
   * Format a number to 2 decimal places
   */
  const formatNumber = (value) => {
    return value ? value.toFixed(2) : 'N/A';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chemical Equipment Data Visualizer</h1>
      </header>
      
      <main className="App-main">
        {/* Upload Section */}
        <section className="upload-section">
          <h2>Upload CSV File</h2>
          <UploadForm onUploadSuccess={handleUploadSuccess} />
        </section>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Summary Dashboard */}
        {summary && (
          <section className="dashboard-section">
            <h2>Latest Summary</h2>
            
            {/* Summary Statistics Cards */}
            <div className="summary-grid">
              <div className="summary-card">
                <h3>Total Records</h3>
                <p className="summary-value">
                  {summary.summary?.total_count || 0}
                </p>
              </div>
              
              <div className="summary-card">
                <h3>Average Flowrate</h3>
                <p className="summary-value">
                  {formatNumber(summary.summary?.averages?.Flowrate)}
                </p>
              </div>
              
              <div className="summary-card">
                <h3>Average Pressure</h3>
                <p className="summary-value">
                  {formatNumber(summary.summary?.averages?.Pressure)}
                </p>
              </div>
              
              <div className="summary-card">
                <h3>Average Temperature</h3>
                <p className="summary-value">
                  {formatNumber(summary.summary?.averages?.Temperature)}
                </p>
              </div>
            </div>

            {/* Type Distribution Chart */}
            {summary.summary?.type_distribution && (
              <div className="chart-section">
                <h3>Equipment Type Distribution</h3>
                <TypeDistributionChart 
                  distribution={summary.summary.type_distribution} 
                />
              </div>
            )}
          </section>
        )}

        {/* History Section */}
        <section className="history-section">
          <h2>Upload History</h2>
          
          {history.length === 0 ? (
            <p>No uploads yet. Upload a CSV file to get started.</p>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-info">
                    <strong>
                      {item.original_filename || 'Unknown'}
                    </strong>
                    <span className="history-date">
                      {new Date(item.uploaded_at).toLocaleString()}
                    </span>
                  </div>
                  
                  {item.id && (
                    <a 
                      href={`http://localhost:8000/api/dataset/${item.id}/download/`}
                      className="download-link"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Download
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
