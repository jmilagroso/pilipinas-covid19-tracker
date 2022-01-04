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


fig = px.line(df, x='date', y='new_cases')
fig.add_bar(df, x='date', y='new_cases')
fig.show()
st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(
    df, 
    x='date', 
    y='new_cases',
    color="new_cases",
    title="New Cases for the past 1 year",
    hover_data=['new_cases', 'total_cases']
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    df, 
    x='date', 
    y='new_deaths',
    title="New Deaths for the past 1 year",
    hover_data=['new_deaths', 'total_deaths']
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    df, 
    x='date', 
    y='total_tests',
    title="Total Tests for the past 1 year",
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(
    df, 
    x='date', 
    y='people_fully_vaccinated',
    title="Total Fully Vaccinated for the past 1 year"
)
st.plotly_chart(fig4, use_container_width=True)

n_days_ago = today - timedelta(days=90)

df = load_data()
df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

fig = px.bar(df, x='date', y='total_cases', color='total_cases', title="Total Number of Cases for the past 90 days")
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df, x='date', y='total_deaths', color='total_deaths', title="Total Number of Deaths for the past 90 days")
st.plotly_chart(fig, use_container_width=True)

st.write("Powered By Altair, Pandas, Plotly Express, Pytz and Streamlit")

st.write("Jay Milagroso <j.milagroso@gmail.com>")
