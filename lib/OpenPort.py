import machine, json, network, ntptime, utime
from socket import socket, AF_INET, SOCK_DGRAM

class PortSetup:
    def led_blinking(self, count, t = 0.1):
        if self.led is not None:
            for i in range(count):
                self.led.value(1)
                utime.sleep(t)
                self.led.value(0)
                utime.sleep(t)
            
    def wlan_connect(self):
        while True:
            for ap in self.wlan.scan():
                print(ap[0].decode("UTF-8"))
                if ap[0].decode("UTF-8") == self.configData["wi-fi"]["ssid"]:
                    self.wlan.connect(self.configData["wi-fi"]["ssid"], self.configData["wi-fi"]["password"])
                    self.wlan.ifconfig(
                        [
                            self.ipAddress,
                            self.configData["wi-fi"]["netmask"],
                            self.configData["wi-fi"]["gateway"],
                            self.configData["wi-fi"]["dns"]
                        ]
                    )
                    return
            print("SSIDが見つかりませんでした")
    def __init__(
        self, 
        configFile          = "./config/config.json", 
        ipAddress           = "192.168.10.80", 
        port                = 80,
        led                 = None,
    ):
        self.wlan_status    ={
            network.STAT_IDLE           : "IDLE",
            network.STAT_CONNECTING     : "CONNECTING",
            network.STAT_WRONG_PASSWORD : "WRONG_PASSWORD",
            network.STAT_NO_AP_FOUND    : "AP_NOT_FOUND",
            network.STAT_CONNECT_FAIL   : "不明なエラー",
            network.STAT_GOT_IP         : "SUCCESS"
        }
        self.led            = led
        with open(configFile, "r", encoding="UTF-8") as configFile:
            self.configData = json.loads(configFile.read())
        self.ipAddress      = ipAddress
        self.port           = port
        self.wlan           = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan_connect()
        
        print('Connecting to Wi-Fi router')
        while not self.wlan.isconnected():
            utime.sleep(1)
            print(self.wlan_status[self.wlan.status()])
            if self.led is not None:
                self.led.value(1 - self.led.value())

        wlanStatus =  self.wlan.ifconfig()
        print(f""" === WLAN STATUS ===
IP Address          : {wlanStatus[0]}
Netmask             : {wlanStatus[1]}
Default Gateway     : {wlanStatus[2]}
Name Server         : {wlanStatus[3]}
"""
        )
        self.led_blinking(3)

        ntptime.host = self.configData["ntp"]["host"]
        while True:
            try:
                ntptime.settime()
                break
            except:
                pass
        (year, month, day, hours, minutes, seconds, weekday, yearday) = utime.localtime(utime.mktime(utime.localtime()) + self.configData["ntp"]["offset"]*3600)
        rtc = machine.RTC()
        rtc.datetime((year, month, day, weekday, hours, minutes, seconds, 0))
    
    def __enter__(self):
        addr = (self.ipAddress, self.port)                  # IPアドレスとポート番号のタプルを作成
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)        # ソケットオブジェクトを作成
        self.udpSocket.bind(addr)                           # IPアドレスとポート番号をバインド
        print(self.udpSocket)                               # ソケットオブジェクトを出力
        return self
    
    def __exit__(self, *args):
        self.udpSocket.close()
        self.wlan.disconnect()
    
    def recvData(self, bufSize = 1024):
        data, addr = self.udpSocket.recvfrom(bufSize)
        return [data, addr]