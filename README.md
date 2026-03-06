# Flamengo 2025 Brasileirão Dashboard

Projeto de análise de dados da campanha do Flamengo no Brasileirão 2025.

A ideia do projeto foi passar por todo o processo de um fluxo de dados real:

API → Python → Estruturação dos dados → Power BI.

## Tecnologias utilizadas

- Python
- API football-data.org
- CSV
- Power BI
- DAX

## Processo do projeto

1. Consumo dos dados através da API football-data.org
2. Extração dos jogos do Brasileirão 2025
3. Tratamento e organização dos dados com Python
4. Criação das tabelas utilizadas no modelo
5. Construção do dashboard no Power BI

## Dados analisados

- Jogos do Flamengo
- Gols marcados
- Gols sofridos
- Desempenho em casa e fora
- Evolução dos pontos ao longo do campeonato
- Adversários mais enfrentados

## Alguns números da campanha

- 78 gols marcados
- 27 gols sofridos
- Média aproximada de 2 gols por jogo

## Dashboard

### Visão geral

![Dashboard](images/dashboard_geral.png)

### Desempenho casa vs fora

![Casa Fora](images/casa_fora.png)

### Linha do tempo da campanha

![Linha do tempo](images/linha_tempo.png)

## Próximos passos

Evoluir o projeto para análises de múltiplas temporadas e ligas completas utilizando um pipeline com SQL.
