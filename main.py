from machine import I2C, Pin, SoftI2C, ADC, PWM
import time
import network, time, urequests, utime, ujson, random, framebuf
import ufirebase as firebase
from ssd1306 import SSD1306_I2C
import ina219_lib
import modulo_sunmonitor
    
#******************************************************Pantalla oled    
ancho = 128
alto = 64
i2c2 = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(ancho, alto, i2c2)
#****************************************************************Código
    
for i in range (4):
    oled.blit(modulo_sunmonitor.buscar_icono("LOGOSUN.pbm"), 0, 0) # ruta y sitio de ubicación
    oled.show()  #mostrar
if modulo_sunmonitor.conectaWifi ("FMLA_ARDILAFLORES", "SamiLunaMichu123*"):
    resultado="   Conectado!   "
    modulo_sunmonitor.oledsaludo(resultado)
    firebase.setURL("https://monitor-panel-solar-default-rtdb.firebaseio.com/")
    while True:
        vbateria=ina219_lib.read_voltage()
        vpanel=ina219_lib.read_voltage_pan()
        print(vpanel)
        time.sleep(3)
        
        modulo_sunmonitor.oledmonitor(vbateria,vpanel,resultado)
        
        message = {"Bateria: ":vbateria, "Panel:":vpanel } 
        #***********************************************************cambiar a una BD limpia
        firebase.put("PanelPrueba/", message, bg=0)
        
        url = "https://maker.ifttt.com/trigger/NotificaVBateria/with/key/cfUEB2Bw5DeKqyM-r7w-Zx?"
        if vbateria>12.4:       
            notifvbateria = urequests.get(url+"&value1="+str(vbateria)) 
            print("text: ",notifvbateria.text)
            print ("status code: ",notifvbateria.status_code)
            notifvbateria.close ()
    
else:
    resultado="  Desconectado!"
    modulo_sunmonitor.oledsaludo(resultado)
    miRed.active (False)