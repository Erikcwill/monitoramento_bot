# handlers/callback.py

from telegram import Update
from telegram.ext import ContextTypes
from filters import zerados, maiores
from handlers.mensagens import mensagens_recebidas

async def callback_botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    mensagem = mensagens_recebidas.get(chat_id)

    if query.data == 'filtrar_zerados' and mensagem:
        pontos_zerados = zerados.filtrar_pontos_zerados_por_cidade(mensagem)
        await query.edit_message_text(text=pontos_zerados)
    elif query.data == 'filtrar_maiores' and mensagem:
        pontos_maiores = maiores.filtrar_pontos_maiores(mensagem)
        await query.edit_message_text(text=pontos_maiores)
    else:
        await query.edit_message_text(text="Nenhuma mensagem foi recebida para processar.")
