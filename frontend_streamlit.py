import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Controle de Estoque",
    page_icon="📦",
    layout="wide"
)

# ---------- ESTILO CSS ----------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#0E1117;
}

[data-testid="stSidebar"]{
    background-color:#1c1f26;
}

.metric-card{
    background:#1c1f26;
    padding:25px;
    border-radius:12px;
    border:1px solid #2a2d34;
}

</style>
""", unsafe_allow_html=True)

st.title("📦 Sistema de Controle de Estoque")

# ---------- LOGIN ----------

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:

    st.subheader("🔐 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        r = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": username,
                "password": password
            }
        )

        if r.status_code == 200:
            token = r.json()["access_token"]
            st.session_state.token = token
            st.success("Login realizado!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

    st.stop()

# ---------- FUNÇÃO API ----------

def carregar_produtos():

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    r = requests.get(f"{API_URL}/produtos", headers=headers)

    if r.status_code != 200:
        st.error("Erro ao acessar API")
        return pd.DataFrame()

    data = r.json()

    if isinstance(data, dict):
        data = [data]

    return pd.DataFrame(data)

# ---------- MENU ----------

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Produtos", "Adicionar Produto"]
)

# ---------- DASHBOARD ----------

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Produtos</div>
    <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Estoque total</div>
    <div class="metric-value">{int(df["quantidade"].sum())}</div>
    </div>
    """, unsafe_allow_html=True)

    valor = (df["preco"] * df["quantidade"]).sum()

    col3.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Valor em estoque</div>
    <div class="metric-value">R$ {valor:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            df,
            names="nome",
            values="quantidade",
            hole=0.6,
            title="Distribuição de Produtos"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig2 = px.bar(
            df,
            x="nome",
            y="quantidade",
            text_auto=True,
            title="Quantidade em Estoque"
        )

        fig2.update_layout(template="plotly_dark")

        st.plotly_chart(fig2, use_container_width=True)

    # ALERTA DE ESTOQUE

    st.divider()

    st.subheader("⚠️ Produtos com estoque baixo")

    baixo = df[df["quantidade"] <= df["estoque_minimo"]]

    if baixo.empty:
        st.success("Nenhum produto com estoque baixo")
    else:
        st.dataframe(baixo)

# ---------- PRODUTOS ----------

elif menu == "Produtos":

    st.subheader("📋 Lista de Produtos")

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    r = requests.get(f"{API_URL}/produtos", headers=headers)

    if r.status_code != 200:
        st.error("Erro ao carregar produtos")
        st.stop()

    produtos = r.json()

    if isinstance(produtos, dict):
        produtos = [produtos]

    df = pd.DataFrame(produtos)

    busca = st.text_input("🔎 Buscar produto")

    if busca:
        df = df[df["nome"].str.contains(busca, case=False)]

    st.dataframe(df, use_container_width=True)

    st.divider()

    # EDITAR

    st.subheader("✏️ Editar Produto")

    if not df.empty:

        produto_id = st.selectbox(
            "Selecione o produto",
            df["id"]
        )

        produto = df[df["id"] == produto_id].iloc[0]

        nome = st.text_input("Nome", value=produto["nome"])
        descricao = st.text_area("Descrição", value=produto["descricao"])

        col1, col2 = st.columns(2)

        with col1:
            quantidade = st.number_input(
                "Quantidade",
                value=int(produto["quantidade"])
            )

        with col2:
            estoque_minimo = st.number_input(
                "Estoque mínimo",
                value=int(produto["estoque_minimo"])
            )

        preco = st.number_input(
            "Preço",
            value=float(produto["preco"])
        )

        if st.button("Salvar Alterações"):

            data = {
                "nome": nome,
                "descricao": descricao,
                "quantidade": quantidade,
                "preco": preco,
                "estoque_minimo": estoque_minimo
            }

            r = requests.put(
                f"{API_URL}/produtos/{produto_id}",
                json=data,
                headers=headers
            )

            if r.status_code in [200, 204]:
                st.success("Produto atualizado!")
                st.rerun()
            else:
                st.error(r.text)

    st.divider()

    # DELETAR

    st.subheader("❌ Deletar Produto")

    if not df.empty:

        produto_delete = st.selectbox(
            "Produto para deletar",
            df["id"],
            key="delete"
        )

        if st.button("Deletar Produto"):

            r = requests.delete(
                f"{API_URL}/produtos/{produto_delete}",
                headers=headers
            )

            if r.status_code in [200, 204]:
                st.success("Produto deletado!")
                st.rerun()
            else:
                st.error(r.text)

# ---------- CADASTRAR ----------

elif menu == "Adicionar Produto":

    st.subheader("➕ Novo Produto")

    nome = st.text_input("Nome do Produto")

    descricao = st.text_area("Descrição")

    col1, col2 = st.columns(2)

    with col1:
        quantidade = st.number_input(
            "Quantidade",
            min_value=0,
            step=1
        )

    with col2:
        estoque_minimo = st.number_input(
            "Estoque mínimo",
            min_value=0,
            step=1
        )

    preco = st.number_input(
        "Preço",
        min_value=0.0,
        step=0.01
    )

    if st.button("Cadastrar Produto"):

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        data = {
            "nome": nome,
            "descricao": descricao,
            "quantidade": quantidade,
            "preco": preco,
            "estoque_minimo": estoque_minimo
        }

        r = requests.post(
            f"{API_URL}/produtos",
            json=data,
            headers=headers
        )

        if r.status_code in [200, 201]:
            st.success("✅ Produto cadastrado com sucesso!")
            st.rerun()
        else:
            st.error(f"Erro ao cadastrar produto: {r.text}")