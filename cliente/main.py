import network
import gc
import urequests
import time
import json
from machine import Pin


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

led = Pin(2, Pin.OUT)


def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando ao WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(2)
        print('Conectado ao WiFi. IP:', sta_if.ifconfig()[0])
    else:
        print('Já conectado ao WiFi. IP:', sta_if.ifconfig()[0])
    return sta_if


def send_data(data):
    try:
        led.value(1)  # Acende o led antes de enviar
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(SERVER_URL, json=data, headers=headers)
        print('Resposta do servidor:', response.status_code, response.text)
        response.close()
        led.value(0)  # Apaga o LED após receber a resposta (ou falhar)
        time.sleep(0.1)  # Pequena pausa para o flash ser visível
        led.value(1)  # Prepara para o próximo envio
        time.sleep(0.1)
        led.value(0)
    except Exception as e:
        print('Erro ao enviar dados:', e)


# Conectar ao WiFi
wifi = connect_wifi()


def get_wifi_info():
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        return {
            "Conectado": True,
            "Nome_Rede": sta_if.config('essid'),
            "Sinal_wifi": sta_if.status('rssi'),
            "IP": sta_if.ifconfig()[0],
            "Endereco_MAC": sta_if.config('mac').hex(':')
        }
    else:
        return {"Conectado": False}


def get_memory_info():
    return {
        "Memoria_Livre": gc.mem_free(),
        "Memoria_Usada": gc.mem_alloc()
    }


while True:
    data = {
        "wifi_info": get_wifi_info(),
        "memoria_info": get_memory_info()
    }
    send_data(data)
    time.sleep(5)  # Envia dados a cada 5 segundos
