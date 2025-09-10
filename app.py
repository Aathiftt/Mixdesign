import streamlit as st

st.title("Concrete Mix Design Automation (IS 10262:2019)")
st.write("Prototype with Rough Cost Estimation (not using DSR)")

# ---- INPUT SECTION ----
st.header("Input Parameters")

grade = st.selectbox("Grade Designation", ["M20", "M25", "M30", "M35", "M40"])
cement_type = st.selectbox("Type of Cement", ["OPC 43", "OPC 53", "PPC", "PSC"])
max_nominal_size = st.selectbox("Maximum Nominal Size of Aggregate (mm)", [10, 20, 40])
slump = st.number_input("Workability (Slump in mm)", min_value=25, max_value=150, step=5)
exposure = st.selectbox("Exposure Condition", ["Mild", "Moderate", "Severe", "Very Severe", "Extreme"])
placing = st.selectbox("Method of Concrete Placing", ["Pumping", "Manual"])
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

# Rough cost inputs
st.subheader("Material Costs (User-defined)")
cost_cement_unit = st.number_input("Cement cost (₹/kg)", value=6.0, step=0.1)
cost_fa_unit = st.number_input("Fine Aggregate cost (₹/kg)", value=1.0, step=0.1)
cost_ca_unit = st.number_input("Coarse Aggregate cost (₹/kg)", value=0.8, step=0.1)
cost_admixture_unit = st.number_input("Admixture cost (₹/kg)", value=50.0, step=1.0)

# ---- PROCESSING SECTION ----
if st.button("Calculate Mix Design with Cost"):
    st.header("Results")

    # Example simple calculations (replace with full IS 10262 steps later)
    target_mean_strength = {"M20": 26.6, "M25": 31.6, "M30": 38.25,
                            "M35": 43.25, "M40": 48.25}[grade]
    st.write(f"**Target Mean Strength**: {target_mean_strength} MPa")

    # Example water-cement ratio lookup
    w_c_ratio = {"M20": 0.55, "M25": 0.50, "M30": 0.45,
                 "M35": 0.40, "M40": 0.35}[grade]
    st.write(f"**Water-Cement Ratio**: {w_c_ratio}")

    # Example water content selection
    water_content = {10: 208, 20: 186, 40: 165}[max_nominal_size]
    # Slump adjustment
    water_content += max(0, slump - 50) * 0.3
    st.write(f"**Water Content**: {water_content:.2f} kg/m³")

    # Cement content
    cement_content = water_content / w_c_ratio
    st.write(f"**Cement Content**: {cement_content:.2f} kg/m³")

    # Coarse & Fine Aggregate proportions (simplified)
    ca_fraction = 0.62 if max_nominal_size == 20 else 0.66
    fa_fraction = 1 - ca_fraction
    ca_content = ca_fraction * 1000
    fa_content = fa_fraction * 1000

    st.write(f"**Coarse Aggregate**: {ca_content:.2f} kg/m³")
    st.write(f"**Fine Aggregate**: {fa_content:.2f} kg/m³")

    # ---- COST ESTIMATION ----
    st.subheader("Rough Cost Estimation")

    cost_cement = cement_content * cost_cement_unit
    cost_fa = fa_content * cost_fa_unit
    cost_ca = ca_content * cost_ca_unit
    # Admixture assumed 5 kg/m³ for demo (user can adjust later)
    admixture_qty = 5  
    cost_admixture = admixture_qty * cost_admixture_unit

    total_cost = cost_cement + cost_fa + cost_ca + cost_admixture

    st.write(f"Cement Cost: ₹{cost_cement:.2f}")
    st.write(f"Fine Aggregate Cost: ₹{cost_fa:.2f}")
    st.write(f"Coarse Aggregate Cost: ₹{cost_ca:.2f}")
    st.write(f"Admixture Cost: ₹{cost_admixture:.2f}")
    st.success(f"**Total Cost: ₹{total_cost:.2f} per m³ (rough)**")
