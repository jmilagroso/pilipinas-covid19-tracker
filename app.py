# -*- coding: utf-8 -*-

import altair as alt
import pandas as pd
import pytz
import streamlit as st

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from pytz import timezone

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

@timed_lru_cache(3600)
def load_data():
    data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    return data

df = load_data()

today = datetime.now() + timedelta(hours=8)
n_days_ago = today - timedelta(days=14)

df = df.loc[df['location'] == 'Philippines']
df = df.loc[df['date'] >= str(n_days_ago.date())]

st.markdown("<h1 style='text-align: center;'>Philippines Covid-19 Statistics</h1>", unsafe_allow_html=True)

st.write("Source: https://covid.ourworldindata.org")

with st.empty():
    st.write(df.describe())

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

with st.empty():
    (base1.encode(y='new_cases') + text1).properties(title=f'New Cases (as of {today})') | (base2.encode(y='new_deaths', color=alt.value("#f54242")) + text2).properties(title=f'New Deaths (as of {today})')



base1 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['total_cases']
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
    text='total_cases:Q'
)

base2 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['total_deaths']
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
    text='total_deaths:Q'
)

with st.empty():
    (base1.encode(y='total_cases') + text1).properties(title=f'Total Cases (as of {today})') | (base2.encode(y='total_deaths', color=alt.value("#f54242")) + text2).properties(title=f'Total Deaths (as of {today})')

base1 = alt.Chart(df).mark_bar().encode(
    x='monthdate(date):O',
    tooltip=['people_vaccinated']
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
    text='people_vaccinated:Q'
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
    (base1.encode(y='people_vaccinated') + text1).properties(title=f'Total Number of Vaccinated (as of {today})') | (base2.encode(y='people_fully_vaccinated', color=alt.value("#228B22")) + text2).properties(title=f'Total Number of Fully Vaccinated (as of {today})')
    
st.write("Powered By Altair, Pandas, Pytz and streamlit.io")

st.write("Made from Google Colab by Jay Milagroso <j.milagroso@gmail.com>")
