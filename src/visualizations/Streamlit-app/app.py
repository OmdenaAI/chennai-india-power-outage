import base64
import os
import streamlit as st
import numpy as np
from PIL import  Image
from streamlit_option_menu import option_menu
import webbrowser

st.set_page_config(
    page_title="Power Outage Analysis in Chennai, Tamilnadu",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    selected = option_menu(
        menu_title='Navigation',
        options=[ "Home", "About",  "Tableau Dashboard", "Conclusion", "Team"],
        
    )


if selected == 'Home':
    
    LOGO_IMAGE = "data/Logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
          f"""
          <div class="container">
               <img class="LOGO_IMAGE" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    st.write('')
    st.subheader('PROBLEM STATEMENT')
    
    st.markdown('Our problem statement is to develop a centralized dashboard with power outage duration and places in Chennai region  for analyzing, interpretation, and visualization using AI for better decision making. This will help policymakers for taking up an action to control the outages in future more effectively & efficiently.', 
         unsafe_allow_html=True)
    
elif selected == 'About':

        
    LOGO_IMAGE = "data/Logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
          f"""
          <div class="container">
               <img class="LOGO_IMAGE" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• Power Outage in Chennai Tamilnadu Dashboard for Analysis, Interpretation and Visualization near Real Time', unsafe_allow_html=True) 
    st.markdown('• Compare Real Water Quality Parameters with Standard Water Quality Limits', unsafe_allow_html=True) 
    
    st.markdown('<h4>Locations Choosen</h4>', unsafe_allow_html=True)
    st.markdown('Installed PowerPlant Details, Generation Capacity, Outage details ',
                unsafe_allow_html=True)
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown('• Installed power plants details are extracted from satllite dataset as well as websites',unsafe_allow_html=True)
    st.markdown('• Research papers were reviewed and important points were noted for different remote sensing data used with machine learning &nbsp; and different satellite sources were revised properly.',unsafe_allow_html=True)
    st.markdown('• Various Data sources were searched in Google Earth Engine and relevant sources were selected for our use-case.',unsafe_allow_html=True)
    st.markdown('• Extracted the power outage details  .',unsafe_allow_html=True)
    st.markdown('• Various Machine learning models were applied on the final dataframe and the metrics were analysed and the best model was &nbsp; &nbsp; chosen with having a good validation accuracy.',unsafe_allow_html=True)
    st.markdown('• A visualisation dashboard is created for the public to enter coordinates, their region of interest(water-body) and the data range to &nbsp; get the outage details for that area along with data visualisation of the collected data from the satellites.',unsafe_allow_html=True)

    
elif selected == 'Tableau Dashboard':
        
    LOGO_IMAGE = "data/Logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
          f"""
          <div class="container">
               <img class="LOGO_IMAGE" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    st.subheader('Tableau Dashboard')

    url = 'https://public.tableau.com/app/profile/sudhakar.reddy7432/viz/TamilnaduEnergyDashboard/TNEnergyDB?publish=yes'

    if st.button('Open Tableau'):
        webbrowser.open_new_tab(url)
   
elif selected == 'Conclusion':
        
    LOGO_IMAGE = "data/Logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
          f"""
          <div class="container">
               <img class="LOGO_IMAGE" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    st.subheader('TECH STACK')

    st.markdown('• Data Collection - Google Earth Datasets, Beautiful Soup, Selenium, public datasets () , websites', unsafe_allow_html=True)
    st.markdown('• EDA - ', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• Machine Learning - Python, Jupyter Notebooks, Time Series', unsafe_allow_html=True) 
    st.markdown('• Dashboard - Streamlit, Tableau', unsafe_allow_html=True) 

    st.subheader('PROJECT SUMMARY')

    st.markdown('', unsafe_allow_html=True) 
    st.markdown('• India is currently undergoing the worst electricity shortage in more than six years. The science behind these ongoing power cuts is simple — increased demand and decreased supply..', unsafe_allow_html=True) 
    st.markdown('• We Collected and pre-processed the historical power generation data for the last few years. We alos Prepared the EDA to understand the co-relation of data. An interactive Plot /Map displaying the relation between supply Vs demand.', unsafe_allow_html=True) 
    st.markdown('• We used time series models to analyse the trend, and plotted the outage details in Chennai . So these could help policymakers to take measures/steps could be supportive to face the challenges in future..', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('We have created a centralized dashboard to understand the power plants details, generation capacity and power outages. This would help in addressing the issues so as to give immediate attention to the plociymakers', unsafe_allow_html=True)

elif selected == 'Team':
        
    LOGO_IMAGE = "data/Logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
          f"""
          <div class="container">
               <img class="LOGO_IMAGE" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    st.subheader('COLLABORATORS')

    st.markdown('• <a href="https://www.linkedin.com/in/vignesh-kanagasabapathi/">Vignesh</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/renju-zachariah-30982247/">Sudhakar</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/ishita-kheria-20b1b31ab/">Christian</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/sairam-kannan-8648a0138/">Deepa</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/prathima-kadari/">Alagu Prakalya</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/himanshu-mishra-851459b5/">Kirthi</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/himanshu-mishra-851459b5/">Vaishnavi</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/bharati-panigrahi-10a9461a0/">Srivatsan</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/deepali-bidwai/">Abhay</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Arpita</a>',
                unsafe_allow_html=True)  
    st.markdown('• <a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Ruslan</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Saurabh Shetty</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Alice</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="">Sanjay Santhakumar</a>',
                unsafe_allow_html=True)
    

    st.subheader('PROJECT MANAGER')

    st.markdown('• <a href="https://www.linkedin.com/in/meenakshiramaswamy/">Meenakshi Ramaswamy</a>', unsafe_allow_html=True)



