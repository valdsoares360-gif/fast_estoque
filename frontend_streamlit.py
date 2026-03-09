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

# ---------- CARREGAR CSS ----------

def carregar_css():
    try:
        with open("style/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

carregar_css()

st.title("📦 Sistema de Controle de Estoque")

# ---------- AUTENTICAÇÃO ----------

if "token" not in st.session_state:
    st.session_state.token = None

if "pagina_auth" not in st.session_state:
    st.session_state.pagina_auth = "inicio"

# ---------- TELA INICIAL ----------

if st.session_state.token is None and st.session_state.pagina_auth == "inicio":

    st.subheader("Bem-vindo ao Sistema")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Entrar"):
            st.session_state.pagina_auth = "login"
            st.rerun()

    with col2:
        if st.button("📝 Criar conta"):
            st.session_state.pagina_auth = "cadastro"
            st.rerun()

    st.stop()

# ---------- LOGIN ----------

if st.session_state.token is None and st.session_state.pagina_auth == "login":

    st.subheader("Login")

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

    if st.button("⬅ Voltar"):
        st.session_state.pagina_auth = "inicio"
        st.rerun()

    st.stop()

# ---------- CADASTRO ----------

if st.session_state.token is None and st.session_state.pagina_auth == "cadastro":

    st.subheader("Criar Conta")

    new_user = st.text_input("Novo usuário")

    new_pass = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Cadastrar"):

        r = requests.post(
            f"{API_URL}/auth/register",
            json={
                "username": new_user,
                "password": new_pass
            }
        )

        if r.status_code in [200, 201]:

            st.success("Conta criada! Faça login.")

            st.session_state.pagina_auth = "login"

            st.rerun()

        else:

            st.error(r.text)

    if st.button("⬅ Voltar"):
        st.session_state.pagina_auth = "inicio"
        st.rerun()

    st.stop()

# ---------- SIDEBAR ----------

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Produtos", "Adicionar Produto", "Movimentações"]
)

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.token = None

    st.session_state.pagina_auth = "inicio"

    st.rerun()

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

# ---------- DASHBOARD ----------

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    col1, col2, col3 = st.columns(3)

    col1.metric("Produtos", len(df))

    col2.metric(
        "Estoque Total",
        int(df["quantidade"].sum())
    )

    valor = (df["preco"] * df["quantidade"]).sum()

    col3.metric(
        "Valor em Estoque",
        f"R$ {valor:.2f}"
    )

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

    st.divider()

    st.subheader("⚠️ Produtos com estoque baixo")

    baixo = df[df["quantidade"] <= df["estoque_minimo"]]

    if baixo.empty:

        st.success("Nenhum produto com estoque baixo")

    else:

        st.dataframe(baixo, use_container_width=True)

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

# ---------- CADASTRAR PRODUTO ----------

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

            st.success("Produto cadastrado!")

            st.rerun()

        else:

            st.error(f"Erro: {r.text}")


# ---------- MOVIMENTAÇOES ----------


elif menu == "Movimentações":

    st.subheader("🔄 Movimentar Estoque")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    produto_nome = st.selectbox(
        "Produto",
        df["nome"]
    )

    produto_id = df[df["nome"] == produto_nome]["id"].values[0]

    tipo = st.selectbox(
        "Tipo de movimentação",
        ["entrada", "saida"]
    )

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1
    )

    if st.button("Registrar movimentação"):

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.post(
            f"{API_URL}/movimentacoes",
            json={
                "produto_id": int(produto_id),
                "tipo": tipo,
                "quantidade": int(quantidade)
            },
            headers=headers
        )

        if r.status_code in [200, 201]:

            st.success("Movimentação registrada com sucesso!")

        else:

            st.error(f"Erro: {r.text}")