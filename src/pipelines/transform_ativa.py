import pandas as pd
from dotenv import load_dotenv
import hashlib

load_dotenv()


def salvar():
    caminho = "data/ativa_final.csv"
    df.to_csv(caminho, index=False)
    print(f"dataframe salvo em: {caminho}")


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


recent_call_report = r"data/ativa.csv"  # Arquivo de chamadas recentes
aux_path = r"data/assist.xlsx"  # Arquivo auxiliar para transformação

df = pd.read_csv(recent_call_report)
aux_df = pd.read_excel(aux_path)
df["Ramal"] = df["Caller ID"].str.extract(r"\((\d{3})\)$")
df["Ramal"] = df["Ramal"].astype(str)
aux_df["Ramal"] = aux_df["Ramal"].astype(str)
df_filtrado = df.merge(aux_df[["Ramal"]], on="Ramal", how="inner")
df = df_filtrado
df = gerar_codigo_base(df)
salvar()
