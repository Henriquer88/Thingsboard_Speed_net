import speedtest
import time
import requests
import json
# tst
MIN_SPEED_THRESHOLD = 10  # Defina o limite mínimo de velocidade desejado em Mbps

# Configurações do ThingBoard
THINGBOARD_URL = "https://thingsboard.cloud"  # Substitua com a URL correta do seu ThingBoard
DEVICE_ACCESS_TOKEN = "m882oyg2zqxstbrp0nrb"  # Substitua com o Token de Acesso do seu dispositivo

THINGBOARD_API_URL = f"{THINGBOARD_URL}/api/v1/{DEVICE_ACCESS_TOKEN}/telemetry"

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()  # Seleciona o melhor servidor para teste
    download_speed = st.download() / 1024 / 1024  # Convertendo bytes para megabytes
    return download_speed

def send_data_to_thingboard(speed):
    payload = {
        "download_speed": speed
    }

    headers = {
        "Content-Type": "application/json",
        "X-Authorization": "Bearer " + DEVICE_ACCESS_TOKEN
    }

    try:
        response = requests.post(THINGBOARD_API_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print("Dados enviados para o ThingBoard com sucesso!")
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para o ThingBoard:", e)

if __name__ == "__main__":
    while True:
        current_speed = test_speed()
        print(f"Velocidade de download: {current_speed:.2f} Mbps")
        send_data_to_thingboard(current_speed)
        time.sleep(50)  # Aguarda 5 minutos (300 segundos) antes de fazer a próxima verificação
