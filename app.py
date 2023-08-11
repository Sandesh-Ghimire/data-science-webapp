import streamlit as st
import pandas as pd
import numpy as np


data_url=("/home/rhyme/Desktop/Project/Book1.csv")


st.title("motor vechicle colliosions in new york city")

st.markdown("this app is a dashboard created by the help of streamline  to analyze motor vechicle collisioon for nyc")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
    lowercase=lambda x: str(x).lower()
    data.rename(lowercase,axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data

data=load_data(50000)


st.header("where are the most people injured in nyc")
injured_people=st.slider("number of persons injured in vechicle colliosions",0.19)
st.map(data.query("injured_persons>=@injured_people")[["latitude","longitude"]].dropna(how="any"))



st.header("how many collisions occur during the given time of the day?")
hour = st.slider("hour to look at", 0,23)
data=data[data['date/time'].dt.hour == hour]


if st.checkbox("show raw data", False):
    st.subheader('raw data')
    st.write(data)
