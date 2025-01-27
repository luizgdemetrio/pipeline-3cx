import pandas as pd
import re
import numpy as np
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Carregar o dicionário MONITORAMENTO como um JSON


# Caminho do arquivo CSV
recent_call_report = (
    r"C:\Users\Luiz Gustavo\workspace\luiz\pipeline-3cx\data\call_reports.csv"
)


# Função para extrair o número de um formato específico
def extrair_numero(numero):
    procurar = re.search(r"\((\d+)\)$", str(numero))
    return procurar.group(1) if procurar else numero


# Função para criar colunas de tempo em formato decimal
def criar_coluna_decimal(df, coluna_nova, coluna_antiga):
    df[coluna_nova] = pd.to_timedelta(df[coluna_antiga])
    df[coluna_nova] = df[coluna_nova].dt.total_seconds() / (3600 * 24)
    return df


# Função para determinar o tipo da chamada
def tipo_chamada(row):
    caller_info = dicionario.get(str(row["Caller ID"]))  # Está quebrado
    destination_info = dicionario.get(str(row["Destination"]))

    if caller_info and caller_info["tipo"] == "Operador":
        return "Ativa"
    elif destination_info and destination_info["tipo"] in ["Operador", "Fila"]:
        return "Receptiva"
    else:
        return "Outro"


# Função principal para processar o DataFrame
def transformar_call_report(caminho_csv):
    # Ler o arquivo CSV
    df = pd.read_csv(caminho_csv)

    # Remover colunas desnecessárias
    df.drop(["Sentiment", "Summary", "Transcription", "Cost"], axis=1, inplace=True)

    # Converter "Call Time" para colunas de data e hora
    df["Call Time"] = pd.to_datetime(df["Call Time"])
    df["Date"] = df["Call Time"].dt.date
    df["Time"] = df["Call Time"].dt.time
    df.drop("Call Time", axis=1, inplace=True)

    # Aplicar a função para extrair números
    df["Caller ID"] = df["Caller ID"].apply(extrair_numero)
    df["Destination"] = df["Destination"].apply(extrair_numero)

    # Selecionar colunas relevantes
    df = df[
        [
            "Date",
            "Time",
            "Caller ID",
            "Destination",
            "Status",
            "Ringing",
            "Talking",
            "Reason",
        ]
    ]

    # Criar colunas de tempo em formato decimal
    df = criar_coluna_decimal(df, "Ringing", "Ringing")
    df = criar_coluna_decimal(df, "Talking", "Talking")

    # Criar a coluna "Tipo Chamada"
    df["Tipo Chamada"] = df.apply(tipo_chamada, axis=1)

    return df


# Executar o processamento
call_report_transform = transformar_call_report(recent_call_report)
