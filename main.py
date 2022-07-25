from machine import I2C, Pin, SoftI2C, ADC, PWM
import time
import network, time, urequests, utime, ujson, random, framebuf
import ufirebase as firebase
from ssd1306 import SSD1306_I2C
import ina219_lib
import modulo_sunmonitor
from time import localtime
import ntptime
    
#******************************************************Pantalla oled    
ancho = 128
alto = 64
i2c2 = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(ancho, alto, i2c2)

hora_act=0
dia_act=0
hora_not=0
dia_not=0
not_env=False

def envia_not(url,vbateria):
    global not_env
    global hora_not
    global dia_not
    notifvbateria = urequests.get(url+"&value1="+str(vbateria)) 
    print(notifvbateria.text)
    print (notifvbateria.status_code)
    notifvbateria.close ()
    not_env=True
    hora_not=hora_act
    dia_not=dia_act

for i in range (4):
    oled.blit(modulo_sunmonitor.buscar_icono("LOGOSUN.pbm"), 0, 0) # ruta y sitio de ubicación
    oled.show()  #mostrar
    
if modulo_sunmonitor.conectaWifi ("FMLA_ARDILAFLORES", "SamiLunaMichu123*"):
    resultado="   Conectado!   "
    modulo_sunmonitor.oledsaludo(resultado)
    
    url = "https://maker.ifttt.com/trigger/NotificaVBateria/with/key/cfUEB2Bw5DeKqyM-r7w-Zx?"
    
    firebase.setURL("https://monitor-panel-solar-default-rtdb.firebaseio.com/")
        
    while True:
        vbateria=round(ina219_lib.read_voltage(),2)
        vpanel=round(ina219_lib.read_voltage_pan(),2)
        time.sleep(4)
        
        modulo_sunmonitor.oledmonitor(vbateria,vpanel,resultado)
        
        message = {"Bateria: ":vbateria, "Panel:":vpanel } 
        firebase.put("PanelPrueba/", message, bg=0)
                
        if vbateria>=2.4:
            hora_act=int(modulo_sunmonitor.hora_actual())
            minuto_act=(modulo_sunmonitor.minuto_actual())
            dia_act=modulo_sunmonitor.fecha_actual()
            
            if dia_not==dia_act:
                if hora_act<=6 or hora_act>=19:
                    if not_env==False:
                     envia_not(url,vbateria)
                else:
                    if hora_act==hora_not:
                        if not_env==False:
                            envia_not(url,vbateria)
                    else:
                        envia_not(url,vbateria)
            else:
                if not_env==False:
                    envia_not(url,vbateria)
             
    
else:
    resultado="  Desconectado!"
    modulo_sunmonitor.oledsaludo(resultado)
    miRed.active (False)