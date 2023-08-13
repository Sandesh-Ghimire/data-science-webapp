import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

data_url=("/home/rhyme/Desktop/Project/Book1.csv")


st.title("Motor vechicle colliosions in new york city")

st.markdown("This app is a dashboard created by the help of streamline  to analyze motor vechicle collisioon for nyc")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
    lowercase=lambda x: str(x).lower()
    data.rename(lowercase,axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data

data=load_data(50000)


st.header("Where are the most people injured in nyc")
injured_people=st.slider("Number of persons injured in vechicle colliosions",0.19)
st.map(data.query("injured_persons>=@injured_people")[["latitude","longitude"]].dropna(how="any"))



st.header("How many collisions occur during the given time of the day?")
hour = st.slider("Hour to look at", 0,23)
data=data[data['date/time'].dt.hour == hour]


st.markdown("Vehicle collisions between %i:00 and %i:00" %(hour,(hour +1)%24))
midpoint= (np.average(data['latitude']),np.average(data['longitude']))


st.write(pdk.crash_date_crash_time(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
))






if st.checkbox("Show raw data", False):
    st.subheader('Raw data')
    st.write(data)
