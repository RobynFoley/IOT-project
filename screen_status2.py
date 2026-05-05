from flask import Flask, request
from gpiozero import Buzzer
from time import sleep
from datetime import datetime, timedelta
import threading
import BlynkLib
import requests

BLYNK_AUTH = 'bFFTX9p1qbTDB5emYl2yOuSqk5-NBBKk'

blynk = BlynkLib.Blynk(BLYNK_AUTH)

app = Flask(__name__)
buzzer = Buzzer(16)
current_speed = 0.0

# run blynk in background
threading.Thread(target=blynk.run, daemon=True).start()
def safe_blynk_write(pin, value):
    try:
        requests.get(
            f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH}&v{pin}={value}",
            timeout=2
        )
    except Exception as e:
        print(f"Blynk write failed: {e}")

# just after blynk setup, before app.run
sleep(2)  # give blynk time to connect
print("Sent test speed to Blynk")
@app.route("/phone")
def phone():
    global current_speed
    state = request.args.get("state")
    speed = request.args.get("speed")
    print("Phone state:", state)

    if speed is not None:
        try:
            current_speed = float(speed)
            safe_blynk_write(1, current_speed)
        except ValueError:
            pass

    if state == "UNLOCKED":
        print("🚨 TRIGGER ALARM")
        safe_blynk_write(0, 1)
        for _ in range(3):
            buzzer.on()
            sleep(0.1)
            buzzer.off()
            sleep(0.1)
        print(speed)
    else:
        print("calm")
        safe_blynk_write(0, 0)
        print(speed)

    return "OK"

def send_to_blynk():
    while True:
        safe_blynk_write(1, current_speed)
        sleep(1)  # send every second

threading.Thread(target=send_to_blynk, daemon=True).start()

def speed_logger():
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Current speed: {current_speed:.1f} km/h")
        with open("speed_log.txt", "a") as f:
            f.write(f"[{timestamp}] {current_speed:.1f} km/h\n")
        sleep(30)

threading.Thread(target=speed_logger, daemon=True).start()
app.run(host="0.0.0.0", port=5000)
