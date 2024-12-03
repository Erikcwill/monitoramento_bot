# bot/utils/response.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_keyboard(buttons):
    """Formata o teclado inline com base na lista de botões"""
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=callback)] for text, callback in buttons])
