import time
import psutil
import socket
import mysql.connector
from datetime import datetime
import os

# Função coleta o hostname
def get_hostname():
    return socket.gethostname()

# Função para coleta do usuário logado
def get_logged_user():
    return os.getlogin()

# Coletar endereço IPV4
def get_ipv4_address():
    hostname = get_hostname()
    return socket.gethostbyname(hostname)

# Coletar uso da CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Coletar uso da memória
def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

# Coletar espaço em disco e uso do disco
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.total, disk.used, disk.free, disk.percent

# Coletar o tráfego de interface de rede (kb/s)
def get_network_traffic(prev_data, interval):
    net_io = psutil.net_io_counters()
    bytes_sent_per_sec = (net_io.bytes_sent - prev_data['bytes_sent']) / interval / 1024
    bytes_recv_per_sec = (net_io.bytes_recv - prev_data['bytes_recv']) / interval / 1024
    return bytes_sent_per_sec, bytes_recv_per_sec, net_io.bytes_sent, net_io.bytes_recv

# Conectar ao banco de dados MySQL
def connect_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "coletor",
        password = "coletor",
        database = "senai"
    )

# Inserir os dados no banco
def insert_data(cursor, data):
    cursor.execute("""
        INSERT INTO monitoramento (
            timestamp, hostname, ipv4, logged_user, cpu_usage, memory_usage, disk_total, disk_usage, disk_free, disk_percent, kb_sent_per_sec, kb_recv_per_sec
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,data)

# Intervalo de coleta em segundos
interval = 10

# Coletar dados iniciais de rede
net_io_initial = psutil.net_io_counters()
prev_data = {'bytes_sent': net_io_initial.bytes_sent, 'bytes_recv': net_io_initial.bytes_recv}

# Conectar ao banco de dados
db_connection = connect_db()
db_cursor = db_connection.cursor()

# Coletar e inserir dados no banco de dados a cada 10 segundos
try:
    while True:
        timestamp = datetime.now()
        hostname = get_hostname()
        logged_user = get_logged_user()  # Coleta o nome de usuário logado
        ipv4_address = get_ipv4_address()
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        total_disk, used_disk, free_disk, percent_disk = get_disk_usage()
        kb_sent_per_sec, kb_recv_per_sec, bytes_sent, bytes_recv = get_network_traffic(prev_data, interval)

        data = (timestamp, hostname, ipv4_address, logged_user, cpu_usage, memory_usage, total_disk, used_disk, free_disk, percent_disk, kb_sent_per_sec, kb_recv_per_sec)
        insert_data(db_cursor, data)
        db_connection.commit()

        # Atualizar os dados anteriores para a próxima coleta
        prev_data['bytes_sent'] = bytes_sent
        prev_data['bytes_recv'] = bytes_recv

        time.sleep(interval)

except KeyboardInterrupt:
    print("Parando a coleta de dados.")
finally:
    db_cursor.close()
    db_connection.close()