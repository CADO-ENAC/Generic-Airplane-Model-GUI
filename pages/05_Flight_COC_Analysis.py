import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

#from gam_utils.physical_data import PhysicalData
#from gam_utils import unit
#from gam_copy import GAM

from draw_domains import find_index #, draw_domains
from doc_vs_techno_commuter_modify import init_commuter
from doc_vs_techno_regional_modify import init_regional
from doc_vs_techno_long_range_modify import init_long
from doc_vs_techno_short_medium_modify import init_short


def pritting_fuel():
    max_fuel_factor = 1.25
    stdm_factor = 1.0
    lod_factor = 1.0

    def plot_domain(ax, init_function, title):
        gam, design_mission, power_system, dist_window, npax_window, criterion = init_function(
            max_fuel_factor, stdm_factor, lod_factor,
            battery_density, fuel_cell_power_density, lh2_tank_index,
            emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
            battery_price, lh2_price, lch4_price, e_fuel_price
        )
        color_ind, npax_list, dist_list = find_index(
            gam, design_mission, power_system, dist_window, npax_window, criterion
        )

        ax.imshow(color_ind, cmap=cmapa, vmin=0, vmax=len(labels) - 1)
        ax.set_xticks(
            np.linspace(0, len(color_ind), 6).astype(int)
        )
        ax.set_xticklabels(
            np.linspace(dist_list[0], dist_list[-1], num=6).astype(int)
        )
        ax.set_yticks(
            np.linspace(0, len(color_ind[0]), 7).astype(int)
        )
        ax.set_yticklabels(
            np.linspace(npax_list[0], npax_list[-1], num=7).astype(int)[::-1]
        )
        ax.set_title(title, fontsize=12)
        return criterion


    st.sidebar.write("### Select the Aircraft Category to Display:")
    airplane_type = st.sidebar.radio("", ["Commuter", "Regional", "Short/Medium Range", "Long Range", "All Categories Combined"])


    if airplane_type == "Commuter":
        st.header("Aircraft Category: Commuter")
        left1, right1 = st.columns(2)

        with left1:
            # st.header("Parameters for commuter airplane")

            left11, right11 = st.columns(2)

            with left11:
                # Sliders for Techno Parameters
                battery_density1 = st.slider("Battery Energy Density (Wh/kg)", 500, 1000, 750, 5)
                
            with right11:
                # Text input for Techno Parameters
                battery_density = float(st.text_input("Battery Energy Density (Wh/kg)", battery_density1))
            
            left12, right12 = st.columns(2)
            with left12:
                fuel_cell_power1_density = st.slider("Fuel Cell Power Density (W/kg)", 0.1, 3.0, 1.0, 0.1)
            with right12:
                fuel_cell_power_density = float(st.text_input("Fuel Cell Power Density (W/kg)", fuel_cell_power1_density))
            
            left13, right13 = st.columns(2)
            with left13:
                lh2_tank_index1 = st.slider("LH2 Tank Gravimetric Index", 0.1, 1.0, 0.4, 0.05)
            with right13:
                lh2_tank_index = float(st.text_input("LH2 Tank Gravimetric Index", lh2_tank_index1))
                
            left14, right14 = st.columns(2)
            with left14: 
                # Sliders for Techno Cost Parameters
                emotor_price1 = st.slider("eMotor Price (/kW)", 50, 200, 104, 2)
            with right14:
                emotor_price = float(st.text_input("eMotor Price (/kW)", emotor_price1))
                
            left15, right15 = st.columns(2)
            with left15: 
                fuel_cell_price1 = st.slider("Fuel Cell Price (/kW)", 20, 100, 44, 2)
            with right15:
                fuel_cell_price = float(st.text_input("Fuel Cell Price (/kW)", fuel_cell_price1))
                
                
            left16, right16 = st.columns(2)
            with left16: 
                lh2_tank_price1 = st.slider("LH2 Tank Price (/kg)", 100, 500, 270, 2)
            with right16:
                lh2_tank_price = float(st.text_input("LH2 Tank Price (/kg)", lh2_tank_price1))
                
                
            left17, right17 = st.columns(2)
            with left17: 
                battery_capacity_price1 = st.slider("Battery Capacity Price (/Wh)", 100, 500, 330, 2)
            with right17:
                battery_capacity_price = float(st.text_input("Battery Capacity Price (/Wh)", battery_capacity_price1))
                
                
            left18, right18 = st.columns(2)
            with left18: 
                # Sliders for Energy Cost Parameters
                battery_price1 = st.slider("Battery Energy Price (/MWh)", 50, 200, 110, 2)
            with right18:
                battery_price = float(st.text_input("Battery Energy Price (/MWh)", battery_price1))
                
            left19, right19 = st.columns(2)
            with left19: 
                lh2_price1 = st.slider("LH2 Energy Price (/MWh)", 50, 200, 140, 2)
            with right19:
                lh2_price = float(st.text_input("LH2 Energy Price (/MWh)", lh2_price1))

            left110, right110 = st.columns(2)
            with left110: 
                lch4_price1 = st.slider("LCH4 Energy Price (/MWh)", 50, 200, 120, 2)
            with right110:
                lch4_price = float(st.text_input("LCH4 Energy Price (/MWh)", lch4_price1))


            left111, right111 = st.columns(2)
            with left111: 
                e_fuel_price1 = st.slider("eFuel Energy Price (/MWh)", 50, 200, 125, 2)
            with right111:
                e_fuel_price = float(st.text_input("eFuel Energy Price (/MWh)", e_fuel_price1))

        with right1:
            # st.header("Domain Visualization")
            figa, ax = plt.subplots(1, 1, figsize=(8, 8))

            colors = ["green", "cyan", "blue", "orange", "brown"]
            cmapa = LinearSegmentedColormap.from_list("mycmap", colors)


            gam, design_mission, power_system, dist_window, npax_window, criterionCum = init_commuter(
                max_fuel_factor, stdm_factor, lod_factor,
                    battery_density, fuel_cell_power_density, lh2_tank_index,
                    emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
                    battery_price, lh2_price, lch4_price, e_fuel_price
            )
            labels = [
                power_system[key]["engine_type"] + " " + power_system[key]["energy_type"]
                for key in power_system.keys()
            ]
            labels[1] += "+fc"

            # plot_domain(ax, init_commuter, "Commuter")
            plot_domain(ax, init_commuter, " ")

            # Colors
            pcolors = cmapa(np.linspace(0.0, 1.0, len(labels)))
            labels = [label.replace("turboprop", "turboprop/fan") for label in labels]
            patches = [
                mpatches.Patch(color=pcolor, label=label) for pcolor, label in zip(pcolors, labels)
            ]

            figa.supxlabel("Range (km)", fontsize=14, y=0.09)
            figa.supylabel("Capacity (seat)", fontsize=14, x=0.04)
            # plt.suptitle("Best domains for: " + criterionCum, fontsize=14)
            plt.figlegend(
                handles=patches, loc=8, bbox_to_anchor=(0.5, 0.01), borderaxespad=0.0, ncol=3
            )
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)

            # Plot of the graphics
            st.pyplot(figa)


    if airplane_type == "Regional":
        st.header("Aircraft Category: Regional")
        left2, right2 = st.columns(2)

        with left2:
            # st.header("Parameters for commuter airplane")

            left21, right21 = st.columns(2)
            with left21:
                battery_density1 = st.slider("Battery Energy Density (Wh/kg)", 500, 1000, 750, 5)
            with right21:
                battery_density = float(st.text_input("Battery Energy Density (Wh/kg)", battery_density1))

            left22, right22 = st.columns(2)
            with left22:
                fuel_cell_power1_density = st.slider("Fuel Cell Power Density (W/kg)", 0.1, 3.0, 2.0, 0.1)
            with right22:
                fuel_cell_power_density = float(st.text_input("Fuel Cell Power Density (W/kg)", fuel_cell_power1_density))
            
            left23, right23 = st.columns(2)
            with left23:
                lh2_tank_index1 = st.slider("LH2 Tank Gravimetric Index", 0.1, 1.0, 0.45, 0.05)
            with right23:
                lh2_tank_index = float(st.text_input("LH2 Tank Gravimetric Index", lh2_tank_index1))
                
            left24, right24 = st.columns(2)
            with left24:
                emotor_price1 = st.slider("eMotor Price (/kW)", 50, 200, 104, 2)
            with right24:
                emotor_price = float(st.text_input("eMotor Price (/kW)", emotor_price1))
                
                
            left25, right25 = st.columns(2)
            with left25: 
                fuel_cell_price1 = st.slider("Fuel Cell Price (/kW)", 20, 100, 44, 2)
            with right25:
                fuel_cell_price = float(st.text_input("Fuel Cell Price (/kW)", fuel_cell_price1))
                
                
                
            left26, right26 = st.columns(2)
            with left26: 
                lh2_tank_price1 = st.slider("LH2 Tank Price (/kg)", 100, 500, 270, 2)
            with right26:
                lh2_tank_price = float(st.text_input("LH2 Tank Price (/kg)", lh2_tank_price1))
                
                
                
            left27, right27 = st.columns(2)
            with left27: 
                battery_capacity_price1 = st.slider("Battery Capacity Price (/Wh)", 100, 500, 330, 2)
            with right27:
                battery_capacity_price = float(st.text_input("Battery Capacity Price (/Wh)", battery_capacity_price1))
                
                
                
            left28, right28 = st.columns(2)
            with left28: 
                battery_price1 = st.slider("Battery Energy Price (/MWh)", 50, 200, 110, 2)
            with right28:
                battery_price = float(st.text_input("Battery Energy Price (/MWh)", battery_price1))
                
                
            left29, right29 = st.columns(2)
            with left29: 
                lh2_price1 = st.slider("LH2 Energy Price (/MWh)", 50, 200, 140, 2)
            with right29:
                lh2_price = float(st.text_input("LH2 Energy Price (/MWh)", lh2_price1))
                

            left210, right210 = st.columns(2)
            with left210: 
                lch4_price1 = st.slider("LCH4 Energy Price (/MWh)", 50, 200, 120, 2)
            with right210:
                lch4_price = float(st.text_input("LCH4 Energy Price (/MWh)", lch4_price1))
                


            left211, right211 = st.columns(2)
            with left211: 
                e_fuel_price1 = st.slider("eFuel Energy Price (/MWh)", 50, 200, 135, 2)
            with right211:
                e_fuel_price = float(st.text_input("eFuel Energy Price (/MWh)", e_fuel_price1))

        with right2:
            # st.header("Domain Visualization")
            figa, ax = plt.subplots(1, 1, figsize=(8, 8))

            colors = ["green", "cyan", "blue", "orange", "brown"]
            cmapa = LinearSegmentedColormap.from_list("mycmap", colors)

            gam, design_mission, power_system, dist_window, npax_window, criterionCum = init_commuter(
                max_fuel_factor, stdm_factor, lod_factor,
                    battery_density, fuel_cell_power_density, lh2_tank_index,
                    emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
                    battery_price, lh2_price, lch4_price, e_fuel_price
            )
            labels = [
                power_system[key]["engine_type"] + " " + power_system[key]["energy_type"]
                for key in power_system.keys()
            ]
            labels[1] += "+fc"

            # plot_domain(ax, init_regional, "Regional")
            plot_domain(ax, init_regional, " ")

            # Colors
            pcolors = cmapa(np.linspace(0.0, 1.0, len(labels)))
            labels = [label.replace("turboprop", "turboprop/fan") for label in labels]
            patches = [
                mpatches.Patch(color=pcolor, label=label) for pcolor, label in zip(pcolors, labels)
            ]

            figa.supxlabel("Range (km)", fontsize=14, y=0.09)
            figa.supylabel("Capacity (seat)", fontsize=14, x=0.04)
            # plt.suptitle("Best domains for: " + criterionCum, fontsize=14)
            plt.figlegend(
                handles=patches, loc=8, bbox_to_anchor=(0.5, 0.01), borderaxespad=0.0, ncol=3
            )
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)

            # Plot of the graphics
            st.pyplot(figa)


    if airplane_type == "Short/Medium Range":
        st.header("Aircraft Category: Short/Medium Range")
        left3, right3 = st.columns(2)

        with left3:
            # st.header("Parameters for commuter airplane")
            
            left31, right31 = st.columns(2)
            with left31:
                battery_density1 = st.slider("Battery Energy Density (Wh/kg)", 500, 1000, 750, 5)
            with right31:
                battery_density = float(st.text_input("Battery Energy Density (Wh/kg)", battery_density1))

            left32, right32 = st.columns(2)
            with left32:
                fuel_cell_power1_density = st.slider("Fuel Cell Power Density (W/kg)", 0.1, 3.0, 2.0, 0.1)
            with right32:
                fuel_cell_power_density = float(st.text_input("Fuel Cell Power Density (W/kg)", fuel_cell_power1_density))
            
            left33, right33 = st.columns(2)
            with left33:
                lh2_tank_index1 = st.slider("LH2 Tank Gravimetric Index", 0.1, 1.0, 0.76, 0.05)
            with right33:
                lh2_tank_index = float(st.text_input("LH2 Tank Gravimetric Index", lh2_tank_index1))
                
            left34, right34 = st.columns(2)
            with left34:
                emotor_price1 = st.slider("eMotor Price (/kW)", 50, 200, 104, 2)
            with right34:
                emotor_price = float(st.text_input("eMotor Price (/kW)", emotor_price1))
                
            left35, right35 = st.columns(2)
            with left35: 
                fuel_cell_price1 = st.slider("Fuel Cell Price (/kW)", 20, 100, 44, 2)
            with right35:
                fuel_cell_price = float(st.text_input("Fuel Cell Price (/kW)", fuel_cell_price1))

                
            left36, right36 = st.columns(2)
            with left36: 
                lh2_tank_price1 = st.slider("LH2 Tank Price (/kg)", 100, 500, 270, 2)
            with right36:
                lh2_tank_price = float(st.text_input("LH2 Tank Price (/kg)", lh2_tank_price1))
                

            left37, right37 = st.columns(2)
            with left37: 
                battery_capacity_price1 = st.slider("Battery Capacity Price (/Wh)", 100, 500, 330, 2)
            with right37:
                battery_capacity_price = float(st.text_input("Battery Capacity Price (/Wh)", battery_capacity_price1))
                

            left38, right38 = st.columns(2)
            with left38: 
                battery_price1 = st.slider("Battery Energy Price (/MWh)", 50, 200, 110, 2)
            with right38:
                battery_price = float(st.text_input("Battery Energy Price (/MWh)", battery_price1))
                
            left39, right39 = st.columns(2)
            with left39: 
                lh2_price1 = st.slider("LH2 Energy Price (/MWh)", 50, 200, 140, 2)
            with right39:
                lh2_price = float(st.text_input("LH2 Energy Price (/MWh)", lh2_price1))
                
            left310, right310 = st.columns(2)
            with left310: 
                lch4_price1 = st.slider("LCH4 Energy Price (/MWh)", 50, 200, 120, 2)
            with right310:
                lch4_price = float(st.text_input("LCH4 Energy Price (/MWh)", lch4_price1))
    
            left311, right311 = st.columns(2)
            with left311: 
                e_fuel_price1 = st.slider("eFuel Energy Price (/MWh)", 50, 200, 145, 2)
            with right311:
                e_fuel_price = float(st.text_input("eFuel Energy Price (/MWh)", e_fuel_price1))
            


        with right3:
            # st.header("Domain Visualization")
            figa, ax = plt.subplots(1, 1, figsize=(8, 8))

            colors = ["green", "cyan", "blue", "orange", "brown"]
            cmapa = LinearSegmentedColormap.from_list("mycmap", colors)

            gam, design_mission, power_system, dist_window, npax_window, criterionCum = init_commuter(
                max_fuel_factor, stdm_factor, lod_factor,
                    battery_density, fuel_cell_power_density, lh2_tank_index,
                    emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
                    battery_price, lh2_price, lch4_price, e_fuel_price
            )
            labels = [
                power_system[key]["engine_type"] + " " + power_system[key]["energy_type"]
                for key in power_system.keys()
            ]
            labels[1] += "+fc"

            # plot_domain(ax, init_short, "Short-medium")
            plot_domain(ax, init_short, " ")

            # Colors
            pcolors = cmapa(np.linspace(0.0, 1.0, len(labels)))
            labels = [label.replace("turboprop", "turboprop/fan") for label in labels]
            patches = [
                mpatches.Patch(color=pcolor, label=label) for pcolor, label in zip(pcolors, labels)
            ]

            figa.supxlabel("Range (km)", fontsize=14, y=0.09)
            figa.supylabel("Capacity (seat)", fontsize=14, x=0.04)
            # plt.suptitle("Best domains for: " + criterionCum, fontsize=14)
            plt.figlegend(
                handles=patches, loc=8, bbox_to_anchor=(0.5, 0.01), borderaxespad=0.0, ncol=3
            )
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)

            # Plot of the graphics
            st.pyplot(figa)


    if airplane_type == "Long Range":
        st.header("Aircraft Category: Long Range")
        left4, right4= st.columns(2)

        with left4:
            # st.header("Parameters for commuter airplane")
            
            left41, right41 = st.columns(2)
            with left41:
                battery_density1 = st.slider("Battery Energy Density (Wh/kg)", 500, 1000, 750, 5)
            with right41:
                battery_density = float(st.text_input("Battery Energy Density (Wh/kg)", battery_density1))

            left42, right42 = st.columns(2)
            with left42:
                fuel_cell_power1_density = st.slider("Fuel Cell Power Density (W/kg)", 0.1, 3.0, 2.0, 0.1)
            with right42:
                fuel_cell_power_density = float(st.text_input("Fuel Cell Power Density (W/kg)", fuel_cell_power1_density))
            
            left43, right43 = st.columns(2)
            with left43:
                lh2_tank_index1 = st.slider("LH2 Tank Gravimetric Index", 0.1, 1.0, 0.73, 0.05)
            with right43:
                lh2_tank_index = float(st.text_input("LH2 Tank Gravimetric Index", lh2_tank_index1))
                
            left44, right44 = st.columns(2)
            with left44:
                emotor_price1 = st.slider("eMotor Price (/kW)", 50, 200, 104, 2)
            with right44:
                emotor_price = float(st.text_input("eMotor Price (/kW)", emotor_price1))
                
            left45, right45 = st.columns(2)
            with left45: 
                fuel_cell_price1 = st.slider("Fuel Cell Price (/kW)", 20, 100, 44, 2)
            with right45:
                fuel_cell_price = float(st.text_input("Fuel Cell Price (/kW)", fuel_cell_price1))

                
            left46, right46 = st.columns(2)
            with left46: 
                lh2_tank_price1 = st.slider("LH2 Tank Price (/kg)", 100, 500, 270, 2)
            with right46:
                lh2_tank_price = float(st.text_input("LH2 Tank Price (/kg)", lh2_tank_price1))
                

            left47, right47 = st.columns(2)
            with left47: 
                battery_capacity_price1 = st.slider("Battery Capacity Price (/Wh)", 100, 500, 330, 2)
            with right47:
                battery_capacity_price = float(st.text_input("Battery Capacity Price (/Wh)", battery_capacity_price1))
                

            left48, right48 = st.columns(2)
            with left48: 
                battery_price1 = st.slider("Battery Energy Price (/MWh)", 50, 200, 110, 2)
            with right48:
                battery_price = float(st.text_input("Battery Energy Price (/MWh)", battery_price1))
                
            left49, right49 = st.columns(2)
            with left49: 
                lh2_price1 = st.slider("LH2 Energy Price (/MWh)", 50, 200, 140, 2)
            with right49:
                lh2_price = float(st.text_input("LH2 Energy Price (/MWh)", lh2_price1))
                
            left410, right410 = st.columns(2)
            with left410: 
                lch4_price1 = st.slider("LCH4 Energy Price (/MWh)", 50, 200, 120, 2)
            with right410:
                lch4_price = float(st.text_input("LCH4 Energy Price (/MWh)", lch4_price1))
    
            left411, right411 = st.columns(2)
            with left411: 
                e_fuel_price1 = st.slider("eFuel Energy Price (/MWh)", 50, 200, 155, 2)
            with right411:
                e_fuel_price = float(st.text_input("eFuel Energy Price (/MWh)", e_fuel_price1))
            

        with right4:
            # st.header("Domain Visualization")
            figa, ax = plt.subplots(1, 1, figsize=(8, 8))

            colors = ["green", "cyan", "blue", "orange", "brown"]
            cmapa = LinearSegmentedColormap.from_list("mycmap", colors)

            gam, design_mission, power_system, dist_window, npax_window, criterionCum = init_commuter(
                max_fuel_factor, stdm_factor, lod_factor,
                    battery_density, fuel_cell_power_density, lh2_tank_index,
                    emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
                    battery_price, lh2_price, lch4_price, e_fuel_price
            )
            labels = [
                power_system[key]["engine_type"] + " " + power_system[key]["energy_type"]
                for key in power_system.keys()
            ]
            labels[1] += "+fc"

            # plot_domain(ax, init_long, "Long range")
            plot_domain(ax, init_long, " ")

            # Colors
            pcolors = cmapa(np.linspace(0.0, 1.0, len(labels)))
            labels = [label.replace("turboprop", "turboprop/fan") for label in labels]
            patches = [
                mpatches.Patch(color=pcolor, label=label) for pcolor, label in zip(pcolors, labels)
            ]

            figa.supxlabel("Range (km)", fontsize=14, y=0.09)
            figa.supylabel("Capacity (seat)", fontsize=14, x=0.04)
            # plt.suptitle("Best domains for: " + criterionCum, fontsize=14)
            plt.figlegend(
                handles=patches, loc=8, bbox_to_anchor=(0.5, 0.01), borderaxespad=0.0, ncol=3
            )
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)

            # Plot of the graphics
            st.pyplot(figa)


    if airplane_type == "All Categories Combined":
        st.header("Aircraft Category: All Categories Combined")
        aleft1, aright1 = st.columns(2)

        with aleft1:
            # st.header("Parameters for all type of airplane")
            
            
            left51, right51 = st.columns(2)
            with left51:
                battery_density1 = st.slider("Battery Energy Density (Wh/kg)", 500, 1000, 750, 5)
            with right51:
                battery_density = float(st.text_input("Battery Energy Density (Wh/kg)", battery_density1))

            left52, right52 = st.columns(2)
            with left52:
                fuel_cell_power1_density = st.slider("Fuel Cell Power Density (W/kg)", 0.1, 3.0, 2.0, 0.1)
            with right52:
                fuel_cell_power_density = float(st.text_input("Fuel Cell Power Density (W/kg)", fuel_cell_power1_density))
            
            left53, right53 = st.columns(2)
            with left53:
                lh2_tank_index1 = st.slider("LH2 Tank Gravimetric Index", 0.1, 1.0, 0.6, 0.05)
            with right53:
                lh2_tank_index = float(st.text_input("LH2 Tank Gravimetric Index", lh2_tank_index1))
                
            left54, right54 = st.columns(2)
            with left54:
                emotor_price1 = st.slider("eMotor Price (/kW)", 50, 200, 104, 2)
            with right54:
                emotor_price = float(st.text_input("eMotor Price (/kW)", emotor_price1))
                
            left55, right55 = st.columns(2)
            with left55: 
                fuel_cell_price1 = st.slider("Fuel Cell Price (/kW)", 20, 100, 44, 2)
            with right55:
                fuel_cell_price = float(st.text_input("Fuel Cell Price (/kW)", fuel_cell_price1))

                
            left56, right56 = st.columns(2)
            with left56: 
                lh2_tank_price1 = st.slider("LH2 Tank Price (/kg)", 100, 500, 270, 2)
            with right56:
                lh2_tank_price = float(st.text_input("LH2 Tank Price (/kg)", lh2_tank_price1))
                

            left57, right57 = st.columns(2)
            with left57: 
                battery_capacity_price1 = st.slider("Battery Capacity Price (/Wh)", 100, 500, 330, 2)
            with right57:
                battery_capacity_price = float(st.text_input("Battery Capacity Price (/Wh)", battery_capacity_price1))
                

            left58, right58 = st.columns(2)
            with left58: 
                battery_price1 = st.slider("Battery Energy Price (/MWh)", 50, 200, 110, 2)
            with right58:
                battery_price = float(st.text_input("Battery Energy Price (/MWh)", battery_price1))
                
            left59, right59 = st.columns(2)
            with left59: 
                lh2_price1 = st.slider("LH2 Energy Price (/MWh)", 50, 200, 140, 2)
            with right59:
                lh2_price = float(st.text_input("LH2 Energy Price (/MWh)", lh2_price1))
                
            left510, right510 = st.columns(2)
            with left510: 
                lch4_price1 = st.slider("LCH4 Energy Price (/MWh)", 50, 200, 120, 2)
            with right510:
                lch4_price = float(st.text_input("LCH4 Energy Price (/MWh)", lch4_price1))
    
            left511, right511 = st.columns(2)
            with left511: 
                e_fuel_price1 = st.slider("eFuel Energy Price (/MWh)", 50, 200, 125, 2)
            with right511:
                e_fuel_price = float(st.text_input("eFuel Energy Price (/MWh)", e_fuel_price1))
            

        with aright1:
            # st.header("Domain Visualization")
            figa, ax = plt.subplots(2, 2, figsize=(8, 8))

            colors = ["green", "cyan", "blue", "orange", "brown"]
            cmapa = LinearSegmentedColormap.from_list("mycmap", colors)

            gam, design_mission, power_system, dist_window, npax_window, criterionCum = init_commuter(
                max_fuel_factor, stdm_factor, lod_factor,
                    battery_density, fuel_cell_power_density, lh2_tank_index,
                    emotor_price, fuel_cell_price, lh2_tank_price, battery_capacity_price,
                    battery_price, lh2_price, lch4_price, e_fuel_price
            )
            labels = [
                power_system[key]["engine_type"] + " " + power_system[key]["energy_type"]
                for key in power_system.keys()
            ]
            labels[1] += "+fc"

            titles = ["Commuter", "Regional", "Short/Medium Range", "Long Range"]
            init_functions = [init_commuter, init_regional, init_short, init_long]
            criteria = []

            for i, (init_func, title) in enumerate(zip(init_functions, titles)):
                criteria.append(plot_domain(ax[i // 2, i % 2], init_func, title))

            # Colors
            pcolors = cmapa(np.linspace(0.0, 1.0, len(labels)))
            labels = [label.replace("turboprop", "turboprop/fan") for label in labels]
            patches = [
                mpatches.Patch(color=pcolor, label=label) for pcolor, label in zip(pcolors, labels)
            ]

            figa.supxlabel("Range (km)", fontsize=14, y=0.09)
            figa.supylabel("Capacity (seat)", fontsize=14, x=0.04)
            # plt.suptitle("Best domains for: " + criteria[-1], fontsize=14)
            plt.figlegend(
                handles=patches, loc=8, bbox_to_anchor=(0.5, 0.01), borderaxespad=0.0, ncol=3
            )
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)

            # Plot of the graphics
            st.pyplot(figa)



def main_graph():
    '''Main, display the dashboard'''
    st.set_page_config(
        page_title="Dashboard for Airplane Fuel Consumption",
        page_icon=":airplane:",
        layout="wide",
    )
    # App title
    st.title("Flight Cash Operating Cost Analysis Tool")
    st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-family: Courier New; color: green;'>An interactive tool for analyzing and visualizing flight cash operating cost at the conceptual design level.</h5>", unsafe_allow_html=True)
    pritting_fuel()


# Run the application
if __name__ == "__main__":
    main_graph()
