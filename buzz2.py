from gpiozero import MotionSensor, Buzzer
from time import sleep

pir = MotionSensor(5)  # D16
buzzer = Buzzer(16)# D5

pir.motion_detected
sleep(10)
while True:
    if pir.motion_detected:
        print("Motion!")
        buzzer.on()
        sleep(0.1)
        buzzer.off()
        sleep(0.1)
        buzzer.on()
        sleep(0.1)
        buzzer.off()
        sleep(0.1)
        buzzer.on()
        sleep(0.1)
        buzzer.off()
    else:
        print("no")
    sleep(1)
