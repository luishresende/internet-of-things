import paho.mqtt.client as mqtt
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import argparse

from config import CHAT_TOPIC, BROKER_HOST, BROKER_PORT, logger

argparser = argparse.ArgumentParser()
argparser.add_argument("username", type=str, help="Username to use")

args = argparser.parse_args()

my_username = args.username


def on_connect(client, userdata, flags, rc, properties):
    logger.info(f"Connected with result code {rc}")
    client.subscribe(CHAT_TOPIC)

def on_message(client, userdata, msg):
    msg_data = msg.payload.decode("utf-8")
    logger.info(f"{msg.topic} → {msg_data}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.on_connect = on_connect

client.connect(BROKER_HOST, BROKER_PORT, 240)
client.loop_start()

session = PromptSession()

try:
    with patch_stdout():
        while True:
            msg = session.prompt("Digite a sua mensagem: ").strip().lower()
            if msg:
                msg = f"{my_username}: {msg}"
                client.publish(CHAT_TOPIC, msg, qos=2)

except KeyboardInterrupt:
    logger.info("Finalizando aplicação...")
finally:
    client.loop_stop()
    client.disconnect()
