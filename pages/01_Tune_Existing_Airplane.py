from pandas._libs.lib import is_integer
from pandas._libs.lib import is_float
import streamlit as st
import pandas as pd
from gam_copy import GAM
from gam_utils import unit



# Load data from the Excel file
def load_data(file):
    '''Read Excel files'''
    return pd.read_excel(file)


def setup3():

    # Load the Excel files
    #file = "airplane_database_copieVF_test.csv"  # File with airplane details
    file = "airplane_database_copieVF.xlsx"

    try:
        data_airplanes = load_data(file)
        filtered_icao  = data_airplanes
        constructor1   = " " 
        selected_type1 = " " 
        icao_code_txt  = " "
    except FileNotFoundError as e:
        st.error(f"File not found: {e.filename}")
        return
    

    if "VARG2" not in st.session_state:
        st.session_state.VARG2 = []

    prop = ["airplane_type",  "name", "manufacturer", "icao_code", "iata_code", "n_pax", "owe",
            "mtow", "mlw", "max_fuel", "n_engine", "engine_type", "thruster_type", "powerplant",
            "bpr", "energy_type", "max_power", "max_thrust", "cruise_speed", "cruise_altitude", "nominal_range"]


    st.header("How would you like to search for your reference airplane?")
    # Choice: Use airplane type or skip directly to ICAO
    search_option = st.radio(
        "",
        ("By Airplane Manufacturer and ICAO Code", "By Airplane Type and ICAO Code", "By ICAO Code Only")
    )


    if search_option == "By Airplane Manufacturer and ICAO Code":
        # List of the name of the airplane constructor
        constructor = [" "]
        errors = ["string", "mach", "None", "unknown", "int", "m", "deg", "m2", "kg", "no_dim", "kW", "N", "km/h", "ft", "km"]
        for element in data_airplanes["Constructor"]:
            if element not in errors:
                if element not in constructor:
                    constructor.append(element)

        # Chose of the constructor
        constructor1 = st.selectbox('Select Airplane Manufacturer', constructor)
        try:
            if constructor1 != " ":
                data_airplanes_cons = data_airplanes[data_airplanes["Constructor"] == constructor1]
                if not data_airplanes_cons.empty:
                    combined_data = pd.DataFrame({"Property": prop})
                    for idx, (_, row) in enumerate(data_airplanes_cons.iterrows(), start=1):
                        column_name = f"{idx}"
                        combined_data[column_name] = [row.get(p, "N/A") for p in prop]
                    st.dataframe(combined_data, hide_index=True)


                # User input for ICAO code
                icao_match = data_airplanes_cons["icao_code"].drop_duplicates().tolist()
                icao_match.insert(0, " ")
                icao_code = st.selectbox("Select ICAO code", icao_match)

                if icao_code:
                    # Find the IATA code from the ICAO code
                    filtered_icao = data_airplanes[data_airplanes["icao_code"] == icao_code]

                    try:
                        if not filtered_icao.empty:
                            iata_code = filtered_icao["iata_code"].iloc[0]
                            # st.success(f"IATA code found: {iata_code}")

                            # Filter airplane details by IATA code and selected construtor
                            airplane_info = data_airplanes[
                                (data_airplanes["iata_code"] == iata_code) &
                                (data_airplanes["Constructor"] == constructor1)
                            ]
                            
                            if not airplane_info.empty:
                                # st.success(f"Airplane details for ICAO code '{icao_code}' and manufacturer '{constructor1}':")
                                combined_data = pd.DataFrame({"Property": prop})

                                for idx, (_, row) in enumerate(airplane_info.iterrows(), start=1):
                                    column_name = f"{idx}"
                                    combined_data[column_name] = [row.get(p, "N/A") for p in prop]

                                st.dataframe(combined_data, hide_index=True)

                            else:
                                st.warning(f"No airplane details found for IATA code '{iata_code}' and manufacturer '{constructor1}'.")
                    except:
                        st.warning(f"No IATA code found for ICAO code '{icao_code}'.")
        except:
            st.warning("Airplane manufacturer must be selected to proceed")

    elif search_option == "By Airplane Type and ICAO Code":
        # Dropdown for airplane type
        atp = [" ", "General", "Commuter", "Regional", "Short Medium Range", "Long Range"]
        corres = ["", "general", "commuter", "regional", "short_medium", "long_range"]

        selected_type1 = st.selectbox("Select Airplane Category", atp)
        selected_type = ""
        for i in range(len(atp)):
            if atp[i] == selected_type1:
                selected_type = corres[i]

        try:
            if selected_type1 != " ":
                # st.success(f"You selected: {selected_type1}")
                data_airplanes_type = data_airplanes[data_airplanes["airplane_type"] == selected_type]
                if not data_airplanes_type.empty:
                    combined_data = pd.DataFrame({"Property": prop})

                    for idx, (_, row) in enumerate(data_airplanes_type.iterrows(), start=1):
                        column_name = f"{idx}"
                        combined_data[column_name] = [row.get(p, "N/A") for p in prop]
                    st.dataframe(combined_data, hide_index=True)

                # User input for ICAO code
                icao_match = data_airplanes_type["icao_code"].drop_duplicates().tolist()
                icao_match.insert(0, " ")
                icao_code = st.selectbox("Select ICAO code", icao_match)

                if icao_code and icao_code != " ":
                    # Find the IATA code from the ICAO code
                    filtered_icao = data_airplanes[data_airplanes["icao_code"] == icao_code]

                    if not filtered_icao.empty :
                        iata_code = filtered_icao["iata_code"].iloc[0]
                        # st.success(f"IATA code found: {iata_code}")

                        # Filter airplane details by IATA code and selected type
                        airplane_info = data_airplanes[
                            (data_airplanes["iata_code"] == iata_code) &
                            (data_airplanes["airplane_type"] == selected_type)
                        ]

                        if not airplane_info.empty:
                            # st.success(f"Airplane details for ICAO code '{icao_code}' and type '{selected_type1}':")
                            combined_data = pd.DataFrame({"Property": prop})

                            for idx, (_, row) in enumerate(airplane_info.iterrows(), start=1):
                                column_name = f"{idx}"
                                combined_data[column_name] = [row.get(p, "N/A") for p in prop]

                            st.dataframe(combined_data, hide_index=True)

                        else:
                            st.warning(f"No airplane details found for IATA code '{iata_code}' and type '{selected_type1}'.")
                    else:
                        st.warning(f"No IATA code found for ICAO code '{icao_code}'.")
        except:
            st.warning("Airplane category must be selected to continue.")

    elif search_option == "By ICAO Code Only":
        # User input for ICAO code without selecting type
        icao_code_txt = st.text_input("Specify an ICAO code:")

        try:
            if icao_code_txt:
                # Find the IATA code from the ICAO code
                filtered_icao = data_airplanes[data_airplanes["icao_code"] == icao_code_txt]

                if not filtered_icao.empty:
                    iata_code = filtered_icao["iata_code"].iloc[0]
                    # st.success(f"IATA code found: {iata_code}")

                    # Retrieve all airplane details for the matched IATA code
                    airplane_info = data_airplanes[data_airplanes["iata_code"] == iata_code]

                    if not airplane_info.empty:
                        # st.success(f"Airplane details for ICAO code '{icao_code_txt}':")
                        combined_data = pd.DataFrame({"Property": prop})

                        for idx, (_, row) in enumerate(airplane_info.iterrows(), start=1):
                            column_name = f"{idx}"
                            combined_data[column_name] = [row.get(p, "N/A") for p in prop]

                        st.dataframe(combined_data, hide_index=True)
                    else:
                        st.warning(f"No airplane details found for ICAO code '{icao_code_txt}'.")
                else:
                    st.warning(f"No airplane with ICAO code '{icao_code_txt}' found.")
        except:
            st.warning("ICAO code must be specified to continue.")


    # User input for airplane name
    try:
        if (constructor1 != " " and icao_code != " ") or (selected_type1 != " " and icao_code!= " ") or (icao_code_txt and icao_code_txt != " "):
            name_match = filtered_icao["name"].drop_duplicates().tolist()
            name_match.insert(0, " ")
            airplane = st.selectbox("Select Airplane Name", name_match)
            
            final_data = []
            if data_airplanes[data_airplanes["name"] == airplane].empty and airplane != " ":
                st.warning(f"No airplane found with the specified name '{airplane}'.")
            if not data_airplanes[data_airplanes["name"] == airplane].empty and airplane != " ":
                # st.success(f"Airplane found: {airplane}")
                # Data of the plane the user search
                final_data = data_airplanes[data_airplanes["name"] == airplane]
    
                final = pd.DataFrame({"Property": prop})

                for idx, (_, row) in enumerate(final_data.iterrows(), start=1):
                    column_name = f"{idx}"
                    final[column_name] = [row.get(p, "N/A") for p in prop]

                st.dataframe(final, hide_index=True)

                st.write("")
                st.header("Design an " + airplane + "-like Airplane")
                
                # Initialization of gam entries
                design_mission = {"category": "",
                                "npax": "",
                                "speed": "",
                                "range": "",
                                "altitude": "",
                                "mtow": "",
                                "owe": "",
                                "payload": "",
                                "payload_max": "",}
                gam = GAM()

                # Complete the power system
                st.write("#### Tune Power System Parameters")

                errors = ["string", "mach", "None", "unknown", "int", "m", "deg", "m2", "kg", "no_dim", "kW", "N", "km/h", "ft", "km"]
                power_data = ["", "", "", "", ""]

                energy_type = ["", "petrol", "kerosene", "gasoline", "compressed_h2", "liquid_h2", "liquid_ch4", "liquid_nh3", "battery"]                
                
                
                energy = st.selectbox("Select Energy Type", energy_type, index=energy_type.index(final['1'][final.index[final["Property"]=="energy_type"].tolist()[0]]))
                power_data[0] = energy

                engine_count =  ["", 1, 2, 4]
                nbengine = st.selectbox("Select Number of Engines", engine_count, index=engine_count.index(final['1'][final.index[final["Property"]=="n_engine"].tolist()[0]]))
                if nbengine != "":
                    if int(nbengine) <= 12 and is_integer(int(nbengine)):
                        power_data[1] = int(nbengine)

                engine_type = ["", "turbofan", "turboprop", "piston", "emotor"]
                etype = st.selectbox("Select Engine Type", engine_type, index=engine_type.index(final['1'][final.index[final["Property"]=="engine_type"].tolist()[0]]))
                power_data[2] = etype

                if power_data[2] == "turbofan":
                    power_data[3] = "fan"
                elif power_data[2] == "turboprop":
                    power_data[3] = "propeller"
                else:
                    power_data[3] = "None"

                if power_data[2] == "turbofan":
                    left_column_bypass, right_column_bypass = st.columns(2)
                    with left_column_bypass:
                        bpr = st.slider("Engine Bypass Ratio", 5., 15., float(final['1'][final.index[final["Property"]=="bpr"].tolist()[0]]), 0.1)
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


                power_system = {"energy_type" : power_data[0], "engine_count" : power_data[1],
                "engine_type" : power_data[2], "thruster_type" : power_data[3] , "bpr" : power_data[4]}
                
                # Complete design mission
                st.write("#### Tune the Design Mission")

                # Complete category
                category = ["general", "business", "commuter", "regional", "short_medium", "long_range"]
                
                    
                for elec in category:
                    test_cat = final_data[final_data["airplane_type"] == elec]
                    if not test_cat.empty:
                        design_mission["category"] = elec
                
                # Complete npax
                pax = st.text_input("Specify Number of Passengers", value = final['1'][final.index[final["Property"]=="n_pax"].tolist()[0]])
                if pax != "":
                    if is_integer(int(pax)) == False:
                        st.warning("Number of passengers must be specified to continue")
                    else:
                        design_mission["npax"] = int(pax)
                
                # Complete speed
                st.write("Specify either cruise speed in km/h or Mach number (one option only).")
                left_column_speed, right_column_speed = st.columns(2)

                
                with left_column_speed:
                    if float(final['1'][final.index[final["Property"]=="cruise_speed"].tolist()[0]]) > 1.0:
                        cruise_speed = st.text_input("Specify Cruise Speed (km/h)", value = final['1'][final.index[final["Property"]=="cruise_speed"].tolist()[0]])
                    else: 
                        cruise_speed = st.text_input("Specify Cruise Speed (km/h)")
                
                
                with right_column_speed:
                    if float(final['1'][final.index[final["Property"]=="cruise_speed"].tolist()[0]]) > 1.0:
                        cruise_speed_mach = st.text_input("Specify Cruise Mach Number (0.5–0.9)")
                    else:
                        cruise_speed_mach = st.text_input("Specify Cruise Mach Number (0.5–0.9)", value = final['1'][final.index[final["Property"]=="cruise_speed"].tolist()[0]])
                
                if cruise_speed != "":
                    if is_float(float(cruise_speed)) and (float(cruise_speed) > 1.):
                        print("cruise speed", cruise_speed)
                        design_mission["speed"] = unit.convert_from("km/h", float(cruise_speed))
                elif cruise_speed_mach != "":
                    if is_float(float(cruise_speed_mach)) and (float(cruise_speed_mach) < 1.):
                        print("cruise speed mach", cruise_speed_mach)
                        design_mission["speed"] = float(cruise_speed_mach)
                else:
                    st.warning("Cruise speed must be specified to continue.")
                
                print(design_mission)
                # Complete range
                dis = {"general": 500., "commuter": 1500., "regioal": 4500.,
                    "short_medium": 8000., "long_range": 15000., "business": 15000.}
            
                
                left_column_range, right_column_range = st.columns(2)
                
                if len(final_data["airplane_type"].values) != 0 and len(final_data["nominal_range"].values) != 0: 
                    with left_column_range:
                        ref_range = float(final['1'][final.index[final["Property"]=="nominal_range"].tolist()[0]])
                        range_slider = st.slider("Specify Design Range (km):", ref_range - 1500., ref_range + 1500., ref_range, 10.)
                    with right_column_range:
                        range_slider = float(st.text_input("Specify Exact Design Range (km) ", range_slider))
                else:
                    ref_range = float(dis[final_data["airplane_type"].values[0]])
                    with left_column_range:
                        range_slider = st.slider("Specify Design Range (km):", 0., ref_range + 1500., ref_range, 10.)
                    with right_column_range:
                        range_slider = float(st.text_input("Specify Exact Design Range (km) ", range_slider))
                
                design_mission["range"] = unit.convert_from("km", range_slider)
                
                # Complete altitude
                cruise_altitude = st.text_input("Specify Cruise Altitude (ft)", value = final['1'][final.index[final["Property"]=="cruise_altitude"].tolist()[0]])
                if cruise_altitude != "":
                    if is_integer(int(cruise_altitude)) == False:
                        st.warning("Cruise altitude must be specified to continue.")
                    else:
                        design_mission["altitude"] = int(cruise_altitude)*0.3048
                
                # Complete MTOW
                for e in data_airplanes["mtow"]:
                    if e not in errors:
                        test_mtow = final_data[final_data["mtow"] == e]
                        if not test_mtow.empty:
                            design_mission["mtow"] = e
                
                # Complete OWE
                for e in data_airplanes["owe"]:
                    if e not in errors:
                        test_owe = final_data[final_data["owe"] == e]
                        if not test_owe.empty:
                            design_mission["owe"] = e
                
                # Complete payload
                for key in dis:
                    test = final_data[final_data["airplane_type"] == key]
                    if not test.empty:
                        if design_mission["npax"] != "":
                            payload = design_mission["npax"]*gam.mpax_dict[key]
                            design_mission["payload"] = payload

                
                # Complete max_payload
                if design_mission["payload"] != "":
                    max_payload = design_mission["payload"]*gam.max_payload_factor
                    design_mission["payload_max"] = float(max_payload)

                
                st.write("")
                c = 0
                this_dict = {}
                for key in design_mission:
                    if design_mission[key] != "":
                        c +=1
                try:
                    if c == 9:
                        table_rows = []
                        this_dict = gam.tune_design(power_system, design_mission)
                        st.write("Select the Airplane Properties to Display:")

                        Name = st.checkbox("Airplane Name")
                        if Name:
                            table_rows.append({
                                    "Property" : "Name",
                                    "Value" : airplane
                                })
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
                                "Property" : " Airplane Type",
                                "Value" : this_dict["airplane_type"]
                            })
                            table_rows.append({
                                "Property" : "Mission Category",
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
                        if Name or propulsion or mission or breakdown or output or factor:
                            st.write("")
                            st.dataframe(table, width=600, column_config={"Property": {"width": 300}, "Value": {"width": 300},}, hide_index=True)
                except:
                    st.warning("All design mission parameters must be specified to continue.")


                st.write("")
                st.write("#### Compute and Display the Payload-Range Diagram")
                
                if this_dict != {}:
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
                            st.session_state.VARG2.append(tup)
                            config_list = []
                            name_list = []
                            if st.session_state.VARG2:
                                print("Configurations found:")
                                config_list.append(st.session_state.VARG2[0][0])
                                name_list.append(st.session_state.VARG2[0][3])
                                gam.payload_range_graph(config_list, name_list)   # Plot payload-range diagram
                            st.session_state.VARG2.pop()
                    except:
                        st.info("No configurations to display.")

                    
                    st.write("")
                    st.write("Save Airplane Configuration")
                    left_column3, right_column3 = st.columns(2)

                    with left_column3:
                        name = st.text_input("Specify Airplane Name")

                        duplicate_name = any(ele[3] == name and ele[3] != "" for ele in st.session_state.VARG2)
                        if duplicate_name:
                            st.warning("Please specify a new name for the airplane.")
                        else:
                            if st.button("Save Airplane", key="save_new_ac"):
                                if name:
                                    tup = (this_dict, two_dict, table, name)
                                    st.session_state.VARG2.append(tup)
                                    st.success(f"{name} saved!")
                                else:
                                    tup = (this_dict, two_dict, table, f"AC {len(st.session_state.VARG2)}")
                                    st.session_state.VARG2.append(tup)
                                    st.success(f"AC {len(st.session_state.VARG2)} saved!")
                                    

    except:
        st.warning("An airplane must be selected to continue.")




def main3():
    '''Main, display the dashboard'''
    st.set_page_config(
        page_title="Dashboard for Airplane Fuel Consumption",
        page_icon=":airplane:",
        layout="centered",
    )
    # App title
    st.title("Existing Airplane Design Tuning Tool")
    st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-family: Courier New; color: green;'>Tune the design parameters of a real, existing airplane at the conceptual level.</h5>", unsafe_allow_html=True)
    setup3()





# Run the application
if __name__ == "__main__":
    main3()
