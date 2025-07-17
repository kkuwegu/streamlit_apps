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
    
    # Improve edge positioning
    dot.attr(concentrate='true')
    # dot.attr(nodesep='1.0')  # Increased horizontal spacing between nodes
    # dot.attr(ranksep='2.0')  # Increased spacing between ranks
    
    # Make diagram and font bigger
    dot.attr(dpi='70')
    # dot.attr(fontsize='30')
    dot.attr(size='16,8!')  # Width=16 inches, Height=8 inches, ! forces exact size
    # dot.attr('node', fontsize='14')
    # dot.attr('edge', fontsize='12')

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

# fill NaN values with the previous value in the column
df_tech_data_all.fillna(method='ffill', inplace=True)



## --- dashboard ---

# show drop list  of technology
technology_list = df_tech_data_all['Technology name'].unique()
select_tech = st.selectbox("Select Technology", technology_list)

# show diagram
dot = create_tech_rep_diagram_graphviz(df_tech_data_all[df_tech_data_all['Technology name'] == select_tech])
st.graphviz_chart(dot.source)