import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.interpolate import interp1d
import plotly.express as px

# Function to parse axis data
def parse_axis(text, dtype=float):
    try:
        return [dtype(item) for item in text.strip().replace(',', ' ').split()]
    except ValueError:
        return None

# Function to parse map data
def parse_map(text, dtype=float):
    try:
        data = [line.strip().replace(',', ' ').split() for line in text.strip().split('\n')]
        return pd.DataFrame([[dtype(cell) for cell in row] for row in data])
    except ValueError:
        return None

# Function to extend air mass map with new points
def extend_air_mass_map(torque_axis, map_df, new_points):
    # Combine the original axis with new points
    extended_axis = sorted(torque_axis + new_points)

    # Create a new DataFrame for the extended map
    extended_map = pd.DataFrame(index=extended_axis, columns=map_df.columns)

    # Copy original data to the new map
    for col in map_df.columns:
        extended_map.loc[torque_axis, col] = map_df[col]

        # Perform linear regression using the last 4 rows
        last_rows = map_df[col].iloc[-4:]
        last_indices = torque_axis[-4:]
        slope, intercept, _, _, _ = linregress(last_indices, last_rows)

        # Forecast values for new points
        for point in new_points:
            extended_map.loc[point, col] = slope * point + intercept

    return extended_axis, extended_map

# Function to suggest new torque axis points based on air mass averages
def suggest_torque_axis(air_mass_map, new_air_mass_points):
    suggested_torque_points = []
    for point in new_air_mass_points:
        row_values = air_mass_map.loc[point]
        suggested_torque_points.append(row_values.mean())
    return suggested_torque_points

# Function to extend torque map based on forecast
def forecast_torque_map(torque_axis, map_df, new_points):
    # Combine the original axis with new points
    extended_axis = sorted(torque_axis + new_points)

    # Create a new DataFrame for the extended map
    extended_map = pd.DataFrame(index=extended_axis, columns=map_df.columns)

    # Copy original data to the new map
    for col in map_df.columns:
        extended_map.loc[torque_axis, col] = map_df[col]

        # Perform linear regression using the last 4 rows
        last_rows = map_df[col].iloc[-4:]
        last_indices = torque_axis[-4:]
        slope, intercept, _, _, _ = linregress(last_indices, last_rows)

        # Forecast values for new points
        for point in new_points:
            extended_map.loc[point, col] = slope * point + intercept

    return extended_axis, extended_map

# Streamlit App
st.title("Air Mass and Torque Map Extension")

# Sidebar for input data
st.sidebar.header("Input Data")
rpm_input = st.sidebar.text_area(
    "RPM Axis (separated by spaces):",
    value="650 800 992 1248 1500 1750 2016 2496 3008 3488 4000 4512 4992 5504 6016 6592"
)
torque_axis_input = st.sidebar.text_area(
    "Torque Axis (separated by spaces):",
    value="0 25 50 100 150 200 250 300 350 400 450 500"
)
air_mass_map_input = st.sidebar.text_area(
    "Air Mass Map Data (rows separated by newlines, columns by spaces):",
    value="""0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
112.799 110.298 108.517 105.084 103.982 103.007 102.583 100.082 96.182 97.793 102.116 49.299 45.696 48.197 100.718 103.897
180.495 177.485 174.518 170.406 169.516 168.71 169.007 168.287 162.988 165.489 167.82 158.791 155.782 160.996 166.294 168.117
319.193 315.802 309.613 305.798 304.908 303.891 303.001 304.484 298.889 299.694 298.804 292.191 292.7 296.896 297.108 297.999
513.38 453.907 445.006 438.817 437.121 436.316 437.121 439.792 434.917 433.179 433.688 444.115 448.1 447.295 445.981 449.88
663.397 598.795 575.396 569.08 562.679 561.407 570.818 574.294 572.301 568.614 569.08 584.086 588.791 585.315 586.502 592.479"""
)
torque_map_input = st.sidebar.text_area(
    "Torque Map Data (rows separated by newlines, columns by spaces):",
    value="""2.844 3.438 3.688 2.906 2.344 1.281 1.281 1.281 1.281 1.281 1.281 25.344 27.375 25.938 23.219 22.031
20.281 21.188 21.781 23.062 23.469 23.844 24.031 24.969 26.969 26.094 24.188 27.875 29.375 27.562 24.719 23.469
57.188 58.344 59.656 61.344 61.656 61.906 61.656 61.594 63.5 62.562 62.281 65.5 66.312 64.344 62.875 62.406"""
)

# Parse the inputs
rpm_axis = parse_axis(rpm_input)
torque_axis = parse_axis(torque_axis_input)
air_mass_map = parse_map(air_mass_map_input)
torque_map = parse_map(torque_map_input)

if rpm_axis and torque_axis and air_mass_map is not None and torque_map is not None:
    air_mass_map.columns = rpm_axis
    air_mass_map.index = torque_axis
    torque_map.columns = rpm_axis
    torque_map.index = torque_axis

    st.sidebar.success("Parsed data successfully!")

    # Input for new axis points for air mass map
    new_air_mass_points = st.sidebar.text_area(
        "New Air Mass Points (separated by spaces):",
        value="550 600 650"
    )
    new_air_mass_points = parse_axis(new_air_mass_points)

    if new_air_mass_points:
        # Extend air mass map
        extended_air_mass_axis, extended_air_mass_map = extend_air_mass_map(torque_axis, air_mass_map, new_air_mass_points)

        # Suggest new torque axis points
        suggested_torque_axis = suggest_torque_axis(extended_air_mass_map, new_air_mass_points)

        # Extend torque map based on suggested points
        extended_torque_axis, extended_torque_map = forecast_torque_map(torque_axis, torque_map, suggested_torque_axis)

        # Display results
        st.subheader("Extended Air Mass Map")
        st.dataframe(extended_air_mass_map)

        st.subheader("Extended Torque Map")
        st.dataframe(extended_torque_map)

        # Visualization
        st.subheader("Visualization: Extended Air Mass Map")
        fig1 = px.imshow(
            extended_air_mass_map,
            labels={'x': "RPM", 'y': "Torque"},
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig1)

        st.subheader("Visualization: Extended Torque Map")
        fig2 = px.imshow(
            extended_torque_map,
            labels={'x': "RPM", 'y': "Torque"},
            color_continuous_scale="Inferno"
        )
        st.plotly_chart(fig2)

        # Download the extended maps
        st.download_button(
            label="Download Extended Air Mass Map as CSV",
            data=extended_air_mass_map.to_csv(index=True).encode('utf-8'),
            file_name='extended_air_mass_map.csv',
            mime='text/csv',
        )

        st.download_button(
            label="Download Extended Torque Map as CSV",
            data=extended_torque_map.to_csv(index=True).encode('utf-8'),
            file_name='extended_torque_map.csv',
            mime='text/csv',
        )
    else:
        st.error("Please provide valid new air mass points.")
else:
    st.error("Please provide valid input data.")
