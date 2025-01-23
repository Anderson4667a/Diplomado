from conexion import Conexion
from sensores import Sensores
from utime import sleep_ms
import ujson

try:
    if Conexion.conectaWifi("LOPEZ 5G", "FIOn41073"):
        print("Conexión exitosa!")
        print("Conectando a MQTT server...")
        clientMqtt = Conexion.conectaMQTT()
        
        try:
            i2c = Sensores.I2c()
            display = Sensores.Display(i2c)
            obtener_flujo = Sensores.medir_caudal()
            
            while True:                
                # Obtenemos variables del sensor
                distan = None
                flujo = None
                distan = Sensores.Hcsr04()

                # Para obtener los datos periódicamente 
                flujo = obtener_flujo()
                flujo_hora = flujo * 60   
               
                
                print("Revisando Condiciones ...... ")
                message = ujson.dumps({
                    "Distancia": distan,
                    "FlujoMin": flujo,
                    "FlujoHora": flujo_hora
                })
                
                # Mostrando datos en Display
                sleep_ms(400)
                Sensores.DisplayView(display, distan, flujo)
                
                # Envio de datos
                MQTT_TOPIC = "Monitoreo/tanque/agua1"
                print("Reportando a MQTT topic {}: {}".format(MQTT_TOPIC, message))
                clientMqtt.publish(MQTT_TOPIC, message)
            
        except KeyboardInterrupt:
                print("Desconectando del broker MQTT...")
                clientMqtt.loop_stop()
                clientMqtt.disconnect()
    else:
        print("Imposible conectar con wifi")
except Exception as ex:
    print('Ha ocurrido un error:', ex)
