import requests
import csv
import time
import os
from dotenv import load_dotenv

load_dotenv()

flamengo_id = 1783
api_token = os.getenv("API_TOKEN")

base_url = "https://api.football-data.org/v4/competitions/2013/matches"
headers = {
    "X-Auth-Token": api_token
}

# buscar todos os jogos com paginação
all_matches = []
offset = 0
limit = 100

while True:
    params = {
        "season": 2025,
        "status": "FINISHED",
        "limit": limit,
        "offset": offset
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print("erro ao acessar api")
        break

    data = response.json()

    if "matches" not in data or len(data["matches"]) == 0:
        break

    all_matches.extend(data["matches"])
    offset += limit
    time.sleep(1)

print(f"total de jogos carregados da api: {len(all_matches)}")

# filtrar jogos do flamengo
jogos_flamengo = [
    jogo for jogo in all_matches
    if jogo["homeTeam"]["id"] == flamengo_id
    or jogo["awayTeam"]["id"] == flamengo_id
]

if len(jogos_flamengo) == 0:
    print("nenhum jogo do flamengo encontrado")
    exit()

# variáveis
jogos = gols_marcados = gols_sofridos = pontos = 0
vitorias = empates = derrotas = 0

vitorias_casa = empates_casa = derrotas_casa = 0
vitorias_fora = empates_fora = derrotas_fora = 0

gols_marcados_casa = gols_sofridos_casa = 0
gols_marcados_fora = gols_sofridos_fora = 0

estatisticas_adversario = {}
maior_vitoria = 0
maior_derrota = 0

# garantir que não haja duplicidade de jogos
ids_processados = set()

# csv de jogos (tabela fato)
with open("flamengo_jogos_2025.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        "match_id", "data_jogo", "local",
        "adversario", "gols_flamengo",
        "gols_adversario", "resultado"
    ])

    for jogo in jogos_flamengo:
        match_id = jogo["id"]

        if match_id in ids_processados:
            continue

        ids_processados.add(match_id)
        jogos += 1

        data_jogo = jogo["utcDate"][:10]

        gols_casa = jogo["score"]["fullTime"]["home"]
        gols_fora = jogo["score"]["fullTime"]["away"]

        if jogo["homeTeam"]["id"] == flamengo_id:
            local = "Casa"
            adversario = jogo["awayTeam"]["name"]
            gols_fla = gols_casa
            gols_adv = gols_fora
        else:
            local = "Fora"
            adversario = jogo["homeTeam"]["name"]
            gols_fla = gols_fora
            gols_adv = gols_casa

        gols_marcados += gols_fla
        gols_sofridos += gols_adv

        if gols_fla > gols_adv:
            resultado = "Vitória"
            vitorias += 1
            pontos += 3
        elif gols_fla == gols_adv:
            resultado = "Empate"
            empates += 1
            pontos += 1
        else:
            resultado = "Derrota"
            derrotas += 1

        if local == "Casa":
            gols_marcados_casa += gols_fla
            gols_sofridos_casa += gols_adv
        else:
            gols_marcados_fora += gols_fla
            gols_sofridos_fora += gols_adv

        diff = gols_fla - gols_adv
        maior_vitoria = max(maior_vitoria, diff)
        maior_derrota = min(maior_derrota, diff)

        if adversario not in estatisticas_adversario:
            estatisticas_adversario[adversario] = {
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_marcados": 0,
                "gols_sofridos": 0
            }

        estatisticas_adversario[adversario]["jogos"] += 1
        estatisticas_adversario[adversario]["gols_marcados"] += gols_fla
        estatisticas_adversario[adversario]["gols_sofridos"] += gols_adv

        if resultado == "Vitória":
            estatisticas_adversario[adversario]["vitorias"] += 1
        elif resultado == "Empate":
            estatisticas_adversario[adversario]["empates"] += 1
        else:
            estatisticas_adversario[adversario]["derrotas"] += 1

        writer.writerow([
            match_id, data_jogo, local,
            adversario, gols_fla,
            gols_adv, resultado
        ])

# csv de adversários 
with open("flamengo_adversario_2025.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        "adversario", "jogos", "vitorias",
        "empates", "derrotas",
        "gols_marcados", "gols_sofridos", "aproveitamento"
    ])

    for adv, stats in estatisticas_adversario.items():
        aproveitamento = (stats["vitorias"] * 3 + stats["empates"]) / (stats["jogos"] * 3) * 100
        writer.writerow([
            adv,
            stats["jogos"],
            stats["vitorias"],
            stats["empates"],
            stats["derrotas"],
            stats["gols_marcados"],
            stats["gols_sofridos"],
            f"{aproveitamento:.2f}".replace('.', ',')
        ])

print("csvas gerados com sucesso")
print(f"total de jogos do flamengo: {jogos}")