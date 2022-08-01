#Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image


# Title and Subheader
st.title("Electricity Power Outage Analysis")

st.subheader("Hydro Power Dataset overview")

st.markdown('<h4>EDA summary</h4>', unsafe_allow_html=True)

st.markdown('* Kunda 2 always had the biggest hydro power generation during the period with a peak in 2007 reaching 903.016 MU. Also, Perunchani and Lower Aliyar Power houses had a negative production in 2014 and 2016 respectively, they could instead be considered as consumers)', unsafe_allow_html=True)
st.markdown('* Nilgiris district always had the biggest hydro power generation during the period with a peak in 2007 reaching 2218.454 MU. Also, Tiruvannamalai district always had the lowest Hydro Power Production with the lowest realised in 2016 at 0.41 MU.', unsafe_allow_html=True)


# EDA
# To Improve speed and cache data
@st.cache(persist=True)
@st.cache(allow_output_mutation=True)
def load_data():
	df = pd.read_csv('data/hydro_power_installed_capacity.csv',encoding='cp1252')
	return df 


df = load_data()



# Show Dataset
if st.checkbox("Preview DataFrame"):
	
        if st.button("Head"):
            st.write(df.head())
        if st.button("Tail"):
            st.write(df.tail())
        if st.button("Describe"):
            st.write(df.describe())
        else:
            st.write(df.head(5))

# Show Entire Dataframe
if st.checkbox("Show All DataFrame"):
	st.dataframe(df)

# Show Description
if st.checkbox("Show All Column Name"):
	st.text("Columns:")
	st.write(df.columns)

# Dimensions
data_dim = st.radio('What Dimension Do You Want to Show',('Rows','Columns'))
if data_dim == 'Rows':
	st.text("Showing Length of Rows")
	st.write(len(df))
if data_dim == 'Columns':
	st.text("Showing Length of Columns")
	st.write(df.shape[1])

image = Image.open('data/images/hydro_01.png')
st.image(image, caption='Boxplot of Hydro power generation per district for every year')

image = Image.open('data/images/hydro_02.png')
st.image(image, caption='Trends of HPG by district from 2007 to 2016')

image = Image.open('data/images/hydro_03.png')
st.image(image, caption='Trends of Total HPG by district from 2007 to 2016')


image = Image.open('data/images/hydro_04.png')
st.image(image, caption=' Boxplot of Hydro power generation per district for every year')




