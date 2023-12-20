from machine import Pin,SPI,PWM,ADC
import framebuf
import time
import math
import network
import socket

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
    def init_display(self):
        self.rst(1)
        self.rst(0)
        self.rst(1)
        self.write_cmd(0x36)
        self.write_data(0x70)
        self.write_cmd(0x3A) 
        self.write_data(0x05)
        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)
        self.write_cmd(0xB7)
        self.write_data(0x35)
        self.write_cmd(0xBB)
        self.write_data(0x19)
        self.write_cmd(0xC0)
        self.write_data(0x2C)
        self.write_cmd(0xC2)
        self.write_data(0x01)
        self.write_cmd(0xC3)
        self.write_data(0x12)   
        self.write_cmd(0xC4)
        self.write_data(0x20)
        self.write_cmd(0xC6)
        self.write_data(0x0F)
        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)
        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)
        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)
    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
               

def sendvalue(val):
    cl.send(str(val))
    
def receivevalue():
    return cl.recv(1024)
    
if __name__=='__main__':
    print("Calibrating...")
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 80))
    s.listen()
    (cl, addr) = s.accept()
    print("Connected")
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)
    LCD = LCD_1inch14()
    LCD.fill(LCD.white)
    LCD.show()

    LCD.show()
    key1 = Pin(2,Pin.IN,Pin.PULL_UP)
    key2 = Pin(3,Pin.IN,Pin.PULL_UP)
    key3 = Pin(15 ,Pin.IN,Pin.PULL_UP)
    key4 = Pin(17 ,Pin.IN,Pin.PULL_UP)
    kuutio = 1
    vuoro = 0
    x = 0
    y = 0
    merkki = ""
    taytetytX = []
    taytetytO = []
    jakojaamat = []
    
    def voitto(ristinolla,voittaja):
        for i in range(len(ristinolla)): # tarkistaa voittaako pystysuunta
            jakojaamat.append(ristinolla[i] % 3)
            for rivit in range(3):
                if jakojaamat.count(rivit) == 3:
                    LCD.text(voittaja+" voitti",150,30,LCD.blue)
                    for i in range(10):
                        taytetytX.append(i)
        kuutiocheck = 0
        
        for i in range(1,10): #tarkistaa voittaako vaakasuunta
            if ristinolla.count(i) == 1:
                kuutiocheck += 1
                if kuutiocheck == 3:
                    LCD.text(voittaja+" voitti",150,30,LCD.blue)
                    for i in range(10):
                        taytetytX.append(i)
                        
            if(i % 3 == 0):
                kuutiocheck = 0
                
        vinokuutiocheck = 0
        for i in range(1,14,4):
            if ristinolla.count(i) == True:
                vinokuutiocheck += 1
                if vinokuutiocheck == 3:
                    LCD.text(voittaja+" voitti",150,30,LCD.blue)
                    for i in range(10):
                        taytetytX.append(i)
                        
        vinokuutiocheck2 = 0
        for i in range(3,8,2):
            if ristinolla.count(i) == True:
                vinokuutiocheck2 += 1
                if vinokuutiocheck2 == 3:
                    LCD.text(voittaja+" voitti",150,30,LCD.blue)
                    for i in range(10):
                        taytetytX.append(i)
                        
    while 1:
        if len(taytetytX) + len(taytetytO) < 9:
            taytetty = True
            if(key1.value() == 0):
                kuutio += 1
                time.sleep(0.25)
            while taytetty == True:
                if(kuutio > 9):
                    kuutio = 1
                if kuutio in taytetytX or kuutio in taytetytO:
                    kuutio += 1
                else:
                    taytetty = False
                    
            x = 80 + (kuutio-1) % 3 * 20
            y = 40 + math.floor((kuutio-0.01)/3)*20
            LCD.rect(100,40,20,20,LCD.blue)
            LCD.rect(100,60,20,20,LCD.blue)
            LCD.rect(100,80,20,20,LCD.blue)
            LCD.rect(80,40,20,20,LCD.blue)
            LCD.rect(80,60,20,20,LCD.blue)
            LCD.rect(80,80,20,20,LCD.blue)
            LCD.rect(120,40,20,20,LCD.blue)
            LCD.rect(120,60,20,20,LCD.blue)
            LCD.rect(120,80,20,20,LCD.blue)
            
            if(vuoro % 2 == 0):
                LCD.text("VALITSE O",150,40,LCD.blue)
                if(key2.value() == 0):
                    LCD.text("O",x+6,y+6,LCD.blue)
                    vuoro += 1
                    taytetytO.append(kuutio)
                    print("O:" ,taytetytO)
                    sendvalue(kuutio)
                    time.sleep(0.25)
                    voitto(taytetytO,"O")
                    LCD.text("VALITSE O",150,40,LCD.white)
                    jakojaamat.clear()
            else:
                
                valu = int(receivevalue())
                x = 80 + (valu-1) % 3 * 20
                y = 40 + math.floor((valu-0.01)/3)*20
                LCD.text("X",x+6,y+6,LCD.blue)
                taytetytX.append(valu)
                print("X:" ,taytetytX)
                time.sleep(0.25)
                voitto(taytetytX,"X")
                    
                jakojaamat.clear()
                vuoro += 1
                
            LCD.rect(x,y,20,20,LCD.red)
            LCD.show()
        elif(len(taytetytO) + len(taytetytX) == 9):
            LCD.text("Tasapeli",150,30,LCD.blue)
            LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)
