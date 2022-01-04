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

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache

def load_data():
    data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    return data

df = load_data()

today = datetime.now() + timedelta(hours=8)
n_days_ago = today - timedelta(days=14)

df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

st.markdown("<h1 style='text-align: center;'>PH Covid-19 Tracker</h1>", unsafe_allow_html=True)

st.write("Source: https://covid.ourworldindata.org")

base1 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['new_cases']
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
    text='new_cases:Q'
)

base2 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['new_deaths']
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
    text='new_deaths:Q'
)

#with st.empty():
    #(base1.encode(y='new_cases') + text1).properties(title=f'New Cases for the past 14 days') | (base2.encode(y='new_deaths', color=alt.value("#f54242")) + text2).properties(title=f'New Deaths for the past 14 days')
fig1 = px.bar(
    df, 
    x='date', 
    y='new_cases',
    hover_data=['new_cases', 'total_cases'], 

    height=500
)


fig2 = px.bar(
    df, 
    x='date', 
    y='new_deaths',
    hover_data=['new_deaths', 'total_deaths'], 
    title=f"New Deaths (as of {today}",
    height=500
)
with st.empty():
    st.plotly_chart(fig1) | st.plotly_chart(fig2)

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

base2 = alt.Chart(df).mark_bar().encode(
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


today = datetime.now() + timedelta(hours=0)
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
