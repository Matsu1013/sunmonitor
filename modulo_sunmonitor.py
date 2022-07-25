from machine import I2C, Pin, SoftI2C, ADC, PWM
import time
import network, time, urequests, utime, ujson, random, framebuf
import ufirebase as firebase
from ssd1306 import SSD1306_I2C
from time import localtime
import ntptime
    
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
    dibujo= open(ruta, "rb")  
    dibujo.readline() 
    xy = dibujo.readline() 
    x = int(xy.split()[0])  
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read()) 
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

#metodos para conexión a internet
def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():             
          miRed.active(True)                 
          miRed.connect(red, password)        
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():        
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True
    
    
#metodos para envio de notificaciones
def notiiftttt(vbateria):
    print("enviar notificación, la bateria esta en: ", vbateria)

#metodos para traer hora local actual
ntptime.host = "co.pool.ntp.org"
ntptime.settime ()     
timezone = -5
ntptime.settime ()
hora_local_seg = time.time () + timezone * 3600  #Hora local en segundos     
hora_local = time.localtime (hora_local_seg)     #Pasa a tupla de 8 elementos
    
def hora_actual():
    hora=("{:02}".format (hora_local[3]))
    return hora
        
def minuto_actual():
    minuto=("{:02}".format (hora_local[4]))
    return minuto
    
def fecha_actual():
    dia=("{:02}".format (hora_local[2]))
    return dia