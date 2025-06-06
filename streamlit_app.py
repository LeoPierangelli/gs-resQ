import streamlit as st

if 'dados_usuarios' not in st.session_state:
    st.session_state['dados_usuarios'] = {
        'nomes': [],
        'senhas': []
    }

st.session_state['pedidos_ajuda'] = [
        {"latitude": -23.5505, "longitude": -46.6333, "descricao": "Ajuda médica urgente"},
        {"latitude": -23.5510, "longitude": -46.6340, "descricao": "Necessita de alimentos"},
    ]

# Definindo as páginas
cadastro_page = st.Page("pages/cadastro.py", title="Cadastro")
mapa_page = st.Page("pages/mapa.py", title="Mapa")
perfil_page = st.Page("pages/perfil.py", title="Perfil")
historico_page = st.Page("pages/historico.py", title="Historico")

# Configurando a navegação
pg = st.navigation([cadastro_page, mapa_page, perfil_page, historico_page])

# Executando a página selecionada
pg.run()

