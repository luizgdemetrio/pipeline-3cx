import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def salvar():
    caminho = "../../data/ativa_final.xlsx"
    df.to_excel(caminho, index=False)
    print(f"dataframe salvo em: {caminho}")


recent_call_report = r"../../data/ativa.csv"  # Arquivo de chamadas recentes
aux_path = r"../../data/assist.xlsx"  # Arquivo auxiliar para transformação

df = pd.read_csv(recent_call_report)
aux_df = pd.read_excel(aux_path)
df["Ramal"] = df["Caller ID"].str.extract(r"\((\d{3})\)$")
df["Ramal"] = df["Ramal"].astype(str)
aux_df["Ramal"] = aux_df["Ramal"].astype(str)
df_filtrado = df.merge(aux_df[["Ramal"]], on="Ramal", how="inner")

salvar()
