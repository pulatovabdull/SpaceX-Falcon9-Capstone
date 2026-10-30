# SpaceX Falcon 9 Landing Prediction

## Project overview
This project analyzes historical SpaceX launch records and explores
factors associated with successful first-stage landings.

It was completed as part of the IBM Applied Data Science Capstone.

## Project components
- API data collection and documented prepared-data fallback
- Web scraping with BeautifulSoup
- Data cleaning and landing-outcome labels
- Exploratory analysis with SQL, pandas, Matplotlib, and Seaborn
- Interactive mapping with Folium
- Interactive dashboard with Plotly Dash
- Classification using Logistic Regression, SVM, Decision Tree, and KNN

## Repository structure
- notebooks/: executed analysis notebooks
- dashboard/: Dash application and its input dataset
- screenshots/: charts, maps, and dashboard views
- presentation/: project presentation

## Running the dashboard
Install the required packages:

    python -m pip install pandas dash plotly

From the dashboard folder, run:

    python spacex-dash-app.py

Keep spacex_launch_dash.csv in the same folder as the script.
Check the script for the configured server port.

## Data and limitations
The project uses course-provided historical datasets.
Dataset scope differs between the SQL, dashboard, and modeling exercises.

Live SpaceX API detail requests returned HTTP 522 during the project.
The prepared course dataset was used as a documented fallback.

## Model results
See the executed machine-learning notebook for actual validation
and test scores.

## Attribution
Course materials and datasets: IBM Skills Network / Coursera.
Original course notices are retained where applicable.
