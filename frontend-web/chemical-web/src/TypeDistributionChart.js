/**
 * Type Distribution Chart Component
 * 
 * Displays a bar chart showing the distribution of equipment types
 * using Chart.js and react-chartjs-2.
 */

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

/**
 * TypeDistributionChart Component
 * 
 * @param {Object} distribution - Object mapping equipment types to counts
 * @param {Object} distribution[type] - Count for each equipment type
 */
export default function TypeDistributionChart({ distribution }) {
  // Validate distribution data
  if (!distribution || Object.keys(distribution).length === 0) {
    return (
      <p className="no-data-message">
        No distribution data available
      </p>
    );
  }

  // Extract labels and values from distribution object
  const labels = Object.keys(distribution);
  const values = labels.map(label => distribution[label]);

  // Chart data configuration
  const chartData = {
    labels,
    datasets: [{ 
      label: 'Count', 
      data: values,
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  };

  // Chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        display: true,
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        enabled: true,
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
}
