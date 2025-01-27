from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

service = Service(GeckoDriverManager().install())

driver = webdriver.Firefox(service=service)


driver.get("https://www.google.com")
print(driver.title)
driver.quit()
print("driver atualizado")
