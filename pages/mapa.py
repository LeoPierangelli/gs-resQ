import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.title("Mapa")
st.write(f"Bem-vindo, {st.session_state['usuario_logado']}!")

# Localização atual do usuário
location = streamlit_geolocation()
latitude = location['latitude']
longitude = location['longitude']

if latitude is None or latitude == []:
    st.warning("permita o acesso a sua localização, por favor")
    st.stop()

# Inicializa o mapa
mapa = folium.Map(location=[latitude, longitude], zoom_start=10)

# Marcador do usuário
folium.Marker(
    [latitude, longitude],
    tooltip="Você está aqui",
    icon=folium.Icon(color="blue", icon="user")
).add_to(mapa)

# Marcadores dos pedidos de ajuda
for pedido in st.session_state['pedidos_ajuda']:
    folium.Marker(
        [pedido["latitude"], pedido["longitude"]],
        tooltip=f"ID {pedido['id']}: {pedido['descricao']}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)

# Exibe o mapa na tela
st_folium(mapa, width=600, height=600)

# Barra de busca por ID
st.write("### Buscar pedido por ID")
busca_id = st.number_input("Digite o ID do pedido", min_value=1, step=1)
if st.button("Buscar"):
    pedido_encontrado = next((p for p in st.session_state['pedidos_ajuda'] if p['id'] == busca_id), None)

    if pedido_encontrado:
        st.success("Pedido encontrado:")
        st.write(f"**Usuário:** {pedido_encontrado['usuario']}")
        st.write(f"**Categoria:** {pedido_encontrado['categoria']}")
        st.write(f"**Descrição:** {pedido_encontrado['descricao']}")

        # Obter endereço a partir da latitude e longitude do pedido
        geolocator = Nominatim(user_agent="resq-app")
        location_pedido = geolocator.reverse((pedido_encontrado["latitude"], pedido_encontrado["longitude"]))

        if location_pedido:
            st.write(f"**Endereço:** {location_pedido.address}")
        else:
            st.write("Endereço não encontrado.")
    else:
        st.error("Nenhum pedido encontrado com esse ID.")
