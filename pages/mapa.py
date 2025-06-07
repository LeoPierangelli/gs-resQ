import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Mapa de Pedidos", layout="wide")
st.title("Mapa de Pedidos de Ajuda")

#Verifica login
def checa_login():
    if 'usuario_logado' not in st.session_state:
        st.warning("Por favor, faça login para acessar o mapa.")
        st.stop()

# Inicializa estados

def inicializar_session_state():
    if 'pedidos_ajuda' not in st.session_state:
        st.session_state['pedidos_ajuda'] = []

    if 'historico_pedidos' not in st.session_state:
        st.session_state['historico_pedidos'] = []

    if 'busca_id' not in st.session_state:
        st.session_state['busca_id'] = None

    if 'pedido_encontrado' not in st.session_state:
        st.session_state['pedido_encontrado'] = None

# Função para criar novo pedido
def criar_pedido(tipo, descricao, latitude, longitude):
    novo_id = 1
    if st.session_state['pedidos_ajuda']:
        novo_id = max(p['id'] for p in st.session_state['pedidos_ajuda']) + 1

    novo_pedido = {
        "id": novo_id,
        "descricao": descricao,
        "tipo": tipo,
        "usuario": st.session_state['usuario_logado'],
        "latitude": latitude,
        "longitude": longitude,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "Pendente"
    }

    st.session_state['pedidos_ajuda'].append(novo_pedido)
    st.session_state['historico_pedidos'].append(novo_pedido)

# Função para buscar pedido por ID
def buscar_pedido_por_id(busca_id):
    return next((p for p in st.session_state['pedidos_ajuda'] if p['id'] == busca_id), None)

#Execução
checa_login()
inicializar_session_state()

st.write(f"Bem-vindo, {st.session_state['usuario_logado']}!")

#Colunas
col1, col2 = st.columns([2, 1])

#Mapa
with col1:
    location = streamlit_geolocation()

    if not location or location['latitude'] is None:
        st.warning("Permita o acesso à sua localização, por favor.")
        st.stop()

    latitude = location['latitude']
    longitude = location['longitude']

    mapa = folium.Map(location=[latitude, longitude], zoom_start=10)

    folium.Marker(
        [latitude, longitude],
        tooltip="Você está aqui",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(mapa)

    for pedido in st.session_state['pedidos_ajuda']:
        folium.Marker(
            [pedido["latitude"], pedido["longitude"]],
            tooltip=f"ID {pedido['id']}: {pedido['tipo']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(mapa)

    st_folium(mapa, width=600, height=600)

#Formulário
with col2:
    st.subheader("Criar Novo Pedido")

    with st.form("criar_pedido_form"):
        tipo = st.selectbox("Tipo de Pedido", ["Ajuda Médica", "Alimentos", "Roupas", "Abrigo", "Outros"])
        descricao = st.text_area("Descrição do Pedido")

        st.write("Sua localização atual:")
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")

        submitted = st.form_submit_button("Criar Pedido")

        if submitted:
            if not descricao:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                criar_pedido(tipo, descricao, latitude, longitude)
                st.success("Pedido criado com sucesso!")

#Busca por Id
st.write("### Buscar pedido por ID")
busca_id = st.number_input("Digite o ID do pedido", min_value=1, step=1)

if st.button("Buscar"):
    st.session_state['busca_id'] = busca_id
    st.session_state['pedido_encontrado'] = buscar_pedido_por_id(busca_id)

if st.session_state['busca_id'] is not None:
    pedido = st.session_state['pedido_encontrado']
    if pedido:
        geolocator = Nominatim(user_agent="resq-app")
        location_pedido = geolocator.reverse((pedido["latitude"], pedido["longitude"]))

        st.success("Pedido encontrado:")
        st.write(f"**Usuário:** {pedido['usuario']} - {pedido['data']}")
        st.write(f"**Tipo:** {pedido['tipo']}")
        st.write(f"**Descrição:** {pedido['descricao']}")
        st.write(f"**Status:** {pedido['status']}")
        st.write(f"**Endereço:** {location_pedido.address if location_pedido else 'Endereço não encontrado'}")

        if st.button("Quero ajudar"):
            pedido['status'] = "Em andamento"
            st.success("Status atualizado para 'Em andamento'.")
    else:
        st.error("Nenhum pedido encontrado com esse ID.")
