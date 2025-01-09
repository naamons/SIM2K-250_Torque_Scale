import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="ECU Map Scaling App", layout="wide")

# Title
st.title("ECU Map Scaling Application")

# Function to parse axis data
def parse_axis(text, dtype=float):
    try:
        axis = [dtype(item) for item in text.strip().replace(',', ' ').split()]
        return axis
    except ValueError:
        return None

# Function to parse map data
def parse_map(text, dtype=float):
    try:
        data = [line.strip().replace(',', ' ').split() for line in text.strip().split('\n')]
        data = [[dtype(item) for item in row] for row in data]
        df = pd.DataFrame(data)
        return df
    except ValueError:
        return None

# Sidebar for user inputs
st.sidebar.header("Input Data")

# Step 1: RPM Axis
st.sidebar.subheader("1. RPM Axis")
rpm_input = st.sidebar.text_area(
    "Paste RPM axis values (separated by spaces or tabs):",
    value="""650 800 992 1248 1500 1750 2016 2496 3008 3488 4000 4512 4992 5504 6016 6592"""
)
rpm_axis = parse_axis(rpm_input)
if rpm_axis:
    st.sidebar.write("**Parsed RPM Axis:**")
    st.sidebar.write(rpm_axis)
    confirm_rpm = st.sidebar.checkbox("Confirm RPM Axis", value=False)
else:
    st.sidebar.error("Invalid RPM axis data. Please check the format.")

# Step 2: Torque Axis for Air Mass Map
st.sidebar.subheader("2. Torque Axis for Air Mass Map")
torque_airmass_axis_input = st.sidebar.text_area(
    "Paste Torque Air Mass axis values (one per line):",
    value="""0
25
50
100
150
200
250
300
350
400
450
500"""
)
torque_airmass_axis = parse_axis(torque_airmass_axis_input, dtype=float)
if torque_airmass_axis:
    st.sidebar.write("**Parsed Torque Air Mass Axis:**")
    st.sidebar.write(torque_airmass_axis)
    confirm_torque_airmass = st.sidebar.checkbox("Confirm Torque Air Mass Axis", value=False)
else:
    st.sidebar.error("Invalid Torque Air Mass axis data. Please check the format.")

# Step 3: Air Mass Map Data
st.sidebar.subheader("3. Air Mass Map Data")
airmass_map_input = st.sidebar.text_area(
    "Paste Air Mass map data (rows separated by newlines, columns by spaces or tabs):",
    value="""..."""  # Add your default Air Mass Map data here
)
airmass_map = parse_map(airmass_map_input)
if airmass_map is not None:
    st.sidebar.write("**Parsed Air Mass Map:**")
    st.sidebar.dataframe(airmass_map)
    confirm_airmass_map = st.sidebar.checkbox("Confirm Air Mass Map Data", value=False)
else:
    st.sidebar.error("Invalid Air Mass map data. Please check the format.")

# Step 4: Torque Axis for Torque Map
st.sidebar.subheader("4. Torque Axis for Torque Map")
torque_map_axis_input = st.sidebar.text_area(
    "Paste Torque axis values for Torque Map (one per line):",
    value="""50.02
99.997
199.994
299.991
399.013
499.01
599.007
702.014
800.018
898.998
1100.009
1400"""
)
torque_map_axis = parse_axis(torque_map_axis_input, dtype=float)
if torque_map_axis:
    st.sidebar.write("**Parsed Torque Map Axis:**")
    st.sidebar.write(torque_map_axis)
    confirm_torque_map_axis = st.sidebar.checkbox("Confirm Torque Map Axis", value=False)
else:
    st.sidebar.error("Invalid Torque Map axis data. Please check the format.")

# Step 5: Torque Map Data
st.sidebar.subheader("5. Torque Map Data")
torque_map_input = st.sidebar.text_area(
    "Paste Torque map data (rows separated by newlines, columns by spaces or tabs):",
    value="""..."""  # Add your default Torque Map data here
)
torque_map = parse_map(torque_map_input)
if torque_map is not None:
    st.sidebar.write("**Parsed Torque Map:**")
    st.sidebar.dataframe(torque_map)
    confirm_torque_map = st.sidebar.checkbox("Confirm Torque Map Data", value=False)
else:
    st.sidebar.error("Invalid Torque map data. Please check the format.")

# Check if all data is confirmed
data_confirmed = (
    'confirm_rpm' in locals() and confirm_rpm and
    'confirm_torque_airmass' in locals() and confirm_torque_airmass and
    'confirm_airmass_map' in locals() and confirm_airmass_map and
    'confirm_torque_map_axis' in locals() and confirm_torque_map_axis and
    'confirm_torque_map' in locals() and confirm_torque_map
)

if not data_confirmed:
    st.warning("Please confirm all data inputs in the sidebar to proceed.")
    st.stop()

# Convert parsed data into DataFrames with proper indices and columns
airmass_df = airmass_map.copy()
airmass_df.columns = rpm_axis
airmass_df.index = torque_airmass_axis

torque_df = torque_map.copy()
torque_df.columns = rpm_axis
torque_df.index = torque_map_axis

# Display the maps as tables
st.header("ECU Maps as Tables")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Air Mass Map")
    st.dataframe(airmass_df)

with col2:
    st.subheader("Torque Map")
    st.dataframe(torque_df)

# Main Functionality: Scaling the Maps
st.header("Scale Torque Axis")

st.markdown("""
Enter the new maximum torque value you want to scale the torque axis to. The app will adjust the torque and airflow maps accordingly by scaling the last three data points and interpolating the rest.
""")

new_max_torque = st.number_input(
    "Enter the new maximum torque (e.g., 650):",
    min_value=0.0,
    max_value=20000.0,
    value=650.0,
    step=1.0
)

x1, x2, x3 = torque_map_axis[-3:]
y1_prime = new_max_torque - 2 * (x3 - x1)
y2_prime = new_max_torque - (x3 - x2)
a = (new_max_torque - y1_prime) / (x3 - x1)
b = y1_prime - a * x1

def scale_torque(x):
    return a * x + b if x >= x1 else x

new_torque_axis = [scale_torque(x) for x in torque_map_axis]
new_torque_airmass_axis = [scale_torque(x) for x in torque_airmass_axis]

# Interpolation
interpolated_values = {}
for rpm in rpm_axis:
    original_x = airmass_df.index.values
    original_y = airmass_df[rpm].values
    new_x = new_torque_airmass_axis
    interpolator = interp1d(original_x, original_y, kind='linear', fill_value="extrapolate")
    interpolated_values[rpm] = interpolator(new_x)

new_airmass_df_interpolated = pd.DataFrame(interpolated_values, index=new_torque_airmass_axis)

new_torque_df = pd.DataFrame(columns=rpm_axis, index=new_torque_axis)
for rpm in rpm_axis:
    cubic_spline = CubicSpline(torque_df.index, torque_df[rpm])
    new_y = cubic_spline(new_torque_axis)
    new_torque_df[rpm] = new_y

# Visualize heatmaps
st.header("Scaled ECU Maps as Tables")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Scaled Air Mass Map")
    fig_airmass = px.imshow(
        new_airmass_df_interpolated,
        labels={'x': "RPM", 'y': "Torque Air Mass Axis"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_airmass)

with col4:
    st.subheader("Scaled Torque Map")
    fig_torque = px.imshow(
        new_torque_df,
        labels={'x': "RPM", 'y': "Torque Axis"},
        color_continuous_scale="Inferno"
    )
    st.plotly_chart(fig_torque)

# Download options
st.header("Download Scaled Maps")
def convert_df(df):
    return df.to_csv(index=True).encode('utf-8')

csv_airmass = convert_df(new_airmass_df_interpolated)
csv_torque = convert_df(new_torque_df)

st.download_button(
    label="Download Scaled Air Mass Map as CSV",
    data=csv_airmass,
    file_name='scaled_airmass_map.csv',
    mime='text/csv',
)

st.download_button(
    label="Download Scaled Torque Map as CSV",
    data=csv_torque,
    file_name='scaled_torque_map.csv',
    mime='text/csv',
)

st.markdown("---")
st.markdown("© 2025 ECU Map Scaling App")
