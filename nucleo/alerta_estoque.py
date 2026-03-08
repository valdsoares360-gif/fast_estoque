import requests

WEBHOOK_N8N = "WEBHOOK_N8N = http://localhost:5678/webhook-test/estoque-baixo"


def enviar_alerta(produto):

    dados = {
        "produto_id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "estoque_minimo": produto.estoque_minimo
    }

    try:
        requests.post(WEBHOOK_N8N, json=dados)

    except Exception as e:
        print("Erro ao enviar webhook:", e)