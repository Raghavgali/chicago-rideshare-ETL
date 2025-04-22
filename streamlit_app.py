import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Chicago Rideshare Dashboard", layout="wide")
st.title("Chicago Rideshare Dashboard")

# Utility to map day numbers to labels
day_map = {1:'Sun', 2:'Mon', 3:'Tue', 4:'Wed', 5:'Thu', 6:'Fri', 7:'Sat'}

# Helper to load and process weekday mapping
def load_and_map_day(file_path, day_col='dayofweek'):
    df = pd.read_csv(file_path)
    df[day_col] = df[day_col].map(day_map)
    return df

# --- 1. Total Tips by Day of Week ---
df_tips = load_and_map_day("data/athena-results/Unsaved/2025/04/21/tips_by_day.csv")
fig = px.bar(
    df_tips,
    x='dayofweek', y='total_tips', color='total_tips',
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Total Tips by Day of Week',
    labels={'dayofweek': 'Day of Week', 'total_tips': 'Total Tips'}
)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# --- 2. Avg Trip Cost by Day ---
df_cost = load_and_map_day("data/athena-results/Unsaved/2025/04/21/avg_trip_cost_by_day.csv")
fig = px.line(
    df_cost,
    x='dayofweek', y='avg_trip_cost', markers=True,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='Average Trip Cost by Day of Week'
)
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

# --- 3. Trip Distance & Duration ---
df_length = load_and_map_day("data/athena-results/Unsaved/2025/04/21/trip_distance_duration_by_day.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_length['dayofweek'], y=df_length['avg_duration_min'],
                         mode='lines+markers', name='Avg Duration (min)', line=dict(color='royalblue')))
fig.add_trace(go.Scatter(x=df_length['dayofweek'], y=df_length['avg_trip_miles'],
                         mode='lines+markers', name='Avg Distance (miles)', line=dict(color='darkorange')))
fig.update_layout(title='Avg Trip Duration & Distance by Day', template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

# --- 4. Top Pickup Locations ---
df_pickup = pd.read_csv("data/athena-results/Unsaved/2025/04/21/top_10_pickup_locations.csv")
df_pickup[['lon', 'lat']] = df_pickup['pickup_centroid_location'].str.extract(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)')
df_pickup[['lon', 'lat']] = df_pickup[['lon', 'lat']].astype(float)
fig = px.scatter_mapbox(df_pickup, lat='lat', lon='lon', size='pickup_count',
                        color='pickup_count', mapbox_style='carto-positron',
                        zoom=10, title='\ud83d\udccd Top 10 Pickup Locations')
st.plotly_chart(fig, use_container_width=True)

# --- 5. Top Dropoff Locations ---
df_dropoff = pd.read_csv("data/athena-results/Unsaved/2025/04/21/top_10_dropoff_locations.csv")
df_dropoff[['lon', 'lat']] = df_dropoff['dropoff_centroid_location'].str.extract(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)')
df_dropoff[['lon', 'lat']] = df_dropoff[['lon', 'lat']].astype(float)
fig = px.scatter_mapbox(df_dropoff, lat='lat', lon='lon', size='dropoff_count',
                        color='dropoff_count', mapbox_style='open-street-map',
                        zoom=10, title='\ud83d\udccd Top 10 Dropoff Locations')
st.plotly_chart(fig, use_container_width=True)

# --- 6. Trips Pooled ---
df_pooled = pd.read_csv("data/athena-results/Unsaved/2025/04/21/trips_pooled_by_day.csv")
fig = px.line(df_pooled, x='dayofweek', y='total_trips_pooled', markers=True,
              title="Total Pooled Trips Per Day",
              color_discrete_sequence=['mediumvioletred'])
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

# --- 7. Fare Breakdown ---
df_fare = pd.read_csv("data/athena-results/Unsaved/2025/04/21/fare_breakdown.csv")
fare_parts = df_fare.iloc[0].to_dict()
fig = px.pie(names=list(fare_parts.keys()), values=list(fare_parts.values()),
             title="Average Fare Breakdown",
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textinfo='percent+label')
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, use_container_width=True)
