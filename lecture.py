import serial
import time
PORT = '/dev/ttyACM0'
BAUD_RATE = 115200
esp32 = None
def init():
    global esp32
    try:
        print(f"Tentative de connexion à {PORT} au baud rate {BAUD_RATE}...")
        esp32 = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Petite pause pour laisser l'ESP32 s'initialiser
        print("Connexion réussie ! En attente de données...\n")
        return True
    except:
        return False

def get_info():
    derniere_valeur = None
    while esp32.in_waiting > 0:
        ligne = esp32.readline().decode("utf-8", errors="ignore").strip()
        try:
            derniere_valeur = int(ligne)
        except ValueError:
            continue
    return derniere_valeur




