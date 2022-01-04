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

today = datetime.now()
n_days_ago = today - timedelta(days=365)

df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

st.markdown("<h1 style='text-align: center;'>PH Covid-19 Tracker</h1>", unsafe_allow_html=True)

st.write("Source: https://covid.ourworldindata.org")


fig0 = px.scatter(df['date'], x="total_cases", y="total_deaths", size="pop", color="continent",
           hover_name="location", log_x=True, size_max=60)
st.plotly_chart(fig0, use_container_width=True)

fig1 = px.bar(
    df, 
    x='date', 
    y='new_cases',
    color="new_cases",
    hover_data=['new_cases', 'total_cases']
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    df, 
    x='date', 
    y='new_deaths',
    hover_data=['new_deaths', 'total_deaths']
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    df, 
    x='date', 
    y='total_tests'
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(
    df, 
    x='date', 
    y='people_fully_vaccinated',
)
st.plotly_chart(fig4, use_container_width=True)

n_days_ago = today - timedelta(days=90)

df = load_data()
df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

fig = px.bar(df, x='date', y='total_cases', color='total_cases', title="Total Number of Cases for the past 90 days")
fig.update_layout(width=1200,height=500)
st.plotly_chart(fig)

fig = px.bar(df, x='date', y='total_deaths', color='total_deaths', title="Total Number of Deaths for the past 90 days")
fig.update_layout(width=1200,height=500)
st.plotly_chart(fig)

st.write("Powered By Altair, Pandas, Plotly Express, Pytz and Streamlit")

st.write("Made from Google Colab by Jay Milagroso <j.milagroso@gmail.com>")
