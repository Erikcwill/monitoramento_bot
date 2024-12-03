# handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot de Monitoramento Iniciado! Envie a mensagem completa para filtrar os pontos zerados ou os maiores.")
