import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(page_title="ECU Map Scaling App", layout="wide")

# Title
st.title("ECU Map Scaling Application")

# Function to parse axis data
def parse_axis(text, dtype=float):
    try:
        # Split by any whitespace and convert to float
        axis = [dtype(item) for item in text.strip().replace(',', ' ').split()]
        return axis
    except ValueError:
        return None

# Function to parse map data
def parse_map(text, dtype=float):
    try:
        # Split by lines, then split each line by whitespace or tabs
        data = [line.strip().replace(',', ' ').split() for line in text.strip().split('\n')]
        # Convert to float
        data = [[dtype(item) for item in row] for row in data]
        # Convert to DataFrame
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
    value="650\t800\t992\t1248\t1500\t1750\t2016\t2496\t3008\t3488\t4000\t4512\t4992\t5504\t6016\t6592"
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
    value="0\n25\n50\n100\n150\n200\n250\n300\n350\n400\n450\n500"
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
    value="""0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0
112.799\t110.298\t108.517\t105.084\t103.982\t103.007\t102.583\t100.082\t96.182\t97.793\t102.116\t49.299\t45.696\t48.197\t100.718\t103.897
180.495\t177.485\t174.518\t170.406\t169.516\t168.71\t169.007\t168.287\t162.988\t165.489\t167.82\t158.791\t155.782\t160.996\t166.294\t168.117
319.193\t315.802\t309.613\t305.798\t304.908\t303.891\t303.001\t304.484\t298.889\t299.694\t298.804\t292.191\t292.7\t296.896\t297.108\t297.999
513.38\t453.907\t445.006\t438.817\t437.121\t436.316\t437.121\t439.792\t434.917\t433.179\t433.688\t444.115\t448.1\t447.295\t445.981\t449.88
663.397\t598.795\t575.396\t569.08\t562.679\t561.407\t570.818\t574.294\t572.301\t568.614\t569.08\t584.086\t588.791\t585.315\t586.502\t592.479
815.787\t804.3\t804.003\t736.18\t709.305\t700.488\t707.016\t709.093\t711.297\t704.811\t707.016\t719.52\t723.505\t722.488\t731.22\t741.521
976.316\t970.382\t966.312\t938.886\t925.195\t890.393\t856.82\t847.283\t853.811\t853.217\t855.888\t878.1\t881.618\t882.805\t896.115\t896.921
1123.111\t1105.52\t1102.001\t1040.197\t1054.779\t1057.111\t1001.793\t997.596\t1002.216\t1004.082\t1003.488\t1030.617\t1049.311\t1054.313\t1065.292\t1092.803
1334.211\t1301.02\t1279.91\t1190.808\t1211.621\t1214.588\t1156.514\t1162.915\t1163\t1164.017\t1157.489\t1198.904\t1233.494\t1266.303\t1304.581\t1323.317
1515.893\t1481.303\t1452.394\t1409.114\t1382.917\t1369.48\t1343.495\t1346.801\t1343.198\t1343.495\t1330.82\t1381.9\t1420.389\t1466.679\t1505.296\t1512.502
1684.307\t1645.817\t1613.813\t1565.701\t1538.487\t1522.294\t1504.999\t1507.119\t1503.007\t1503.092\t1489.484\t1538.699\t1578.206\t1629.709\t1672.48\t1680.492"""
)
airmass_map = parse_map(airmass_map_input)
if airmass_map is not None:
    st.sidebar.write("**Parsed Air Mass Map:**")
    st.sidebar.dataframe(airmass_map)
    confirm_airmass_map = st.sidebar.checkbox("Confirm Air Mass Map Data", value=False)
else:
    st.sidebar.error("Invalid Air Mass map data. Please check the format.")

# Step 4: Torque Air Mass Axis
st.sidebar.subheader("4. Torque Axis for Torque Map")
torque_map_axis_input = st.sidebar.text_area(
    "Paste Torque axis values for Torque Map (one per line):",
    value="50.02\n99.997\n199.994\n299.991\n399.013\n499.01\n599.007\n702.014\n800.018\n898.998\n1100.009\n1400"
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
    value="""2.844\t3.438\t3.688\t2.906\t2.344\t1.281\t1.281\t1.281\t1.281\t1.281\t1.281\t25.344\t27.375\t25.938\t23.219\t22.031
20.281\t21.188\t21.781\t23.062\t23.469\t23.844\t24.031\t24.969\t26.969\t26.094\t24.188\t27.875\t29.375\t27.562\t24.719\t23.469
57.188\t58.344\t59.656\t61.344\t61.656\t
