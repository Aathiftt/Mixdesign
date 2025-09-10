def mix_design():
    print("\n--- Concrete Mix Design Automation (IS 10262:2019) ---\n")

    # --- Step 1: User Inputs ---
    grade = input("Enter grade designation (e.g., M20, M25, M30): ").strip()
    cement_type = input("Enter type of cement (OPC/PPC/PSC): ").strip()
    agg_size = int(input("Enter maximum nominal size of aggregate (10/20/40 mm): "))
    slump = float(input("Enter desired slump in mm: "))
    exposure = input("Enter exposure condition (Mild/Moderate/Severe/Very Severe/Extreme): ").strip()
    placing_method = input("Enter method of concrete placing (Manual/Pumped): ").strip()
    supervision = input("Enter degree of supervision (Good/Fair/Poor): ").strip()
    agg_type = input("Enter type of aggregate (Crushed/Rounded): ").strip()
    admixture_type = input("Enter chemical admixture type (None/Plasticizer/Superplasticizer): ").strip()

    # --- Material Properties ---
    sp_gr_cement = float(input("Enter specific gravity of cement: "))
    sp_gr_ca = float(input("Enter specific gravity of coarse aggregate: "))
    sp_gr_fa = float(input("Enter specific gravity of fine aggregate: "))
    sp_gr_admixture = float(input("Enter specific gravity of admixture: "))
    fa_zone = input("Enter fine aggregate zone (Zone I/Zone II/Zone III/Zone IV): ").strip()

    # --- Step 2: Target Mean Strength ---
    fck_values = {"M20": 20, "M25": 25, "M30": 30}
    sigma_values = {"good": 4.0, "fair": 5.0, "poor": 6.0}
    k = 1.65

    fck = fck_values.get(grade.upper(), 25)
    sigma = sigma_values.get(supervision.lower(), 5.0)
    f_target = fck + k * sigma
    print(f"\nTarget mean strength = {f_target:.2f} MPa")

    # --- Step 3: Water-Cement Ratio (Simplified) ---
    wc_ratio_table = {
        "mild": 0.55, "moderate": 0.50, "severe": 0.45,
        "very severe": 0.45, "extreme": 0.40
    }
    wc_ratio = wc_ratio_table.get(exposure.lower(), 0.50)
    print(f"Adopted water-cement ratio = {wc_ratio}")

    # --- Step 4: Water Content ---
    water_content_table = {10: 208, 20: 186, 40: 165}  # for 50 mm slump
    base_water = water_content_table.get(agg_size, 186)
    water = base_water + (slump - 50) * 0.3  # simple correction
    print(f"Water content = {water:.1f} kg/m³")

    # --- Step 5: Cement Content ---
    cement = water / wc_ratio
    print(f"Cement content = {cement:.1f} kg/m³")

    # --- Step 6: Aggregate Proportions ---
    fa_fraction = 0.35 if fa_zone in ["Zone II", "Zone III"] else 0.30
    ca_fraction = 1 - fa_fraction
    print(f"FA fraction = {fa_fraction}, CA fraction = {ca_fraction}")

    # --- Step 7: Mass of Aggregates ---
    total_agg_mass = 1000 - (cement / sp_gr_cement * 0.315) - water
    fa = fa_fraction * total_agg_mass * sp_gr_fa
    ca = ca_fraction * total_agg_mass * sp_gr_ca

    # --- Step 8: Output Mix ---
    print("\n--- Mix Proportions (per m³) ---")
    print(f"Cement: {cement:.1f} kg")
    print(f"Water: {water:.1f} kg")
    print(f"Fine Aggregate: {fa:.1f} kg")
    print(f"Coarse Aggregate: {ca:.1f} kg")
    print(f"Admixture: To be added as per dosage\n")


# Run the program
mix_design()
