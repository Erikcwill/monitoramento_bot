# filters/maiores.py

import re
from utils.regex import clean_text

def filtrar_pontos_maiores(texto):
    blocos = re.split(r'(?=🔵ROTA \d+🔵|Монитор #[\d]+)', texto)
    cidades_pontos = {}
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

        regex = re.compile(r'- (\d+)')
        pontos_com_quantidade = [
            (ponto, int(regex.search(ponto).group(1))) for ponto in pontos_unidos if regex.search(ponto)
        ]

        if pontos_com_quantidade:
            if rota_nome not in cidades_pontos:
                cidades_pontos[rota_nome] = []
            cidades_pontos[rota_nome].extend(pontos_com_quantidade)

    resposta = "📈 Pontos com maior quantidade de patinetes:\n\n"
    todos_pontos = [
        (rota, ponto, quantidade) for rota, pontos in cidades_pontos.items() for ponto, quantidade in pontos
    ]
    maiores_pontos = sorted(todos_pontos, key=lambda x: x[2], reverse=True)[:5]

    rotas_maiores = {}
    for rota, ponto, quantidade in maiores_pontos:
        if rota not in rotas_maiores:
            rotas_maiores[rota] = []
        rotas_maiores[rota].append((ponto, quantidade))

    for rota, pontos in rotas_maiores.items():
        resposta += f"{rota}:\n"
        for ponto, quantidade in pontos:
            ponto_limpo = clean_text(ponto)
            resposta += f" 🅿️🏆{ponto_limpo} - {quantidade}\n"

    return resposta.strip() if maiores_pontos else "Nenhum ponto com quantidade significativa encontrado."
