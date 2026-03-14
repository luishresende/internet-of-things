import paho.mqtt.client as mqtt

from config import BROKER_HOST, BROKER_PORT, logger

class Lamp:
    def __init__(self):
        self.is_on = False

    def get_state(self):
        if self.is_on:
            return "on"
        return "off"

    def set_state(self, state):
        state = state.lower().strip()
        if state == "on":
            self.is_on = True
        elif state == "off":
            self.is_on = False
        logger.info(f"Estado atual da luz: {self.get_state()}")


# This is executed by cellphone.py
def turn_on_lamp_controller():
    lamp = Lamp()

    def on_connect(client, userdata, flags, rc, properties):
        print("Connected with result code "+str(rc))
        client.subscribe("luisresende/q10/light/")

    def on_message(client, userdata, msg):
        msg_data = msg.payload.decode("utf-8")
        lamp.set_state(msg_data) # Seta o novo estado da lampada


    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(BROKER_HOST, BROKER_PORT, 240)
    client.loop_start()
    return lamp
