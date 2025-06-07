import streamlit as st
from streamlit_geolocation import streamlit_geolocation
#Biblioteca para puxar informações de endereço e localização
import folium
from streamlit_folium import st_folium
#Criar o mapa
from datetime import datetime
#Datas
from geopy.geocoders import Nominatim
#Endereço e localização também

st.title("Mapa")

#verificação de login do usuário
if 'usuario_logado' not in st.session_state:
    st.warning("Por favor, faça login para acessar o mapa.")
    st.stop()

st.write(f"Bem-vindo, {st.session_state['usuario_logado']}!")

#Duas colunas: mapa e formulário
col1, col2 = st.columns([2, 1])

#Mapa
with col1:
    #Pega latitude e longitude do usuário
    location = streamlit_geolocation()
    #Para não crashar
    if location['latitude'] is None or location['latitude'] == []:
        st.warning("permita o acesso a sua localização, por favor")
        st.stop()

    if location:
        latitude = location['latitude']
        longitude = location['longitude']

        #Cria o mapa centrado na localização do usuário
        mapa = folium.Map(location=[latitude, longitude], zoom_start=10)

        #Adiciona um marcador do usuário
        folium.Marker(
            [latitude, longitude],
            tooltip="Você está aqui",
            icon=folium.Icon(color="blue", icon="user")
        ).add_to(mapa)

        #Adiciona os marcadores dos pedidos
        for pedido in st.session_state['pedidos_ajuda']:
            folium.Marker(
                [pedido["latitude"], pedido["longitude"]],
                tooltip=f"ID {pedido['id']}: {pedido['tipo']}",
                icon=folium.Icon(color="red", icon="user")
            ).add_to(mapa)

        st_folium(mapa, width=600, height=600)

#Formulário
with col2:
    st.subheader("Criar Novo Pedido")
    
    #Forms do pedido
    with st.form("criar_pedido_form"):
        tipo = st.selectbox(
            "Tipo de Pedido",
            ["Ajuda Médica", "Alimentos", "Roupas", "Abrigo", "Outros"]
        )
        descricao = st.text_area("Descrição do Pedido")

        #Mostrar localização atual
        st.write("Sua localização atual:")
        st.write(f"Latitude: {location['latitude']}")
        st.write(f"Longitude: {location['longitude']}")
        
        submitted = st.form_submit_button("Criar Pedido")
        
        if submitted:
            if not descricao:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                novo_id = max(p['id'] for p in st.session_state['pedidos_ajuda']) + 1
                #Adicionando pedido ao dicionário
                novo_pedido = {
                    "id": novo_id,
                    "descricao": descricao,
                    "tipo": tipo,
                    "usuario": st.session_state['usuario_logado'],
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "status": "Pendente"
                }
                st.session_state['pedidos_ajuda'].append(novo_pedido)
                
                #Adicionando ao histórico do usuário
                if 'historico_pedidos' not in st.session_state:
                    st.session_state['historico_pedidos'] = []
                st.session_state['historico_pedidos'].append(novo_pedido)
                
                st.success("Pedido criado com sucesso!")

#Buscar pedidos por id
st.write("### Buscar pedido por ID")
busca_id = st.number_input("Digite o ID do pedido", min_value=1, step=1)
if st.button("Buscar"):
    pedido_encontrado = next((p for p in st.session_state['pedidos_ajuda'] if p['id'] == busca_id), None)

    if pedido_encontrado:
        geolocator = Nominatim(user_agent="resq-app")
        location_pedido = geolocator.reverse((pedido_encontrado["latitude"], pedido_encontrado["longitude"]))

        #Mostrando informações do pedido
        st.success("Pedido encontrado:")
        st.write(f"**Usuário:** {pedido_encontrado['usuario']} - {pedido_encontrado['data']}")
        st.write(f"**Tipo:** {pedido_encontrado['tipo']}")
        st.write(f"**Descrição:** {pedido_encontrado['descricao']}")
        st.write(f"**Status:** {pedido_encontrado['status']}")
        #Pegando endereço através de latitude e longitude
        st.success(f"**Endereço:** {location_pedido.address}")

        if st.button("Quero ajudar"):
            pedido_encontrado['status'] = "Em andamento"

    else:
        st.error("Nenhum pedido encontrado com esse ID.")