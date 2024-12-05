# filters/alerta.py

import re
from utils.regex import clean_text

def filtrar_pontos_com_alerta(texto):
    blocos = re.split(r'(?=🔵ROTA \d+🔵|Монитор #[\d]+)', texto)
    rotas_pontos = {}
    pontos_de_fundo = []
    pontos_reservas = []

    for bloco in blocos:
        linhas = bloco.split("\n")
        rota_nome = linhas[0].strip()
        rota_nome = re.sub(r'(🔵ROTA \d+🔵).*', r'\1', rota_nome)

        pontos_unidos = []
        ponto_atual = ""

        # Une linhas de pontos para tratá-las juntas
        for linha in linhas[1:]:
            if linha.startswith(("🅿️", "🏆", "🛻")):
                if ponto_atual:
                    pontos_unidos.append(ponto_atual.strip())
                ponto_atual = linha
            else:
                ponto_atual += " " + linha

        if ponto_atual:
            pontos_unidos.append(ponto_atual.strip())

        # Procura pontos com ❗️ que não sejam zerados
        regex = re.compile(r'.* - (\d+)❗️.*')
        pontos_com_alerta = [
            (ponto, int(regex.search(ponto).group(1)))
            for ponto in pontos_unidos if regex.search(ponto) and not re.search(r' - 0❗️', ponto)
        ]

        # Classifica os pontos por rota, fundo ou reserva
        for ponto, quantidade in pontos_com_alerta:
            ponto_limpo = clean_text(ponto)
            ponto_formatado = ponto_limpo + f" - {quantidade}❗️"  # Corrigido: "quantidade" é usado aqui.

            if "Reserva" in ponto:
                if ponto_formatado not in pontos_reservas:  # Evita duplicatas
                    pontos_reservas.append(ponto_formatado)
            elif not ("🌞" in ponto or "💼" in ponto):  # Pontos sem sol ou maleta
                # Adiciona apenas se o ponto ainda não estiver presente
                if ponto_limpo not in [p.split(" - ")[0] for p in pontos_de_fundo]:
                    pontos_de_fundo.append(ponto_formatado)
            else:
                if rota_nome not in rotas_pontos:
                    rotas_pontos[rota_nome] = []
                if ponto_formatado not in rotas_pontos[rota_nome]:  # Evita duplicatas
                    rotas_pontos[rota_nome].append(ponto_formatado)

    # Monta a resposta organizada
    resposta = "🚨 Pontos com alerta encontrados:\n\n"

    # Adiciona pontos por rota
    for rota, pontos in rotas_pontos.items():
        if pontos:
            resposta += f"{rota}:\n"
            resposta += "\n".join(pontos) + "\n\n"

    # Adiciona pontos de fundo
    if pontos_de_fundo:
        resposta += "🔵PONTOS DE FUNDO🔵\n"
        resposta += "\n".join(pontos_de_fundo) + "\n\n"

    # Adiciona reservas
    if pontos_reservas:
        resposta += "🔵RESERVAS🔵\n"
        resposta += "\n".join(pontos_reservas) + "\n\n"

    resposta = re.sub(r'\n{3,}', '\n\n', resposta).strip()
    return resposta if len(rotas_pontos) > 0 or len(pontos_de_fundo) > 0 or len(pontos_reservas) > 0 else "Nenhum ponto com alerta encontrado!"
