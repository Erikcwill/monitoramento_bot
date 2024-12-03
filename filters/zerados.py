# filters/zerados.py

import re
from utils.regex import clean_text

def filtrar_pontos_zerados_por_cidade(texto):
    blocos = re.split(r'(?=🔵ROTA \d+🔵|Монитор #[\d]+)', texto)
    cidades_pontos = {}
    pontos_de_fundo = []
    pontos_reservas = []
    cidade_atual = None

    for bloco in blocos:
        linhas = bloco.split("\n")
        rota_nome = linhas[0].strip()
        rota_nome = re.sub(r'(🔵ROTA \d+🔵).*', r'\1', rota_nome)

        if 'ITAJAI' in bloco:
            cidade_atual = 'ITAJAI'
            continue
        elif 'NAVEGANTES' in bloco:
            cidade_atual = 'NAVEGANTES'
            continue

        pontos_unidos = []
        ponto_atual = ""

        for linha in linhas[1:]:
            if linha.startswith(("🅿️", "🏆", "🛻")):
                if ponto_atual:
                    pontos_unidos.append(ponto_atual.strip())
                ponto_atual = linha
            else:
                ponto_atual += " " + linha

        if ponto_atual:
            pontos_unidos.append(ponto_atual.strip())

        regex = re.compile(r'.* - 0❗️.*')
        pontos_zerados = [ponto for ponto in pontos_unidos if regex.search(ponto)]

        for ponto in pontos_zerados:
            if "Reserva" in ponto:
                pontos_reservas.append(ponto)
            elif "🌞" in ponto and "💼" in ponto:
                if rota_nome not in cidades_pontos:
                    cidades_pontos[rota_nome] = {'ITAJAI': [], 'NAVEGANTES': []} if cidade_atual else []
                if cidade_atual:
                    cidades_pontos[rota_nome][cidade_atual].append(ponto)
                else:
                    cidades_pontos[rota_nome].append(ponto)
            else:
                pontos_de_fundo.append(ponto)

    resposta = "🚨 Pontos zerados encontrados:\n\n"
    emoji_cidade = "🏙️"
    if 'ITAJAI' in texto or 'NAVEGANTES' in texto:
        if 'ITAJAI' in texto:
            resposta += f"{emoji_cidade} ITAJAI:\n"
            pontos_itajai_existem = False
            for rota, pontos in cidades_pontos.items():
                if pontos['ITAJAI']:
                    pontos_itajai_existem = True
                    resposta += f"\n{rota}:\n"
                    for ponto in pontos['ITAJAI']:
                        ponto_limpo = re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', ponto).strip()
                        if "- 0❗️" not in ponto_limpo:
                            ponto_limpo += " - 0❗️"
                        resposta += f"{ponto_limpo}\n"
            if not pontos_itajai_existem:
                resposta += "Nenhum ponto zerado!\n"

        resposta += "\n"

        if 'NAVEGANTES' in texto:
            resposta += f"{emoji_cidade} NAVEGANTES:\n"
            pontos_navegantes_existem = False
            for rota, pontos in cidades_pontos.items():
                if pontos['NAVEGANTES']:
                    pontos_navegantes_existem = True
                    resposta += f"\n{rota}:\n"
                    for ponto in pontos['NAVEGANTES']:
                        ponto_limpo = re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', ponto).strip()
                        if "- 0❗️" not in ponto_limpo:
                            ponto_limpo += " - 0❗️"
                        resposta += f"{ponto_limpo}\n"
            if not pontos_navegantes_existem:
                resposta += "Nenhum ponto zerado!\n"

        resposta += "\n"
    else:
        for rota, pontos in cidades_pontos.items():
            if pontos:
                resposta += f"\n{rota}:\n"
                for ponto in pontos:
                    ponto_limpo = re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', ponto).strip()
                    if "- 0❗️" not in ponto_limpo:
                        ponto_limpo += " - 0❗️"
                    resposta += f"{ponto_limpo}\n"

    if pontos_de_fundo:
        resposta += "\n🔵PONTOS DE FUNDO🔵\n"
        for ponto in pontos_de_fundo:
            ponto_limpo = re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', ponto).strip()
            if "- 0❗️" not in ponto_limpo:
                ponto_limpo += " - 0❗️"
            resposta += f"{ponto_limpo}\n"

    if pontos_reservas:
        resposta += "\n🔵RESERVAS🔵\n"
        for ponto in pontos_reservas:
            ponto_limpo = re.sub(r'(\s?🌞.*|💼.*|🎉.*|https?:\/\/\S+|\(.*?\))', '', ponto).strip()
            if "- 0❗️" not in ponto_limpo:
                ponto_limpo += " - 0❗️"
            resposta += f"{ponto_limpo}\n"

    resposta = re.sub(r'\n{3,}', '\n\n', resposta).strip()
    return resposta if len(cidades_pontos) > 0 or len(pontos_de_fundo) > 0 or len(pontos_reservas) > 0 else "Nenhum ponto está zerado no momento."
