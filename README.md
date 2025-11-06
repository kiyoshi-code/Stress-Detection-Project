# Smart Cities Stress Detection Project

This project combines machine learning with a modern web interface to predict stress levels based on lifestyle factors.

## Project Structure

```
project/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── backend/           # Flask backend
│   ├── app.py
│   └── requirements.txt
└── main.ipynb        # Jupyter notebook with ML model
```

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm run dev
```

The frontend will be available at http://localhost:5173

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install requirements:
```powershell
pip install -r requirements.txt
```

4. Start the Flask server:
```powershell
python app.py
```

The backend API will be available at http://localhost:5000

## Features

1. Interactive Stress Prediction
   - Input lifestyle factors
   - Get instant stress level predictions
   - Visual feedback on results

2. Data Insights
   - Feature importance visualization
   - Model performance comparison
   - Key findings summary

3. Project Overview
   - SDG alignment
   - Methodology explanation
   - Impact analysis