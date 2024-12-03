# handlers/mensagens.py

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.response import format_keyboard
from filters import zerados, maiores
from utils.regex import clean_text

# Dicionário para armazenar as mensagens recebidas
mensagens_recebidas = {}

async def perguntar_acao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    mensagem_texto = update.message.text
    mensagens_recebidas[chat_id] = mensagem_texto

    keyboard = format_keyboard([
        ("Filtrar zerados", 'filtrar_zerados'),
        ("Top 5 maiores", 'filtrar_maiores')
    ])
    
    await update.message.reply_text('O que você gostaria de fazer com a mensagem recebida?', reply_markup=keyboard)
