from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import os

load_dotenv()
report_login_url = os.getenv("REPORT_LOGIN_URL")
login_ramal = os.getenv("LOGIN_RAMAL")
password_ramal = os.getenv("PASSWORD_RAMAL")
report_calls = os.getenv("REPORT_CALLS")

# Configurações do Firefox
options = Options()
options.headless = (
    True  # Executar o navegador em modo headless (sem interface gráfica), opcional
)
options.set_preference(
    "browser.download.dir", os.path.join(os.getcwd(), "data")
)  # Diretório de download
options.set_preference("browser.download.folderList", 2)  # Usar diretório personalizado
options.set_preference("browser.download.useDownloadDir", True)
options.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/csv, application/octet-stream",
)  # Tipo de arquivo permitido para download

# Inicializa o WebDriver com o GeckoDriver (Firefox) via WebDriver Manager
driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()), options=options
)

# Exemplo de navegação
driver.get(report_login_url)

# Código para fazer login
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "loginInput"))
).send_keys(login_ramal)
element = driver.find_element(By.ID, "passwordInput").send_keys(password_ramal)
time.sleep(5)
driver.find_element(By.ID, "submitBtn").click()
print(f"login realizado com o usuário: {login_ramal}")

# Código para remover o arquivo anterior
if os.path.exists("data/call_reports.csv"):
    os.remove("data/call_reports.csv")
else:
    print("Relatório não encontrado")

# Código para extrair relatório
driver.get(report_calls)
element = WebDriverWait(
    driver,
    10,
).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//button[@type='button']//app-download-solid-icon")
    )
)
element.click()

# Fecha o WebDriver
tempo_esperado = int(0)
tempo_limite = int(30)
while not os.path.exists("data/call_reports.csv") and tempo_esperado < tempo_limite:
    time.sleep(1)
    tempo_esperado += 1
    print(f"Aguarde: {tempo_esperado}s")
if os.path.exists("data/call_reports.csv"):
    print(
        f"Relatório extraido com sucesso, salvo em: {os.path.join(os.getcwd(), 'data/call_reports.csv')}"
    )
    driver.quit()
    True
else:
    print(f"O relatório não foi encontrado após {tempo_limite} segundos.")
    driver.quit()
    False
