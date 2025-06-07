#Leonardo de Souza Pierangelli RM560501
#Leandro Kamada RM560381
#Pedro Arão Baquini RM559580

import streamlit as st
#Utilizamos a biblioteca streamlit para que o projeto fique na web e tenha uma interface

#aqui criamos o banco de dados com as informações de login dos usuários
if 'dados_usuarios' not in st.session_state:
    st.session_state['dados_usuarios'] = {
        'nomes': [],
        'senhas': []
    }

#aqui armazenamos os pedidos de ajuda
st.session_state['pedidos_ajuda'] = [
    {
        "id": 1,
        "descricao": "Precisamos de roupas de frio",
        "tipo": "Roupas",
        "usuario": "joao123",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "data": "22/04/2025 11:09",
        "status": "Pendente"
    },
    {
        "id": 2,
        "descricao": "Precisamos de alimentos",
        "tipo": "Alimentos",
        "usuario": "maria456",
        "latitude": -23.5510,
        "longitude": -46.6340,
        "data": "14/05/2025 21:03",
        "status": "Pendente"
    }
]

#Páginas
cadastro_page = st.Page("pages/cadastro.py", title="Cadastro")
mapa_page = st.Page("pages/mapa.py", title="Mapa")
perfil_page = st.Page("pages/perfil.py", title="Perfil")

#Navegação
pg = st.navigation([cadastro_page, mapa_page, perfil_page])

pg.run()

