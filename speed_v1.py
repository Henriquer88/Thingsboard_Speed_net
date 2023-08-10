import speedtest
import time

MIN_SPEED_THRESHOLD = 10  # Defina o limite mínimo de velocidade desejado em Mbps

def test_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convertendo bytes para megabytes
    return download_speed

def check_speed():
    current_speed = test_speed()
    print(f"Velocidade de download: {current_speed:.2f} Mbps")

    if current_speed < MIN_SPEED_THRESHOLD:
        print("A velocidade da internet está baixa.")

if __name__ == "__main__":
    while True:
        check_speed()
        time.sleep(300)  # Aguarda 5 minutos antes de fazer a próxima verificação
