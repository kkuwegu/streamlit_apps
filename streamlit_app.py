import streamlit as st
import pandas as pd
from graphviz import Digraph



## --- functions ---

def create_tech_rep_diagram_graphviz(df_tech_data):
    """Create a technology diagram for the given process name and tech data using graphviz."""
    tech_name = df_tech_data['Technology name'].iat[0]
    dot = Digraph(name=tech_name)
    
    # Set horizontal layout (Left to Right)
    dot.attr(rankdir='LR')
    
    # Set orthogonal edges (90-degree turns)
    dot.attr(splines='ortho')
    
    # Store nodes to avoid duplicates
    carrier_nodes = set()
    process_nodes = set()

    for indx in df_tech_data.index:
        name_proc = df_tech_data['Process name'][indx]
        # Add process node
        if name_proc not in process_nodes:
            dot.node(name_proc, shape='box', style='filled', fillcolor='lightblue')
            process_nodes.add(name_proc)

        # Add carrier nodes and edges
        for col, direction in [('Process input', 'in'), ('Process output', 'out')]:
            li_inout = [x.strip() for x in df_tech_data.at[indx, col].split(',')]
            for carr in li_inout:
                if carr not in carrier_nodes:
                    dot.node(carr, shape='box', style='filled', fillcolor='lightgreen')
                    carrier_nodes.add(carr)
                if direction == 'in':
                    dot.edge(carr + ':c', name_proc + ':c')
                else:
                    dot.edge(name_proc + ':c', carr + ':c')
    return dot



## --- load data ---

# read csv file
df_tech_data_all = pd.read_csv("data/tech_representation.csv")

# Download data from Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1_ZOiXZGA3DzyhO4cEZe0XlztVPwsVj1FnDgYM0hcsUk/"
df_tech_data_all = pd.read_csv(sheet_url + 'export?format=csv')

# fill NaN values with the previous value in the column
df_tech_data_all.fillna(method='ffill', inplace=True)



## --- dashboard ---

st.markdown('# Technology Representation Dashboard')
st.markdown('This dashboard visualizes the technology representation data.')
st.markdown('Author: Barton Chen / yi-chung.chen@empa.ch')
st.markdown('Urban Energy Systems Lab')
st.markdown('Empa (Swiss Federal Laboratories for Materials Science and Technology)')
st.markdown('Last updated: July 2025')
st.markdown('')


# show link to source file
st.markdown(f'Access to the source file ([Technology representation Google Sheet]({sheet_url}))')
st.markdown('')

# Add a textbox for keyword input
keyword = st.text_input("Filter by keyword (optional)")

# Filter dataframe by keyword if provided
if keyword:
    df_tech_data_all = df_tech_data_all[df_tech_data_all.apply(lambda row: keyword.lower() in row.astype(str).str.lower().to_string(), axis=1)]

# show drop list  of technology
technology_list = df_tech_data_all['Technology name'].unique()
select_tech = st.selectbox("Select Technology", technology_list)

# show diagram
if select_tech is not None:
    dot = create_tech_rep_diagram_graphviz(df_tech_data_all[df_tech_data_all['Technology name'] == select_tech])
    st.graphviz_chart(dot.source, use_container_width=False)