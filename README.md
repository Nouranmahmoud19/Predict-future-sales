# Predict Future Sales – Bike Sales Forecasting Using Machine Learning

Welcome to the **Predict Future Sales** project! This project uses machine learning to predict bike sales based on historical data and weather conditions. By analyzing time series data and weather-related features, we aim to forecast the **number of bikes sold** accurately. The project also includes a user-friendly **Streamlit dashboard** for data visualization and real-time sales predictions.

---

## What’s the Project About?

The goal of this project is to predict bike sales by analyzing historical sales data and weather conditions. By using machine learning models, we can accurately forecast how many bikes will be sold, helping businesses optimize their operations and make better decisions.

The dashboard allows users to:
- Explore the relationship between weather conditions and bike sales.
- Input weather data and see real-time predictions for future sales.

---

## Key Features

- **Data Exploration & Analysis:** Dive into the data to identify trends, patterns, and outliers, focusing on how weather affects sales.
- **Visualizations:** Beautiful and interactive charts created with **Matplotlib**, **Seaborn**, and **Plotly** to showcase key insights.
- **Prediction Models:** We used several machine learning models such as **Linear Regression**, **Random Forest**, and **XGBoost** to predict future sales.
- **Streamlit Dashboard:** An interactive web app that allows users to visualize data and predict future sales by entering specific weather features.

---

## Technologies Used

This project is built using the following technologies:

- **Python** – The core language for data analysis, machine learning, and app development.
- **Libraries:**
  - Data Processing: `pandas`, `numpy`
  - Visualization: `matplotlib`, `seaborn`, `plotly`
  - Machine Learning: `scikit-learn`, `xgboost`
  - Web App: `streamlit`

---

## Streamlit Dashboard

The **Streamlit dashboard** is where you can see the magic in action. It lets you:

- **Visualize Data:** Get insights into trends and patterns in the sales data.
- **Make Predictions:** Input weather information (e.g., temperature, season) and get an instant prediction of bike sales.

The app is simple and intuitive—just run it and start exploring!

---

## Project Structure

Here’s a quick overview of the project structure:

predict-future-sales/
│
├── data/ # Contains raw and processed datasets
├── notebooks/ # Jupyter notebooks for EDA and model experiments
├── models/ # Trained machine learning models
├── app.py # The Streamlit app running the dashboard
├── utils.py # Helper functions used throughout the project
├── README.md # This file
└── requirements.txt # Required Python libraries

---

## How to Get Started

To get started, follow these simple steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ayahijab/predict-future-sales.git
   cd predict-future-sales
2. **Install the dependencies** :
    pip install -r requirements.txt
3. **Run the Streamlit app** :
    streamlit_dashboard run app.py   

Once the app is running, you can start exploring the data and even input your own weather data to predict future sales.

Future Improvements
Here are a few things we plan to add in the future:

Real-Time Weather Data: Integrate real-time weather data APIs for more accurate predictions.

Model Comparison: Let users compare predictions from different models to choose the best one.

Cloud Deployment: Host the Streamlit app online so others can access it without installing anything.
