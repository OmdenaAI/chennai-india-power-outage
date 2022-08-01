#Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image



# Title and Subheader
st.title("Electricity Power Outage Analysis")

st.subheader("Demand and supply Dataset overview")
st.markdown('<h3>EDA summary</h3>', unsafe_allow_html=True)

st.markdown('* Prior to 2016, there has been significant deficit and surplus of MW. ', unsafe_allow_html=True)
st.markdown('* November 2012 saw the lowest MW supplied with a deficit of -1643.0.', unsafe_allow_html=True)
st.markdown('* December 2012 saw the highest deficit of MW (-3745.0).', unsafe_allow_html=True)
st.markdown('* November 2014 saw the highest surplus of MW (2360.0).', unsafe_allow_html=True)
st.markdown('* The highest MW (17563.0) provided was in April 2022 but had a deficit of -83.0.', unsafe_allow_html=True)
    
    
# EDA
# To Improve speed and cache data
@st.cache(persist=True)
@st.cache(allow_output_mutation=True)
def load_data():
	df_monthly = pd.read_csv('data/demand_supply_monthly.csv')
	return df_monthly 


df_monthly = load_data()
st.text("monthly data")
st.write(df_monthly.head())
st.write(df_monthly.info())

df_yearly = df_monthly.groupby('year').mean().reset_index()

# drop unwamted columns
df_yearly.drop(columns=['month', 'month_published', 'year_published'], inplace=True)
st.text("Yearly data")
st.write(df_yearly.head())
st.write(df_yearly.info())

# Show Dataset
if st.checkbox("Preview DataFrame"):
	
        if st.button("Head"):
            st.write(df_yearly.head())
        if st.button("Tail"):
            st.write(df_yearly.tail())
        if st.button("Describe"):
            st.write(df_yearly.describe())
        else:
            st.write(df_yearly.head(5))

# Show Entire Dataframe
if st.checkbox("Show All DataFrame"):
	st.dataframe(df_yearly)

# Show Description
if st.checkbox("Show All Column Name"):
	st.text("Columns:")
	st.write(df_yearly.columns)

# Dimensions
data_dim = st.radio('What Dimension Do You Want to Show',('Rows','Columns'))
if data_dim == 'Rows':
	st.text("Showing Length of Rows")
	st.write(len(df_yearly))
if data_dim == 'Columns':
	st.text("Showing Length of Columns")
	st.write(df_yearly.shape[1])



image = Image.open('data/images/demand_01.png')
st.image(image, caption='The MU required and met')

image = Image.open('data/images/demand_02.png')
st.image(image, caption='The surplus/Defecit of MU per day')

image = Image.open('data/images/demand_03.png')
st.image(image, caption='The MU required and met')

image = Image.open('data/images/demand_04.png')
st.image(image, caption='TThe surplus/Defecit of MU')

image = Image.open('data/images/demand_05.png')
st.image(image, caption='The MW required and met')

image = Image.open('data/images/demand_06.png')
st.image(image, caption='Surplus(+)/Deficit(-)(MW)')


    
    


