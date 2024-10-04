import psutil
import csv
import time
from datetime import datetime

# Função para coletar uso da CPU
def get_uso_cpu():
    return psutil.cpu_percent(interval=1)

# Coletar uso de memória
def get_uso_memoria():
    memoria = psutil.virtual_memory()
    return memoria.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.total, disk.free, disk.used, disk.percent

# Chamar as funções e iniciar a coleta de dados
uso_cpu = get_uso_cpu()
memoria = get_uso_memoria()
disco = get_disk_usage()

# Exibir os resultados
print(f'Uso da CPU: {uso_cpu}%')
print(f'Uso da Memória: {memoria}')
print(f'Coleta de dados iniciada. Tecle CONTROL + C para cancelar.')

# Criar cabeçalho de arquivo de log CSV
log_file = 'log_monitoramento.log'

with open(log_file, 'w', newline='') as file:
    gravar = csv.writer(file)
    gravar.writerow(['timestamp','uso_cpu','memoria','total_disco','disco_livre','disco_usado','percent_uso_disco'])

# Coletar e gravar dados a cada 10 segundos
try:
    while True:
        with open(log_file, 'a', newline='') as file:
            data = datetime.now().isoformat()
            gravar = csv.writer(file)
            gravar.writerow([data,uso_cpu,memoria,disco])
            time.sleep(10)

except KeyboardInterrupt:
    print(f'Parando a coleta de dados!')