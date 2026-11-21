# 🚖 Uber Trip Explorer & Analytics Dashboard

An interactive, no-code data storytelling web application built with **Python** and **Gradio** to analyze and visualize Uber trip demand, active vehicle fleets, and dispatching base operations.

---

## 📌 Project Overview

This project provides an intuitive analytics dashboard for exploring historical Uber dispatch data. By combining data manipulation with dynamic interactive charts, users can filter by date ranges and dispatching bases to uncover travel patterns, rush hours, and vehicle fleet activity.

Developed as part of the **Unified Mentor Internship Program**.

---

## 🚀 Key Features

- **📍 Dynamic Dispatching Base Filtering**: Filter records across all major dispatching bases (`B02512`, `B02765`, `B02764`, `B02682`, `B02617`, `B02598`) or view combined performance.
- **📊 Interactive Visualizations**:
  - **Hourly Peak Trips (Bar Chart)**: 24-hour demand breakdown to identify morning and evening rush hours.
  - **Base Distribution (Pie Chart)**: Market share of completed trips across dispatching bases.
  - **Daily Trip Trend (Line Chart)**: Daily trip completion patterns over time.
- **📈 Real-time KPI Summary Cards**:
  - **Total Trips Completed**
  - **Total Active Vehicles**
  - **Top Performing Base**
  - **Peak Rush Hour & Demand Volume**
- **📋 Live Data Table**: Interactive preview of the filtered trip records.

---

## 🛠️ Tools & Technologies

- **Language**: Python 3.x
- **App Framework**: [Gradio](https://gradio.app/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **Data Visualization**: [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/)

---

## 📁 Dataset Details

The dataset (`Uber file.csv`) tracks Uber dispatching activity with the following attributes:
- `Date/Time`: Timestamp of the record
- `dispatching_base_number`: TLC base license code
- `active_vehicles`: Number of active vehicles on the road
- `trips`: Number of completed trips

---

## 🧪 Installation & How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/uber-trip-explorer.git
cd uber-trip-explorer
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Open your browser and navigate to the local URL displayed in the terminal (typically `http://127.0.0.1:7860`).

---

## 👤 Author

- **Ashmitha A** – B.Sc. Data Science
- **Project Type**: Unified Mentor Internship Project
