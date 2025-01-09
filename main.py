import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
    st.sidebar.write("Parsed RPM Axis:")
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
    st.sidebar.write("Parsed Torque Air Mass Axis:")
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
    st.sidebar.write("Parsed Air Mass Map:")
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
    st.sidebar.write("Parsed Torque Map Axis:")
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
57.188\t58.344\t59.656\t61.344\t61.656\t61.906\t61.656\t61.594\t63.5\t62.562\t62.281\t65.5\t66.312\t64.344\t62.875\t62.406
93.094\t94.312\t96.469\t97.844\t98.188\t98.531\t98.875\t98.344\t100.406\t100.125\t100.469\t102.906\t102.656\t101.156\t101.094\t100.781
128.719\t130\t132.719\t134.531\t135.062\t135.438\t135.75\t134.844\t136.906\t137.375\t137.219\t135.312\t134.312\t133.906\t134.438\t133.531
145.375\t166.406\t170.281\t173.438\t174.25\t174.531\t173.188\t171.969\t173.406\t174.281\t174.094\t167.875\t166.281\t167.219\t167.562\t165.875
177.625\t200.062\t209.188\t211.344\t214.688\t215.344\t210.531\t209.219\t209.688\t211.25\t211.031\t205.625\t203.812\t205.219\t204.625\t202.375
213.438\t226.906\t230.719\t242.719\t248.438\t250.531\t248.312\t247.406\t246.719\t249.031\t248.281\t244.375\t242.969\t243.5\t241.188\t238.25
245.781\t248.938\t248.938\t263.594\t269.438\t278.219\t281.812\t283.25\t281.406\t282.938\t282.094\t275.938\t275.031\t274.594\t270.75\t267.438
267.188\t273.25\t275.125\t280.281\t289.875\t302.062\t313.5\t318.344\t315.656\t314.719\t313.812\t306.438\t305.312\t304.969\t300.875\t300.719
339.531\t348.594\t349.438\t379.562\t367.438\t363\t384.875\t382.906\t382.531\t382.188\t383.406\t373\t365.094\t363.25\t360.25\t351.844
410.594\t425.312\t433.75\t447.094\t455\t459.844\t465.125\t464.469\t465.75\t465.719\t469.969\t454.938\t443.531\t429.531\t418.531\t416.531"""
)
torque_map = parse_map(torque_map_input)
if torque_map is not None:
    st.sidebar.write("Parsed Torque Map:")
    st.sidebar.dataframe(torque_map)
    confirm_torque_map = st.sidebar.checkbox("Confirm Torque Map Data", value=False)
else:
    st.sidebar.error("Invalid Torque map data. Please check the format.")

# Check if all data is confirmed
data_confirmed = (
    confirm_rpm and
    confirm_torque_airmass and
    confirm_airmass_map and
    confirm_torque_map_axis and
    confirm_torque_map
)

if not data_confirmed:
    st.warning("Please confirm all data inputs in the sidebar to proceed.")
    st.stop()

# Convert parsed data into DataFrames with proper indices and columns
# Air Mass Map: Rows - Torque Air Mass Axis, Columns - RPM Axis
airmass_df = airmass_map.copy()
airmass_df.columns = rpm_axis
airmass_df.index = torque_airmass_axis

# Torque Map: Rows - Torque Map Axis, Columns - RPM Axis
torque_df = torque_map.copy()
torque_df.columns = rpm_axis
torque_df.index = torque_map_axis

# Display the maps
st.header("ECU Maps")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Air Mass Map")
    plt.figure(figsize=(10, 8))
    sns.heatmap(airmass_df, annot=False, cmap="viridis")
    plt.xlabel("RPM")
    plt.ylabel("Torque Air Mass")
    plt.title("Air Mass Map")
    st.pyplot(plt)

with col2:
    st.subheader("Torque Map")
    plt.figure(figsize=(10, 8))
    sns.heatmap(torque_df, annot=False, cmap="plasma")
    plt.xlabel("RPM")
    plt.ylabel("Torque")
    plt.title("Torque Map")
    st.pyplot(plt)

# Main Functionality: Scaling the Maps
st.header("Scale Torque Axis")

st.markdown("""
Enter the new maximum torque value you want to scale the torque axis to. The app will adjust the torque and airflow maps accordingly using linear regression based on the last three known data points.
""")

# Input for new max torque
new_max_torque = st.number_input(
    "Enter the new maximum torque (e.g., 650):",
    min_value=torque_map_axis[-1],
    max_value=20000.0,
    value=650.0,
    step=1.0
)

# Define new torque axis for airflow map
new_torque_axis = sorted(list(set([0, 25, 50, 100, 150, 200, 250, 300, 350, 450, 550, new_max_torque])))

# Display new torque axis
st.write("New Torque Axis for Airflow Map:")
st.write(new_torque_axis)

# Perform linear regression based on the last three data points
# Assuming last three torque points in torque_map_axis are used for scaling
last_three_torque = torque_map_axis[-3:].reshape(-1, 1)
new_last_three_torque = np.array(new_torque_axis[-3:]).reshape(-1, 1)

# Fit linear regression model
reg = LinearRegression()
reg.fit(last_three_torque, new_last_three_torque)
# Predict scaling factor
scaling_factor = reg.coef_[0][0]
intercept = reg.intercept_[0]

st.write(f"Scaling Factor: {scaling_factor:.4f}")
st.write(f"Intercept: {intercept:.4f}")

# Scale the airflow (assuming airflow is inversely related to torque)
# New airflow axis can be derived similarly
# Here, we'll assume airflow scales linearly with torque

# Update RPM axis remains the same
new_rpm_axis = rpm_axis.copy()

# Update Torque Air Mass Axis based on scaling
new_torque_airmass_axis = [scaling_factor * torque + intercept for torque in torque_airmass_axis]

# Create new Air Mass DataFrame
new_airmass_df = airmass_df.copy()
new_airmass_df.index = new_torque_airmass_axis

# Update Torque Map Axis
new_torque_map_axis = new_torque_axis

# Create new Torque DataFrame by interpolating to new torque axis
# Here we use linear interpolation for simplicity
torque_df_reset = torque_df.reset_index().rename(columns={'index': 'Torque'})
new_torque_df = pd.DataFrame(columns=new_rpm_axis, index=new_torque_map_axis)

for rpm in new_rpm_axis:
    # Get the original torque and corresponding values
    X = torque_df.index.values.reshape(-1, 1)
    y = torque_df[rpm].values
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    # Predict for new torque axis
    new_y = model.predict(np.array(new_torque_map_axis).reshape(-1,1))
    new_torque_df[rpm] = new_y

# Update Air Mass Map based on new torque air mass axis
# This step depends on how airflow is related to torque. Assuming inverse scaling.
# Here, we'll use interpolation for simplicity.

new_airmass_df_interpolated = airmass_df.copy()
new_airmass_df_interpolated.index = new_torque_airmass_axis
new_airmass_df_interpolated = new_airmass_df_interpolated.reindex(new_torque_airmass_axis).interpolate(method='linear', axis=0)

# Display the scaled maps
st.header("Scaled ECU Maps")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Scaled Air Mass Map")
    plt.figure(figsize=(10, 8))
    sns.heatmap(new_airmass_df_interpolated, annot=False, cmap="viridis")
    plt.xlabel("RPM")
    plt.ylabel("Scaled Torque Air Mass")
    plt.title("Scaled Air Mass Map")
    st.pyplot(plt)

with col4:
    st.subheader("Scaled Torque Map")
    plt.figure(figsize=(10, 8))
    sns.heatmap(new_torque_df, annot=False, cmap="plasma")
    plt.xlabel("RPM")
    plt.ylabel("Scaled Torque")
    plt.title("Scaled Torque Map")
    st.pyplot(plt)

# Optionally, allow users to download the scaled maps
def convert_df(df):
    return df.to_csv(index=True).encode('utf-8')

st.header("Download Scaled Maps")

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

# Footer
st.markdown("---")
st.markdown("© 2025 ECU Map Scaling App")
