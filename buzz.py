from gpiozero import Buzzer
from time import sleep
from grove.gpio import GPIO

buzzer = Buzzer(5)  # D5 = GPIO5
PIR_PIN = 16      # D16

#buzzer.on()
sleep(0.1)
buzzer.off()

def read_pir():
    pir = GPIO(PIR_PIN, GPIO.IN)
    return pir.read()

while True:
    motion = read_pir()
    print(f"Motion:      {motion}")
    sleep(3)

