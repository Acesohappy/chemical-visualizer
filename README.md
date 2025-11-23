# Chemical Equipment Data Visualizer

A full-stack application for uploading, analyzing, and visualizing chemical equipment data from CSV files. Available as both a web application (React) and desktop application (PyQt5).

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **Node.js 14+** (Node.js 18+ recommended)
- **npm** (comes with Node.js)

### Download & Setup

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd chemical-visualizer
   ```

2. **Set up the Backend (Django)**
   ```bash
   cd backend
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   # Install dependencies (if needed)
   pip install django djangorestframework pandas django-cors-headers
   
   # Run migrations
   python manage.py migrate
   
   # Start the server
   python manage.py runserver
   ```
   Backend will run at: **http://localhost:8000**

3. **Set up the Web Frontend (React)**
   
   Open a new terminal:
   ```bash
   cd frontend-web/chemical-web
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm start
   ```
   Web app will open at: **http://localhost:3000**

4. **Set up the Desktop Frontend (PyQt5)** - Optional
   
   Open a new terminal:
   ```bash
   cd frontend-desktop
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   # Install dependencies (if needed)
   pip install PyQt5 matplotlib requests
   
   # Run the application
   python main.py
   ```

## 📖 Usage

### Web Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Choose File" and select a CSV file with equipment data
3. Click "Upload and Analyze"
4. View the statistics and charts showing:
   - Average values
   - Type distribution
   - Visual charts

### Desktop Application

1. Run `python main.py` from the `frontend-desktop` directory
2. Click "Browse" to select a CSV file
3. Click "Upload and Analyze"
4. View the results in the application window

### Sample Data

A sample CSV file is available in the `sampledata/` directory for testing.

## 📁 Project Structure

```
chemical-visualizer/
├── backend/              # Django REST API
├── frontend-web/         # React web application
├── frontend-desktop/     # PyQt5 desktop application
└── sampledata/           # Sample CSV files
```

## 🔧 API Endpoints

- `POST /api/upload/` - Upload and analyze CSV file
- `GET /api/stats/` - Get statistics for uploaded files

## 📚 Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework, Pandas
- **Web Frontend**: React, Chart.js, Axios
- **Desktop Frontend**: PyQt5, Matplotlib

## 📝 License

[Add your license here]

