#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import pandas as pd
import base64
import io
from statistics import mode
import re
import yagmail

#create download link
@st.cache
def get_table_download_link(df):
    towrite = io.BytesIO()			
    csv = df.to_excel(towrite, encoding='utf-8', index=False)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings <-> bytes conversions necessary here
    #href = f'<a href="data:file/csv;base64,{b64}" download="Predictions.xlsx">Download Excel file</a>'
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="processed_data.xlsx">Download processed file</a>'
    return href

#Start of the app    
st.title('Data Cleaner')
uploaded_file = st.file_uploader("Upload a Dataset (CSV) for Processing", type="csv")

#Check if file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,encoding='cp1252')
    
    st.subheader('Raw Data')
    st.write(df)
          
    st.subheader('Processed Data')
    
    #drop necessary columns
    nulls = df.isnull().sum()
    mode_col = nulls[nulls == mode(nulls)].index[0]
    df.dropna(subset=[mode_col], inplace = True)
    
    #change date columns to datetime
    date = re.compile(r'DATE|Date|date')

    date_loc = []
    for i, col in enumerate(df.columns):
        date_col = re.search(date,col)
        if date_col:
            date_loc.append(i)
    
    for i in date_loc:
        df.iloc[:,i] = pd.to_datetime(df.iloc[:,i])
        
    st.write(df)
    
    #provide download link
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    st.markdown('Thank you for using Data Cleaner!')
    
    receiver = "akmal.nordi@cima.com.my"
    body = "Raw Data Processing app was used"

    yag = yagmail.SMTP("pythonakmal@gmail.com",st.secrets['email']['pwd'])
    yag.send(
        to=receiver,
        subject="Raw Data Processing",
        contents=body, 
    )
    
    
#provide suggestion link
link = '[Please click here if you have any suggestion for improvement or if you want to report a bug](https://forms.office.com/Pages/ResponsePage.aspx?id=BlODKFlo-E6I5KHr1GzOJEv7TmtyHRNHnUMQjktWMlhUMjlMOElYRjJES1VYVEtKN1E2RUFTQjRJVS4u)'
st.markdown(link, unsafe_allow_html=True)









