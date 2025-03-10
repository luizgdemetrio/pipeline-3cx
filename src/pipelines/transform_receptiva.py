import pandas as pd
from dotenv import load_dotenv
import re
import hashlib

load_dotenv()


def salvar():
    caminho = "data/receptiva_final.csv"
    df.to_csv(caminho, index=False)
    print(f"dataframe salvo em: {caminho}")


def status_chamada(linha):
    if linha["Status"] == "answered":
        return "atendida"
    elif linha["Status"] == "unanswered":
        if linha["Reason"].strip() == f"Terminated by {linha['Destination'].strip()}":
            return "sem agente"
        elif linha["Talking int"] >= 0.000115740740740741:
            return "abandonada"
        else:
            return "desistente"
    return "indefinido"


def ordenar_personalizado(df):
    df["Q_prioridade"] = df["Destination"].str.startswith("Q").astype(int)
    df_sorted = df.sort_values(
        by=["Call Time", "Q_prioridade"], ascending=[True, False]
    )
    df_sorted.drop(columns=["Q_prioridade"], inplace=True)
    df = df_sorted
    return df


def fila_origem(linha, df):
    if linha["Função"] == "Fila":
        return linha["Destination"]
    elif linha["Função"] == "Operador":
        fila = df[(df["Caller ID"] == linha["Caller ID"]) & (df["Função"] == "Fila")]
        if not fila.empty:
            return fila.iloc[0]["Destination"]
    return "Indefinido"


def gerar_codigo_base(df):
    """Gera um código único baseado na primeira ocorrência da sequência de chamadas."""
    grupo_id = {}  # Dicionário para armazenar códigos já atribuídos

    def atribuir_codigo(linha):
        identificador = (
            f"{linha['Caller ID']}"  # Chave única para sequência de chamadas
        )

        if identificador not in grupo_id:
            # Criar um código único baseado na primeira ocorrência dessa combinação
            hash_code = hashlib.md5(
                f"{linha['Call Time']}_{linha['Caller ID']}".encode()
            ).hexdigest()[:10]
            grupo_id[identificador] = hash_code  # Armazena o código gerado

        return grupo_id[identificador]  # Retorna o código para a sequência já existente

    df["Codigo Unico"] = df.apply(atribuir_codigo, axis=1)
    return df


recent_call_report = r"data/receptiva.csv"  # Arquivo de chamadas recentes
aux_path = r"data/assist.xlsx"  # Arquivo auxiliar para transformação

df = pd.read_csv(recent_call_report)
aux_df = pd.read_excel(aux_path)
df["Ramal"] = df["Destination"].str.extract(r"\((\d{3})\)$")
df["Ramal"] = df["Ramal"].astype(str)
aux_df["Ramal"] = aux_df["Ramal"].astype(str)
df_filtrado = df.merge(aux_df[["Ramal", "Função"]], on="Ramal", how="inner")
df = df_filtrado
df["Status"] = df.apply(status_chamada, axis=1)
df = ordenar_personalizado(df)
df["Fila Origem"] = df.apply(lambda linha: fila_origem(linha, df), axis=1)
df = gerar_codigo_base(df)
# df_filtrado.to_excel("data/receptiva_filtrado.xlsx", index=False)
salvar()
