📦 VSestoque

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED)
![n8n](https://img.shields.io/badge/n8n-Automation-orange)
![Render](https://img.shields.io/badge/Deploy-Render-purple)









Sistema completo de gerenciamento de estoque com autenticação de usuários, dashboard interativo e automação com chatbot.

O projeto demonstra a construção de uma aplicação moderna utilizando:

API REST

frontend desacoplado

automação de processos

deploy em nuvem


🌐 Acesse a aplicação
Frontend

https://estoque-frontend-yi4t.onrender.com

Backend

https://estoque-backend-pyq6.onrender.com

Automação (n8n)

https://n8n-ldgy.onrender.com




# 🎥 Demonstração

### 🔐 Login e cadastro

![Login](docs/gifs/tela_login.gif)

---

### 📊 Dashboard

![Dashboard](docs/gifs/tela_dashboard.gif)

---

### 📦 Gerenciamento de produtos

![Produtos](docs/gifs/tela_produtos.gif)

---

### ➕ Adicionar produto

![Adicionar Produto](docs/gifs/tela_add.gif)

---

### 🔄 Movimentações de estoque

![Movimentações](docs/gifs/tela_mov.gif)

---

### 📜 Histórico de movimentações

![Histórico](docs/gifs/tela_history.gif)

---

### 🤖 VsBot (chatbot)

![VsBot](docs/gifs/tela_vsbot.gif)




✔️ Funcionalidades

Cadastro de usuários

Login com autenticação JWT

Gerenciamento completo de produtos

Entrada e saída de estoque

Histórico de movimentações

Dashboard com gráficos interativos

Integração com chatbot

Automação utilizando n8n

API REST com FastAPI

Interface moderna com Streamlit

Notificaçao automatica de estoque baixo


🛠️ Tecnologias Utilizadas
Backend

Python

FastAPI

SQLAlchemy

JWT Authentication

Frontend

Streamlit

Plotly

Banco de Dados

PostgreSQL

Automação

n8n

Infraestrutura

Docker

Render


🏗️ Arquitetura do Sistema

Arquitetura modular baseada em serviços desacoplados.

Usuário
   ↓
Frontend (Streamlit)
   ↓
Backend API (FastAPI)
   ↓
Banco de Dados (PostgreSQL)
   ↓
Automação (n8n)
   ↓
Chatbot (VsBot)

💻 Como Rodar o Projeto Localmente
1️⃣ Clonar o repositório
git clone https://github.com/valdsoares360-gif/controle-estoque.git
2️⃣ Entrar na pasta do projeto
cd controle-estoque
3️⃣ Criar ambiente virtual
python -m venv venv
4️⃣ Ativar ambiente virtual
Windows
venv\Scripts\activate
5️⃣ Instalar dependências
pip install -r requirements.txt
6️⃣ Rodar Backend
uvicorn app.main:app --reload

Backend disponível em:

http://localhost:8000
7️⃣ Rodar Frontend
streamlit run frontend/app.py

Frontend disponível em:

http://localhost:8501
🤖 Integração com n8n

O projeto utiliza n8n para automação de processos e integração com o chatbot.

Fluxo de funcionamento:

Aplicação → Webhook → n8n → Automação → Resposta ao usuário

Isso permite criar integrações e automações baseadas em eventos do sistema.

📚 Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conceitos importantes como:

desenvolvimento de APIs REST

autenticação com JWT

arquitetura desacoplada

integração entre serviços

manipulação de banco de dados

automação com n8n

deploy em nuvem

🚀 Possíveis melhorias futuras

sistema de permissões de usuário

exportação de relatórios

dashboard avançado

integração com APIs externas

👨‍💻 Autor

Valdinei Santos Soares

GitHub

https://github.com/valdsoares360-gif
