# Basics
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 1000)
from datetime import datetime as dt
import itertools
import pickle
import streamlit as st
import prophet
from PIL import Image


# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
from statsmodels.tsa.seasonal import seasonal_decompose

# Time-Series statsmodels
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Testing
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error

# Warnings
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning, ValueWarning
warnings.simplefilter('ignore', ConvergenceWarning)
warnings.simplefilter('ignore', ValueWarning)



st.title('Time Series Forecasting Using Streamlit')

# load in outage data as df
df = pd.read_csv('data/demand_supply_monthly.csv')
df.head()
st.write('Dataset overview')
st.write(df.head())

#create unique dates using year and month column
df['year']=df['year'].astype(str)
df['month']=df['month'].astype(str)
df['ts_date'] = df[['year', 'month']].agg('-'.join, axis=1)
df['ts_date'] = pd.to_datetime(df['ts_date'], format = '%Y-%m')

# set index
df = df.set_index(['ts_date'])

# delete all extra columns from the dataframe
ts = df.drop(columns=['Requirement(MU/DAY)', 'Energy_met(MU/DAY)',
       'Surplus(+)/Deficit(-)(MU/DAY)', 'Requirement(MW)',
       'Peak_Demand_Met5(MW)', 'Surplus(+)/Deficit(-)(MW)', '%Shortage(MW)',
       'name_report', 'year', 'month', 'date_published', 'month_published',
       'year_published'])

# Sort and reset index
ts = ts.sort_index()

# visualize the time series 
st.subheader("Outage per Month")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ts.index, ts['Surplus(+)/Deficit(-)(MU)'])
st.pyplot(fig)

timeperiod = ts[ts.index > '2018-12-01']
timeperiod


fig, ax = plt.subplots(figsize=(10, 5))
timeperiod = ts[(ts.index > '2018-12-01') & (ts.index < '2020-01-01')]
ax.plot(timeperiod.index, timeperiod['Surplus(+)/Deficit(-)(MU)'])
ax.set_title('Outage per Month')
ax.set_ylabel('Outage')
st.pyplot(fig)

# create time series data with only date as index and Surplus/Deficit as the only column
st.write('create time series data with only date as index and Surplus/Deficit as the only column')
ts_new = ts['Surplus(+)/Deficit(-)(MU)']
ts_new

# lineplot
st.write('Lineplot')
ts_new.plot(figsize=(15,10))
st.pyplot(fig)

# Generate a box and whiskers plot for ts_new dataframe to see the distribution over time

year_groups = ts_new[(ts_new.index>'2012-12-01') & (ts_new.index<'2022-01-01')].groupby(pd.Grouper(freq='A'))
ts_annual = pd.DataFrame()

for yr, group in year_groups:
    ts_annual[yr.year] = group.values.ravel()

ts_annual
st.write('Generate a box and whiskers plot for ts_new dataframe to see the distribution over time')
fig = plt.figure(figsize=(10,6))
ts_annual.boxplot()
st.pyplot(fig)

#Time Series Decomposition
st.subheader('Time Series Decomposition')
# Decompose it!
decomposition = seasonal_decompose(ts_new)
decomposition
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
trend
decomposition.observed


image = Image.open('data/images/time_01.png')
st.image(image, caption='There is the seasonality component in the data;')

# Drop NaN values from residuals.

ts_log_decompose = residual
ts_log_decompose.dropna(inplace=True)



##Modeling
st.subheader('Modeling')
# find the index which allows us to split off 20% of the data
cutoff = round(ts_new.shape[0]*0.8)
cutoff

# Define train and test sets according to the index found above
train = ts_new[:cutoff]

test = ts_new[cutoff:]

# Plot it!
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(train, label='train')
ax.plot(test, label='test')
ax.set_title('Train-Test Split')
st.pyplot(fig)

train

# TimeSeriesSplit
split = TimeSeriesSplit()

for train_ind, val_ind in split.split(train):
    st.write(f'Train index: {train_ind}')
    st.write(f'Test  index: {val_ind}')

baseline = pd.DataFrame(np.hstack((train.values.reshape(-1, 1),
                       train.shift().values.reshape(-1, 1),
                       train.shift(periods=2).values.reshape(-1, 1))),
             columns=['orig', 'shifted_one_period', 'shifted_two_periods'])
baseline.head()

# line plot of the baseline model



image = Image.open('data/images/time_02.png')
st.image(image, caption='line plot of the baseline model')

# testing with rmse

rms_shift1 = mean_squared_error(baseline['orig'][1:], baseline['shifted_one_period'][1:], squared=False)
rms_shift2 = mean_squared_error(baseline['orig'][2:], baseline['shifted_two_periods'][2:], squared=False)
st.write('rms_shift1:')
rms_shift1
st.write('rms_shift1:')
rms_shift2

#ARIMA Model
st.subheader('ARIMA Model')

# ar_1 model with differencing
ar_1 = ARIMA(train, order=(1, 1, 0)).fit()

# We put a typ='levels' to convert our predictions to remove the differencing performed.
ar_1.predict(typ='levels')

# summary of ar_1
st.write(ar_1.summary())

random_walk_model = ARIMA(train, order=(0, 1, 0)).fit()
st.subheader('Random walk model')
st.write(random_walk_model.summary())

# Baseline ARIMA model
st.subheader('Baseline ARIMA model')
baseline_ar = ARIMA(train, order=(0,0,0)).fit()
bl_preds = baseline_ar.predict(typ='levels')
bl_rmse = np.sqrt(mean_squared_error(train, bl_preds))
baseline_ar.summary()

bl_preds

st.write(f'Baseline AIC: {baseline_ar.aic}')
st.write(f'Random Walk AIC: {random_walk_model.aic}')
st.write(f'AR(1, 1, 0) AIC: {ar_1.aic}')

y_hat_ar1 = ar_1.predict(typ='levels')
ar1_rmse = np.sqrt(mean_squared_error(train, y_hat_ar1))
y_hat_rw = random_walk_model.predict(typ='levels')
rw_rmse = np.sqrt(mean_squared_error(train, y_hat_rw))

st.write(f'Baseline RMSE:    {bl_rmse}')
st.write(f'Random Walk RMSE: {rw_rmse}')
st.write(f'AR1 RMSE:         {ar1_rmse}')

#Cross-Validation
st.subheader('Cross-Validation')

train.index
train_with_ind = train.reset_index()
for train_ind, val_ind in split.split(train_with_ind):
    ar = ARIMA(endog=train_with_ind.iloc[train_ind, -1], order=(1, 1, 0)).fit()
    preds = ar.predict(typ='levels', start=val_ind[0], end=val_ind[-1])
    true = train_with_ind.iloc[val_ind, -1]
    st.write(np.sqrt(mean_squared_error(true, preds)))


st.subheader('SRIMAX Modeling')
p = q = range(0, 2)
pdq = list(itertools.product(p, [1], q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, [1], q))]
print('Examples of parameter for SARIMA...')
for i in pdq:
    for s in seasonal_pdq:
        st.write('SARIMAX: {} x {}'.format(i, s))


for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod=SARIMAX(train,
                         order=param,
                         seasonal_order=param_seasonal,
                         enforce_stationarity=False,
                         enforce_invertibility=False, freq=train.index.inferred_freq)
            results = mod.fit()
            st.write('ARIMA{}x{} - AIC:{}'.format(param,param_seasonal,results.aic))
        except: 
            st.write('Oops!')
            continue

sari_mod =SARIMAX(train,
                  order=(0, 1, 1),
                  seasonal_order=(1, 1, 1, 12),
                  enforce_stationarity=False,
                  enforce_invertibility=False).fit()

for train_ind, val_ind in split.split(train_with_ind):
    sarimax = SARIMAX(endog=train_with_ind.iloc[train_ind, -1],
                      order=(0, 1, 1),
                     seasonal_order=(1, 1, 1, 12),
                     enforce_stationarity=False,
                     enforce_invertibility=False).fit()
    preds = sarimax.predict(typ='levels', start=val_ind[0], end=val_ind[-1])
    true = train_with_ind.iloc[val_ind, -1]
    st.write(np.sqrt(mean_squared_error(true, preds)))


y_hat_train = sari_mod.predict(typ='levels')
y_hat_test = sari_mod.predict(start=test.index[0], end=test.index[-1],typ='levels')

fig, ax = plt.subplots()
ax.plot(train, label='train')
ax.plot(test, label='test')
ax.plot(y_hat_train, label='train_pred')
ax.plot(y_hat_test, label='test_pred')

st.pyplot(fig)

# Let's zoom in on test
fig, ax = plt.subplots()

ax.plot(test, label='true')
ax.plot(y_hat_test, label='pred')

st.pyplot(fig)

np.sqrt(mean_squared_error(test, y_hat_test))

st.subheader('Forecast with final model')
sari_mod = SARIMAX(ts_new,
                  order=(0, 1, 1),
                  seasonal_order=(1, 1, 1, 12),
                  enforce_stationarity=False,
                  enforce_invertibility=False).fit()

forecast = sari_mod.forecast(steps=12)

fig, ax = plt.subplots()
ax.plot(ts_new, label='so_far')
ax.plot(forecast, label='forecast')
ax.set_title('Power outage in Tamilnadu\n One Year out')

st.pyplot(fig)
