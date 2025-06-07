import streamlit as st
#Leonardo de Souza Pierangelli RM560501
#Leandro Kamada RM560381
#Pedro Arão Baquini RM559580
if 'dados_usuarios' not in st.session_state:
    st.session_state['dados_usuarios'] = {
        'nomes': [],
        'senhas': []
    }

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

# Definindo as páginas
cadastro_page = st.Page("pages/cadastro.py", title="Cadastro")
mapa_page = st.Page("pages/mapa.py", title="Mapa")
perfil_page = st.Page("pages/perfil.py", title="Perfil")

# Configurando a navegação
pg = st.navigation([cadastro_page, mapa_page, perfil_page])

# Executando a página selecionada
pg.run()

