# Chemical Equipment Data Visualizer - Documentation

## Table of Contents
1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Backend Setup](#backend-setup)
6. [Web Frontend Setup](#web-frontend-setup)
7. [Desktop Frontend Setup](#desktop-frontend-setup)
8. [Running the Application](#running-the-application)
9. [API Endpoints](#api-endpoints)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Chemical Equipment Data Visualizer is a full-stack application that allows users to upload CSV files containing equipment data, analyze the data, and visualize statistics through both web and desktop interfaces. The system processes CSV files with equipment information and generates summary statistics including averages, type distributions, and visual charts.

---

## Tech Stack

### Backend

#### **Django 5.2.8**
- **Why**: Django is a high-level Python web framework that provides rapid development, clean design, and pragmatic solutions. It includes:
  - Built-in admin interface
  - ORM (Object-Relational Mapping) for database operations
  - Security features (CSRF protection, SQL injection prevention)
  - RESTful API support through Django REST Framework
  - Excellent documentation and large community

#### **Django REST Framework (DRF)**
- **Why**: DRF is a powerful toolkit for building Web APIs in Django. It provides:
  - Serializers for converting complex data types to/from JSON
  - ViewSets and APIViews for handling HTTP requests
  - Authentication and permissions
  - Browsable API interface
  - Easy integration with frontend frameworks

#### **Pandas**
- **Why**: Pandas is a data manipulation and analysis library. It's used for:
  - Reading and parsing CSV files efficiently
  - Data validation and cleaning
  - Statistical calculations (averages, distributions)
  - Handling large datasets with ease

#### **SQLite**
- **Why**: SQLite is a lightweight, serverless database engine. It's ideal for:
  - Development and small to medium applications
  - No separate database server required
  - Easy setup and portability
  - Sufficient for this application's data storage needs

#### **django-cors-headers**
- **Why**: Enables Cross-Origin Resource Sharing (CORS) to allow:
  - Frontend applications (running on different ports) to communicate with the backend
  - Web and desktop clients to access the API
  - Secure cross-origin requests

### Web Frontend

#### **React 19.2.0**
- **Why**: React is a popular JavaScript library for building user interfaces. It provides:
  - Component-based architecture for reusable UI elements
  - Virtual DOM for efficient rendering
  - Large ecosystem and community support
  - Easy state management
  - Excellent developer tools

#### **Chart.js & react-chartjs-2**
- **Why**: Chart.js is a powerful charting library. It's used for:
  - Creating beautiful, responsive charts
  - Multiple chart types (bar, line, pie, etc.)
  - Easy integration with React through react-chartjs-2
  - Customizable and interactive visualizations
  - Lightweight and performant

#### **Axios**
- **Why**: Axios is a promise-based HTTP client. It provides:
  - Simple API for making HTTP requests
  - Request/response interceptors
  - Automatic JSON data transformation
  - Better error handling than fetch API
  - Support for request cancellation

### Desktop Frontend

#### **PyQt5**
- **Why**: PyQt5 is a set of Python bindings for the Qt application framework. It's used for:
  - Creating native-looking desktop applications
  - Cross-platform support (Windows, macOS, Linux)
  - Rich set of widgets and components
  - Professional GUI development
  - Good documentation and examples

#### **Matplotlib**
- **Why**: Matplotlib is a plotting library for Python. It's used for:
  - Creating static, animated, and interactive visualizations
  - Integration with PyQt5 through backend_qt5agg
  - Professional-quality charts
  - Extensive customization options
  - Scientific and data visualization capabilities

#### **Requests**
- **Why**: Requests is a simple HTTP library for Python. It provides:
  - Easy-to-use API for making HTTP requests
  - Better than urllib for API communication
  - Automatic content decoding
  - Connection pooling and session management
  - File upload support

---

## Project Structure

```
chemical-visualizer/
├── backend/                    # Django backend application
│   ├── analytics/              # Main app for data processing
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── serializers.py     # Data serializers
│   │   ├── urls.py            # URL routing
│   │   └── admin.py           # Admin configuration
│   ├── backend_project/        # Django project settings
│   │   ├── settings.py        # Project configuration
│   │   ├── urls.py            # Root URL configuration
│   │   └── wsgi.py            # WSGI configuration
│   ├── manage.py              # Django management script
│   ├── venv/                  # Python virtual environment
│   └── media/                  # Uploaded files storage
│
├── frontend-web/               # React web application
│   └── chemical-web/
│       ├── src/
│       │   ├── App.js         # Main application component
│       │   ├── UploadForm.js  # File upload component
│       │   ├── TypeDistributionChart.js  # Chart component
│       │   ├── api.js         # API client configuration
│       │   └── App.css        # Application styles
│       ├── public/            # Static files
│       └── package.json       # Dependencies
│
├── frontend-desktop/           # PyQt5 desktop application
│   ├── main.py                # Main application window
│   ├── api.py                 # API client functions
│   └── venv/                  # Python virtual environment
│
└── sampledata/                 # Sample CSV files for testing
```

---

## Prerequisites

### For Backend and Desktop:
- **Python 3.8+** (Python 3.13 recommended)
- **pip** (Python package manager)
- **Virtual environment** (venv)

### For Web Frontend:
- **Node.js 14+** (Node.js 18+ recommended)
- **npm** (Node Package Manager, comes with Node.js)

---

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies (if not already installed)
```bash
pip install django djangorestframework pandas django-cors-headers
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Start Development Server
```bash
python manage.py runserver
```

The backend will be available at: **http://localhost:8000**

---

## Web Frontend Setup

### Step 1: Navigate to Web Frontend Directory
```bash
cd frontend-web/chemical-web
```

### Step 2: Install Dependencies
```bash
npm install
```

This will install all required packages including:
- react
- react-dom
- chart.js
- react-chartjs-2
- axios

### Step 3: Start Development Server
```bash
npm start
```

The web application will automatically open in your browser at: **http://localhost:3000**

### Building for Production
```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

---

## Desktop Frontend Setup

### Step 1: Navigate to Desktop Frontend Directory
```bash
cd frontend-desktop
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies (if not already installed)
```bash
pip install PyQt5 matplotlib requests
```

### Step 4: Run the Application
```bash
python main.py
```

The desktop application window will open.

---

## Running the Application

### Complete Setup (All Components)

1. **Start Backend Server** (Terminal 1):
   ```bash
   cd backend
   venv\Scripts\activate
   python manage.py runserver
   ```
   Backend runs on: `http://localhost:8000`

2. **Start Web Frontend** (Terminal 2):
   ```bash
   cd frontend-web/chemical-web
   npm start
   ```
   Web app runs on: `http://localhost:3000`

3. **Start Desktop Application** (Terminal 3 - Optional):
   ```bash
   cd frontend-desktop
   venv\Scripts\activate
   python main.py
   ```

### Important Notes:
- The backend must be running before using the web or desktop frontends
- The web frontend communicates with the backend via API calls
- The desktop application also communicates with the backend API
- Both frontends can run simultaneously

---

## API Endpoints

### Base URL: `http://localhost:8000/api/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload/` | POST | Upload a CSV file |
| `/history/` | GET | Get all uploaded datasets |
| `/summary/latest/` | GET | Get latest dataset summary |
| `/dataset/<id>/download/` | GET | Download a specific dataset file |

### Example API Usage

**Upload CSV:**
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -F "file=@sample_equipment_data.csv"
```

**Get Latest Summary:**
```bash
curl http://localhost:8000/api/summary/latest/
```

**Get History:**
```bash
curl http://localhost:8000/api/history/
```

---

## CSV File Format

The application expects CSV files with the following required columns:

- **Equipment Name** - Name of the equipment
- **Type** - Type/category of equipment
- **Flowrate** - Flow rate value (numeric)
- **Pressure** - Pressure value (numeric)
- **Temperature** - Temperature value (numeric)

### Example CSV:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Centrifugal,100.5,50.2,25.3
Pump B,Positive Displacement,85.0,45.1,22.8
```

---

## Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError: No module named 'django'**
- **Solution**: Activate the virtual environment and install dependencies:
  ```bash
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

**Problem: Port 8000 already in use**
- **Solution**: Use a different port:
  ```bash
  python manage.py runserver 8001
  ```

**Problem: Migration errors**
- **Solution**: Delete database and re-run migrations:
  ```bash
  rm db.sqlite3
  python manage.py makemigrations
  python manage.py migrate
  ```

### Web Frontend Issues

**Problem: npm install fails**
- **Solution**: Clear npm cache and try again:
  ```bash
  npm cache clean --force
  npm install
  ```

**Problem: Port 3000 already in use**
- **Solution**: React will automatically use the next available port (3001, 3002, etc.)

**Problem: Cannot connect to backend**
- **Solution**: 
  1. Ensure backend is running on port 8000
  2. Check `src/api.js` has correct base URL
  3. Verify CORS is enabled in backend settings

### Desktop Frontend Issues

**Problem: PyQt5 not found**
- **Solution**: Install PyQt5:
  ```bash
  pip install PyQt5
  ```

**Problem: Application window doesn't open**
- **Solution**: Check if backend is running and accessible at `http://localhost:8000`

**Problem: Import errors**
- **Solution**: Ensure all dependencies are installed:
  ```bash
  pip install PyQt5 matplotlib requests
  ```

### General Issues

**Problem: CORS errors in browser console**
- **Solution**: Ensure `django-cors-headers` is installed and `CORS_ALLOW_ALL_ORIGINS = True` in settings.py

**Problem: File upload fails**
- **Solution**: 
  1. Check file format matches required columns
  2. Ensure file is a valid CSV
  3. Check backend logs for specific error messages

---

## Development Tips

1. **Backend Development**:
   - Use Django admin at `http://localhost:8000/admin/` to manage data
   - Check Django logs in terminal for debugging
   - Use Django REST Framework browsable API for testing endpoints

2. **Web Frontend Development**:
   - React hot-reloads automatically on file changes
   - Use browser DevTools for debugging
   - Check Network tab for API call issues

3. **Desktop Frontend Development**:
   - Use print statements for debugging
   - Check terminal output for errors
   - Test API connectivity independently

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

## License

This project is provided as-is for educational and development purposes.

---

## Support

For issues or questions, please check the troubleshooting section above or review the code documentation in the source files.

