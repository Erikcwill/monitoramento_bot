# bot/utils/regex.py

import re

def clean_text(texto):
    """Remove elementos desnecessários de texto, como emojis e links."""
    return re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', texto).strip()
