import subprocess

# Lista de scripts a serem executados na ordem desejada
scripts = [
    # "pipelines/update_webdriver.py",
    # "pipelines/extract.py",
    "pipelines/transform.py",
    "pipelines/transform_ativa.py",
    "pipelines/transform_receptiva.py",
    "pipelines/consolidar.py",
]


def executar_script(script):
    print(f"\n🚀 Executando: {script} ...")
    resultado = subprocess.run(
        [
            "poetry",
            "run",
            "python",
            f"src/{script}",
        ],  # Usa Poetry para rodar no ambiente virtual
        capture_output=True,
        text=True,
        encoding="utf-8",  # Ou "cp1252", conforme necessário
        errors="replace",  # Adicione esse parâmetro para evitar UnicodeDecodeError
    )

    if resultado.returncode == 0:
        print(f"✅ {script} executado com sucesso!")
    else:
        print(f"❌ Erro ao executar {script}:")
        print(resultado.stderr)
        exit(1)


# Executar todos os scripts na sequência definida
if __name__ == "__main__":
    for script in scripts:
        executar_script(script)

    print("\n🎉 Todos os scripts foram executados com sucesso!")
