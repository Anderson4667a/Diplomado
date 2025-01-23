from umqtt.simple import MQTTClient
import network, time

class Conexion():
    def conectaMQTT():
        # MQTT Server Parameters
        MQTT_CLIENT_ID = "clientasnKfj5x5zDA"
        MQTT_BROKER    = "broker.hivemq.com"
        #MQTT_BROKER    = "192.168.20.25"  #  en docker apuntar al host local
        MQTT_USER      = ""
        MQTT_PASSWORD  = ""
       
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
        client.connect()
        return client
    
    #___________________________________________________________#
    # conexion a internet
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
