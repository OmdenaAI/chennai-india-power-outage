#Import Libraries

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import seaborn as sns ; sns.set(font_scale=1)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime as dt
import re


# Title and Subheader
st.title("Electricity Power Outage Analysis")

st.subheader("Demand and supply Dataset overview")

st.markdown('<h4>EDA summary observed</h4>', unsafe_allow_html=True)

st.markdown('* There is no year where the supply in MW was up to or more than the demand', unsafe_allow_html=True)
st.markdown('* 2012 with 12.67% is the year having the biggest deficit', unsafe_allow_html=True)
st.markdown('* 2019 with 0.06% corresponds to the year with the smallest deficit', unsafe_allow_html=True)
st.markdown('* The maximum and minimum Energy supplied in the period were respectively 184835 MW in 2021 and 92862 MW in 2012', unsafe_allow_html=True)
st.markdown('* The demand trend is always above the supply trend during the period', unsafe_allow_html=True)
st.markdown('* Percentage of shortages in MW trend : The shortages are reducing as we move from 2012 to 2021', unsafe_allow_html=True)
st.markdown('* The supply of energy was enough 45% of the time(56 months out of 122 months) during the period of study)', unsafe_allow_html=True)
st.markdown('* In 2012 and 2013 the supply of energy was lower than the demand for each month of the year', unsafe_allow_html=True)
st.markdown('* The level of monthly highest deficit rate is reducing with time and is contantly less than 1% since end of 2015. April, May, June and July are the most represented', unsafe_allow_html=True)
st.markdown('* What are the maximum and minimum Energy supplied in the period and when was that? (Ans: max supplied: 17563 MW in april 2022, min supplied: 8518 MW in november 2012)', unsafe_allow_html=True)
st.markdown('*   and supply trends (Obs: The difference between demand and supply per month is getting smaller with time enven if in general demand is above supply)', unsafe_allow_html=True)
st.markdown('* Percentage of shortages in MW - trend (Obs: The shortages rate per month are reducing to zero as we move from 2012 to 2022)', unsafe_allow_html=True)

# EDA
# To Improve speed and cache data
@st.cache(allow_output_mutation=True)
@st.cache(persist=True)

def load_data():
	energy_ds = pd.read_csv('data/POSOCO_DEMAND_SUPPLY_TamilNadu.csv')
	return energy_ds 


energy_ds = load_data()

st.write(energy_ds.head())
st.write(energy_ds.info())

def extract_month (x):
    month_ = re.split(r'_| ', x)[2]
    if month_.lower() == 'monthly':
        month = re.split(r'_| ', x)[0]
    else:
        month = month_
    return month    

def extract_year (x):
    year_ = re.split(r"[_. ]", x.strip())[3]
    if year_.lower() == 'report':
        year = re.split(r"[_. ]", x.strip())[1]
    else:
        year = year_
    return year


# Extract the Year corresponding to the data presented
energy_ds['year'] = energy_ds['name_report'].apply(extract_year)
#energy_ds['year'].astype(int)

# Extract the Month corresponding to the data presented
energy_ds['month'] = energy_ds['name_report'].apply(extract_month)
#energy_ds['month'].astype(int)

st.write('verify that the month and year were well extracted')
st.write(energy_ds['month'].unique())
st.write(energy_ds['year'].unique())

# replace months in words by months in figures
to_replace_dic = {'Apr':4, 'May':5, 'Mar':3, 'Jan':1, 'Nov':11, 'Sep':9, 'Jul':7, 'Feb':2, 'Dec':12, 'Oct':10, 'Aug':8, 'Jun':6, 'April':4, 'March':3, 'January':1, 'November':11,
       'September':9, 'July':7, 'February':2, 'December':12, 'October':10, 'August':8, 'June':6}

energy_ds['month'].replace(to_replace=to_replace_dic , inplace=True)

energy_ds['year'] = energy_ds['year'].astype(int)

st.write('info on the dataset')
st.write(energy_ds.info())




image = Image.open('data/images/supply_01.png')
st.image(image, caption='Percentage of shortages in MW - trend (Obs: The shortages are reducing as we move from 2012 to 2021)')

image = Image.open('data/images/supply_02.png')
st.image(image, caption='The level of monthly highest deficit rate is reducing with time ')

image = Image.open('data/images/supply_03.png')
st.image(image, caption='Percentage of shortages in MW - trend (Obs: The shortages rate per month are reducing to zero as we move from 2012 to 2022)')
