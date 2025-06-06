import streamlit as st

st.title("Criar Conta")
novo_usuario = st.text_input("Nome de usuário")
nova_senha = st.text_input("Senha", type="password")
if st.button("Criar conta"):
    if novo_usuario in st.session_state['dados_usuarios']['nomes']:
        st.error("Nome de usuário já existe.")
    elif novo_usuario == "" or nova_senha == "":
        st.error("Preencha todos os campos.")
    else:
        st.session_state['dados_usuarios']['nomes'].append(novo_usuario)
        st.session_state['dados_usuarios']['senhas'].append(nova_senha)
        st.success("Conta criada com sucesso! Volte para o login.")

if st.button("Voltar para login"):
    st.switch_page("pages/login.py")
