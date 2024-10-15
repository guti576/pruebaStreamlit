import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Letters
kpis = ['letters sent', '€ / letter']
rename_columns = {'case_id':'letters sent', 'recovery_no_at':'recovery'}

letters_date = pd.read_excel('./actuals/letters.xlsx', sheet_name='date')
letters_date = letters_date.rename(columns=rename_columns)

# Sidebar for product selection
st.sidebar.header("Letter - PI")

# Set title of the dashboard
st.title(f"Actuals for letters PI")

# Display line chart for the selected product (One tab per kpi)
st.subheader(f"Line chart")
tab1, tab2 = st.tabs(kpis)

with tab1:
         fig = px.line(letters_date, x='month', y=kpis[0], color='year', markers=True)
         st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab2:
        fig = px.line(letters_date, x='month', y=kpis[1], color='year', markers=True)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# Display tables
st.subheader(f"Date view")
st.dataframe(letters_date.set_index(['year', 'month']).sort_index(ascending=False), height=250)