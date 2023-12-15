import csv

import pandas as pd
import geopandas as gpd

import folium
import streamlit as st
from streamlit_folium import st_folium


keys = ('name_TT', 'latitude', 'longitude')
records = []

msk_centroid = [55.751244, 37.618423]

with open('data/tt_msk.csv', encoding='utf-8') as tt:
    reader = csv.DictReader(tt)
    for row in reader:
        records.append({key: row[key] for key in keys})

msk = gpd.read_file('data/msk.json')
# msk = msk.fillna('-')

# msk = msk[msk['official_status'].str.contains("ru:внутригородская территория города федерального значения")][['name', 'geometry']]

m = folium.Map(
    location=msk_centroid,
    zoom_start=10
)

for _, r in msk.iterrows():
    sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
    folium.Popup(r["name"]).add_to(geo_j)
    geo_j.add_to(m)

for record in records:
    coords = (record['latitude'], record['longitude'])
    folium.Marker(coords, popup=record['name_TT']).add_to(m)

st.title('Распределение ТТ, Москва')
st_folium(m, width=700)
