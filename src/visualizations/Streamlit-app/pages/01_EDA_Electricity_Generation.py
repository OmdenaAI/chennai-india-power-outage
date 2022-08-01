#Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image


# Title and Subheader
st.title("Electricity Power Outage Analysis")

st.subheader("Elecricity generation dataset overview")


st.markdown('<h4>EDA summary</h4>', unsafe_allow_html=True)

st.markdown('* From the visualization and excluding the year 2022, Gas and Thermal Net Generations has seen a decline since 2014.', unsafe_allow_html=True)
st.markdown('* Hydro Net Generation (excluding the year 2022) has seen an increase since 2017 but a decrease electricity supply in 2020 and then an increase in 2021.', unsafe_allow_html=True)
st.markdown('* Wind Mill & Solar from TNEB only supplied electricity in the year 2018.', unsafe_allow_html=True)




# EDA
# To Improve speed and cache data
@st.cache(persist=True)
@st.cache(allow_output_mutation=True)
def load_data():
	df = pd.read_csv('data/electricity_generation_consolidated_supply_only.csv')
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


st.text("check for values count by type")
st.write(df['Type'].value_counts())

st.text("check for values count by name")
st.write(df['Name'].value_counts())

#check for null values
st.text("check for null values")
st.write(df[df['Net Generation(M.U)'].isna()])

# remove null values
df.dropna(inplace=True)

plt.figure(figsize = [15, 5])

#  LEFT plot: Bar plot of 'Type'

st.header("Electricity Generation Type Distribution")
fig = plt.figure(figsize=(10,5))
sns.set_style('whitegrid')
sns.countplot(x='Type',data=df)
st.pyplot(fig)
    
# RIGHT plot: Bar plot of 'Name'
st.header("Electricity Generation Places Distribution")
fig = plt.figure(figsize=(10,5))
sns.set_style('whitegrid')
sns.countplot(x='Name',data=df)
st.pyplot(fig)


image = Image.open('data/images/generation_01.png')

st.image(image, caption='The Average & Total Net Generation(M.U) By Place')

image = Image.open('data/images/generation_02.png')

st.image(image, caption='The Average & Total Net Generation(M.U) By Name')


image = Image.open('data/images/generation_03.png')

st.image(image, caption='Net Generation by Gas and Hydro')


image = Image.open('data/images/generation_04.png')

st.image(image, caption='Net Generation by Thermal')

