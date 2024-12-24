import os
import time

tempo_esperado = int(0)
tempo_maximo = int(30)
while not os.path.exists('data/call_reports.csv') and tempo_esperado < tempo_maximo:
    time.sleep(1)
    tempo_esperado += 1
    print(f"Aguarde: {tempo_esperado}s")
if os.path.exists('data/call_reports.csv'):
    print(f"Relatório extraido com sucesso, salvo em: {os.path.join(os.getcwd(), 'data/call_reports.csv')}")
    True
else:
    print(f"O relatório não foi encontrado após {tempo_maximo} segundos.")
    False







"""else:
    print(f"Relatório extraido com sucesso, salvo em: {os.path.join(os.getcwd(), 'data/call_reports.csv')}")
    print("driver.quit()")"""