import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime

st.title("Criar Novo Pedido")

# Verificar se o usuário está logado
if 'usuario_logado' not in st.session_state:
    st.warning("Por favor, faça login para criar um pedido.")
    st.stop()

# Obter localização do usuário
location = streamlit_geolocation()

if location['latitude'] is None or location['latitude'] == []:
    st.warning("Permita o acesso à sua localização para criar um pedido.")
    st.stop()

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
            st.switch_page("pages/mapa.py")