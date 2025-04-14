import network
import urequests
import time
import json


def load_config(filename="config.txt"):
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except OSError:
        print(f"Erro ao ler arquivo de configuração '{filename}'.")
    finally:
        print('\nLeitura do arquivo finalizada.')
    return config


# Carrega do arquivo de configuração
config = load_config()

# Configurações da rede WiFi
WIFI_SSID = config.get('WIFI_SSID_NODE')
WIFI_PASSWORD = config.get('WIFI_PASSWORD_NODE')
SERVER_IP = config.get('SERVER_IP')
SERVER_PORT = config.get('SERVER_PORT')

# Endereço do servidor Flask
SERVER_URL = f'http://{SERVER_IP}:{SERVER_PORT}/data'


def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando ao WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(2)
        print('Conectado ao WiFi. IP:', sta_if.ifconfig()[0])
        return sta_if
    else:
        print('Já conectado ao WiFi. IP:', sta_if.ifconfig()[0])
        return sta_if


def send_data(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(SERVER_URL, json=data, headers=headers)
        print('Resposta do servidor:', response.status_code, response.text)
        response.close()
    except Exception as e:
        print('Erro ao enviar dados:', e)


# Conectar ao WiFi
wifi = connect_wifi()

# Exemplo de dados a serem enviados
sensor_data = {
    'temperatura': 25.5,
    'umidade': 60.2,
    'leitura': 123
}

# Enviar os dados periodicamente
while True:
    send_data(sensor_data)
    time.sleep(5)  # Envia dados a cada 5 segundos
