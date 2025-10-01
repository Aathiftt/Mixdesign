import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

st.title("Concrete Mix Design Automation (IS 10262:2019)")
st.write("Prototype with Rough Cost Estimation (not using DSR)")

# ---- INPUT SECTION ----
st.header("Input Parameters")

grade = st.selectbox("Grade Designation", ["M20", "M25", "M30", "M35", "M40"])
cement_type = st.selectbox("Type of Cement", ["OPC 33", "OPC 43", "OPC 53"])
max_nominal_size = st.selectbox("Maximum Nominal Size of Aggregate (mm)", [10, 20, 40])
slump = st.number_input("Workability (Slump in mm)", min_value=25, max_value=150, step=5)
exposure = st.selectbox("Exposure Condition", ["Mild", "Moderate", "Severe", "Very Severe", "Extreme"])
placing = st.selectbox("Method of Concrete Placing", ["Manual", "Pumping"])
supervision = st.selectbox("Degree of Supervision", ["Good", "Fair", "Poor"])
agg_type = st.selectbox("Type of Aggregate", ["Crushed Angular", "Natural Rounded", "Other"])
admixture_type = st.selectbox("Type of Chemical Admixture", ["None", "Plasticizer", "Superplasticizer"])

# Material properties
st.subheader("Material Properties")
sg_cement = st.number_input("Specific Gravity of Cement", value=3.15, step=0.01)
sg_ca = st.number_input("Specific Gravity of Coarse Aggregate", value=2.7, step=0.01)
sg_fa = st.number_input("Specific Gravity of Fine Aggregate", value=2.65, step=0.01)
sg_admixture = st.number_input("Specific Gravity of Admixture", value=1.1, step=0.01)
fa_zone = st.selectbox("Fine Aggregate Zone", ["Zone I", "Zone II", "Zone III", "Zone IV"])

# Material costs
st.subheader("Material Costs (User-defined)")
cost_cement_unit = st.number_input("Cement cost (₹/kg)", value=6.0, step=0.1)
cost_fa_unit = st.number_input("Fine Aggregate cost (₹/kg)", value=1.0, step=0.1)
cost_ca_unit = st.number_input("Coarse Aggregate cost (₹/kg)", value=0.8, step=0.1)
cost_admixture_unit = st.number_input("Admixture cost (₹/kg)", value=50.0, step=1.0)

# ---- PROCESSING SECTION ----
if st.button("Calculate Mix Design with Cost"):
    st.header("Results")

    # Step 1: Target mean strength
    target_mean_strength = {"M20":26.6,"M25":31.6,"M30":38.25,"M35":43.25,"M40":48.25}[grade]
    st.write(f"**Target Mean Strength**: {target_mean_strength} MPa")

    # Step 2: Water-cement ratio selection using 3 curves
    cement_curve_map = {"OPC 33":"Curve_1","OPC 43":"Curve_2","OPC 53":"Curve_3"}
    curve_sheet = cement_curve_map[cement_type]
    
    df_curve = pd.read_excel("water_cement_ratio_curves.xlsx", sheet_name=curve_sheet)
    X = df_curve[['Compressive_Strength']].values
    y = df_curve['Water_Cement_Ratio'].values
    
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    
    predicted_wc_ratio = model.predict(poly.transform([[target_mean_strength]]))[0]
    st.write(f"**Predicted Water-Cement Ratio**: {predicted_wc_ratio:.3f}")

    # Step 3: Water content selection (IS 10262 logic)
    water_content_base = {10:208, 20:186, 40:165}[max_nominal_size]

    # Slump adjustment: 25–50mm = base; every +25mm => +3%
    if slump > 50:
        extra_intervals = (slump - 50) // 25
        water_content = water_content_base * (1 + 0.03 * extra_intervals)
    else:
        water_content = water_content_base

    # Step 3b: Superplasticizer adjustment (reduce water by 20%)
    if admixture_type == "Superplasticizer":
        water_content *= 0.8

    st.write(f"**Adjusted Water Content**: {water_content:.2f} kg/m³")

    # Step 4: Cement content calculation
    cement_content = water_content / predicted_wc_ratio
    st.write(f"**Cement Content**: {cement_content:.2f} kg/m³")

    # Step 5b: Pumpable concrete adjustment
    if placing=="Pumping":
        water_content += 10
        cement_content = water_content / predicted_wc_ratio
        st.write(f"**Adjusted Cement Content for Pumping**: {cement_content:.2f} kg/m³")

    # Step 6: Mix calculation (simplified)
    ca_fraction = 0.62 if max_nominal_size==20 else 0.66
    fa_fraction = 1 - ca_fraction
    ca_content = ca_fraction*1000
    fa_content = fa_fraction*1000
    
    st.write(f"**Coarse Aggregate**: {ca_content:.2f} kg/m³")
    st.write(f"**Fine Aggregate**: {fa_content:.2f} kg/m³")

    # Step 7: Final Mix Ratio C:FA:CA
    fa_ratio = fa_content / cement_content
    ca_ratio = ca_content / cement_content
    st.write(f"**Final Mix Ratio (C:FA:CA)** = 1 : {fa_ratio:.2f} : {ca_ratio:.2f}")

    # Step 8: Rough Cost Estimation
    cost_cement = cement_content*cost_cement_unit
    cost_fa = fa_content*cost_fa_unit
    cost_ca = ca_content*cost_ca_unit
    admixture_qty = 5 if admixture_type!="None" else 0
    cost_admixture = admixture_qty*cost_admixture_unit
    total_cost = cost_cement + cost_fa + cost_ca + cost_admixture

    st.write(f"Cement Cost: ₹{cost_cement:.2f}")
    st.write(f"Fine Aggregate Cost: ₹{cost_fa:.2f}")
    st.write(f"Coarse Aggregate Cost: ₹{cost_ca:.2f}")
    st.write(f"Admixture Cost: ₹{cost_admixture:.2f}")
    st.success(f"**Total Cost: ₹{total_cost:.2f}/m³ (rough estimate)**")
