import streamlit as st
import pandas as pd
import numpy as np

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
torque_airmass_axis = parse_axis(torque_airmass_input)
if not torque_airmass_axis:
    st.sidebar.error("Invalid Torque Air Mass axis data. Please check the format.")
    st.stop()

# Air Mass Map Data
st.sidebar.subheader("3. Air Mass Map Data")
airmass_map_input = st.sidebar.text_area(
    "Paste Air Mass map data (rows separated by newlines, columns by spaces or tabs):",
    value="""0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
112.799 110.298 108.517 105.084 103.982 103.007 102.583 100.082 96.182 97.793 102.116 49.299 45.696 48.197 100.718 103.897
180.495 177.485 174.518 170.406 169.516 168.71 169.007 168.287 162.988 165.489 167.82 158.791 155.782 160.996 166.294 168.117
319.193 315.802 309.613 305.798 304.908 303.891 303.001 304.484 298.889 299.694 298.804 292.191 292.7 296.896 297.108 297.999
513.38 453.907 445.006 438.817 437.121 436.316 437.121 439.792 434.917 433.179 433.688 444.115 448.1 447.295 445.981 449.88
663.397 598.795 575.396 569.08 562.679 561.407 570.818 574.294 572.301 568.614 569.08 584.086 588.791 585.315 586.502 592.479
815.787 804.3 804.003 736.18 709.305 700.488 707.016 709.093 711.297 704.811 707.016 719.52 723.505 722.488 731.22 741.521
976.316 970.382 966.312 938.886 925.195 890.393 856.82 847.283 853.811 853.217 855.888 878.1 881.618 882.805 896.115 896.921
1123.111 1105.52 1102.001 1040.197 1054.779 1057.111 1001.793 997.596 1002.216 1004.082 1003.488 1030.617 1049.311 1054.313 1065.292 1092.803
1334.211 1301.02 1279.91 1190.808 1211.621 1214.588 1156.514 1162.915 1163 1164.017 1157.489 1198.904 1233.494 1266.303 1304.581 1323.317
1515.893 1481.303 1452.394 1409.114 1382.917 1369.48 1343.495 1346.801 1343.198 1343.495 1330.82 1381.9 1420.389 1466.679 1505.296 1512.502
1684.307 1645.817 1613.813 1565.701 1538.487 1522.294 1504.999 1507.119 1503.007 1503.092 1489.484 1538.699 1578.206 1629.709 1672.48 1680.492"""
)
airmass_map = parse_map(airmass_map_input)
if airmass_map is None:
    st.sidebar.error("Invalid Air Mass map data. Please check the format.")
    st.stop()

# Airflow Axis for Torque Map
st.sidebar.subheader("4. Airflow Axis for Torque Map")
torque_map_input = st.sidebar.text_area(
    "Paste Torque axis values for Torque Map (one per line):",
    value="50.02\n99.997\n199.994\n299.991\n399.013\n499.01\n599.007\n702.014\n800.018\n898.998\n1100.009\n1400"
)
torque_map_axis = parse_axis(torque_map_input)
if not torque_map_axis:
    st.sidebar.error("Invalid Airflow axis data. Please check the format.")
    st.stop()

# Torque Map Data
st.sidebar.subheader("5. Torque Map Data")
torque_map_input = st.sidebar.text_area(
    "Paste Torque map data (rows separated by newlines, columns by spaces or tabs):",
    value="""2.844 3.438 3.688 2.906 2.344 1.281 1.281 1.281 1.281 1.281 1.281 25.344 27.375 25.938 23.219 22.031
20.281 21.188 21.781 23.062 23.469 23.844 24.031 24.969 26.969 26.094 24.188 27.875 29.375 27.562 24.719 23.469
57.188 58.344 59.656 61.344 61.656 61.906 61.656 61.594 63.5 62.562 62.281 65.5 66.312 64.344 62.875 62.406
93.094 94.312 96.469 97.844 98.188 98.531 98.875 98.344 100.406 100.125 100.469 102.906 102.656 101.156 101.094 100.781
128.719 130 132.719 134.531 135.062 135.438 135.75 134.844 136.906 137.375 137.219 135.312 134.312 133.906 134.438 133.531
145.375 166.406 170.281 173.438 174.25 174.531 173.188 171.969 173.406 174.281 174.094 167.875 166.281 167.219 167.562 165.875
177.625 200.062 209.188 211.344 214.688 215.344 210.531 209.219 209.688 211.25 211.031 205.625 203.812 205.219 204.625 202.375
213.438 226.906 230.719 242.719 248.438 250.531 248.312 247.406 246.719 249.031 248.281 244.375 242.969 243.5 241.188 238.25
245.781 248.938 248.938 263.594 269.438 278.219 281.812 283.25 281.406 282.938 282.094 275.938 275.031 274.594 270.75 267.438
267.188 273.25 275.125 280.281 289.875 302.062 313.5 318.344 315.656 314.719 313.812 306.438 305.312 304.969 300.875 300.719
339.531 348.594 349.438 379.562 367.438 363 384.875 382.906 382.531 382.188 383.406 373 365.094 363.25 360.25 351.844
410.594 425.312 433.75 447.094 455 459.844 465.125 464.469 465.75 465.719 469.969 454.938 443.531 429.531 418.531 416.531"""
)
torque_map = parse_map(torque_map_input)
if torque_map is None:
    st.sidebar.error("Invalid Torque map data. Please check the format.")
    st.stop()

# New Maximum Torque Input
st.sidebar.subheader("6. New Maximum Torque Axis Value")
new_max_torque = st.sidebar.number_input(
    "Enter the new maximum torque value (e.g., 650):",
    min_value=0.0,
    max_value=20000.0,
    value=650.0,
    step=1.0
)

# Scale New Torque Axis Points
new_torque_points = [new_max_torque * (550 / 650), new_max_torque * (600 / 650), new_max_torque]

# Extend Air Mass Map
st.header("Extend Air Mass Map")
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
new_torque_map_axis = list(torque_map.index) + list(new_torque_axis_points)
new_torque_map_axis.sort()

# Extend Torque Map
st.header("Extend Torque Map")
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
st.markdown("© 2025 SXTH Element Engineering")
