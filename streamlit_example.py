import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Config layout
st.set_page_config(layout="wide")

# Parameters
products = ['letters', 'w2c_pi', 'post90', 'dsa']
skills = ['A', 'B', 'C', 'D', 'E', 'Z', 'A1', 'B1', 'C1', 'D1', 'E1', 'Z1', 'A2', 'B2', 'C2', 'D2', 'E2', 'Z2']

kpis = {
    'post90': ['recovery', '€ / contact'],
    'letters': ['letters sent', '€ / letter'],
    'w2c_pi': ['recovery', '€ / contact'],
    'dsa': ['has_letter', 'recovery', '€ / letter']}

# Rename
rename_columns = {
    'post90': {'year_maestra':'year', 'month_maestra':'month', 'recovery_no_at': 'recovery'},
    'letters': {'case_id':'letters sent', 'recovery_no_at':'recovery'},
    'w2c_pi': {'year_call':'year', 'month_call':'month', 'recovery_no_at': 'recovery'},
    'dsa': {'month_keydate':'month', 'year_keydate':'year', 'payment_30_days_keydate':'recovery', 'score_bin':'skill'}
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

# DSA
dsa_date = pd.read_excel('./actuals/dsa.xlsx', sheet_name='date')
dsa_skill = pd.read_excel('./actuals/dsa.xlsx', sheet_name='skill')

# Sidebar for product selection
st.sidebar.header("Filters")
product_filter = st.sidebar.selectbox("Product:", products)

# Select the appropriate DataFrame based on the selected product
if product_filter == 'letters':
    df_date = letters_date
    df_skill = letters_skill
elif product_filter == 'post90':
    df_date = post90_date
    df_skill = post90_skill
elif product_filter == 'dsa':
    df_date = dsa_date
    df_skill = dsa_skill
else:
    df_date = w2c_pi_date
    df_skill = w2c_pi_skill

df_date = df_date.rename(columns=rename_columns[product_filter])
try:
    df_skill = df_skill.rename(columns=rename_columns[product_filter])
except:
    pass

# Set title of the dashboard
st.title(f"Actuals for {product_filter}")

# Display line chart for the selected product (One tab per kpi)
st.subheader(f"Line chart")
tabs = st.tabs([f"{tab_name}" for tab_name in kpis[product_filter]])

for i, tab in enumerate(tabs):
    with tab:
         fig = px.line(df_date, x='month', y=kpis[product_filter][i], color='year', markers=True)
         st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# Display tables
col1, col2 = st.columns(spec=[.5, .5])

with col1:
    st.subheader(f"Date view")
    st.dataframe(df_date.set_index(['year', 'month']).sort_index(ascending=False), height=250)

with col2:
    if(product_filter != 'letters'):
        st.subheader(f"Skill view")
        styled_df = df_skill.set_index('skill')
        #styled_df = styled_df.style.background_gradient(subset=['€ / contact'])
        st.dataframe(styled_df, height=250)