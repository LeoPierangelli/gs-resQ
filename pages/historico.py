import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Histórico de Pedidos")

# Verificar se o usuário está logado
if 'usuario_logado' not in st.session_state:
    st.warning("Por favor, faça login para ver seu histórico de pedidos.")
    st.stop()

# Inicializar o histórico de pedidos se não existir
if 'historico_pedidos' not in st.session_state:
    st.session_state['historico_pedidos'] = []

# Exibir o histórico de pedidos
if st.session_state['historico_pedidos']:
    # Converter para DataFrame para melhor visualização
    df = pd.DataFrame(st.session_state['historico_pedidos'])
    
    # Ordenar por data (mais recente primeiro)
    if 'data' in df.columns:
        df = df.sort_values('data', ascending=False)
    
    # Exibir os pedidos
    for _, pedido in df.iterrows():
        with st.expander(f"Pedido de {pedido.get('data', 'Data não disponível')}"):
            st.write(f"**Descrição:** {pedido.get('descricao', 'N/A')}")
            st.write(f"**Localização:** Latitude {pedido.get('latitude', 'N/A')}, Longitude {pedido.get('longitude', 'N/A')}")
            st.write(f"**Status:** {pedido.get('status', 'Pendente')}")
else:
    st.info("Você ainda não tem pedidos registrados.")