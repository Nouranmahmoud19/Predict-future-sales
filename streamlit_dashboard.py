
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np


st.set_page_config(page_title="Bike sharing Dashboard", layout="wide")

df = pd.read_csv("cleaned_df.csv")  

# Data preprocessing

df['season'] = df['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
df['weekday'] = df['weekday'].map({0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"})
df['year'] = df['year'].map({0: 2011, 1: 2012})
df['weather'] = df['weather'].map({1: "Clear", 2: "Mist", 3: "Light Snow", 4: "Heavy Rain"})
df['month'] = df['month'].map({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})

# reverse normalization in columns 
temp_max = 41
atemp_max = 50
humidity_max = 100
windspeed_max = 67

df["temp"] = df["temp"] * temp_max
df["atemp"] = df["atemp"] * atemp_max
df["humidity"] = df["humidity"] * humidity_max
df["windspeed"] = df["windspeed"] * windspeed_max

#make new column part of day
def get_part_of_day(hour):
    hour = int(hour)
    if 5 <= hour <= 11:
        return "Morning"
    elif 12 <= hour <= 16:
        return "Afternoon"
    elif 17 <= hour <= 20:
        return "Evening"
    else:
        return "Night"

df["part_of_day"] = df["hour"].astype(int).apply(get_part_of_day)

#make new column for rush hour
def is_rush_hour(hour):
    # Define the rush hour as 7-9 AM and 5-7 PM
    if (7 <= hour <= 9) or (17 <= hour <= 19):
        return 1
    else:
        return 0

df['rush_hour'] = df['hour'].apply(is_rush_hour)


# Sidebar filters using selectbox
st.sidebar.header("📊 Filter the Data")
year = st.sidebar.selectbox("Select Year", sorted(df['year'].unique()))
month = st.sidebar.selectbox("Select Month", sorted(df['month'].unique()))
weekday = st.sidebar.selectbox("Select Weekday", sorted(df['weekday'].unique()))
weather = st.sidebar.selectbox("Select Weather", sorted(df['weather'].unique()))
part_of_day=st.sidebar.selectbox("Select Part of Day", sorted(df['part_of_day'].unique()))

# Filter the data based on sidebar selections
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['year'] == year]
df_filtered = df_filtered[df_filtered['month'] == month]
df_filtered = df_filtered[df_filtered['weekday'] == weekday]
df_filtered = df_filtered[df_filtered['weather'] == weather]

# KPIs Section
st.title("🚲 Bike Sharing Dashboard")
st.markdown("### Overview of Bike Sharing")

col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", f"{df_filtered['count'].sum():,}")
col2.metric("Casual Users", f"{df_filtered['casual'].sum():,}")
col3.metric("Registered Users", f"{df_filtered['registered'].sum():,}")

# Daily trend - Line chart
st.markdown("### 📅 Daily Ride Trend")
daily = df_filtered.groupby('datetime')['count'].sum().reset_index()
fig1 = px.line(daily, x='datetime', y='count', title="Total Rides per Day", template="plotly_dark")
fig1.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Date", yaxis_title="Total Rides")
st.plotly_chart(fig1, use_container_width=True)

# Season distribution - Bar chart
st.markdown("### 🌦️ Rides by Season")
season_df = df_filtered.groupby('season')['count'].sum().reset_index()
fig2 = px.bar(season_df, x='season', y='count', color='season', title="Total Rides per Season", template="plotly_dark")
fig2.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Season", yaxis_title="Total Rides")
st.plotly_chart(fig2, use_container_width=True)

# Temperature scatter plot with trendline
st.markdown("### 🌡️ Temperature Effect on Rides")
fig3 = px.scatter(df_filtered, x='temp', y='count', color='season', title="Temperature vs Ride Count", template="plotly_dark")
fig3.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Temperature", yaxis_title="Total Rides")
st.plotly_chart(fig3, use_container_width=True)


st.markdown("### 🌅 Ride Distribution by Part of Day")
part_day_df = df_filtered.groupby('part_of_day')['count'].sum().reset_index().sort_values(by='count', ascending=False)

fig_part_day = px.bar(part_day_df,x='part_of_day',y='count',color='part_of_day',title="Total Rides by Part of Day",template="plotly_dark")
fig_part_day.update_layout(xaxis_title="Part of Day",yaxis_title="Total Rides",title_font_size=24,title_x=0.5)
st.plotly_chart(fig_part_day, use_container_width=True)

st.markdown("### 🧍‍♂️ User Type Distribution")
user_counts = df_filtered[['casual', 'registered']].sum().reset_index()
user_counts.columns = ['User Type', 'Count']
fig6 = px.pie(user_counts, values='Count', names='User Type', title='User Type Proportion', template="plotly_dark")
st.plotly_chart(fig6, use_container_width=True)

st.markdown("### 💧 Humidity vs Ride Count")
fig7 = px.scatter(df_filtered, x='humidity', y='count', color='season', title="Humidity vs Ride Count", labels={"hum": "Humidity", "cnt": "Ride Count"}, template="plotly_dark")
st.plotly_chart(fig7, use_container_width=True)

st.markdown("### 📦 Ride Count Distribution by Month")
fig9 = px.box(df_filtered, x='month', y='count', color='month', title="Distribution of Ride Counts by Month", template="plotly_dark")
st.plotly_chart(fig9, use_container_width=True)


model = joblib.load("bike_count_prediction_rf.joblib")


# Input widgets for features
st.markdown("### 🧑‍🔬 Predict Bike Rentals")
st.markdown("Fill in the details below to predict bike rentals.")

col1, col2, col3 = st.columns(3)

with col1:
    season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
    year = st.selectbox("Year", [2011, 2012])
    month = st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    hour = st.slider("Hour of Day", 0, 23, 12)

with col2:
    holiday = st.selectbox("Holiday", ["No", "Yes"])
    weekday = st.selectbox("Weekday", ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    workingday = st.selectbox("Working Day", ["No", "Yes"])
    weather = st.selectbox("Weather", ["Clear", "Mist", "Light Snow", "Heavy Rain"])

with col3:
    temp = st.slider("Temperature")
    atemp = st.slider("Feels-like Temperature ")
    humidity = st.slider("Humidity")
    windspeed = st.slider("Windspeed")
    rush_hour = st.selectbox("Rush Hour", ["No", "Yes"])

# Preprocess inputs
season_map = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
weekday_map = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
binary_map = {"No": 0, "Yes": 1}

input_data = {
    "season": int(season_map[season]),
    "year": int(0 if year == 2011 else 1),
    "month": int(month_map[month]),
    "hour": int(hour),
    "holiday": int(binary_map[holiday]),
    "weekday": int(weekday_map[weekday]),
    "workingday": int(binary_map[workingday]),
    "weather": weather,  
    "temp": float(temp),
    "atemp": float(atemp),
    "humidity": float(humidity),
    "windspeed": float(windspeed),
    "rush_hour": int(binary_map[rush_hour])
}

# Convert input data to DataFrame for prediction
input_df = pd.DataFrame([input_data]).astype({
    "season": "int64",
    "year": "int64",
    "month": "int64",
    "hour": "int64",
    "holiday": "int64",
    "weekday": "int64",
    "workingday": "int64",
    "weather": "object",  
    "rush_hour": "int64",
    "temp": "float64",
    "atemp": "float64",
    "humidity": "float64",
    "windspeed": "float64"
})

# Debugging: Display input DataFrame and types
st.write("Input DataFrame:")
st.write(input_df)

# Make prediction
if st.button("Predict Bike Rentals"):
    try:
        prediction = model.predict(input_df)
        st.success(f"Predicted Bike Rental Count: **{int(prediction[0])}** bikes")
        
        st.markdown("### 📈 Predicted Demand Analysis")
        fig_pred = px.bar(
            x=["Predicted Rentals"],
            y=[int(prediction[0])],
            labels={"x": "Label", "y": "Count"},
            title="Predicted Bike Rentals",
            text=[int(prediction[0])],
            template="plotly_dark"
        )
        st.plotly_chart(fig_pred, use_container_width=True)
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")


# Download filtered data
st.download_button("📥 Download Filtered Data", df_filtered.to_csv(index=False), file_name="filtered_bike_data.csv")
