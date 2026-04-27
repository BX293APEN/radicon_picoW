from OpenPort import PortSetup
from machine import Pin

class RadioControlCar():
    def control(self, key = " "):
        if(key == "w"):
            self.leftGPIO1.value(1)
            self.leftGPIO2.value(0)
            self.rightGPIO1.value(1)
            self.rightGPIO2.value(0)

            self.leftLED.value(1)
            self.rightLED.value(1)
            return "UP"

        elif(key == "s"):
            self.leftGPIO1.value(0)
            self.leftGPIO2.value(1)
            self.rightGPIO1.value(0)
            self.rightGPIO2.value(1)
            self.leftLED.value(0)
            self.rightLED.value(0)
            return "DOWN"

        elif(key == "d"):
            self.leftGPIO1.value(0)
            self.leftGPIO2.value(1)
            self.rightGPIO1.value(1)
            self.rightGPIO2.value(0)
            self.leftLED.value(0)
            self.rightLED.value(1)
            return "RIGHT"

        
        elif(key == "a"): # 左
            self.leftGPIO1.value(1)
            self.leftGPIO2.value(0)
            self.rightGPIO1.value(0)
            self.rightGPIO2.value(1)
            self.leftLED.value(1)
            self.rightLED.value(0)
            return "LEFT"


        else:
            self.leftGPIO1.value(0)
            self.leftGPIO2.value(0)
            self.rightGPIO1.value(0)
            self.rightGPIO2.value(0)
            self.leftLED.value(0)
            self.rightLED.value(0)
            return "STOP"

    def __init__(
        self,
        leftLED         = 4,
        rightLED        = 7,
        leftGPIO1       = 14,
        leftGPIO2       = 15,
        rightGPIO1      = 17,
        rightGPIO2      = 16
    ):
        self.ledOnboard = Pin('LED', Pin.OUT)
        self.ledOnboard.value(0)
        self.leftLED    = Pin(leftLED, Pin.OUT)
        self.rightLED   = Pin(rightLED, Pin.OUT)
        self.leftGPIO1  = Pin(leftGPIO1, Pin.OUT)
        self.leftGPIO2  = Pin(leftGPIO2, Pin.OUT)
        self.rightGPIO1 = Pin(rightGPIO1, Pin.OUT)
        self.rightGPIO2 = Pin(rightGPIO2, Pin.OUT)

        self.control()

if __name__ == "__main__":
    rcc = RadioControlCar()
    with PortSetup("./config.json", ipAddress = "192.168.10.60", port = 8080) as udpPort:
        while True:
            data, sIPAddr = udpPort.recvData()
            d = data.decode("UTF-8").strip()
            print(rcc.control(d))

