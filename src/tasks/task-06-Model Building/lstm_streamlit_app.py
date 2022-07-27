import pickle
import streamlit as st
import pandas as pd
import numpy as np

filename = 'finalized_lstm_model.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))


st.title('Peak Demand LSTM Regressor Web App')
st.write('This is a web app to predict the Peak Demand for the next month, provided we have last 5 peak demand of electricity in Chennai. After that, click on the Predict button at the bottom to\
        see the prediction of the regressor.')

val1 = float(st.text_input(label='Power Demand 1', value="14501"))
val2 = float(st.text_input(label='Power Demand 2', value="15290"))
val3 = float(st.text_input(label='Power Demand 3', value="16262"))
val4 = float(st.text_input(label='Power Demand 4', value="17196"))
val5 = float(st.text_input(label='Power Demand 5', value="17563"))


features = np.asarray([val1, val2, val3, val4, val5])
print(features)

# features = agg['var1(t)'].to_numpy()[115:120]
# features = np.asarray([14501., 15290., 16262., 17196., 17563.])

features_df  = pd.DataFrame([features])

st.table(features_df) 

if st.button('Predict'):
    #x_input = features_df.reshape(1, n_steps, n_features)
    
    yhat = loaded_model.predict(features_df, verbose=0)

        
    st.write(' Based on feature values, the peak demand load is '+ str(int(yhat)))
    
    
#streamlit run streamlit_app.py

