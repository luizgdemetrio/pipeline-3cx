# Pipeline de Dados 3CX

Este projeto implementa um pipeline de dados para extrair, transformar e carregar (ETL) relatórios do sistema 3CX, com o objetivo de alimentar dashboards no Power BI com informações gerenciais. O pipeline automatiza o download de relatórios, sua transformação em formatos prontos para análise e a integração com ferramentas de BI.

---

## Estrutura do Projeto

```
├── docs/
│   └── README.md
├── test/
│   ├── webdriver.py
│   └── while.py
├── src/
│   ├── ETL/
│   │   ├── extract.py
│   │   └── transform.py
├── data/  # Diretório para arquivos baixados
├── .python-version
├── pyproject.toml
```

---

## Dependências

- **Python**: 3.12.4
- **Selenium**: ^4.27.1
- **WebDriver Manager**
- **Dotenv**: ^1.0.0
- **Pandas**: ^2.1.1

### Instalação das Dependências

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

2. Instale as dependências:
   ```bash
   poetry install
   ```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
REPORT_LOGIN_URL=<URL de login no sistema>
LOGIN_RAMAL=<Seu login>
PASSWORD_RAMAL=<Sua senha>
OFFICE_DASHBOARD=<URL do painel do escritório>
```

---

## Como Executar

### Etapa 1: Extração

A extração dos relatórios é realizada por meio de automação com Selenium. Para iniciar o processo, execute:

```bash
python src/ETL/extract.py
```
Os relatórios serão salvos no diretório `data/`.

### Etapa 2: Transformação

Para transformar os dados extraídos em um formato adequado para análise:

```bash
python src/ETL/transform.py
```
Certifique-se de que os arquivos extraídos estejam no diretório `data/`.

---

## Testes

O projeto inclui scripts de teste localizados no diretório `test/`. Para executar os testes:

```bash
pytest test/
```

---

## Logs

O sistema utiliza a biblioteca `logging` para monitorar eventos importantes. Certifique-se de verificar o terminal para mensagens informativas e de erro.

---

## Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

---

## Autor

- Luiz (<lgds.demtrio@gmail.com>)

