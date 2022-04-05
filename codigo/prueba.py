import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('/dev/ttyACM0')
    print("Communication Successfully started")
    LED = board.digital[9]
    LED.mode = pyfirmata.PWM
    x = 0
    while True:
        print(x)
        LED.write(x)
        time.sleep(3)
        x = x+10

