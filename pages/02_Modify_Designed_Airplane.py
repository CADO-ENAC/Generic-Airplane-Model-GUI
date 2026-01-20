from pandas._libs.lib import is_integer, is_float
import streamlit as st
import pandas as pd
from gam_copy import GAM
from gam_utils import unit


def tweak_graphic():
    gam = GAM()

    dis = {"general": 95, "commuter": 105, "regional": 110,
        "short_medium": 115, "long_range": 120, "business": 120}

    graph_list = [""]
    name_list  = [""]
    if "VARG1" in st.session_state:
        data1 = st.session_state.VARG1
        print(data1)
        for element1 in data1:
            if element1[3] != ' ':
                graph_list.append(element1[0])
                name_list.append(element1[3])
    if "VARG2" in st.session_state:
        data2 = st.session_state.VARG2
        for element2 in data2:
            if element2[3] != '':
                graph_list.append(element2[0])
                name_list.append(element2[3])
    if "VARG3" not in st.session_state:
        st.session_state.VARG3 = []
    if graph_list != [] and name_list != []:
        st.header("Select an Airplane to Modify")
        final_name = st.selectbox("Select an Airplane from the List: ", name_list)
        if final_name != "":
            final_data = [graph_list[name_list.index(final_name)], final_name]
            st.header("Select Design Parameters to Modify")
            left1, right1 = st.columns(2)

            with left1:
                st.write("#### Technological Parameters")
                # prop_system_eff
                prop_sys_eff = st.text_input("Propulsion System Efficiency (default: 1.0)")
                if prop_sys_eff != "":
                    if is_float(float(prop_sys_eff)) == False:
                        st.warning("Please select a number for the propulsion system efficiency.")
                    else:
                        gam.prop_system_eff = float(prop_sys_eff)
                elif prop_sys_eff == "":
                    gam.prop_system_eff = 1
                # lod_factor
                lod = st.text_input("Lift-to-Drag Ratio Factor (default: 1.0)")
                if lod != "":
                    if is_float(float(lod)) == False:
                        st.warning("Please select a number for the LOD factor.")
                    else:
                        gam.lod_factor = float(lod)
                elif lod == "":
                    gam.lod_factor = 1
                # stdm_factor
                stdm = st.text_input("Structural Technology Development Multiplier (STDM) (default: 1.0)")
                if stdm != "":
                    if is_float(float(stdm)) == False:
                        st.warning("Please select a number for the STDM factor.")
                    else:
                        gam.stdm_factor = float(stdm)
                elif stdm == "":
                    gam.stdm_factor = 1

            with right1:
                st.write("#### Payload-Range Parameters")
                # mpax
                mpax = st.text_input("Mass per Passenger (PAX)")
                if mpax != "":
                    if is_float(float(mpax)) == False:
                        st.warning("Please select a number for the masse of one PAX.")
                    else:
                        for key in dis:
                            data = final_data[0]
                            if data["airplane_type"] == key:
                                gam.mpax_dict[key] = float(mpax)
                if mpax == "":
                    for key in dis:
                        data = final_data[0]
                        if data["airplane_type"] == key:
                            gam.mpax_dict[key] = dis[key]
                # max_payload_factor
                max_payload = st.text_input("Maximum Payload Factor (default: 1.15)")
                if max_payload != "":
                    if is_float(float(max_payload)) == False:
                        st.warning("Please select a number for the max payload factor.")
                    else:
                        gam.max_payload_factor = float(max_payload)
                elif max_payload == "":
                    gam.max_payload_factor = 1.15
                # max_fuel_factor
                mff = st.text_input("Maximum Fuel Factor (default: 1.25)")
                if mff != "":
                    if is_float(float(mff)) == False:
                        st.warning("Please select a number for the max fuel factor.")
                    else:
                        gam.max_fuel_factor = float(mff)
                elif mff == "":
                    gam.max_fuel_factor = 1.25

            ## Make the power system and the design mession for tweak
            st.header("Display Payload–Range of the Modified Airplane")
            fpower_system = {}
            fdesign_mission = {}
            for elements in final_data[0]:
                if elements == "power_system":
                    fpower_system = final_data[0]["power_system"]
                if elements == "mission":
                    fdesign_mission = final_data[0]["mission"]
                if elements == "mtow":
                    fdesign_mission["mtow"] = final_data[0]["mtow"]
                if elements == "owe":
                    fdesign_mission["owe"] = final_data[0]["owe"]
            for key in dis:
                if final_data[0]["airplane_type"] == key:
                    if fdesign_mission["npax"] != "":
                        payload = fdesign_mission["npax"]*gam.mpax_dict[key]
                        fdesign_mission["payload"] = payload
            if fdesign_mission["payload"] != "":
                max_payload = fdesign_mission["payload"]*gam.max_payload_factor
                fdesign_mission["payload_max"] = float(max_payload)



            # Run the GAM with the design_airplane
            if fpower_system != {} and fdesign_mission != {}:
                tweak_dict = gam.tune_design(fpower_system, fdesign_mission)
                table_rows = []

                st.write("Select Airplane Properties to Display:")

                Name = st.checkbox("Airplane Name")
                if Name:
                    table_rows.append({
                            "Property" : "Name",
                            "Value" : "Generic Airplane"
                        })
                propulsion = st.checkbox("Propulsion System Definition")
                if propulsion:
                    table_rows.append({
                        "Property": "Engine Type",
                        "Value": tweak_dict["power_system"]["engine_type"]
                    })
                    table_rows.append({
                        "Property": "Energy Type",
                        "Value": tweak_dict["power_system"]["energy_type"]
                    })
                    table_rows.append({
                        "Property": "Thruster Type",
                        "Value": tweak_dict["power_system"]["thruster_type"]
                    })
                    table_rows.append({
                        "Property" : "Number of Engines",
                        "Value" : "%.0f" % tweak_dict["n_engine"]
                    })
                    table_rows.append({
                        "Property": "Engine Bypass Ratio (BPR)",
                        "Value": tweak_dict["by_pass_ratio"]
                    })
                mission = st.checkbox("Design Mission Definition")
                if mission:
                    table_rows.append({
                        "Property" : "Mission Category",
                        "Value" : tweak_dict["airplane_type"]
                    })
                    table_rows.append({
                        "Property" : "Number of Passengers",
                        "Value" : "%.0f" % tweak_dict["npax"]
                    })
                    table_rows.append({
                        "Property" : "Design Range",
                        "Value" : "%.0f km" % unit.convert_to("km", tweak_dict["nominal_range"])
                    })
                    if tweak_dict["cruise_speed"] > 1:
                        table_rows.append({
                            "Property" : " Cruise Speed ",
                            "Value" : "%.1f km/h" % unit.convert_to("km/h", tweak_dict["cruise_speed"]) 
                        })
                    if tweak_dict["cruise_speed"] <= 1:
                        table_rows.append({
                            "Property" : " Cruise Mach ",
                            "Value" : "%.2f" % tweak_dict["cruise_speed"]
                        })
                    table_rows.append({
                        "Property" : " Cruise Altitude ",
                        "Value" : "%.1f ft" % unit.convert_to("ft", tweak_dict["altitude_data"]["mission"]),
                    })
                breakdown = st.checkbox("Mass Breakdown")
                if breakdown:
                    table_rows.append({
                        "Property": "MTOM",
                        "Value": "%.0f kg" % tweak_dict["mtow"]
                    })
                    table_rows.append({
                        "Property": "MZFM",
                        "Value": "%.0f kg" % tweak_dict["mzfw"]
                    })
                    table_rows.append({
                        "Property": "Max Payload",
                        "Value": "%.0f kg" % tweak_dict["payload_max"]
                    })
                    table_rows.append({
                        "Property": "Max Payload Factor",
                        "Value": "%.3f" % tweak_dict["max_payload_factor"]
                    })
                    table_rows.append({
                        "Property": "OEM",
                        "Value": "%.0f kg" % tweak_dict["owe"]
                    })
                    table_rows.append({
                        "Property": "Operator Items",
                        "Value": "%.0f kg" % tweak_dict["op_item"]
                    })
                    table_rows.append({
                        "Property": "MEM",
                        "Value": "%.0f kg" % tweak_dict["mwe"]
                    })
                    table_rows.append({
                        "Property": "Furnishing",
                        "Value": "%.0f kg" % tweak_dict["furnishing"]
                    })
                    table_rows.append({
                        "Property": "Standard MEM",
                        "Value": "%.0f kg" % tweak_dict["std_mwe"]
                    })
                    table_rows.append({
                        "Property": "Propulsion Mass",
                        "Value": "%.0f kg" % tweak_dict["propulsion_mass"]
                    })
                    table_rows.append({
                        "Property": "Energy Storage Mass",
                        "Value": "%.0f kg" % tweak_dict["energy_storage_mass"]
                    })
                    table_rows.append({
                        "Property": "Fuel Cell System Mass",
                        "Value": "%.0f kg" % tweak_dict["fuel_cell_system_mass"]
                    })
                    table_rows.append({
                        "Property": "Basic MEM",
                        "Value": "%.0f kg" % tweak_dict["basic_mwe"]
                    })
                    table_rows.append({
                        "Property": "MEM Shift",
                        "Value": "%.0f kg" % tweak_dict["stdm_shift"]
                    })
                output = st.checkbox("Design Mission Results")
                if output:
                    table_rows.append({
                        "Property": "Nominal Passenger Mass Allowance",
                        "Value": "%.1f kg" % tweak_dict["mpax"]
                    })
                    table_rows.append({
                        "Property": "Nominal Payload Delta",
                        "Value": "%.0f kg" % tweak_dict["delta_payload"]
                    })
                    table_rows.append({
                        "Property": "Nominal Payload",
                        "Value": "%.0f kg" % tweak_dict["payload"]
                    })
                    table_rows.append({
                        "Property": "Nominal Mission Time",
                        "Value": "%.1f h" % unit.h_s(tweak_dict["nominal_time"])
                    })

                    table_rows.append({
                        "Property": "Mission Fuel",
                        "Value": "%.0f kg" % tweak_dict["mission_fuel"]
                    })
                    table_rows.append({
                        "Property": "Reserve Fuel",
                        "Value": "%.0f kg" % tweak_dict["reserve_fuel"]
                    })
                    table_rows.append({
                        "Property": "Total Fuel",
                        "Value": "%.0f kg" % tweak_dict["total_fuel"]
                    })
                    table_rows.append({
                        "Property": "Fuel Consumption",
                        "Value": "%.2f L/pax/100km" % unit.convert_to("L", tweak_dict["fuel_consumption"] * unit.m_km(100))
                    })
                    table_rows.append({
                        "Property": "Mission Energy",
                        "Value": "%.0f kWh" % unit.kWh_J(tweak_dict["mission_enrg"])
                    })
                    table_rows.append({
                        "Property": "Reserve Energy",
                        "Value": "%.0f kWh" % unit.kWh_J(tweak_dict["reserve_enrg"])
                    })
                    table_rows.append({
                        "Property": "Total Energy",
                        "Value": "%.0f kWh" % unit.kWh_J(tweak_dict["total_energy"])
                    })
                    table_rows.append({
                        "Property": "Energy Consumption",
                        "Value": "%.2f kWh/pax/100km" % unit.kWh_J(tweak_dict["enrg_consumption"] * unit.m_km(100))
                    })
                    table_rows.append({
                        "Property": "Wake Turbulence Category",
                        "Value": tweak_dict["wake_turbulence_class"]
                    })
                factor = st.checkbox("Performance Factors & Efficiencies")
                if factor:
                    table_rows.append({
                        "Property": "Max Power",
                        "Value": "%.0f kW" % unit.kW_W(tweak_dict["max_power"])
                    })
                    table_rows.append({
                        "Property": "Standard Mass Factor",
                        "Value": "%.4f" % tweak_dict["stdm_factor"]
                    })
                    table_rows.append({
                        "Property": "Aerodynamic Efficiency Factor",
                        "Value": "%.4f" % tweak_dict["aero_eff_factor"]
                    })
                    table_rows.append({
                        "Property": "Aerodynamic Efficiency (L/D)",
                        "Value": "%.2f" % tweak_dict["aerodynamic_efficiency"]
                    })
                    table_rows.append({
                        "Property": "Propulsion System Efficiency",
                        "Value": "%.3f" % tweak_dict["propulsion_system_efficiency"]
                    })
                    table_rows.append({
                        "Property": "Storage Energy Density",
                        "Value": "%.0f Wh/kg" % unit.Wh_J(tweak_dict["storage_energy_density"])
                    })
                    table_rows.append({
                        "Property": "Propulsion Power Density",
                        "Value": "%.2f kW/kg" % unit.kW_W(tweak_dict["propulsion_power_density"])
                    })
                    table_rows.append({
                        "Property": "Structural Factor (OEM/MTOM)",
                        "Value": "%.2f" % tweak_dict["structural_factor"]
                    })
                    table_rows.append({
                        "Property": "Energy Efficiency Factor (P.K/E)",
                        "Value": "%.2f pax.km/kWh" % unit.convert_to("km/kWh", tweak_dict["pk_o_enrg"])
                    })
                    table_rows.append({
                        "Property": "Mass Efficiency Factor (P.K/M)",
                        "Value": "%.2f pax.km/kg" % unit.convert_to("km/kg", tweak_dict["pk_o_mass"])
                    })
                    st.write("")
                    table = pd.DataFrame(table_rows)
                    st.dataframe(table, width=600, column_config={"Property": {"width": 300}, "Value": {"width": 300},}, hide_index=True)

            else:
                st.warning("The program cannot compute the data with the current input parameters.")

            st.write("")
            st.write("Compute and Display the Payload-Range Diagram")
            if tweak_dict != {}:
                two_dict2 = gam.build_payload_range(tweak_dict)    # Compute payload-range data and add them in ac_dict
                left_column4 , right_column4 = st.columns(2)

                if 'payload_info' not in st.session_state:
                    st.session_state.payload_info = False

                with left_column4:
                    if st.button("Show payload-range information"):
                        st.session_state.payload_info = True
                with right_column4:
                    if st.button("Hide payload-range information"):
                        st.session_state.payload_info = False

                if st.session_state.payload_info :
                    gam.print_payload_range(tweak_dict)    # Print payload-range data
                    tup = (tweak_dict, two_dict2, table, '')
                    st.session_state.VARG3.append(tup)
                    config_list = []
                    name_list = []
                    if st.session_state.VARG3:
                        print("Configurations found:")
                        config_list.append(st.session_state.VARG3[0][0])
                        name_list.append(st.session_state.VARG3[0][3])
                        gam.payload_range_graph(config_list, name_list)   # Plot payload-range diagram
                else:
                    st.info("No configurations to display.")

                st.write("")
                st.write("Save Airplane Configuration")
                left_column3, right_column3 = st.columns(2)

                with left_column3:
                    name = st.text_input("Specify Airplane Name")

                    duplicate_name = any(ele[3] == name and ele[3] != "" for ele in st.session_state.VARG3)
                    if duplicate_name:
                        st.warning("Please select a new name for this AC.")
                    else:
                        if st.button("Save Airplane", key="save_new_ac"):
                            if name:
                                tup = (tweak_dict, two_dict2, table, name)
                                st.session_state.VARG3.append(tup)
                                st.success(f"{name} saved!")
                            else:
                                tup = (tweak_dict, two_dict2, table, f"AC {len(st.session_state.VARG3)}")
                                st.session_state.VARG3.append(tup)
                                st.success(f"AC {len(st.session_state.VARG3)} saved!")


            else:
                st.warning("The data can't be computed.")



def main_tweak():
    '''Main, display the dashboard'''
    st.set_page_config(
        page_title="Dashboard for Airplane Fuel Consumption",
        page_icon=":airplane:",
        layout="centered",
    )
    # App title
    st.title("Designed Airplane Tuning Tool")
    st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-family: Courier New; color: green;'>Refine and adjust airplane configurations previously designed with this tool.</h5>", unsafe_allow_html=True)

    tweak_graphic()




# Run the application
if __name__ == "__main__":
    main_tweak()
