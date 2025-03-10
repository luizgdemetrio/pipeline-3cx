import pandas as pd
import os

arquivo_consolidado_ativa = "data/consolidado_ativa.csv"
arquivo_consolidado_receptiva = "data/consolidado_receptiva.csv"
arquivo_chamada_ativa = "data/ativa_final.csv"
arquivo_chamada_receptiva = "data/receptiva_final.csv"


def consolidar_chamadas(novo, consolidado):

    df_novo = pd.read_csv(novo)

    if os.path.exists(consolidado):
        df_consolidado = pd.read_csv(consolidado)
        df_consolidado = pd.concat([df_consolidado, df_novo]).drop_duplicates()
        df_consolidado["Ringing int"] = (
            df_consolidado["Ringing int"].astype(str).str.replace(".", ",", regex=False)
        )
        df_consolidado["Talking int"] = (
            df_consolidado["Talking int"].astype(str).str.replace(".", ",", regex=False)
        )
    else:
        df_consolidado = df_novo

    df_consolidado.to_csv(consolidado, index=False)
    print(f"Arquivo {consolidado} atualizado com sucesso!")


consolidar_chamadas(arquivo_chamada_ativa, arquivo_consolidado_ativa)
consolidar_chamadas(arquivo_chamada_receptiva, arquivo_consolidado_receptiva)
