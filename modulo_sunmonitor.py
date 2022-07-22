from machine import I2C, Pin, SoftI2C, ADC, PWM
import time
import network, time, urequests, utime, ujson, random, framebuf
import ufirebase as firebase
from ssd1306 import SSD1306_I2C
    
#metodos para el manejo de la pantalla oled    
ancho = 128
alto = 64
i2c2 = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(ancho, alto, i2c2)

def oledsaludo(resultado):
    oled.fill(0)
    oled.text("*"*16,0,0)
    oled.text("   Sunmonitor   ",0,10)
    oled.text("   Bienvenido   ", 0, 20)
    oled.text(resultado, 0, 30)
    oled.text("*"*16, 0, 40)
    oled.show()

def oledmonitor(vbateria,vpanel,resultado):
    oled.fill(0)
    oled.text("*"*16,0,0)
    oled.text("   Sunmonitor   ",0,10)
    oled.text(" ", 0, 20)
    oled.text(f"Bateria: {vbateria} V", 0, 30)
    oled.text(f"Panel:   {vpanel} V", 0, 40)
    oled.text(resultado, 0, 50)
    oled.text("*"*16, 0, 70)
    oled.show()
    
def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

def notiiftttt(vbateria):
    print("enviar notificación, la bateria esta en: ", vbateria)