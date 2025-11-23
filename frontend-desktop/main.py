"""
Desktop Application for Chemical Equipment Data Visualizer

PyQt5-based desktop application that provides a GUI for:
- Uploading CSV files
- Viewing summary statistics
- Displaying type distribution charts
- Browsing upload history

Requires:
- PyQt5
- matplotlib
- requests
- Backend API running on http://localhost:8000
"""

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFileDialog, QLabel, 
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import api

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.auth = None  # tuple (user, pass) if using basic auth
        self.initUI()
        self.refresh_data()
        
    def initUI(self):
        self.setWindowTitle('Chemical Equipment Data Visualizer')
        self.setGeometry(100, 100, 1000, 700)
        
        main_layout = QVBoxLayout()
        
        # Header with upload button
        header_layout = QHBoxLayout()
        self.upload_btn = QPushButton('Upload CSV File')
        self.upload_btn.clicked.connect(self.upload)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.refresh_btn = QPushButton('Refresh Data')
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        header_layout.addWidget(self.upload_btn)
        header_layout.addWidget(self.refresh_btn)
        header_layout.addStretch()
        
        self.msg = QLabel('Ready to upload CSV files')
        self.msg.setStyleSheet("padding: 5px; color: #666;")
        header_layout.addWidget(self.msg)
        
        main_layout.addLayout(header_layout)
        
        # Tabs for different views
        self.tabs = QTabWidget()
        
        # Summary Tab
        summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        
        # Summary stats
        self.stats_label = QLabel('No data available')
        self.stats_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        summary_layout.addWidget(self.stats_label)
        
        # Chart
        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        summary_layout.addWidget(self.canvas)
        
        summary_widget.setLayout(summary_layout)
        self.tabs.addTab(summary_widget, 'Summary & Charts')
        
        # History Tab
        history_widget = QWidget()
        history_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(['Filename', 'Upload Date', 'Total Records'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_layout.addWidget(self.history_table)
        
        history_widget.setLayout(history_layout)
        self.tabs.addTab(history_widget, 'Upload History')
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
    def upload(self):
        """Handle CSV file upload"""
        path, _ = QFileDialog.getOpenFileName(
            self, 'Open CSV File', '', 'CSV Files (*.csv)'
        )
        if not path:
            return
            
        self.msg.setText('Uploading...')
        self.msg.setStyleSheet("padding: 5px; color: #2196F3;")
        self.upload_btn.setEnabled(False)
        
        try:
            res = api.upload_csv(path, auth=self.auth)
            self.msg.setText(f'✓ Uploaded successfully: {res.get("original_filename", "file")}')
            self.msg.setStyleSheet("padding: 5px; color: #4CAF50; font-weight: bold;")
            # Refresh data after upload
            self.refresh_data()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', str(e))
                except:
                    error_msg = e.response.text or str(e)
            self.msg.setText(f'✗ Error: {error_msg}')
            self.msg.setStyleSheet("padding: 5px; color: #f44336; font-weight: bold;")
        except Exception as e:
            self.msg.setText(f'✗ Error: {str(e)}')
            self.msg.setStyleSheet("padding: 5px; color: #f44336; font-weight: bold;")
        finally:
            self.upload_btn.setEnabled(True)
            
    def refresh_data(self):
        """Refresh summary and history data"""
        try:
            # Get latest summary
            summary_data = api.get_latest_summary(auth=self.auth)
            self.update_summary(summary_data)
            
            # Get history
            history_data = api.get_history(auth=self.auth)
            self.update_history(history_data)
            
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 404:
                    # No data yet, that's okay
                    self.stats_label.setText('No data available. Upload a CSV file to get started.')
                    self.plot_empty()
                    self.history_table.setRowCount(0)
                    return
            self.msg.setText(f'Error refreshing: {str(e)}')
            self.msg.setStyleSheet("padding: 5px; color: #f44336;")
        except Exception as e:
            self.msg.setText(f'Error: {str(e)}')
            self.msg.setStyleSheet("padding: 5px; color: #f44336;")
            
    def update_summary(self, summary_data):
        """Update the summary display"""
        summary = summary_data.get('summary', {})
        
        if not summary:
            self.stats_label.setText('No summary data available')
            self.plot_empty()
            return
            
        # Update stats label
        stats_text = f"""
        <b>Latest Dataset Summary</b><br>
        <b>File:</b> {summary_data.get('original_filename', 'N/A')}<br>
        <b>Upload Date:</b> {summary_data.get('uploaded_at', 'N/A')}<br><br>
        <b>Total Records:</b> {summary.get('total_count', 0)}<br>
        <b>Average Flowrate:</b> {summary.get('averages', {}).get('Flowrate', 0):.2f}<br>
        <b>Average Pressure:</b> {summary.get('averages', {}).get('Pressure', 0):.2f}<br>
        <b>Average Temperature:</b> {summary.get('averages', {}).get('Temperature', 0):.2f}
        """
        self.stats_label.setText(stats_text)
        
        # Update chart
        type_dist = summary.get('type_distribution', {})
        if type_dist:
            self.plot_summary(type_dist)
        else:
            self.plot_empty()
            
    def plot_summary(self, type_distribution):
        """Plot the type distribution chart"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        keys = list(type_distribution.keys())
        vals = [type_distribution[k] for k in keys]
        
        bars = ax.bar(keys, vals, color='#2196F3', alpha=0.7)
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Equipment Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def plot_empty(self):
        """Show empty chart"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'No data to display', 
                ha='center', va='center', fontsize=14, color='gray')
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
        
    def update_history(self, history_data):
        """Update the history table"""
        self.history_table.setRowCount(len(history_data))
        
        for row, item in enumerate(history_data):
            filename = item.get('original_filename', 'Unknown')
            uploaded_at = item.get('uploaded_at', 'N/A')
            total_count = item.get('summary', {}).get('total_count', 0) if item.get('summary') else 0
            
            self.history_table.setItem(row, 0, QTableWidgetItem(str(filename)))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(uploaded_at)))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(total_count)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
