# -*- coding: utf-8 -*-

import altair as alt
import json
import pandas as pd
import plotly.express as px
import pytz
import streamlit as st

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from pytz import timezone
from urllib.request import urlopen

st.set_page_config(page_title="PH Covid 19 Tracker",layout='wide')
alt.renderers.enable('default')

def load_data():
    data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    return data

df = load_data()

filter_duration = {
    730: "Past 2 Years", 
    365: "Past Year", 
    183: "Past 6 Months", 
    91: "Past 3 Months", 
    31: "Past Month",
    16: "Past 2 Weeks",
    8: "Past 7 Days"
}

def format_func(option):
    return filter_duration[option]


st.markdown("<h1 style='text-align: center;'>PH Covid-19 Tracker</h1>", unsafe_allow_html=True)

st.write("Source: https://covid.ourworldindata.org")

option = st.selectbox("", options=list(filter_duration.keys()), format_func=format_func, index=0)

today = datetime.now()
n_days_ago = today - timedelta(days=option)

df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

fig1 = px.bar(
    df, 
    x='date', 
    y='new_cases',
    color='new_cases',
    title='New Cases',
    hover_data=['new_cases', 'total_cases']
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    df, 
    x='date', 
    y='new_deaths',
    title='New Deaths',
    hover_data=['new_deaths', 'total_deaths']
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    df, 
    x='date', 
    y='total_tests',
    color='total_tests',
    title='Total Tests'
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(
    df, 
    x='date', 
    y='people_fully_vaccinated',
    title='Total Fully Vaccinated'
)
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.bar(
    df, 
    x='date', 
    y='total_cases', 
    color='total_cases', 
    title='Total Number of Cases'
)
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.bar(
    df, 
    x='date', 
    y='total_deaths', 
    color='total_deaths', 
    title='Total Number of Deaths'
)
st.plotly_chart(fig6, use_container_width=True)

st.write("Powered By Pandas, Plotly Express and Streamlit")

st.write("Jay Milagroso <j.milagroso@gmail.com>")
