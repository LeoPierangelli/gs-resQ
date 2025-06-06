import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Perfil do Usuário")

# Verificar se o usuário está logado
if 'usuario_logado' not in st.session_state:
    st.warning("Por favor, faça login para ver seu perfil.")
    st.stop()

# Informações do usuário
st.header("Informações Pessoais")
st.write(f"**Nome de usuário:** {st.session_state['usuario_logado']}")

# Estatísticas do usuário
st.header("Estatísticas")
if 'historico_pedidos' in st.session_state:
    pedidos_usuario = [p for p in st.session_state['historico_pedidos'] if p['usuario'] == st.session_state['usuario_logado']]
    total_pedidos = len(pedidos_usuario)
    pedidos_pendentes = len([p for p in pedidos_usuario if p['status'] == 'Pendente'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Pedidos", total_pedidos)
    with col2:
        st.metric("Pedidos Pendentes", pedidos_pendentes)
else:
    st.info("Você ainda não tem pedidos registrados.")

# Histórico de Pedidos
st.header("Histórico de Pedidos")

if 'historico_pedidos' in st.session_state and pedidos_usuario:
    # Converter para DataFrame para melhor visualização
    df = pd.DataFrame(pedidos_usuario)
    
    # Ordenar por data (mais recente primeiro)
    if 'data' in df.columns:
        df = df.sort_values('data', ascending=False)
    
    # Exibir os pedidos
    for _, pedido in df.iterrows():
        with st.expander(f"Pedido de {pedido.get('data', 'Data não disponível')} - {pedido.get('titulo', 'Sem título')}"):
            st.write(f"**Tipo:** {pedido.get('tipo', 'N/A')}")
            st.write(f"**Descrição:** {pedido.get('descricao', 'N/A')}")
            st.write(f"**Localização:** Latitude {pedido.get('latitude', 'N/A')}, Longitude {pedido.get('longitude', 'N/A')}")
            st.write(f"**Status:** {pedido.get('status', 'Pendente')}")
else:
    st.info("Você ainda não tem pedidos registrados.")