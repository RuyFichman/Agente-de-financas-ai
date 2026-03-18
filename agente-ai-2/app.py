from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
from datetime import datetime

app = Flask(__name__)

# Função para extrair os dados da mensagem
def processar_mensagem(mensagem):
    padrao = r"gastei\s*(\d+(?:[\.,]\d{1,2})?)\s*reais?\s*na\s*(.+)"
    match = re.search(padrao, mensagem, re.IGNORECASE)

    if match:
        valor = float(match.group(1).replace(",", "."))
        descricao = f"Compra na {match.group(2).strip().title()}"
        categoria = "Alimentação"  
        data = datetime.today().strftime("%d/%m/%Y")
        
        return descricao, categoria, valor, data
    return None

@app.route("/webhook", methods=["POST"])
def webhook():
    mensagem = request.values.get("Body", "").lower()
    resposta = MessagingResponse()

    dados = processar_mensagem(mensagem)
    
    if dados:
        descricao, categoria, valor, data = dados
        texto_resposta = (f"📌 **Resumo do gasto:**\n"
                          f"📝 Descrição: {descricao}\n"
                          f"📂 Categoria: {categoria}\n"
                          f"💰 Valor: R${valor:.2f}\n"
                          f"📅 Data: {data}\n\n"
                          f"Esses dados estão corretos? (Responda SIM ou NÃO)")
    else:
        texto_resposta = "❌ Não entendi o gasto. Tente algo como: 'Gastei 10 reais na padaria'."

    resposta.message(texto_resposta)
    return str(resposta)

if __name__ == "__main__":
    app.run(debug=True)
