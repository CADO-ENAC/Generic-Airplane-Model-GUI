import streamlit as st
from gam_copy import GAM


def graphic():
    gam = GAM()
    graph_list = []
    name_list = []
    if 'VARG1' in st.session_state:
        data1 = st.session_state.VARG1
        for element1 in data1:
            graph_list.append(element1[0])
            name_list.append(element1[3])
    if 'VARG2' in st.session_state:
        data2 = st.session_state.VARG2
        for element2 in data2:
            graph_list.append(element2[0])
            name_list.append(element2[3])
    if 'VARG3' in st.session_state:
        data3 = st.session_state.VARG3
        for element3 in data3:
            graph_list.append(element3[0])
            name_list.append(element3[3])
    if graph_list != [] and name_list != []:
        gam.payload_range_graph(graph_list, name_list)
    else:
        st.info("No configuration found")


def main():
    '''Main, display the dashboard'''
    st.set_page_config(
        page_title="Dashboard for Airplane Fuel Consumption",
        page_icon=":airplane:",
        layout="centered",
    )
    # App title
    st.title("Payload–Range Analysis Tool")
    st.markdown("<h3><em>Developed by the CADO Team at ENAC</em></h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-family: Courier New; color: green;'>An interactive tool for comparing payload–range diagrams of previously designed airplanes.</h5>", unsafe_allow_html=True)

    graphic()




# Run the application
if __name__ == "__main__":
    main()
