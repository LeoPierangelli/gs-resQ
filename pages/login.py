import streamlit as st

st.title("Login")
usuario = st.text_input("Nome de usuário")
senha = st.text_input("Senha", type="password")
if st.button("Login"):
    # Verifica se o usuário existe e senha bate
    if usuario in st.session_state['dados_usuarios']['nomes']:
        idx = st.session_state['dados_usuarios']['nomes'].index(usuario)
        if senha == st.session_state['dados_usuarios']['senhas'][idx]:
            st.session_state['usuario_logado'] = usuario
            st.switch_page("pages/mapa.py")
        else:
            st.error("Senha incorreta.")
    else:
        st.error("Usuário não encontrado.")
st.markdown("Não tem conta?")

if st.button("Criar conta"):
    st.switch_page("pages/criar_conta.py")
