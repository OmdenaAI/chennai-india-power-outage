import pickle
import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

filename = 'pages/finalized_lstm_model.sav'

df_peak_demand = pd.read_csv('data/peak_demand_5features.csv', index_col=0)

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))


st.title('Peak Demand LSTM Regressor Web App')
st.write('This is a web app to predict the Peak Demand for the next month, provided we have last 5 peak demand of electricity in Chennai. After that, click on the Predict button at the bottom to\
        see the prediction of the regressor.')

val1 = int(st.selectbox('Year', ('2019', '2020', '2021','2022')))
val2 = int(st.selectbox('Month', ('1', '2', '3','4','5','6','7','8','9','10','11','12')))


# val1 = int(st.text_input(label='Year', value="2022"))
# val2 = int(st.text_input(label='Month', value="01"))
# val3 = float(st.text_input(label='Power Demand 3', value="16262"))
# val4 = float(st.text_input(label='Power Demand 4', value="17196"))
# val5 = float(st.text_input(label='Power Demand 5', value="17563"))

# features = np.asarray([val1, val2, val3, val4, val5])
# print(features)

# features = agg['var1(t)'].to_numpy()[115:120]
# features = np.asarray([14501., 15290., 16262., 17196., 17563.])

import datetime
# year = '2022'
# month = '01'
year = str(val1)
month = str(val2)

format = "%Y-%m" 
index = year+"-"+month
ind = str(datetime.datetime.strptime(index, format).date())
features_df  = df_peak_demand[df_peak_demand.index==ind].drop(df_peak_demand.columns[[df_peak_demand.shape[1]-1]], axis=1)
# features_df  = df_peak_demand[df_peak_demand.index==ind].drop(df_peak_demand.columns[[5]], axis=1)

st.table(features_df) 

if st.button('LSTM Predict '):
    #x_input = features_df.reshape(1, n_steps, n_features)
    
    yhat = loaded_model.predict(features_df, verbose=0)

        
    st.write(' Based on feature values, the peak demand load is '+ str(int(yhat)))
    
    
    
    
######################################################################################    

st.title('Peak Demand Auto Regressor Web App')
    
filename = 'pages/finalized_ar1_model.sav'

# loaded_ar_model=pickle.load(open(filename, 'rb'))

# load
with open(filename, 'rb') as f:
    loaded_ar_model = pickle.load(f)

start_year = (st.text_input(label='Start Year', value="2022"))
start_month = (st.text_input(label='Start Month', value="01"))
#format = "%Y-%m" 
start_index = start_year+"-"+start_month
start_index = str(datetime.datetime.strptime(start_index, format).date())

end_year = (st.text_input(label='End Year', value="2022"))
end_month = (st.text_input(label='End Month' , value="08"))
#format = "%Y-%m" 
end_index = end_year+"-"+end_month
end_index = str(datetime.datetime.strptime(end_index, format).date())

print('start_index: {}'.format(start_index))
print('end_index: {}'.format(end_index))

actual_df = pd.read_csv('data/train_data_peak_demand.csv', index_col=0 )
actual_df.index = pd.to_datetime(actual_df.index)

start = '2012-05-01' #YYY-MM-DD

dates = pd.date_range(start, periods=150, freq='MS')
start_val = (dates == pd.Timestamp(start_index)).argmax()
end_val = (dates == pd.Timestamp(end_index)).argmax()

print('start_val: {}'.format(start_val))
print('end_val: {}'.format(end_val))


if st.button('AR Predict '):
    pred = loaded_ar_model.predict(start_val, end_val)
    pred_df  = pd.DataFrame([pred])
    st.table(pred_df)
    pred_df = pred_df.T
    act_df = pd.concat([actual_df,pred_df], axis=1)
    act_df.columns=['actual_demand','predicted_demand']
    act_df["actual_demand"].fillna(0.0, inplace = True)
    act_df["predicted_demand"].fillna(0.0, inplace = True)
    st.bar_chart(act_df)
    st.line_chart(act_df)


#streamlit run streamlit_app.py

