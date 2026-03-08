import requests

WEBHOOK_N8N = "http://localhost:5678/webhook-test/estoque-baixo"

def enviar_alerta(produto):

    dados = {
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "estoque_minimo": produto.estoque_minimo
    }

    try:
        response = requests.post(WEBHOOK_N8N, json=dados)

        print("STATUS:", response.status_code)
        print("RESPOSTA:", response.text)

    except Exception as e:
        print("Erro ao enviar webhook:", e)