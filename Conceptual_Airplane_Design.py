from pandas._libs.lib import is_float, is_integer
import streamlit as st
import pandas as pd
from gam_copy import GAM
from gam_utils import unit


# Load data from the Excel file
#def load_data(file):
#    return pd.read_excel(file)


def setup2():
    if "VARG1" not in st.session_state:
        st.session_state.VARG1 = []
    # if "VARG2" not in st.session_state:
    #     st.session_state.VARG2 = []
    # if "VARG3" not in st.session_state:
    #     st.session_state.VARG3 = []


    st.header("Select Power System Parameters")

    #errors = ["string", "mach", "None", "unknown", "int", "m", "deg", "m2", "kg", "no_dim", "kW", "N", "km/h", "ft", "km"]
    power_data = ["", "", "", "", ""]
    
    energy_type = ["", "Petrol", "Kerosene", "Gasoline", "Compressed H2", "Liquid H2", "Liquid CH4", "Liquid NH3", "Battery"]
    energy = st.selectbox("Select Energy Type", energy_type)
    if energy == "Petrol":
        power_data[0] = "petrol"
    elif energy == "Kerosene":
        power_data[0] = "kerosene"     
    elif energy == "Gasoline":
        power_data[0] = "gasoline"
    elif energy == "Compressed H2":
        power_data[0] = "compressed_h2"
    elif energy == "Liquid H2": 
        power_data[0] = "liquid_h2"
    elif energy == "Liquid CH4":
        power_data[0] = "liquid_ch4"
    elif energy == "Liquid NH3":    
        power_data[0] = "liquid_nh3"
    elif energy == "Battery":                               
        power_data[0] = "battery"

    engine_count =  ["", 1, 2, 4]
    nbengine = st.selectbox("Select Number of Engines", engine_count)
    power_data[1] = nbengine

    engine_type = ["", "Turbofan", "Turboprop", "Piston", "E-motor"]
    etype = st.selectbox("Select Engine Type", engine_type)
    if etype == "Turbofan":
        power_data[2] = "turbofan"
        power_data[3] = "fan"
    elif etype == "Turboprop":
        power_data[2] = "turboprop"
    elif etype == "Piston":
        power_data[2]= "piston"
    elif etype == "E-motor":    
        power_data[2] = "emotor"
        
    

    if  power_data[2] == "turboprop" or power_data[2] == "piston" or power_data[2] == "emotor":
        power_data[3] = "propeller"
        ttype = "Propeller" 
    else:
        power_data[3] = "None"
        ttype = "None"

    if power_data[2] == "turbofan":
        
        left_column_bypass, right_column_bypass = st.columns(2)

        with left_column_bypass:
            bpr = st.slider("Engine Bypass Ratio", 5, 15, 10, 1)
            bpr1 = bpr

        with right_column_bypass:
            bpr1 = st.text_input("Specify Engine Bypass Ratio", bpr1)
        
        if bpr1 != bpr:
            bpr = bpr1
        if bpr1 != "":
            if is_float(float(bpr1)):
                power_data[4] = float(bpr1)
            else:
                st.warning("An engine bypass ratio (BPR) must be specified to continue.")
        else:
            st.warning("An engine bypass ratio (BPR) must be specified to continue.")
    else:
        power_data[4] = "None"

    # st.write("")
    # st.write("Display Selected Power System Configuration")

    # left1, right1 = st.columns(2)
    # power_system = {"Energy Type" : energy, "Number of Engines" : nbengine,
    #             "Engine Type" : etype, "Thruster Type" : ttype , "Engine Bypass Ratio (BPR)" : power_data[4]}
    
    power_system_gam = {"energy_type" : power_data[0], "engine_count" : power_data[1],
                "engine_type" : power_data[2], "thruster_type" : power_data[3] , "bpr" : power_data[4]}
    


######################################################################################################


    st.write("")
    st.header("Select the Design Mission")

    design_mission = {"Category": "", "Number of Passengers": "", "Cruise Speed": "", "Design Range (km)": "", "Cruise Altitude (ft)": ""}
    design_mission_gam = {"category" : "", "npax" : "", "speed" : "", "range" : "", "altitude" : ""}
    
    corres_cat  = ["", "General", "Commuter", "Regional", "Short/Medium Range", "Long Range"]
    cat = ["", "general", "commuter", "regional", "short_medium", "long_range"]

    airplane_type = st.selectbox("Select Aircraft Category", corres_cat)
    
    try:
        if airplane_type != "":
            design_mission["Category"] = airplane_type
            if airplane_type == "General":
                design_mission_gam["category"] = "general"
            elif airplane_type == "Commuter":
                design_mission_gam["category"] = "commuter"
            elif airplane_type == "Regional":
                design_mission_gam["category"] = "regional"
            elif airplane_type == "Short/Medium Range":
                design_mission_gam["category"] = "short_medium"
            elif airplane_type == "Long Range":
                design_mission_gam["category"] = "long_range"

            dis = {"general": 500, "commuter": 1500, "regional": 4500,
                    "short_medium": 8000, "long_range": 15000}
            
            left_column_range, right_column_range = st.columns(2)


            for key in dis:
                if key == design_mission_gam["category"]:
                    if dis[key] - 5000 >= 0:
                        with left_column_range:
                            range_slider = st.slider("Airplane Design Range (km):", dis[key] - 5000, dis[key], dis[key] - 2500, 10)
                            range_slider1 = range_slider
                        with right_column_range:
                            range_slider1 = int(st.text_input("Specify the desired design range (km):", range_slider1))
                        design_mission_gam["range"] = unit.m_km(range_slider1)
                        design_mission["Design Range (km)"] = range_slider1
                        if range_slider1 != range_slider:
                            range_slider = range_slider1
                        # st.write(f"### Selected Design Range: {range_slider1} km")
                    else:
                        with left_column_range:
                            range_slider = st.slider("Airplane Design Range (km):", 0, int(dis[key]), int(dis[key]/2), 10)
                            range_slider1 = range_slider
                        with right_column_range:
                            range_slider1 = int(st.text_input("Specify the desired design range (km):", range_slider1))
                        design_mission_gam["range"] = unit.m_km(range_slider1)
                        design_mission["Design Range (km)"] = range_slider1
                        if range_slider1 != range_slider:
                            range_slider = range_slider1
                        # st.write(f"### Selected Design Range: {range_slider1} km")


            cap = {"general": 6, "commuter": 19, "regional": 80,
                    "short_medium": 250, "long_range": 550}
            pax = st.text_input("Specify Number of Passengers")
            try:
                if pax !=  "":
                    if is_integer(int(pax)) == False:
                        st.warning("Number of passengers must be specified to continue")
                    elif int(pax) <= cap[design_mission_gam["category"]]:
                        design_mission_gam["npax"] = int(pax)
                        design_mission["Number of Passengers"] = int(pax)
                    else:
                        st.warning("Please specify a number of passengers that is consistent with the selected airplane category: " + str(cap[design_mission_gam["category"]]))
            except:
                st.warning("Number of passengers must be specified to continue.")    



            st.write("Please select either cruise speed in km/h or Mach number (one option only).")
            left_column_speed, right_column_speed = st.columns(2)
            cspeed = [""]
            s = 200
            for i in range(10):
                cspeed.append(s)
                s += 25
            with left_column_speed:
                cruisespeed = st.selectbox("Select Cruise Speed (km/h)", cspeed)

            with right_column_speed:
                maspeed = st.text_input("Specify Cruise Mach Number (0.5–0.9)")
                
            
            try:
                if cruisespeed != "" and maspeed == "":
                    design_mission_gam["speed"] = cruisespeed*(10/36)
                    design_mission["Cruise Speed"] = cruisespeed
                elif cruisespeed == "" and maspeed != "":
                    if is_float(float(maspeed)) and 0.5 < float(maspeed) < 0.9:
                        design_mission_gam["speed"] = float(maspeed)
                        design_mission["Cruise Speed"] = float(maspeed)
                    else:
                        st.warning("Cruise Mach number must be between 0.5 and 0.9.")
                elif cruisespeed != "" and maspeed != "":
                    st.warning("Please clear one of the cruise speed inputs to continue.")
            except:
                st.warning("Cruise speed must be specified to continue.")


            alt = ["", 1500, 3000, 5000, 6000, 10000, 20000, 25000, 30000, 35000]
            altitude = st.selectbox("Select Cruise Altitude (ft)", alt)
            try:
                if altitude != "":
                    design_mission_gam["altitude"] = altitude*0.3048
                    design_mission["Cruise Altitude (ft)"] = altitude
            except:
                st.warning("Cruise altitude must be specified to continue.")
    except:
        st.warning("A design mission must be selected to continue.")



    st.header("Display Aircraft Configuration")
    st.write("The aircraft configuration generated from the selected power system and design mission is displayed below.")
    c = 0
    for key in power_system_gam:
        if power_system_gam[key] != "":
            c += 1
    c1 = 0
    for key in design_mission_gam:
        if design_mission_gam[key] != "":
            c1 += 1
    try:
        if c1 == 5 and  c == 5:
            gam = GAM()
            st.write("")
            table_rows = []
            this_dict = gam.design_airplane(power_system_gam, design_mission_gam)
            st.write("Select the Airplane Properties to Display:")


            propulsion = st.checkbox("Propulsion System Definition")
            if propulsion:
                table_rows.append({
                    "Property": "Engine Type",
                    "Value": this_dict["power_system"]["engine_type"]
                })
                table_rows.append({
                    "Property": "Energy Type",
                    "Value": this_dict["power_system"]["energy_type"]
                })
                table_rows.append({
                    "Property": "Thruster Type",
                    "Value": this_dict["power_system"]["thruster_type"]
                })
                table_rows.append({
                    "Property" : "Number of Engines",
                    "Value" : "%.0f" % this_dict["n_engine"]
                })
                table_rows.append({
                    "Property": "Engine Bypass Ratio (BPR)",
                    "Value": this_dict["by_pass_ratio"]
                })
            mission = st.checkbox("Design Mission Definition")
            if mission:
                table_rows.append({
                    "Property" : "Mission Category",
                    "Value" : this_dict["airplane_type"]
                })
                table_rows.append({
                    "Property" : "Number of Passengers",
                    "Value" : "%.0f" % this_dict["npax"]
                })
                table_rows.append({
                    "Property" : "Design Range",
                    "Value" : "%.0f km" % unit.convert_to("km", this_dict["nominal_range"])
                })
                if this_dict["cruise_speed"] > 1:
                    table_rows.append({
                        "Property" : " Cruise Speed ",
                        "Value" : "%.1f km/h" % unit.convert_to("km/h", this_dict["cruise_speed"]) 
                    })
                if this_dict["cruise_speed"] <= 1:
                    table_rows.append({
                        "Property" : " Cruise Mach ",
                        "Value" : "%.2f" % this_dict["cruise_speed"]
                    })
                table_rows.append({
                    "Property" : " Cruise Altitude ",
                    "Value" : "%.1f ft" % unit.convert_to("ft", this_dict["altitude_data"]["mission"]),
                })
            breakdown = st.checkbox("Mass Breakdown")
            if breakdown:
                table_rows.append({
                    "Property": "MTOM",
                    "Value": "%.0f kg" % this_dict["mtow"]
                })
                table_rows.append({
                    "Property": "MZFM",
                    "Value": "%.0f kg" % this_dict["mzfw"]
                })
                table_rows.append({
                    "Property": "Max Payload",
                    "Value": "%.0f kg" % this_dict["payload_max"]
                })
                table_rows.append({
                    "Property": "Max Payload Factor",
                    "Value": "%.3f" % this_dict["max_payload_factor"]
                })
                table_rows.append({
                    "Property": "OEM",
                    "Value": "%.0f kg" % this_dict["owe"]
                })
                table_rows.append({
                    "Property": "Operator Items",
                    "Value": "%.0f kg" % this_dict["op_item"]
                })
                table_rows.append({
                    "Property": "MEM",
                    "Value": "%.0f kg" % this_dict["mwe"]
                })
                table_rows.append({
                    "Property": "Furnishing",
                    "Value": "%.0f kg" % this_dict["furnishing"]
                })
                table_rows.append({
                    "Property": "Standard MEM",
                    "Value": "%.0f kg" % this_dict["std_mwe"]
                })
                table_rows.append({
                    "Property": "Propulsion Mass",
                    "Value": "%.0f kg" % this_dict["propulsion_mass"]
                })
                table_rows.append({
                    "Property": "Energy Storage Mass",
                    "Value": "%.0f kg" % this_dict["energy_storage_mass"]
                })
                table_rows.append({
                    "Property": "Fuel Cell System Mass",
                    "Value": "%.0f kg" % this_dict["fuel_cell_system_mass"]
                })
                table_rows.append({
                    "Property": "Basic MEM",
                    "Value": "%.0f kg" % this_dict["basic_mwe"]
                })
                table_rows.append({
                    "Property": "MEM Shift",
                    "Value": "%.0f kg" % this_dict["stdm_shift"]
                })
            output = st.checkbox("Design Mission Results")
            if output:
                table_rows.append({
                    "Property": "Nominal Passenger Mass Allowance",
                    "Value": "%.1f kg" % this_dict["mpax"]
                })
                table_rows.append({
                    "Property": "Nominal Payload Delta",
                    "Value": "%.0f kg" % this_dict["delta_payload"]
                })
                table_rows.append({
                    "Property": "Nominal Payload",
                    "Value": "%.0f kg" % this_dict["payload"]
                })
                table_rows.append({
                    "Property": "Nominal Mission Time",
                    "Value": "%.1f h" % unit.h_s(this_dict["nominal_time"])
                })

                table_rows.append({
                    "Property": "Mission Fuel",
                    "Value": "%.0f kg" % this_dict["mission_fuel"]
                })
                table_rows.append({
                    "Property": "Reserve Fuel",
                    "Value": "%.0f kg" % this_dict["reserve_fuel"]
                })
                table_rows.append({
                    "Property": "Total Fuel",
                    "Value": "%.0f kg" % this_dict["total_fuel"]
                })
                table_rows.append({
                    "Property": "Fuel Consumption",
                    "Value": "%.2f L/pax/100km" % unit.convert_to("L", this_dict["fuel_consumption"] * unit.m_km(100))
                })
                table_rows.append({
                    "Property": "Mission Energy",
                    "Value": "%.0f kWh" % unit.kWh_J(this_dict["mission_enrg"])
                })
                table_rows.append({
                    "Property": "Reserve Energy",
                    "Value": "%.0f kWh" % unit.kWh_J(this_dict["reserve_enrg"])
                })
                table_rows.append({
                    "Property": "Total Energy",
                    "Value": "%.0f kWh" % unit.kWh_J(this_dict["total_energy"])
                })
                table_rows.append({
                    "Property": "Energy Consumption",
                    "Value": "%.2f kWh/pax/100km" % unit.kWh_J(this_dict["enrg_consumption"] * unit.m_km(100))
                })
                table_rows.append({
                    "Property": "Wake Turbulence Category",
                    "Value": this_dict["wake_turbulence_class"]
                })
            factor = st.checkbox("Performance Factors & Efficiencies")
            if factor:
                table_rows.append({
                    "Property": "Max Power",
                    "Value": "%.0f kW" % unit.kW_W(this_dict["max_power"])
                })
                table_rows.append({
                    "Property": "Standard Mass Factor",
                    "Value": "%.4f" % this_dict["stdm_factor"]
                })
                table_rows.append({
                    "Property": "Aerodynamic Efficiency Factor",
                    "Value": "%.4f" % this_dict["aero_eff_factor"]
                })
                table_rows.append({
                    "Property": "Aerodynamic Efficiency (L/D)",
                    "Value": "%.2f" % this_dict["aerodynamic_efficiency"]
                })
                table_rows.append({
                    "Property": "Propulsion System Efficiency",
                    "Value": "%.3f" % this_dict["propulsion_system_efficiency"]
                })
                table_rows.append({
                    "Property": "Storage Energy Density",
                    "Value": "%.0f Wh/kg" % unit.Wh_J(this_dict["storage_energy_density"])
                })
                table_rows.append({
                    "Property": "Propulsion Power Density",
                    "Value": "%.2f kW/kg" % unit.kW_W(this_dict["propulsion_power_density"])
                })
                table_rows.append({
                    "Property": "Structural Factor (OEM/MTOM)",
                    "Value": "%.2f" % this_dict["structural_factor"]
                })
                table_rows.append({
                    "Property": "Energy Efficiency Factor (P.K/E)",
                    "Value": "%.2f pax.km/kWh" % unit.convert_to("km/kWh", this_dict["pk_o_enrg"])
                })
                table_rows.append({
                    "Property": "Mass Efficiency Factor (P.K/M)",
                    "Value": "%.2f pax.km/kg" % unit.convert_to("km/kg", this_dict["pk_o_mass"])
                })
            
            table = pd.DataFrame(table_rows)
            if propulsion or mission or breakdown or output or factor:
                st.write("")
                st.dataframe(table, width=600, column_config={"Property": {"width": 300}, "Value": {"width": 300},}, hide_index=True)

            st.write("")
            st.write("Compute and Display the Payload-Range Diagram")
            
            try:
                two_dict = gam.build_payload_range(this_dict)    # Compute payload-range data and add them in ac_dict
            except:
                st.info("Failed to build payload-range diagram.")
            left_column4 , right_column4 = st.columns(2)

            if 'payload_info' not in st.session_state:
                st.session_state.payload_info = False
            elif st.session_state.payload_info == True:
                st.session_state.payload_info = False

            with left_column4:
                if st.button("Show Payload-Range Diagram"):
                    st.session_state.payload_info = True
            with right_column4:
                if st.button("Hide Payload-Range Diagram"):
                    st.session_state.payload_info = False
            try:
                if st.session_state.payload_info:
                    gam.print_payload_range(this_dict)    # Print payload-range data
                    tup = (this_dict, two_dict, table, ' ')
                    st.session_state.VARG1.append(tup)
                    config_list = []
                    name_list = []
                    if st.session_state.VARG1:
                        print("Configurations found:")
                        config_list.append(st.session_state.VARG1[0][0])
                        name_list.append(st.session_state.VARG1[0][3])
                        gam.payload_range_graph(config_list, name_list)   # Plot payload-range diagram
                    st.session_state.VARG1.pop()  # Remove the last added configuration to avoid duplication
            except:
                st.info("No configurations to display.")

            st.write("")
            st.write("Save Airplane Configuration")
            left_column3, right_column3 = st.columns(2)

            with left_column3:
                name = st.text_input("Specify Airplane Name")

                duplicate_name = any(ele[3] == name and ele[3] != "" for ele in st.session_state.VARG1)
                if duplicate_name:
                    st.warning("Please specify a new name for the airplane.")
                else:
                    if st.button("Save Airplane", key="save_new_ac"):
                        if name:
                            tup = (this_dict, two_dict, table, name)
                            st.session_state.VARG1.append(tup)
                            st.success(f"{name} saved!")
                        else:
                            tup = (this_dict, two_dict, table, f"AC {len(st.session_state.VARG1)}")
                            st.session_state.VARG1.append(tup)
                            st.success(f"AC {len(st.session_state.VARG1)} saved!")

    except:
        st.warning("Please finish to choose the different parameters to proceed")



def main2():
    '''Main, display the dashboard'''
    st.set_page_config(
        page_title="Dashboard for Conceptual Airplane Design",
        page_icon=":airplane:",
        layout="centered",
    )
    # App title
    st.title("Airplane Conceptual Design Tool")
    st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-family: Courier New; color: green;'>Design a new aircraft configuration from scratch at the conceptual level.</h5>", unsafe_allow_html=True)

    setup2()





# Run the application
if __name__ == "__main__":
    main2()
