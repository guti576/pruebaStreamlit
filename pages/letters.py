import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
from millify import millify

# Config layout
st.set_page_config(layout="wide")
template = 'ggplot2'

# Letters
kpis = ['letters sent', '€ / letter', 'Actuals']
rename_columns = {'case_id':'letters sent', 'recovery_no_at':'recovery'}
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
current_year = datetime.date.today().year
letters_date = pd.read_excel('./actuals/letters.xlsx', sheet_name='date')
letters_date = letters_date.rename(columns=rename_columns)
letters_date['month_label'] = pd.to_datetime(letters_date['month'], format='%m').dt.strftime('%b.')

# Sidebar for product selection
uplift = st.sidebar.number_input('Uplift (%)', format='%0.1f', value=19.1)

# Set title of the dashboard
st.header("ES - Letters PI")

# Main KPIs
col1, col2, col3 = st.columns(3)
letters_ytd = millify(letters_date[letters_date.year == current_year]['letters sent'].sum())
letters_date['Actuals'] = round(letters_date['recovery'] * uplift / 100, 0)
actuals_ytd = millify(letters_date[letters_date.year == current_year]['Actuals'].sum())
col1.metric("Letters sent (YTD)", letters_ytd)
col2.metric("Actuals (YTD)", actuals_ytd + '€')
#col3.metric("Humidity", "86%", "4%")

# Display charts for the selected product (One tab per kpi)
tab1, tab2, tab3 = st.tabs(kpis)

with tab1:
    fig = px.histogram(letters_date, x="month_label", y=kpis[0],
                      color='year', barmode='group', template=template,
                      color_discrete_map={2022: "#e5e8e8", 2023: "#99a3a4", 2024: "#2980b9"})
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, theme=None, use_container_width=True)

with tab2:
    fig = px.line(letters_date, x="month_label", y=kpis[1],
                      color='year', markers='*', template=template,
                      color_discrete_map={2022: "#e5e8e8", 2023: "#99a3a4", 2024: "#2980b9"})
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, theme=None, use_container_width=True)

with tab3:
    fig = px.histogram(letters_date, x="month_label", y='Actuals',
                      color='year', barmode='group', template=template,
                      color_discrete_map={2022: "#e5e8e8", 2023: "#99a3a4", 2024: "#2980b9"})
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, theme=None, use_container_width=True)

# Display tables
st.subheader(f"Date view")
st.dataframe(letters_date.set_index(['year', 'month']).sort_index(ascending=False), height=150)