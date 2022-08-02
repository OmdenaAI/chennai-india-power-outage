#!/usr/bin/env python
# coding: utf-8


# Streamlit visualization of Chennai power outage using XGBoost - done by Sriparna


##Import Libraries
import pandas as pd
import numpy as np
import pickle
import streamlit as st
import prophet
import plotly.figure_factory as ff
import plotly.graph_objs  as go

from numpy import asarray
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from matplotlib import pyplot



#loading the raw data
daily_load_shedding_df = pd.read_csv('data/dayly_load_shedding_schedule_chennai_2014_2022.csv')
demand_supply_monthly_df = pd.read_csv('data/demand_supply_monthly.csv')
demand_supply_yearly_df= pd.read_csv('data/demand_supply_yearly.csv')
electricity_consumption_df = pd.read_csv('data/electricity_consumption_consolidated.csv')
electricity_generation_df = pd.read_csv('data/electricity_generation_consolidated_supply_only.csv')


# ## Questions to be addressed
# <b> Build a model to predict the following based on the month-wise energy consumption pattern in Tamil Nadu, India data collected    <br>
# 1) Predict the Requirements (MU/Day)   <br>
# 2) Requirement(MU)   <br>
# 3) Requirement(MW)   <br>
# 4) Predict the Peak_Demand_Met5(MW) for future months
# </b>
# <br> <br> MU means Million units of electricity. One unit of electricity is one Kilowatt per hour. One Kilowatt are a thousand Watts.
# <br><br>
# MW - Megawatts are basic to understanding electricity planning concepts. Watts (W) are the yardstick for measuring power. A one hundred watt light bulb, for example, is rated to consume one hundred watts of power when turned on. If such a light bulb were on for four hours it would consume a total of 400 watt-hours (Wh) of energy. Watts, therefore, measure instantaneous power while watt hours measure the total amount of energy consumed over a period of time.
# <br><br>
# A megawatt (MW) is one million watts and a kilowatt (kW) is one thousand watts. Both terms are commonly used in the power business when describing generation or load consumption. For instance, a 100 MW rated wind farm is capable of producing 100 MW during peak winds, but will produce much less than its rated amount when winds are light.
# <br><br>
# The ratio of a power plant’s average production to its rated capability is known as capacity factor. Load factor generally, on the other hand, is calculated by dividing the average load by the peak load over a certain period of time. If the residential load at a utility averaged 5,000 MW over the course of a year and the peak load was 10,000 MW, then the residential customers would be said to have a load factor of 50 percent (5,000 MW average divided by 10,000 MW peak).

# In[30]:


# Collecting only the required columns
df_temp = demand_supply_monthly_df[['Requirement(MU/DAY)', 'Energy_met(MU/DAY)', 'Requirement(MU)', 
                                    'Energy_met(MU)','Requirement(MW)', 'Peak_Demand_Met5(MW)','year', 'month']]


# In[31]:


df_temp['date'] = pd.to_datetime(df_temp['year'].apply(str)+'-'+df_temp['month'].apply(str)+'-'+str(1), format='%Y-%m-%d')


# In[32]:


df_temp.sort_values('date', inplace=True)


# In[33]:


df_temp1 = df_temp[['date','Peak_Demand_Met5(MW)']]

df_temp1.set_index('date', inplace=True)


# In[34]:


df = df_temp1


# In[35]:


# First-order difference
df['Peak_Demand_Met5_MW_diff1'] = df['Peak_Demand_Met5(MW)'].diff(periods=1)
df = df.dropna()


# In[36]:


# Second-order difference
df['Peak_Demand_Met5_MW_diff2'] = df['Peak_Demand_Met5(MW)'].diff(periods=2)
df = df.dropna()


# ## Training using XGBoost

# In[37]:


#restructuring this time series dataset as a supervised learning problem by using the value at the previous time step to predict the value at the next time-step.
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols = list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    # put it all together
    agg = concat(cols, axis=1)
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg.values


# In[38]:


# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    return data[:-n_test, :], data[-n_test:, :]


# In[39]:


# fit an xgboost model and make a one step prediction
def xgboost_forecast(train, testX):
    # transform list into array
    train = asarray(train)
    # split into input and output columns
    trainX, trainy = train[:, :-1], train[:, -1]
    # fit model
    model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
    pickle.dump(model, open('Peak_Demand_Met5.pkl','wb'))
    model.fit(trainX, trainy)
    # make a one-step prediction
    yhat = model.predict([testX])
    return yhat[0]


# In[40]:


def walk_forward_validation(data, n_test):
    predictions = list()
    # split dataset
    train, test = train_test_split(data, n_test)
    # seed history with training dataset
    history = [x for x in train]
    # step over each time-step in the test set
    for i in range(len(test)):
        # split test row into input and output columns
        testX, testy = test[i, :-1], test[i, -1]
        # fit model on history and make a prediction
        yhat = xgboost_forecast(history, testX)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        history.append(test[i])
        # summarize progress
       # print('>expected=%.1f, predicted=%.1f' % (testy, yhat))
    # estimate prediction error
    error = mean_absolute_error(test[:, -1], predictions)
    return error, test[:, 1], predictions


# In[41]:


df1 = df[['Peak_Demand_Met5(MW)']]

df2 = df[['Peak_Demand_Met5_MW_diff1']]

df3 = df[['Peak_Demand_Met5_MW_diff2']]


# In[42]:


# loading in the model to predict Peak_Demand_Met5_MW and other required features on the data
#pickle_in = open('Peak_Demand_Met5.pkl', 'rb')
#classifier = pickle.load(pickle_in)

def prediction(df,lb):
    
    series = df

    values = series.values
# transform the time series data into supervised learning
    data = series_to_supervised(values, n_in=6)
# evaluate
    mae, y, yhat = walk_forward_validation(data, 12)
   # st.write(mae)
    # plot expected vs preducted
    f=pyplot.figure()
    pyplot.plot(y, label='Expected '+lb)
    pyplot.plot(yhat, label='Predicted '+lb)
 #   pyplot.title(titlename)
    pyplot.legend()
    st.pyplot(f)
  #  pyplot.show()


# In[ ]:


# this is the main function in which we define our webpage 
def main():
# giving the webpage a title
   # st.title("Prediction of Energy Consumption using XGBoost Model")

# here we define some of the front end elements of the web page like 
# the font and background color, the padding and the text to be displayed
    html_temp = """
    <div style ="background-color:yellow;padding:8px">
    <h1 style ="color:black;text-align:center;">Prediction of Energy Consumption using XGBoost Model </h1>
    </div>
    """
      
# this line allows us to display the front end aspects we have 
# defined in the above code
# this line allows us to display the front end aspects we have 
# defined in the above code
    st.markdown(html_temp, unsafe_allow_html = True)

# 
    pd_mw_1 = st.sidebar.checkbox("Show prediction of Peak Demand in MW", True)
    pd_mu_2 = st.sidebar.checkbox("Show prediction of Requirements MU/day", False)
    pd_mu_3 = st.sidebar.checkbox("Show prediction of Requirement(MU)", False)
    pd_mw_4 = st.sidebar.checkbox("Show prediction of Requirement(MW)", False)

    if pd_mw_1:
       # st.subheader("Prediction of Peak Demand in MW")
        st.empty()
        prediction(df1,'Peak Demand in MW')
        
    if pd_mu_2:
    #    if "selected" in st.session_state:
   #         del st.session_state.selected
        df4 = df_temp[['date','Requirement(MU/DAY)']]
        df4.set_index('date', inplace=True)
        prediction(df4,'Requirement(MU/DAY)')
    
    if pd_mu_3:
        st.empty()
        df5 = df_temp[['date','Requirement(MU)']]
        df5.set_index('date', inplace=True)
        prediction(df5,'Requirement(MU)')
        
    if pd_mw_4:
        st.empty()
        df6 = df_temp[['date','Requirement(MW)']]
        df6.set_index('date', inplace=True)
        prediction(df6,'Requirement(MW)')
        
        
if __name__=='__main__':
    main()


# In[ ]:




