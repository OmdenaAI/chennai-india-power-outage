#Import Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

# Title and Subheader
st.title("Electricity Power Outage Analysis")

st.subheader("Dataset overview")

st.text("Consumer and Consumption dataset")


# EDA
# To Improve speed and cache data
@st.cache(persist=True)
def load_data():
	
	df = pd.read_csv ('data/electricity_consumption_consolidated.csv')
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



#check for null values
st.text("check for null values")
st.write(df.isnull())

#visualization analysis of the data
st.header("Visualization analysis of the data")
fig = plt.figure(figsize=(10,5))
sns.set_style('whitegrid')
sns.countplot(x='Category',data=df)
st.pyplot(fig)

#histogram plot by year
st.text("Histogram plot by year")
fig, ax = plt.subplots()
ax = df['Year'].hist(color='purple',bins=40,figsize=(10,4))
st.pyplot(fig)

#visual comparison between consumers and category
st.text("Comparison between consumers and category")
fig = plt.figure(figsize=(10,5))
sns.barplot(x="Category Id", y="Consumers", hue='Category',data=df)
st.pyplot(fig)

#line plot by comparing category id and consumers
#st.text("Comparing category id and consumers")
#fig, ax = plt.subplots(figsize=(9,7))
#ax = sns.relplot(data=df ,x="Category Id",y="Consumers", kind="line", markers=True)
#st.pyplot(fig)

st.title("Pairplot")
fig, ax = plt.subplots(figsize=(9,7))
fig = sns.pairplot(data=df, hue="Category")
st.pyplot(fig)

