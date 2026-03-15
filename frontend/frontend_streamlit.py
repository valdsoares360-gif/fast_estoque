
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io 
from datetime import datetime
import sys
import os


# Garante que o diretório pai esteja no path (para imports de módulos)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Caminho base do script (para CSS e imagens)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_URL = "https://estoque-backend-pyq6.onrender.com/"

st.set_page_config(
    page_title="Controle de Estoque",
    layout="wide"
)

# CSS
def carregar_css():
    try:
        css_path = os.path.join(BASE_DIR, "style", "style.css")
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar CSS: {e}")

carregar_css()

# HEADER
if "menu" not in st.session_state or st.session_state.get("menu") != "VsBot":

    col_logo, col_title = st.columns([1,5])

    with col_logo:
        img_path = os.path.join(BASE_DIR, "imagens", "vsoares.png")

    with col_title:
        st.title("Sistema de Controle de Estoque")

# =============================
# AUTENTICAÇÃO
# =============================

if "token" not in st.session_state:
    st.session_state.token = None

if "pagina_auth" not in st.session_state:
    st.session_state.pagina_auth = "login"


# =============================
# FUNÇÕES API
# =============================

def carregar_produtos():

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    r = requests.get(f"{API_URL}/produtos", headers=headers)

    if r.status_code != 200:
        st.error("Erro ao acessar API")
        return pd.DataFrame()

    data = r.json()

    if isinstance(data, dict):
        data = [data]

    return pd.DataFrame(data)


def carregar_movimentacoes():

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    r = requests.get(f"{API_URL}/movimentacoes", headers=headers)

    if r.status_code != 200:
        return []

    return r.json()

@st.dialog("✏️ Editar Produto")
def editar_produto_modal(produto):

    with st.form("form_editar_produto_modal"):

        nome = st.text_input("Nome", value=produto["nome"])

        descricao = st.text_area(
            "Descrição",
            value=produto["descricao"]
        )

        preco = st.number_input(
            "Preço",
            value=float(produto["preco"]),
            min_value=0.0,
            step=0.1
        )

        quantidade = st.number_input(
            "Quantidade",
            value=int(produto["quantidade"]),
            min_value=0
        )

        estoque_minimo = st.number_input(
            "Estoque mínimo",
            value=int(produto["estoque_minimo"]),
            min_value=0
        )

        salvar = st.form_submit_button("💾 Salvar alterações")

    if salvar:

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.put(
            f"{API_URL}/produtos/{produto['id']}",
            json={
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "quantidade": quantidade,
                "estoque_minimo": estoque_minimo
            },
            headers=headers
        )

        if r.status_code == 200:

            st.success("Produto atualizado com sucesso!")
            st.rerun()

        else:

            st.error(r.text)

# =============================
# LOGIN
# =============================

if st.session_state.token is None and st.session_state.pagina_auth == "login":

    st.subheader("Login")

    username = st.text_input("Email")
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

    if st.button("Criar conta"):
        st.session_state.pagina_auth = "cadastro"
        st.rerun()

    st.stop()


# =============================
# CADASTRO
# =============================

if st.session_state.token is None and st.session_state.pagina_auth == "cadastro":

    st.subheader("Criar Conta")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):

        r = requests.post(
            f"{API_URL}/usuarios/",
            json={
                "email": email,
                "senha": senha
            }
        )

        if r.status_code in [200, 201]:

            st.success("Conta criada! Faça login.")
            st.session_state.pagina_auth = "login"
            st.rerun()

        else:

            st.error(r.text)

    if st.button("Voltar"):
        st.session_state.pagina_auth = "login"
        st.rerun()

    st.stop()


# =============================
# SIDEBAR
# =============================

menu = st.sidebar.radio(
    "   Menu",
    [
        "Dashboard",
        "Produtos",
        "Adicionar Produto",
        "Movimentações",
        "Histórico de Movimentações",
        "VsBot"
    ]
)

st.session_state.menu = menu
# =============================
# HISTÓRICO
# =============================

st.sidebar.divider()
st.sidebar.subheader("Histórico")

movs = carregar_movimentacoes()

if not movs:

    st.sidebar.caption("Nenhuma movimentação")

else:

    for mov in movs:

        data = pd.to_datetime(mov["data"])
        data_br = data.strftime("%d/%m %H:%M")

        if mov["tipo"] == "entrada":
            texto = f"+{mov['quantidade']}"
        else:
            texto = f"-{mov['quantidade']}"

        produto = mov.get("produto_nome", "Produto")

        st.sidebar.write(f"{data_br} | {texto} {produto}")

# LOGOUT

st.sidebar.divider()

if st.sidebar.button("Logout"):

    st.session_state.token = None
    st.session_state.pagina_auth = "login"
    st.rerun()


# =============================
# DASHBOARD
# =============================

if menu == "Dashboard":

    st.subheader("Dashboard")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    col1, col2, col3 = st.columns(3)

    col1.metric("Produtos", len(df))
    col2.metric("Estoque Total", int(df["quantidade"].sum()))

    valor = (df["preco"] * df["quantidade"]).sum()
    col3.metric("Valor em Estoque", f"R$ {valor:.2f}")

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
       
       
       def cor_linha(row):

          if row["quantidade"] < row["estoque_minimo"]:
             return ["background-color:#ff4b4b"]*len(row)

          elif row["quantidade"] == row["estoque_minimo"]:
             return ["background-color:#f9c74f"]*len(row)

          else:
             return [""]*len(row)

       st.dataframe(
        baixo[["nome","quantidade","estoque_minimo"]]
        .style.apply(cor_linha, axis=1),
        use_container_width=True
    )
    

    movs = carregar_movimentacoes()

    if movs:

      df_mov = pd.DataFrame(movs)

      df_mov["data"] = pd.to_datetime(df_mov["data"])

      df_mov["mes"] = df_mov["data"].dt.to_period("M").astype(str)

      mov_mes = df_mov.groupby("mes")["quantidade"].sum().reset_index()

      fig3 = px.line(
        mov_mes,
        x="mes",
        y="quantidade",
        markers=True,
        title="Movimentações por mês"
    )

      fig3.update_layout(template="plotly_dark")

      st.plotly_chart(fig3, use_container_width=True)

    if movs:

      df_mov = pd.DataFrame(movs)

      ranking = (
        df_mov.groupby("produto_nome")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

      fig4 = px.bar(
        ranking,
        x="produto_nome",
        y="quantidade",
        title="Produtos mais movimentados",
        text_auto=True
    )

      fig4.update_layout(template="plotly_dark")

      st.plotly_chart(fig4, use_container_width=True)

# =============================
# PRODUTOS (VERSÃO MODERNA)
# =============================

elif menu == "Produtos":

    st.title("📦 Gestão de Produtos")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    # BUSCA
    busca = st.text_input("🔎 Buscar produto")

    if busca:
        df = df[df["nome"].str.contains(busca, case=False)]

    st.divider()

    # GRID DE PRODUTOS
    cols = st.columns(3)

    for i, produto in df.iterrows():

        with cols[i % 3]:

            estoque = produto["quantidade"]
            minimo = produto["estoque_minimo"]

            alerta = "⚠️ Estoque baixo" if estoque <= minimo else "✅ Estoque OK"

            with st.container(border=True):

                st.subheader(produto["nome"])

                st.write(f"💰 **R$ {produto['preco']}**")

                st.write(f"📦 Estoque: **{estoque}**")

                st.caption(f"Estoque mínimo: {minimo}")

                st.write(alerta)

                st.write(produto["descricao"])

                col1, col2 = st.columns(2)

                # BOTÃO EDITAR (ABRE POPUP)
                if col1.button("✏️ Editar", key=f"edit_{produto['id']}"):

                    editar_produto_modal(produto)

                # BOTÃO DELETAR
                if col2.button("🗑️ Deletar", key=f"del_{produto['id']}"):

                    headers = {
                        "Authorization": f"Bearer {st.session_state.token}"
                    }

                    r = requests.delete(
                        f"{API_URL}/produtos/{produto['id']}",
                        headers=headers
                    )

                    if r.status_code == 200:

                        st.success("Produto deletado com sucesso!")
                        st.rerun()

                    else:

                        st.error(r.text)

# =============================
# ADICIONAR PRODUTO
# =============================

elif menu == "Adicionar Produto":

    st.subheader("Novo Produto")

    nome = st.text_input("Nome")
    descricao = st.text_area("Descrição")

    col1, col2 = st.columns(2)

    with col1:
        quantidade = st.number_input("Quantidade", min_value=0)

    with col2:
        estoque_minimo = st.number_input("Estoque mínimo", min_value=0)

    preco = st.number_input("Preço", min_value=0.0)

    if st.button("Cadastrar Produto"):

        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        r = requests.post(
            f"{API_URL}/produtos",
            json={
                "nome": nome,
                "descricao": descricao,
                "quantidade": quantidade,
                "preco": preco,
                "estoque_minimo": estoque_minimo
            },
            headers=headers
        )

        if r.status_code in [200, 201]:
            st.success("Produto cadastrado!")
        else:
            st.error(r.text)


# =============================
# MOVIMENTAÇÕES
# =============================

elif menu == "Movimentações":

    st.subheader("🔄 Movimentar Estoque")

    df = carregar_produtos()

    if df.empty:
        st.warning("Nenhum produto cadastrado")
        st.stop()

    df["produto_display"] = df["id"].astype(str) + " - " + df["nome"]

    produto_display = st.selectbox(
        "Produto",
        df["produto_display"]
    )

    produto_id = int(produto_display.split(" - ")[0])

    produto = df[df["id"] == produto_id].iloc[0]

    st.info(f"📦 Estoque atual: {produto['quantidade']} unidades")
    st.caption(f"⚠️ Estoque mínimo: {produto['estoque_minimo']}")

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
                "produto_id": produto_id,
                "tipo": tipo,
                "quantidade": int(quantidade)
            },
            headers=headers
        )

        if r.status_code in [200, 201]:

            st.success("Movimentação registrada com sucesso!")
            st.rerun()

        else:

            st.error(r.text)

    st.divider()


# =============================
#  HISTORICO DE MOVIMENTAÇÕES
# =============================

elif menu == "Histórico de Movimentações":

    st.title("Histórico de Movimentações")

    movs = carregar_movimentacoes()

    if not movs:
        st.info("Nenhuma movimentação registrada")
        st.stop()

    df_mov = pd.DataFrame(movs)

    df_mov["data"] = pd.to_datetime(df_mov["data"])

    st.subheader("📅 Filtrar histórico")

    col1, col2 = st.columns(2)

    data_inicio = col1.date_input("Data inicial")
    data_fim = col2.date_input("Data final")

    if data_inicio and data_fim:
        df_mov = df_mov[
            (df_mov["data"].dt.date >= data_inicio) &
            (df_mov["data"].dt.date <= data_fim)
        ]

    st.subheader("📊 Movimentações no período")

    if not df_mov.empty:

        grafico = (
            df_mov.groupby("produto_nome")["quantidade"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            grafico,
            x="produto_nome",
            y="quantidade",
            title="Movimentação por produto"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    meses = df_mov["data"].dt.to_period("M").astype(str).unique()

    mes_selecionado = st.selectbox(
        "Filtrar por mês",
        ["Todos"] + sorted(meses)
    )

    if mes_selecionado != "Todos":
        df_mov = df_mov[
            df_mov["data"].dt.to_period("M").astype(str) == mes_selecionado
        ]

    df_mov["data"] = df_mov["data"].dt.strftime("%d/%m/%Y %H:%M")

    st.dataframe(
        df_mov[["data","produto_nome","tipo","quantidade"]],
        use_container_width=True
    )


# =============================
# VSBOT
# =============================

elif menu == "VsBot":

    st.markdown("""
    <style>

    /* fundo geral */
    [data-testid="stAppViewContainer"]{
        background-color:#0e1117;
    }

    /* centralizar chat */
    .chat-container{
        max-width:900px;
        margin:auto;
    }

    /* bolha usuário */
    .user-bubble{
        background:#2563eb;
        padding:12px 16px;
        border-radius:12px;
        color:white;
        margin-bottom:10px;
        text-align:right;
    }

    /* bolha bot */
    .bot-bubble{
        background:#1f2937;
        padding:12px 16px;
        border-radius:12px;
        color:white;
        margin-bottom:10px;
        text-align:left;
    }

    /* titulo */
    .vsbot-title{
        text-align:center;
        font-size:32px;
        font-weight:700;
        margin-bottom:30px;
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        "<div class='vsbot-title'>🤖 VsBot - Assistente do Estoque</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)


    if "chat_vsbot" not in st.session_state:
        st.session_state.chat_vsbot = []


    # mostrar histórico
    for role, msg in st.session_state.chat_vsbot:

        if role == "user":

            st.markdown(
                f"<div class='user-bubble'>🤵 {msg}</div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"<div class='bot-bubble'>🤖 {msg}</div>",
                unsafe_allow_html=True
            )


    pergunta = st.chat_input("Pergunte algo sobre o estoque...")


    if pergunta:

        st.session_state.chat_vsbot.append(("user", pergunta))


        with st.spinner("VsBot está pensando..."):

            r = requests.post(
                "http://n8n:5678/webhook/vsbot",
                json={
                    "pergunta": pergunta,
                    "token": st.session_state.token
                
               }
            )


            if r.status_code == 200:

                data = r.json()

                if isinstance(data, list):
                    data = data[0]

                resposta = data.get("resposta") or data.get("output") or "Sem resposta"

            else:

                resposta = "Erro ao consultar VsBot"


        st.session_state.chat_vsbot.append(("bot", resposta))

        st.rerun()


    st.markdown("</div>", unsafe_allow_html=True)







