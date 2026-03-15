import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"


def dashboard():

    token = st.session_state["token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    produtos = requests.get(
        f"{API_URL}/produtos",
        headers=headers
    ).json()

    movimentacoes = requests.get(
        f"{API_URL}/movimentacoes",
        headers=headers
    ).json()

    total_produtos = len(produtos)

    estoque_baixo = len([
        p for p in produtos
        if p["quantidade"] <= p["estoque_minimo"]
    ])

    total_movimentacoes = len(movimentacoes)

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Produtos", total_produtos)

    with col2:
        st.metric("Estoque Baixo", estoque_baixo)

    with col3:
        st.metric("Movimentações", total_movimentacoes)

    st.subheader("📦 Últimas Movimentações")

    df = pd.DataFrame(movimentacoes)

    if not df.empty:
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.info("Nenhuma movimentação registrada.")