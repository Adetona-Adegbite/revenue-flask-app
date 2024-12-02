import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL") 
supabase: Client = create_client(url, key)

@st.cache_data
def load_data():
    response = supabase.table('traffic_predictions').select('*').execute()  
    data = pd.DataFrame(response.data)
    return data

data = load_data()

st.title("Network Traffic Dashboard")
st.write("Visualize and analyze the data sent to the anomaly detection model.")

st.subheader("Raw Data")
st.write(data)

st.subheader("Feature Distribution")
feature = st.selectbox("Select Feature", data.columns)
fig = px.histogram(
    data,
    x=feature,
    color="prediction",
    color_discrete_map={0: "blue", 1: "red"}, 
    title=f"Distribution of {feature} by Class"
)
st.plotly_chart(fig)

st.subheader("Anomalies Overview")
anomaly_count = data[data["prediction"] == 1].shape[0]
normal_count = data[data["prediction"] == 0].shape[0]
st.write(f"Anomalies: {anomaly_count}, Normal: {normal_count}")

st.subheader("Anomaly vs Normal Distribution")
pie_data = pd.DataFrame({
    "Type": ["Normal", "Anomalies"],
    "Count": [normal_count, anomaly_count]
})
pie_fig = px.pie(
    pie_data,
    values="Count",
    names="Type",
    title="Traffic Distribution",
    color="Type",
    color_discrete_map={"Normal": "blue", "Anomalies": "red"}  
)
st.plotly_chart(pie_fig)

if "timestamp" in data.columns:
    st.subheader("Feature Trends Over Time")
    time_feature = st.selectbox("Select Feature for Time Analysis", data.columns)
    time_fig = px.line(
        data,
        x="timestamp",
        y=time_feature,
        color="prediction",
        color_discrete_map={0: "blue", 1: "red"}, 
        title=f"{time_feature} Over Time"
    )
    st.plotly_chart(time_fig)

numeric_data = data.select_dtypes(include=['number'])

if not numeric_data.empty:
    st.subheader("Correlation Heatmap")
    correlation_matrix = numeric_data.corr()
    heatmap_fig = px.imshow(
        correlation_matrix,
        title="Feature Correlations",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(heatmap_fig)

st.subheader("Scatter Plot Matrix")
scatter_features = st.multiselect(
    "Select Features for Scatter Plot Matrix",
    options=data.columns,
    default=data.columns[:4]
)
if len(scatter_features) > 1:
    scatter_fig = px.scatter_matrix(
        data,
        dimensions=scatter_features,
        color="prediction",
        color_discrete_map={0: "blue", 1: "red"},
        title="Scatter Plot Matrix by Class"
    )
    st.plotly_chart(scatter_fig)

st.subheader("Feature Comparison: Box Plots")
box_feature = st.selectbox("Select Feature for Box Plot", data.columns)
box_fig = px.box(
    data,
    x="prediction",
    y=box_feature,
    color="prediction",
    color_discrete_map={0: "blue", 1: "red"},
    labels={"class": "Traffic Type"},
    title=f"Box Plot of {box_feature} by Traffic Type"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(box_fig)

with col2:
    st.subheader("Anomaly-Specific Feature Analysis")
    anomaly_features = data[data["prediction"] == 1]
    if not anomaly_features.empty:
        anomaly_feature = st.selectbox("Select Feature for Anomaly Analysis", anomaly_features.columns)
        anomaly_fig = px.histogram(
            anomaly_features,
            x=anomaly_feature,
            title=f"Distribution of {anomaly_feature} (Anomalies)",
            color_discrete_sequence=["red"]
        )
        st.plotly_chart(anomaly_fig)
    else:
        st.write("No anomalies detected in the dataset.")
