import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

import plotly.express as px

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
original_data = data # can be used to filter later as its original data.

st.header("Where are the most people injured in nyc")
injured_people=st.slider("Number of persons injured in vechicle colliosions",0.19)
st.map(data.query("injured_persons>=@injured_people")[["latitude","longitude"]].dropna(how="any"))



st.header("How many collisions occur during the given time of the day?")
hour = st.slider("Hour to look at", 0,23)
data=data[data['date/time'].dt.hour == hour]


st.markdown("Vehicle collisions between %i:00 and %i:00" %(hour,(hour +1)%24))
midpoint= (np.average(data['latitude']),np.average(data['longitude']))


st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },

layers=[
    pdk.Layer(
        "HexagonLayer",
        data = data[['date/time','latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius=100,
        extruded=True,  #changes to 3D if set to false map will be 2d.
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
    ),
],

))


st.subheader("Breakdown by minute between %i:00 and %i:00" %(hour,(hour +1)%24))
filtered = data[
    (data['data/time'].dt.hour>=hour)&(data['data/time'].dt.hour<(hour+1))

]
hist=np.histogram(filtered['data/time'].dt.minute, bins=60 , range=(0,60))[0]

chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar (chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)



st.header("top 5 dangerous streets by affected people")
select = st.selectbox('Affected type of people', hover_data=['minute','crashes'],height=400)

if select=='Pedestrians':
    st.write(original_data.query("injured_pedestrains>=1")[["on_street_name","injured_pedestrains"]].sort_values(by=['injured_pedestrains'],ascending=False).dropna(how='any')[:5])


elif select=='Cyclists':
    st.write(original_data.query("injured_cyclists>=1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'],ascending=False).dropna(how='any')[:5])


else:
    st.write(original_data.query("injured_motorists>=1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'],ascending=False).dropna(how='any')[:5])


if st.checkbox("Show raw data", False):
    st.subheader('Raw data')
    st.write(data)
