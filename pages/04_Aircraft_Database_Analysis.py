import streamlit as st
import pandas as pd
#import matplotlib as plt
import plotly.express as px

# Load data from the Excel file
def load_data(files):
    '''Read Excel files'''
    return pd.read_excel(files)

st.title("Airplane Database Analysis Tool")
st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
st.markdown("<h5 style='font-family: Courier New; color: green;'>An interactive tool for visualizing and exploring existing airplane data from a reference database.</h5>", unsafe_allow_html=True)


# Load the Excel files
#file = "airplane_database_copieVF_test.csv"  # File with airplane details
file = "airplane_database_copieVF.xlsx"

try:
    data_airplanes = load_data(file)
except FileNotFoundError as e:
    st.error(f"File not found: {e.filename}")

# Data
prop = ["", "airplane_type",  "name", "Constructor", "icao_code", "iata_code", "n_pax", "owe",
        "mtow", "mlw", "max_fuel", "n_engine", "engine_type", "thruster_type", "powerplant", "bpr",
        "energy_type", "max_power", "max_thrust", "cruise_speed", "cruise_altitude","nominal_range"]

show = ["", "Airplane type", "Airplane name", "Manufacturer", "ICAO code", "IATA code",
        "Number of pax", "OEM", "MTOM", "MLM", "Max fuel", "Number of engines", "Engine type",
        "Thruster type", "Powerplant", "BPR", "Energy type", "Max power", "Max thrust",
        "Cruise speed", "Cruise altitude", "Nominale range"]

errors = ["string", "None", "int", "m", "deg", "m2", "kg",
          "no dim", "kW", "N", "km/h", "ft", "km", "mach"]

colors = {"general": "#d2b48c", "commuter": "#8a9a5b", "regional": "#5f9ea0", "short_medium Range": "#556b2f", "long_range": "#3a5f0b", "business": "#4b5320"}


# Parameters selection
if st.checkbox("Display Entire Airplane Database"):
    if not data_airplanes.empty:
        combined_data = pd.DataFrame({"Properties": prop})

        for idx, (_, row) in enumerate(data_airplanes.iterrows(), start=1):
            column_name = f"Airplane {idx}"
            combined_data[column_name] = [row.get(p, "None") for p in prop]
        st.dataframe(combined_data, hide_index=True)

st.write("")

## Selection of the 2 parameters
# st.write("### Select Visualization Parameters")
left_column1, right_column1 = st.columns(2)

with left_column1:
    para1 = st.selectbox("Select Vertical Axis Parameter", show)

show2 = []
for element in show:
    if element == "" or element != para1:
        show2.append(element)

with right_column1:
    para2 = st.selectbox("Select Horizontal Axis Parameter", show2)

try:
    # Make the graphic
    # Create the 2 list of data
    if para1 != "" and para2 != "":
        # st.success("Selected Parameters: "+ para1+ " vs. "+ para2)
        
        for i in range(len(prop)):
            if show[i] == para1:
                par1 = prop[i]
                prop2 = prop
                del(prop2[i])
        for j in range(len(show2)):
            if show2[j] == para2:
                par2 = prop2[j]
        
        data1               = []
        data2               = []
        colors_list         = []
        airplane_types_list = []

        for ele1, ele2, airplane_type in zip(data_airplanes[par1], data_airplanes[par2], data_airplanes["airplane_type"]):
            if ele1 not in errors and ele2 not in errors:
                data1.append(ele1)
                data2.append(ele2)

                colors_list.append(colors.get(airplane_type, "#654321"))
                airplane_types_list.append(airplane_type if pd.notna(airplane_type) else "Unknown")
        
        # Use a 'Type' column so Plotly shows a legend for aircraft types
        data_frame = pd.DataFrame({
            para2: data2,
            para1: data1,
            "Type": airplane_types_list
        })

        fig = px.scatter(
            data_frame,
            x=para2,
            y=para1,
            # marker_size=10,
            color="Type",
            color_discrete_map=colors,
            title=f"{para1} as a function of {para2}",
            labels={para1: para1, para2: para2, "Type": "Airplane Category"},
        )

        
        # Customize legend title / layout
        fig.update_layout(legend_title_text="Airplane Category")
        fig.update_traces(marker_size=10)
        
        # Add the AC you made at the graphic with the airplane data base data

        # st.header("Select Airplane to Add to the Plot")
        
        graph_list = []
        if 'VARG1' in st.session_state:
            data1 = st.session_state.VARG1
            for element1 in data1:
                # if element1[3] != ' ':
                graph_list.append(element1)
        if 'VARG2' in st.session_state:
            data2 = st.session_state.VARG2
            for element2 in data2:
                # if element2[3] != ' ':
                graph_list.append(element2)
        if 'VARG3' in st.session_state:
            data3 = st.session_state.VARG3
            for element3 in data3:
                # if element3[3] != ' ':
                graph_list.append(element3)
        
        if graph_list != []:
            name = [""]
            for ele in graph_list:
                name.append(ele[3])
            config = st.selectbox("Select Airplane to Add to the Plot", name)
            data_graph = 0
            for ele in graph_list:
                if ele[3] == config:
                    data_graph = [ele[0], ele[3]]
            slt1 = None
            slt2 = None
            if data_graph != 0:
                if par1 == "name":
                    slt1 = data_graph[1]
                if par2 == "name":
                    slt2 = data_graph[1]
                for slt_ele in data_graph[0]:
                    if par1 == slt_ele:
                        slt1 = data_graph[0][slt_ele]
                    if par2 == slt_ele:
                        slt2 = data_graph[0][slt_ele]
                    if slt_ele == "mission":
                        for key1 in slt_ele:
                            if par1 == key1:
                                slt1 = data_graph[0]["mission"][key1]
                            if par2 == key1:
                                slt2 = data_graph[0]["mission"][key1]
                    if slt_ele == "altitude_data":
                        for key2 in slt_ele:
                            if par1 == key2:
                                slt1 = data_graph[0]["altitude_data"][key2]
                            if par2 == key2:
                                slt2 = data_graph[0]["altitude_data"][key2]
                    if slt_ele == "reserve_data":
                        for key3 in slt_ele:
                            if par1 == key3:
                                slt1 = data_graph[0]["reserve_data"][key3]
                            if par2 == key3:
                                slt2 = data_graph[0]["reserve_data"][key3]
                    if slt_ele == "power_system":
                        for key4 in slt_ele:
                            if par1 == key4:
                                slt1 = data_graph[0]["power_system"][key4]
                            if par2 == key4:
                                slt2 = data_graph[0]["power_system"][key4]
                else:
                    if slt1 == None:
                        st.warning("No value is available for the selected parameter (" + para1 + ") in the designed airplane.")
                    if slt2 == None:
                        st.warning("No value is available for the selected parameter (" + para2 + ") in the designed airplane.")
                if slt1 == None or slt2 == None:
                    st.plotly_chart(fig)
                    st.warning("The selected airplane is not included in the current scatter plot.")
                if slt1 != None and slt2 != None:
                    special_point = pd.DataFrame({para2: [slt2], para1: [slt1], "Color": ["#C6E79B"]})
                    fig.add_scatter(x=[slt2], y=[slt1], mode="markers", marker=dict(color=["#C6E79B"], size=15, symbol="star"), name=config)
                    st.plotly_chart(fig)
                    # st.success("The selected airplane has been successfully added to the scatter plot.")
        else:
            st.plotly_chart(fig)


except:
    st.warning("Two parameters must be selected to generate the plot.")

