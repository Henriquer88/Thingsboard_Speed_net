import speedtest
import time
import requests
import json

MIN_SPEED_THRESHOLD = 10  # Defina o limite mínimo de velocidade desejado em Mbps
CHECK_INTERVAL_SECONDS = 30  # Intervalo de verificação em segundos (30 segundos)

# Configurações do ThingBoard
THINGBOARD_URL = "https://thingsboard.cloud"  # Substitua com a URL correta do seu ThingBoard
DEVICE_ACCESS_TOKEN = "m882oyg2zqxstbrp0nrb"  # Substitua com o Token de Acesso do seu dispositivo

THINGBOARD_API_URL = f"{THINGBOARD_URL}/api/v1/{DEVICE_ACCESS_TOKEN}/telemetry"


def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()  # Seleciona o melhor servidor para teste
    download_speed = st.download() / 1024 / 1024  # Convertendo bytes para megabytes
    return download_speed


def send_data_to_thingboard(speed, alert=None):
    payload = {
        "download_speed": speed
    }

    if alert:
        payload["alert"] = alert

    headers = {
        "Content-Type": "application/json"
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

        if current_speed < MIN_SPEED_THRESHOLD:
            print("A velocidade da internet está baixa. Enviando alerta para o ThingBoard...")
            send_data_to_thingboard(current_speed, "A velocidade da internet está abaixo do limite.")
        else:
            send_data_to_thingboard(current_speed)  # Envia dados de velocidade mesmo se não houver alerta

        time.sleep(CHECK_INTERVAL_SECONDS)  # Aguarda o intervalo de verificação antes da próxima verificação
