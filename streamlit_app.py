import streamlit as st

if 'dados_usuarios' not in st.session_state:
    st.session_state['dados_usuarios'] = {
        'nomes': [],
        'senhas': []
    }

st.session_state['pedidos_ajuda'] = [
    {
        "id": 1,
        "descricao": "Ajuda médica urgente",
        "categoria": "Saúde",
        "usuario": "joao123",
        "latitude": -23.5505,
        "longitude": -46.6333
    },
    {
        "id": 2,
        "descricao": "Necessita de alimentos",
        "categoria": "Alimentos",
        "usuario": "maria456",
        "latitude": -23.5510,
        "longitude": -46.6340
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

