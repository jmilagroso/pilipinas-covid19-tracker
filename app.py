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
n_days_ago = today - timedelta(days=60)

df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

st.markdown("<h1 style='text-align: center;'>PH Covid-19 Tracker</h1>", unsafe_allow_html=True)

st.write("Source: https://covid.ourworldindata.org")

fig1 = px.bar(
    df, 
    x='date', 
    y='new_cases',
    color="new_cases",
    hover_data=['new_cases', 'total_cases']
)
fig1.update_layout(width=1240)
st.plotly_chart(fig1)

fig2 = px.bar(
    df, 
    x='date', 
    y='new_deaths',
    color="new_deaths",
    hover_data=['new_deaths', 'total_deaths'], 
    title=f"New Deaths (as of {today}"
)
fig2.update_layout(width=1240)
st.plotly_chart(fig2)

n_days_ago = today - timedelta(days=15)
df = load_data()
df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

base1 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['total_tests']
).properties(
    width=500
)

text1 = base1.mark_text(
    align='center',
    baseline='line-top',
    color='#404040',
    angle=70,
    dy=-5
).encode(
    text='total_tests:Q'
)

base2 = alt.Chart(df2).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['people_fully_vaccinated']
).properties(
    width=500
)

text2 = base1.mark_text(
    align='center',
    baseline='line-top',
    color='#404040',
    angle=70,
    dy=-5
).encode(
    text='people_fully_vaccinated:Q'
)

with st.empty():
    (base1.encode(y='total_tests', color=alt.value("#ffb347")) + text1).properties(title=f'Total Number of Tests for the past 14 days') | (base2.encode(y='people_fully_vaccinated', color=alt.value("#228B22")) + text2).properties(title=f'Total Number of Fully Vaccinated for the past 14 days')

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
