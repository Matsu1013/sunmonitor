from machine import I2C, Pin, SoftI2C, ADC, PWM
import time
import network, time, urequests, utime, ujson, random, framebuf
""" 
INA219 Power Monitor interface.
Copyright GPL3.0 sergei.nz.
https://www.ti.com/lit/ds/symlink/ina219.pdf
"""

MAX_CURRENT = 3.2 # Amps
CURRENT_LSB = MAX_CURRENT/(2**15)
R_SHUNT = 0.1 # Ohms
CALIBRATION = int(0.04096 / (CURRENT_LSB * R_SHUNT))

CONF_R = 0x00
BUS_V_R = 0x02
POWER_R = 0x03
CURRENT_R = 0x04
CALIBRATION_R = 0x05

ADDRESS = 0x40

SDA = Pin(21)
SCL = Pin(22)
FREQ = 400000

i2c = SoftI2C(sda=SDA,scl=SCL,freq=FREQ)
i2c.writeto_mem(ADDRESS, CALIBRATION_R ,(CALIBRATION).to_bytes(2, 'big'))

def read_voltage():
    return (int.from_bytes(i2c.readfrom_mem(ADDRESS, BUS_V_R, 2), 'big') >> 3) * 0.004

def read_current():
    raw_current = int.from_bytes(i2c.readfrom_mem(ADDRESS, SHUNT_V_R, 2), 'big')
    if raw_current >> 15:
        raw_current -= 2**16
    return raw_current * CURRENT_LSB

#nuevo metodo creado para consultar voltaje de una segunda fuente.

SDA_pan = Pin(19)
SCL_pan = Pin(18)

i2c_pan = SoftI2C(sda=SDA_pan,scl=SCL_pan,freq=FREQ)
i2c_pan.writeto_mem(ADDRESS, CALIBRATION_R ,(CALIBRATION).to_bytes(2, 'big'))
def read_voltage_pan():
    return (int.from_bytes(i2c_pan.readfrom_mem(ADDRESS, BUS_V_R, 2), 'big') >> 3) * 0.004