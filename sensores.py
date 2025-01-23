from machine import Pin, I2C, Timer
import time
from hcsr04 import HCSR04
from ssd1306 import SSD1306_I2C

class Sensores():
        
    def Hcsr04():
        sensor = HCSR04 (trigger_pin=12, echo_pin=14) #objetos  
        return sensor.distance_cm()
        
    def I2c():
        return I2C(sda=Pin(21), scl=Pin(22))
    
    def Display(i2c):
        return SSD1306_I2C(128, 64, i2c)# display depende de la pantalla 

    def DisplayView(display, distan, flujo):
        display.fill(0)  # Limpiar la pantalla al inicio
        display.pixel(64, 32, 1)  # Muestra un pixel
        display.hline(0, 0, 128, 1)
        display.hline(0, 20, 128, 1)
        display.vline(0, 0, 20, 1)
        display.vline(127, 0, 20, 1)
        display.text("Datos", 50, 10)
        display.text("Distancia:", 0, 40)
        display.text(str(round(distan, 2)), 80, 40)
        display.text("Flujo:", 0, 50)
        display.text(str(round(flujo, 2)), 80, 50)
        display.show()
        time.sleep(1) 

            
    def medir_caudal(): 
        sf = Pin(25, Pin.IN) 
        count = 0 
        Q_min = 0.0 
        reloj = Timer(0) 
        def conteo(pin): 
            nonlocal count 
            count += 1 
            
        def freq(timer): 
            nonlocal count, Q_min 
            frec = count 
            Q_min = frec / 7.5 # Litros por minuto 
            count = 0
        
        sf.irq(trigger=Pin.IRQ_RISING, handler=conteo)
        reloj.init(mode=Timer.PERIODIC, period=1000, callback=freq) 
        print(Q_min)
        # Devolvemos una función para obtener los valores actuales 
        def obtener_Q_min():
            return Q_min
        
        return obtener_Q_min