import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="ECU Map Scaling App", layout="wide")

# Title
st.title("ECU Map Scaling Application")

# Helper functions
def parse_axis(text, dtype=float):
    try:
        axis = [dtype(item) for item in text.strip().replace(',', ' ').split()]
        return axis
    except ValueError:
        return None

def parse_map(text, dtype=float):
    try:
        data = [line.strip().replace(',', ' ').split() for line in text.strip().split('\n')]
        data = [[dtype(item) for item in row] for row in data]
        df = pd.DataFrame(data)
        return df
    except ValueError:
        return None

def forecast_linear(x, y, new_x):
    """Forecast new y values using linear interpolation."""
    x = np.array(x)
    y = np.array(y)
    coefficients = np.polyfit(x, y, 1)  # Linear fit
    return coefficients[0] * new_x + coefficients[1]

# Sidebar for user inputs
st.sidebar.header("Input Data")

# RPM Axis
st.sidebar.subheader("1. RPM Axis")
rpm_input = st.sidebar.text_area(
    "Paste RPM axis values (separated by spaces or tabs):",
    value="650 800 992 1248 1500 1750 2016 2496 3008 3488 4000 4512 4992 5504 6016 6592"
)
rpm_axis = parse_axis(rpm_input)
if not rpm_axis:
    st.sidebar.error("Invalid RPM axis data. Please check the format.")
    st.stop()

# Torque Axis for Air Mass Map
st.sidebar.subheader("2. Torque Axis for Air Mass Map")
torque_airmass_input = st.sidebar.text_area(
    "Paste Torque Air Mass axis values (one per line):",
    value="0\n25\n50\n100\n150\n200\n250\n300\n350\n400\n450\n500"
)
torque_airmass_axis = parse_axis(torque_airmass_input, dtype=float)
if not torque_airmass_axis:
    st.sidebar.error("Invalid Torque Air Mass axis data. Please check the format.")
    st.stop()

# Air Mass Map Data
st.sidebar.subheader("3. Air Mass Map Data")
airmass_map_input = st.sidebar.text_area(
    "Paste Air Mass map data (rows separated by newlines, columns by spaces or tabs):",
    value="..."  # Add default Air Mass Map data here
)
airmass_map = parse_map(airmass_map_input)
if airmass_map is None:
    st.sidebar.error("Invalid Air Mass map data. Please check the format.")
    st.stop()

# Torque Axis for Torque Map
st.sidebar.subheader("4. Torque Axis for Torque Map")
torque_map_input = st.sidebar.text_area(
    "Paste Torque axis values for Torque Map (one per line):",
    value="50.02\n99.997\n199.994\n299.991\n399.013\n499.01\n599.007\n702.014\n800.018\n898.998\n1100.009\n1400"
)
torque_map_axis = parse_axis(torque_map_input, dtype=float)
if not torque_map_axis:
    st.sidebar.error("Invalid Torque Map axis data. Please check the format.")
    st.stop()

# Torque Map Data
st.sidebar.subheader("5. Torque Map Data")
torque_map_input = st.sidebar.text_area(
    "Paste Torque map data (rows separated by newlines, columns by spaces or tabs):",
    value="..."  # Add default Torque Map data here
)
torque_map = parse_map(torque_map_input)
if torque_map is None:
    st.sidebar.error("Invalid Torque map data. Please check the format.")
    st.stop()

# Extend Air Mass Map
st.header("Extend Air Mass Map")
new_torque_points = [550, 600, 650]
airmass_map.columns = rpm_axis
airmass_map.index = torque_airmass_axis

extended_airmass_map = airmass_map.copy()
for new_point in new_torque_points:
    new_values = []
    for rpm in rpm_axis:
        x_values = airmass_map.index[-4:]
        y_values = airmass_map[rpm].iloc[-4:]
        new_value = forecast_linear(x_values, y_values, new_point)
        new_values.append(new_value)
    extended_airmass_map.loc[new_point] = new_values

extended_airmass_map.sort_index(inplace=True)

st.subheader("Extended Air Mass Map")
st.dataframe(extended_airmass_map)

# Suggest New Torque Map Axis
new_torque_axis_points = extended_airmass_map.loc[new_torque_points].mean(axis=1).values
new_torque_map_axis = list(torque_map_axis) + list(new_torque_axis_points)
new_torque_map_axis.sort()

# Extend Torque Map
st.header("Extend Torque Map")
torque_map.columns = rpm_axis
torque_map.index = torque_map_axis

extended_torque_map = torque_map.copy()
for new_point in new_torque_axis_points:
    new_values = []
    for rpm in rpm_axis:
        x_values = torque_map.index[-4:]
        y_values = torque_map[rpm].iloc[-4:]
        new_value = forecast_linear(x_values, y_values, new_point)
        new_values.append(new_value)
    extended_torque_map.loc[new_point] = new_values

extended_torque_map.sort_index(inplace=True)

st.subheader("Extended Torque Map")
st.dataframe(extended_torque_map)

# Visualization
st.header("Visualize Scaled Maps")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Air Mass Map Heatmap")
    fig_airmass = px.imshow(
        extended_airmass_map,
        labels={"x": "RPM", "y": "Torque Air Mass Axis"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_airmass)

with col2:
    st.subheader("Torque Map Heatmap")
    fig_torque = px.imshow(
        extended_torque_map,
        labels={"x": "RPM", "y": "Torque Axis"},
        color_continuous_scale="Inferno"
    )
    st.plotly_chart(fig_torque)

# Download Options
st.header("Download Scaled Maps")
def convert_df_to_csv(df):
    return df.to_csv(index=True).encode("utf-8")

st.download_button(
    label="Download Scaled Air Mass Map",
    data=convert_df_to_csv(extended_airmass_map),
    file_name="scaled_airmass_map.csv",
    mime="text/csv",
)

st.download_button(
    label="Download Scaled Torque Map",
    data=convert_df_to_csv(extended_torque_map),
    file_name="scaled_torque_map.csv",
    mime="text/csv",
)

st.markdown("---")
st.markdown("© 2025 ECU Map Scaling App")
