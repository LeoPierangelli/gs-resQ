import streamlit as st

st.title("Cadastro")

#Abas de login e criar conta
tab1, tab2 = st.tabs(["Login", "Criar Conta"])

with tab1:
    st.subheader("Login")
    #Inputs
    usuario = st.text_input("Nome de usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")
    
    if st.button("Entrar"):
        #Verifica se o usuário existe e se a senha bate (com aquele dicionário lá do streamlit_app.py)
        if usuario in st.session_state['dados_usuarios']['nomes']:
            idx = st.session_state['dados_usuarios']['nomes'].index(usuario)
            if senha == st.session_state['dados_usuarios']['senhas'][idx]:
                st.session_state['usuario_logado'] = usuario
                st.switch_page("pages/mapa.py")
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Usuário não encontrado.")

with tab2:
    st.subheader("Criar Nova Conta")
    #Inputs
    novo_usuario = st.text_input("Nome de usuário", key="novo_usuario")
    nova_senha = st.text_input("Senha", type="password", key="nova_senha")
    
    if st.button("Criar conta"):
        #Verificações de preenchimento
        if novo_usuario in st.session_state['dados_usuarios']['nomes']:
            st.error("Nome de usuário já existe.")
        elif novo_usuario == "" or nova_senha == "":
            st.error("Preencha todos os campos.")
        else:
            #Adiciona as informações ao dicionário
            st.session_state['dados_usuarios']['nomes'].append(novo_usuario)
            st.session_state['dados_usuarios']['senhas'].append(nova_senha)
            st.success("Conta criada com sucesso! Faça login para continuar.")