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
        leftLED         = 0,
        rightLED        = 0,
        leftGPIO1       = 19,
        leftGPIO2       = 20,
        rightGPIO1      = 22,
        rightGPIO2      = 21
    ):
        self.ledOnboard = Pin('LED', Pin.OUT)
        self.ledOnboard.value(0)
        self.leftLED    = leftLED
        self.rightLED   = rightLED
        self.leftGPIO1  = leftGPIO1
        self.leftGPIO2  = leftGPIO2
        self.rightGPIO1 = rightGPIO1
        self.rightGPIO2 = rightGPIO2

        self.control()

if __name__ == "__main__":
    rcc = RadioControlCar()
    with PortSetup("./config.json", ipAddress = "192.168.10.80", port = 8080) as udpPort:
        while True:
            data, sIPAddr = udpPort.recvData()
            d = data.decode("UTF-8").strip()
            print(rcc.control(d))

