import streamlit as st
import numpy as np
import pandas as pd
#import plotly.express as px
import os
from random import sample
#import textstat
#import pickle
#import sklearn.linear_model
import gspread
#from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive

#@st.cache_data
def load_data(paths):
    res = []
    for path in paths:
        ds = pd.read_csv(path, sep = ',',  header = 0)
        res.append(ds)
    
    return res
    
def button_pressed(side):
    if side == 'left':
        st.write("You chose the left one")
    else: st.write("You chose the right one")
    
#@st.cache_data
def connect_google(url):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file('gatech-group-project-2ea6ba5df261.json', scopes=scopes)
    gc = gspread.authorize(credentials)

    # open a google sheet
    gs = gc.open_by_url(url)
    return gs
    
def log_result(more_useful_id, less_useful_id, gs, d):
    df = pd.DataFrame({'more_useful':more_useful_id, 'less_useful':less_useful_id, 'dataset': d}, index=[0])
    df_values = df.values.tolist()
    gs.values_append('Sheet1', {'valueInputOption': 'RAW'}, {'values': df_values})

gs = connect_google('https://docs.google.com/spreadsheets/d/1-bwdZxKpnV1BIMLRDLEAUUChbYeXJJKiAqVv1Jhzvco')
    
#st.text(os.getcwd())
datasets = load_data(['ta_text_sample.csv','yelp_cinema_text_sample.csv', 'yelp_hotel_text_sample.csv', 'yelp_restaurant_text_sample.csv' ])

d = np.random.randint(low = 0, high = 3)

ds = datasets[d]

industries = ['hotel', 'cinema','hotel','restaurant']
industry = industries[d]

st.title('Which of these reviews you find more helpful?')
#st.write('This is a review for a ', industry)

#get review 1
i = np.random.randint(low = 0, high = 999)
#st.write('Chose review number ', i)
left_review_id = ds.loc[i]['review_id']
left_review_text = ds.loc[i]['text']
#st.write(left_review_id)
#st.write(left_review_text)
#st.write(max(ta_gunning))

#get review 2
j = np.random.randint(low = 0, high = 999)
#st.write('Chose review number ', j)
right_review_id = ds.loc[j]['review_id']
right_review_text = ds.loc[j]['text']

#layout
col1, col2 = st.columns(2)
col1.header("Review 1")
if col1.button("This one!",key='left_button'):
     #console.log('You chose the left one')
     log_result(left_review_id, right_review_id, gs, d)
col1.markdown(left_review_text)

col2.header("Review 2")
#col2.button("This one!", key = 'right_button')#, on_click = button_pressed('right'))
if col2.button("This one!",key='right_button'):
     #console.log('You chose the right one')
     log_result(right_review_id, left_review_id, gs, d)
col2.markdown(right_review_text)

