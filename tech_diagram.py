import streamlit as st
import pandas as pd
from graphviz import Digraph



## --- functions ---

def warptext(text, max_chars=20):
    """Wrap text to a maximum number of characters per line."""
    text_final = ''
    text_temp = text

    while len(text_temp) > max_chars:
        # Find the last underscore before the max_chars limit
        last_underscore = text_temp.rfind('_', 0, max_chars)

        if last_underscore == -1:
            last_underscore = max_chars

        text_final += text_temp[:last_underscore] + '_\n'
        text_temp = text_temp[last_underscore + 1:]

    text_final += text_temp

    return text_final


def create_tech_diagram_graphviz(row):
    """Create a technology diagram for the given process name and tech data using graphviz."""

    tech_id = row['ehubX Tech ID']
    dot = Digraph(comment=tech_id)
    dot.attr(rankdir='LR')
    dot.attr(splines='ortho')

    # --- load data for each processes
    tech_type_spec = row['Process Type'] + '-' + row['Category Specification']

    # Add process node
    dot.node(tech_id, warptext(tech_id), shape='box', style='filled', fillcolor='lightblue')

    di_tech = {}
    for io in ['Input', 'Output']:
        di_tech[io] = {}
        di_tech[io]['carriers'] = [x.strip() for x in row[f'{io} Carriers'].split(',')]
        di_tech[io]['shares'] = [float(x.strip()) for x in row[f'{io} Shares'].split(',')]
        di_tech[io]['units'] = [x.strip() for x in row[f'{io} Units'].split(',')]

        input_lengths = [len(di_tech[io][key]) for key in di_tech[io]]
        if len(set(input_lengths)) != 1:
            print(f"[Warning] {tech_id} has input lists have different lengths:", input_lengths)

        di_tech[io]['main carrier'] = row[f'Main {io} Carrier'].strip()
        if di_tech[io]['main carrier'] not in di_tech[io]['carriers']:
            print(f"[Warning] {tech_id} main {io} carrier '{di_tech[io]['main carrier']}' not in {io} carriers:", di_tech[io]['carriers'])
            di_tech[io]['main carrier'] = di_tech[io]['carriers'][0]

    # Add carrier nodes and edges
    for io in ['Input', 'Output']:
        for i in range(len(di_tech[io]['carriers'])):
            carr = di_tech[io]['carriers'][i]
            share = di_tech[io]['shares'][i]
            unit = di_tech[io]['units'][i]
            dot.node(carr, carr, shape='box', style='filled', fillcolor='lightgrey')

            label = f"{share} {unit}"
            if io == 'Input':
                dot.edge(carr, tech_id, label=label)
            else:
                dot.edge(tech_id, carr, label=label)

    return dot



## --- load data ---
df_tech_conv = pd.read_csv('data/tech_conv.csv')



## --- preprocess data ---

# na to empty string
li_cols_fillna = ['Description', 'Process Type', 'Main Sector', 'Main Category', 'Category Specification', 'Tech Type']
df_tech_conv.loc[:, li_cols_fillna] = df_tech_conv.loc[:, li_cols_fillna].fillna('')

li_cols_str = ['Output Shares', 'Input Shares']
df_tech_conv.loc[:, li_cols_str] = df_tech_conv.loc[:, li_cols_str].astype(str)



## --- dashboard ---

st.markdown('# Technology Input/Output Dashboard')
st.markdown('This dashboard visualizes the technology input/output data.')
st.markdown('Creator: Barton Chen / yi-chung.chen@empa.ch')
st.markdown('Urban Energy Systems Lab')
st.markdown('Empa (Swiss Federal Laboratories for Materials Science and Technology)')
st.markdown('Last updated: July 2025')
st.markdown('')


# show link to source file
# st.markdown(f'Access to the source file ([Technology representation Google Sheet]({sheet_url}))')
st.markdown('')

# Add a textbox for keyword input
keyword = st.text_input("Filter by keyword (optional)")

# get list of tech IDs
technology_list = df_tech_conv['ehubX Tech ID'].unique()

# Filter dataframe by keyword if provided
if keyword:
    technology_list = [tech_id for tech_id in technology_list if keyword.lower() in str(tech_id).lower()]

# show drop list  of technology
select_id = st.selectbox("Select Tech ID", technology_list)
row = df_tech_conv[df_tech_conv['ehubX Tech ID'] == select_id].iloc[0]


# show diagram
if select_id is not None:
    dot = create_tech_diagram_graphviz(row)
    st.graphviz_chart(dot.source, use_container_width=False)


    if st.button("Plot all filtered technologies"):

        for select_id in technology_list:
            row = df_tech_conv[df_tech_conv['ehubX Tech ID'] == select_id].iloc[0]
            dot = create_tech_diagram_graphviz(row)
            st.graphviz_chart(dot.source, use_container_width=False)