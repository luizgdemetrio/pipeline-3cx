import pandas as pd
import re
import numpy as np

recent_call_report = (
    r"C:\Users\Luiz Gustavo\workspace\luiz\pipeline-3cx\data\call_reports.csv"
)


def x(x):
    y = df.head(x)
    return y


def visualizacaofiltroData(data, coluna, df):
    mascara = df[str(coluna)] == data
    visu = df.loc[mascara]
    return visu


def criar_coluna_decimal(coluna_nova, coluna_antiga):
    df[coluna_nova] = pd.to_timedelta(df[coluna_antiga])
    criar_coluna = df[coluna_nova] = df[coluna_nova].dt.total_seconds() / (3600 * 24)
    return criar_coluna


def extrair_numero_entrada(numero):
    procurar = re.search(r"\((\d+)\)$", numero)
    if procurar:
        return procurar.group(1)
    else:
        return numero


def separar_destino_do_ramal(destination):
    match = re.match(r"(.+?)\s*\((\d+)\)$", destination)
    if match:
        return pd.Series(match.groups())
    else:
        return pd.Series([destination, None])


def gerar_arquivo():
    x = df.to_csv("Receptivas.csv")  # Carregar Arquivo
    print("Arquivo gerado")
    return x


def identificar_reason(row):
    if row is None:
        return "None"
    row = str(row).strip()
    if re.search(r"\(\d{3}\)$", row) and row.startswith("Q"):
        return "Fila"
    elif re.search(r"\(\d{3}\)$", row):
        return "Operador"
    else:
        return "Cliente"


df = pd.read_csv(recent_call_report)  # Carregar e Pular cabeçalho

df.drop(columns=["Cost"], inplace=True)  # Remoção de coluna

# Separação Call Time
df["Call Time"] = pd.to_datetime(df["Call Time"])
df["DataChamada"] = df["Call Time"].dt.date
df["HoraChamada"] = df["Call Time"].dt.time

df["NumeroEntrada"] = df["Caller ID"].apply(
    extrair_numero_entrada
)  # Extrair Numero do Caller ID

# Separar Multivalorado Destino
df[["Destino", "RamalDestino"]] = df["Destination"].apply(
    lambda x: separar_destino_do_ramal(x)
)

# Criação das colunas decimal
criar_coluna_decimal("RingingDecimal", "Ringing")
criar_coluna_decimal("TalkingDecimal", "Talking")

df = df.rename(
    columns={
        "Call Time": "CallTime_Legado",
        "Caller ID": "CallerID_Legado",
        "Destination": "Destination_Legado",
        "Status": "Status_Legado",
        "Ringing": "Ringing_Legado",
        "Talking": "Talking_Legado",
        "Reason": "Reason_Legado",
    }
)  # Renomeia Legado


# separar o multivalorado reason e Aplicar o preenchimento para baixo no NaT
# Cara vou separar mais não kkk

# Preenchimento dos NaN
mask = (
    df["CallTime_Legado"].notna()
    & df["DataChamada"].notna()
    & df["HoraChamada"].notna()
)
df["SK"] = np.nan
df.loc[mask, "SK"] = ["Receptiva" + str(i) for i in range(1, mask.sum() + 1)]
df["SK"] = df["SK"].fillna(method="ffill")
df["CallTime_Legado"] = df["CallTime_Legado"].fillna(method="ffill")
df["DataChamada"] = df["DataChamada"].fillna(method="ffill")
df["HoraChamada"] = df["HoraChamada"].fillna(method="ffill")  # Criação surrogate key

# Criacao do Historico da Fila
df["HistoricoFila"] = np.where(df["Destino"].str.contains("Q "), df["Destino"], np.nan)
df["HistoricoFila"] = df["HistoricoFila"].fillna(method="ffill")

# Tipo do Destino Para transformar o Talking e o Ringing Corretamente
df["Tipo Destino"] = np.where(
    df["Destino"].str.startswith("Q "), "Fila", "Operador"
)  # Adição do Tipo Destino

# Atendido = answered
# Sem Agente = Talking = 0
# Desistente = Talking na Fila <= 10 segundos
# Abadonado = Talking na Fila > 10 segundos

df[["Reason_AfterBy", "Reason_BeforeBy"]] = df["Reason_Legado"].str.split(
    "by", n=1, expand=True
)


df["ReasonOutput"] = df["Reason_BeforeBy"].apply(identificar_reason)


condicoes = [
    (df["Status_Legado"] == "answered"),
    (df["Status_Legado"] == "unanswered") & (df["ReasonOutput"] == "Fila"),
    (df["Status_Legado"] == "unanswered") & (df["TalkingDecimal"] <= 0.000116),
    (df["Status_Legado"] == "unanswered") & (df["TalkingDecimal"] > 0.000116),
]

valores_status = ["Atendido", "Sem Agente", "Desistente", "Abandonado"]

df["Status"] = np.select(condicoes, valores_status, default="Erro_Validacao")

# Trocar os valores entre Ringing e Decimal quando for Fila
df["Temp"] = np.where(
    df["Tipo Destino"] == "Fila", df["TalkingDecimal"], df["RingingDecimal"]
)
df["TalkingDecimal"] = np.where(
    df["Tipo Destino"] == "Fila", df["RingingDecimal"], df["TalkingDecimal"]
)
df["RingingDecimal"] = df["Temp"]
df.drop(columns=["Temp"], inplace=True)

gerar_arquivo()
