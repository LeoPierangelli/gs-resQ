import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim

st.title("Mapa")

# Verificar se o usuário está logado
if 'usuario_logado' not in st.session_state:
    st.warning("Por favor, faça login para acessar o mapa.")
    st.stop()

st.write(f"Bem-vindo, {st.session_state['usuario_logado']}!")

# Criar duas colunas: uma para o mapa e outra para o formulário
col1, col2 = st.columns([2, 1])

with col1:
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
                tooltip=f"ID {pedido['id']}: {pedido['descricao']}",
                icon=folium.Icon(color="red", icon="user")
            ).add_to(mapa)

        st_folium(mapa, width=600, height=600)

with col2:
    st.subheader("Criar Novo Pedido")
    
    # Formulário para criar pedido
    with st.form("criar_pedido_form"):
        titulo = st.text_input("Título do Pedido")
        descricao = st.text_area("Descrição do Pedido")
        tipo = st.selectbox(
            "Tipo de Pedido",
            ["Ajuda Médica", "Alimentos", "Roupas", "Abrigo", "Outros"]
        )
        
        # Mostrar localização atual
        st.write("Sua localização atual:")
        st.write(f"Latitude: {location['latitude']}")
        st.write(f"Longitude: {location['longitude']}")
        
        submitted = st.form_submit_button("Criar Pedido")
        
        if submitted:
            if not titulo or not descricao:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Criar novo pedido
                novo_pedido = {
                    "titulo": titulo,
                    "descricao": descricao,
                    "tipo": tipo,
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "usuario": st.session_state['usuario_logado'],
                    "status": "Pendente"
                }
                
                # Inicializar lista de pedidos se não existir
                if 'pedidos_ajuda' not in st.session_state:
                    st.session_state['pedidos_ajuda'] = []
                
                # Adicionar pedido à lista
                st.session_state['pedidos_ajuda'].append(novo_pedido)
                
                # Adicionar ao histórico do usuário
                if 'historico_pedidos' not in st.session_state:
                    st.session_state['historico_pedidos'] = []
                st.session_state['historico_pedidos'].append(novo_pedido)
                
                st.success("Pedido criado com sucesso!")
                st.rerun()

# Seção de busca de pedidos
st.write("### Buscar pedido por ID")
busca_id = st.number_input("Digite o ID do pedido", min_value=1, step=1)
if st.button("Buscar"):
    pedido_encontrado = next((p for p in st.session_state['pedidos_ajuda'] if p['id'] == busca_id), None)

    if pedido_encontrado:
        geolocator = Nominatim(user_agent="resq-app")
        location_pedido = geolocator.reverse((pedido_encontrado["latitude"], pedido_encontrado["longitude"]))

        st.success("Pedido encontrado:")
        st.write(f"**Usuário:** {pedido_encontrado['usuario']}")
        st.write(f"**Categoria:** {pedido_encontrado['categoria']}")
        st.write(f"**Descrição:** {pedido_encontrado['descricao']}")
        st.write(f"**Endereço:** {location_pedido.address}")

    else:
        st.error("Nenhum pedido encontrado com esse ID.")