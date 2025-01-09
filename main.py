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
    value="""0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
112.799	110.298	108.517	105.084	103.982	103.007	102.583	100.082	96.182	97.793	102.116	49.299	45.696	48.197	100.718	103.897
180.495	177.485	174.518	170.406	169.516	168.71	169.007	168.287	162.988	165.489	167.82	158.791	155.782	160.996	166.294	168.117
319.193	315.802	309.613	305.798	304.908	303.891	303.001	304.484	298.889	299.694	298.804	292.191	292.7	296.896	297.108	297.999
513.38	453.907	445.006	438.817	437.121	436.316	437.121	439.792	434.917	433.179	433.688	444.115	448.1	447.295	445.981	449.88
663.397	598.795	575.396	569.08	562.679	561.407	570.818	574.294	572.301	568.614	569.08	584.086	588.791	585.315	586.502	592.479
815.787	804.3	804.003	736.18	709.305	700.488	707.016	709.093	711.297	704.811	707.016	719.52	723.505	722.488	731.22	741.521
976.316	970.382	966.312	938.886	925.195	890.393	856.82	847.283	853.811	853.217	855.888	878.1	881.618	882.805	896.115	896.921
1123.111	1105.52	1102.001	1040.197	1054.779	1057.111	1001.793	997.596	1002.216	1004.082	1003.488	1030.617	1049.311	1054.313	1065.292	1092.803
1334.211	1301.02	1279.91	1190.808	1211.621	1214.588	1156.514	1162.915	1163	1164.017	1157.489	1198.904	1233.494	1266.303	1304.581	1323.317
1515.893	1481.303	1452.394	1409.114	1382.917	1369.48	1343.495	1346.801	1343.198	1343.495	1330.82	1381.9	1420.389	1466.679	1505.296	1512.502
1684.307	1645.817	1613.813	1565.701	1538.487	1522.294	1504.999	1507.119	1503.007	1503.092	1489.484	1538.699	1578.206	1629.709	1672.48	1680.492"""
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
    value="""2.844	3.438	3.688	2.906	2.344	1.281	1.281	1.281	1.281	1.281	1.281	25.344	27.375	25.938	23.219	22.031
20.281	21.188	21.781	23.062	23.469	23.844	24.031	24.969	26.969	26.094	24.188	27.875	29.375	27.562	24.719	23.469
57.188	58.344	59.656	61.344	61.656	61.906	61.656	61.594	63.5	62.562	62.281	65.5	66.312	64.344	62.875	62.406
93.094	94.312	96.469	97.844	98.188	98.531	98.875	98.344	100.406	100.125	100.469	102.906	102.656	101.156	101.094	100.781
128.719	130	132.719	134.531	135.062	135.438	135.75	134.844	136.906	137.375	137.219	135.312	134.312	133.906	134.438	133.531
145.375	166.406	170.281	173.438	174.25	174.531	173.188	171.969	173.406	174.281	174.094	167.875	166.281	167.219	167.562	165.875
177.625	200.062	209.188	211.344	214.688	215.344	210.531	209.219	209.688	211.25	211.031	205.625	203.812	205.219	204.625	202.375
213.438	226.906	230.719	242.719	248.438	250.531	248.312	247.406	246.719	249.031	248.281	244.375	242.969	243.5	241.188	238.25
245.781	248.938	248.938	263.594	269.438	278.219	281.812	283.25	281.406	282.938	282.094	275.938	275.031	274.594	270.75	267.438
267.188	273.25	275.125	280.281	289.875	302.062	313.5	318.344	315.656	314.719	313.812	306.438	305.312	304.969	300.875	300.719
339.531	348.594	349.438	379.562	367.438	363	384.875	382.906	382.531	382.188	383.406	373	365.094	363.25	360.25	351.844
410.594	425.312	433.75	447.094	455	459.844	465.125	464.469	465.75	465.719	469.969	454.938	443.531	429.531	418.531	416.531"""
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
# Air Mass Map: Rows - Torque Air Mass Axis, Columns - RPM Axis
airmass_df = airmass_map.copy()
airmass_df.columns = rpm_axis
airmass_df.index = torque_airmass_axis

# Torque Map: Rows - Torque Map Axis, Columns - RPM Axis
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
Enter the new maximum torque value you want to scale the torque axis to. The app will adjust the torque and airflow maps accordingly using linear regression based on the last three known data points.
""")

# Input for new max torque
# Fixing the error by setting min_value to the smallest torque value or lower
new_max_torque = st.number_input(
    "Enter the new maximum torque (e.g., 650):",
    min_value=0.0,  # Changed from torque_map_axis[-1] to 0.0
    max_value=20000.0,
    value=650.0,
    step=1.0
)

# Define new torque axis for airflow map
# Ensure the new max torque is included
new_torque_axis = sorted(list(set([0, 25, 50, 100, 150, 200, 250, 300, 350, 450, 550, new_max_torque])))

# Display new torque axis
st.write("**New Torque Axis for Airflow Map:**")
st.write(new_torque_axis)

# Perform linear regression based on the last three data points
# Ensure that there are at least three data points
if len(torque_map_axis) < 3:
    st.error("Not enough data points in Torque Map Axis to perform scaling.")
    st.stop()

# Extract the last three torque points and their corresponding new values
last_three_torque = np.array(torque_map_axis[-3:]).reshape(-1, 1)
last_three_new_torque = np.array(new_torque_axis[-3:]).reshape(-1, 1)

# Fit linear regression model
reg = LinearRegression()
reg.fit(last_three_torque, last_three_new_torque)

# Predict scaling factor and intercept
scaling_factor = reg.coef_[0][0]
intercept = reg.intercept_[0]

st.write(f"**Scaling Factor:** {scaling_factor:.4f}")
st.write(f"**Intercept:** {intercept:.4f}")

# Scale the airflow (assuming airflow scales linearly with torque)
# Update Torque Air Mass Axis based on scaling
new_torque_airmass_axis = [scaling_factor * torque + intercept for torque in torque_airmass_axis]

# Create new Air Mass DataFrame
new_airmass_df = airmass_df.copy()
new_airmass_df.index = new_torque_airmass_axis

# Update Torque Map Axis
new_torque_map_axis = new_torque_axis

# Create new Torque DataFrame by interpolating to new torque axis
new_torque_df = pd.DataFrame(columns=new_rpm_axis := rpm_axis.copy(), index=new_torque_map_axis)

for rpm in new_rpm_axis:
    # Get the original torque and corresponding values
    X = np.array(torque_df.index).reshape(-1, 1)
    y = torque_df[rpm].values
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    # Predict for new torque axis
    new_y = model.predict(np.array(new_torque_map_axis).reshape(-1,1))
    new_torque_df[rpm] = new_y

# Update Air Mass Map based on new torque air mass axis
# Assuming linear relationship for simplicity
new_airmass_df_interpolated = new_airmass_df.copy()

# Since the new torque air mass axis may have different values, we perform interpolation
new_airmass_df_interpolated = airmass_df.copy()
new_airmass_df_interpolated.index = new_torque_airmass_axis
new_airmass_df_interpolated = new_airmass_df_interpolated.reindex(new_torque_airmass_axis).interpolate(method='linear', axis=0)

# Display the scaled maps as tables
st.header("Scaled ECU Maps as Tables")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Scaled Air Mass Map")
    st.dataframe(new_airmass_df_interpolated)

with col4:
    st.subheader("Scaled Torque Map")
    st.dataframe(new_torque_df)

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
