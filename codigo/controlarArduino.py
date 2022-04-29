import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('/dev/ttyACM0')
    print("Communication Successfully started")
    LED = board.digital[9]
    LED1 = board.digital[10]
    LED.mode = pyfirmata.PWM
    LED1.mode = pyfirmata.PWM
    x = 0
    while True:
        print(x)
        LED.write(x)
        LED1.write(x)
        time.sleep(3)
        x = x+10

