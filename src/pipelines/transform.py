import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def salvar():
    caminho = "data/dataframe.xlsx"
    df.to_excel(caminho, index=False)
    print(f"dataframe salvo em: {caminho}")


def remover_sinal_negativo(df, coluna1, coluna2):
    df[coluna1] = df[coluna1].str.replace(r"[^0-9:]", "", regex=True)
    df[coluna2] = df[coluna2].str.replace(r"[^0-9:]", "", regex=True)
    return df


def criar_coluna_decimal(df, coluna_nova, coluna_antiga):
    df[coluna_nova] = pd.to_timedelta(df[coluna_antiga])
    df[coluna_nova] = df[coluna_nova].dt.total_seconds() / (3600 * 24)
    return df


recent_call_report = r"data/call_reports.csv"  # Arquivo de chamadas recentes
aux_path = r"data/assist.xlsx"  # Arquivo auxiliar para transformação

df = pd.read_csv(recent_call_report)
aux_df = pd.read_excel(aux_path)
aux_df = aux_df[["Ramal", "Função"]]

df.drop(["Sentiment", "Summary", "Transcription", "Cost"], axis=1, inplace=True)
df["Call Time"] = pd.to_datetime(df["Call Time"])
df_sort = df.sort_values(by="Call Time", ascending=True, inplace=True)
df["Ramal"] = df["Caller ID"].str.extract(r"\((\d{3})\)$")
df["Ramal"] = df["Ramal"].astype(str)
aux_df["Ramal"] = aux_df["Ramal"].astype(str)
df_result = df.merge(aux_df, on="Ramal", how="left")
df = df_result
df["Função"] = df["Função"].fillna("Cliente")
df["Call Type"] = df["Função"].apply(
    lambda x: (
        "Ativa" if x == "Operador" else "Receptiva" if x == "Cliente" else "Indefinido"
    )
)
df.drop(["Função", "Ramal"], axis=1, inplace=True)
df = remover_sinal_negativo(df, "Ringing", "Talking")
df = criar_coluna_decimal(df, "Ringing int", "Ringing")
df = criar_coluna_decimal(df, "Talking int", "Talking")

salvar()

df_ativa = df.loc[df["Call Type"] == "Ativa"].copy()
df_ativa.to_csv("data/ativa.csv", index=False)
print(f"df_ativa salvo em: data/ativa.csv")
df_receptiva = df.loc[df["Call Type"] == "Receptiva"].copy()
df_receptiva.to_csv("data/receptiva.csv", index=False)
print(f"df_receptiva salvo em: data/receptiva.csv")

# df.to_excel("../../data/dataframe.xlsx", index=False)
