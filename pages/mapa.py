import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium



st.title("Mapa")
st.write(f"Bem-vindo, {st.session_state['usuario_logado']}!")

location = streamlit_geolocation()

if location['latitude'] is None or location['latitude'] == []:
    st.warning("permita o acesso a sua localização, por favor")
    st.stop()

if location:
    latitude = location['latitude']
    longitude = location['longitude']

    # Cria o mapa centrado na localização do usuário
    mapa = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Adiciona um marcador para a localização do usuário
    folium.Marker(
        [latitude, longitude],
        tooltip="Você está aqui",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(mapa)

    # Adiciona os marcadores ao mapa
    for pedido in st.session_state['pedidos_ajuda']:
        folium.Marker(
            [pedido["latitude"], pedido["longitude"]],
            tooltip=pedido["descricao"],
            icon=folium.Icon(color="red", icon="user")
        ).add_to(mapa)

    st_folium(mapa, width=600, height=600)

