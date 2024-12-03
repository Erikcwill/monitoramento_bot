# main.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.start import start
from handlers.mensagens import perguntar_acao
from handlers.callback import callback_botao
from config import TOKEN  # Importando o token corretamente

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, perguntar_acao))
    app.add_handler(CallbackQueryHandler(callback_botao))

    app.run_polling()

if __name__ == '__main__':
    main()
