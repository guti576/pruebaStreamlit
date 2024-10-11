import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Config layout
st.set_page_config(layout="wide")

# Parameters
products = ['letters', 'w2c_pi', 'post90']
skills = ['A', 'B', 'C', 'D', 'E', 'Z', 'A1', 'B1', 'C1', 'D1', 'E1', 'Z1', 'A2', 'B2', 'C2', 'D2', 'E2', 'Z2']

kpis = {
    'post90': ['recovery', '€ / contact'],
    'letters': ['letters sent', '€ / letter'],
    'w2c_pi': ['recovery', '€ / contact']}

kpis = {
    'post90': ['€ / contact'],
    'letters': ['€ / letter'],
    'w2c_pi': ['€ / contact']}

rename_columns = {
    'post90': {'year_maestra':'year', 'month_maestra':'month', 'recovery_no_at': 'recovery'},
    'letters': {'case_id':'letters sent', 'recovery_no_at':'recovery'},
    'w2c_pi': {'year_call':'year', 'month_call':'month', 'recovery_no_at': 'recovery'}
}

# Letters
letters_date = pd.read_excel('./actuals/letters.xlsx', sheet_name='date')
letters_skill = None

# W2C PI
w2c_pi_date = pd.read_excel('./actuals/w2c_pi.xlsx', sheet_name='date')
w2c_pi_skill = pd.read_excel('./actuals/w2c_pi.xlsx', sheet_name='skill')

# W2C Post90
post90_date = pd.read_excel('./actuals/post90.xlsx', sheet_name='date')
post90_skill = pd.read_excel('./actuals/post90.xlsx', sheet_name='skill')

# Sidebar for product selection
st.sidebar.header("Filter by Product")
product_filter = st.sidebar.selectbox("Select a product:", ['w2c_pi', 'letters', 'post90'])

# Select the appropriate DataFrame based on the selected product
if product_filter == 'letters':
    df_date = letters_date
    df_skill = letters_skill

elif product_filter == 'post90':
    df_date = post90_date
    df_skill = post90_skill
else:
    df_date = w2c_pi_date
    df_skill = w2c_pi_skill

df_date = df_date.rename(columns=rename_columns[product_filter])

# Set title of the dashboard
st.title(f"Actuals for {product_filter}")

col1, col2 = st.columns(spec=[.5, .5])

with col1:
    # Display the selected DataFrame as a table
    st.subheader(f"Date view")
    st.dataframe(df_date.set_index(['year', 'month']).sort_index(ascending=False), height=250)

with col2:
    # Display the selected DataFrame as a table
    if(product_filter != 'letters'):
        st.subheader(f"Skill view")
        st.dataframe(df_skill[df_skill.skill.isin(skills)].set_index('skill'), height=250)

# Display line chart for the selected product
st.subheader(f"Line chart")
fig = px.line(df_date, x='month', y=kpis[product_filter], color='year', markers=True)
fig.update_layout(title='Average High and Low Temperatures in New York',
                   xaxis_title='Month',
                   yaxis_title=kpis[product_filter][0])

st.plotly_chart(fig, use_container_width=True, theme="streamlit")



