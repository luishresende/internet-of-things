import paho.mqtt.client as mqtt

from config import TOPIC_TEMPERATURE, TOPIC_LIGHT, TOPIC_HUMIDITY, BROKER_HOST, BROKER_PORT, logger
from lamp import turn_on_lamp_controller

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC_TEMPERATURE)
    client.subscribe(TOPIC_HUMIDITY)

def on_message(client, userdata, msg):
    msg_data = msg.payload.decode("utf-8")
    logger.info(f"{msg.topic} → {msg_data}")


lamp = turn_on_lamp_controller()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.on_connect = on_connect

client.connect(BROKER_HOST, BROKER_PORT, 240)

client.loop_start()

try:
    while True:
        cmd = input("Digite 'on' ou 'off' para controlar a luz: ").strip().lower()
        if cmd in ("on", "off"):
            client.publish(TOPIC_LIGHT, cmd)
            logger.info(f"Comando enviado para a luz: {cmd}")

except KeyboardInterrupt:
    logger.info("Finalizando aplicação...")
finally:
    client.loop_stop()
    client.disconnect()
