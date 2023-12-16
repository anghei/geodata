import csv

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


# for _, r in msk.iterrows():
#     sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001)
#     geo_j = sim_geo.to_json()
#     geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
#     folium.Popup(r["name"]).add_to(geo_j)
#     geo_j.add_to(total)


action = st.radio('Выберите действие:',
                 ['Отобразить все ТТ на карте', 'Выбрать ТТ из списка'],
                  index=None)

if action == 'Выбрать ТТ из списка':
    option = st.selectbox(
        label='',
        placeholder='Укажите ТТ',
        options=[records[idx]['name_TT'] for idx in range(len(records))],
        index=0
    )
    lat = [records[idx]['latitude'] for idx in range(len(records)) if records[idx]['name_TT'] == option][0]
    lon = [records[idx]['longitude'] for idx in range(len(records)) if records[idx]['name_TT'] == option][0]

    exact = folium.Map(
        location=[lat, lon],
        zoom_start=15
    )

    folium.Marker(
        (lat, lon),
        popup=option).add_to(exact)

    st.write('Вы выбрали: ', option)
    st.title(f'Расположение {option}')
    st_folium(exact, width=700)

elif action == 'Отобразить все ТТ на карте':
    total = folium.Map(
        location=msk_centroid,
        zoom_start=10
    )

    for record in records:
        coords = (record['latitude'], record['longitude'])
        folium.Marker(coords, popup=record['name_TT']).add_to(total)

    st.write('Вы выбрали отображение всех ТТ. Это может занять некоторое время')
    st.title('Распределение ТТ, Москва')
    st_folium(total, width=700)
else:
    pass