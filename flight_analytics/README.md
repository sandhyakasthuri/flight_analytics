# flight_analytics
DS_Masterclass_project
# ✈️ Air Tracker: Flight Analytics

A comprehensive aviation data analytics project built using the AeroDataBox API, PostgreSQL, and Streamlit.

##  Project Overview
This project fetches real-time aviation data from the AeroDataBox API, stores it in a PostgreSQL database, and visualises it through an interactive Streamlit dashboard.

## Project Structure
flight_analytics/
├── Flight_Analytics.ipynb  # Data extraction and cleaning
├── sql_imp.ipynb           # SQL queries
├── app.py                  # Streamlit application
├── airports_clean.csv      # Airport data
├── flights_master.csv             # Flight data
├── aircraft.csv            # Aircraft data
├── airport_delays.csv      # Delay statistics
└── .streamlit/
└── config.toml         # Streamlit theme config
## 🛠️ Tech Stack
- **Language:** Python
- **Database:** PostgreSQL
- **API:** AeroDataBox (via RapidAPI)
- **Application:** Streamlit
- **Libraries:** pandas, sqlalchemy, psycopg2, pydeck

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/sandhyakasthuri/flight_analytics.git
cd flight_analytics
```

### 2. Install dependencies
```bash
pip install pandas sqlalchemy psycopg2 streamlit pydeck
```

### 3. Setup PostgreSQL
- Create a database called `flight_analytics`
- Update the connection string in `app.py` with your credentials:
```python
engine = create_engine("postgresql+psycopg2://username:password@localhost:port/flight_analytics")
```

### 4. Load data into PostgreSQL
- Run `Flight_Analytics.ipynb` to fetch and clean data
- Run `sql_imp.ipynb` to load CSVs into PostgreSQL

### 5. Run the Streamlit app
```bash
python -m streamlit run app.py
```

## Features
- **Homepage Dashboard** — summary stats, quick insights and world map of airports
- **Search & Filter Flights** — filter by flight number, airline, status, origin
- **Airport Details Viewer** — explore airport info and linked flights
- **Delay Analysis** — visualise delays and cancellations by airport
- **Route Leaderboards** — busiest routes and most delayed airports
- **Airline Performance** — delay percentage and stats by airline

##  Database Schema
- airport — airport details including location and timezone
- flights — flight schedules, status and route information
- aircraft — aircraft registration, model and manufacturer
- airport_delays — delay statistics per airport

## Data
- **Airports:** 15 major international airports
- **Flights:** 17,640 flights fetched on 2026-05-31
- **Aircraft:** 98 unique aircraft
- **Delays:** 14 airports with delay statistics
