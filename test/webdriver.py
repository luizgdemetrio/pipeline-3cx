from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os

# Configurações do Firefox
options = Options()
options.headless = True  # Executar o navegador em modo headless (sem interface gráfica), opcional
options.set_preference('browser.download.dir', os.path.join(os.getcwd(), 'downloads'))  # Diretório de download
options.set_preference('browser.download.folderList', 2)  # Usar diretório personalizado
options.set_preference('browser.download.useDownloadDir', True)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv, application/octet-stream')  # Tipo de arquivo permitido para download

# Inicializa o WebDriver com o GeckoDriver (Firefox) via WebDriver Manager
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

# Exemplo de navegação
driver.get('https://www.google.com/')

# Código para interagir com a página, por exemplo:
element = driver.find_element(By.NAME, 'q')
element.send_keys('Selenium Firefox')
element.submit()

# Código para fazer download de relatórios ou outras tarefas

# Fecha o WebDriver
driver.quit()
