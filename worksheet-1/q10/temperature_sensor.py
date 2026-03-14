import paho.mqtt.client as mqtt
import random

from time import sleep

from config import TOPIC_TEMPERATURE, BROKER_HOST, BROKER_PORT


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect(BROKER_HOST, BROKER_PORT, 240)
mqttc.loop_start()

class TemperatureSensor:
    def __init__(self):
        self.temp = random.uniform(-4, 35)
    def get_temperature(self):
        self.temp = random.uniform(self.temp-2, self.temp+2)
        return self.temp

temp_sensor = TemperatureSensor()

while True:
    temp = temp_sensor.get_temperature()
    msg = f"{temp:.2f}"
    if not msg:
        break
    msg = msg.encode("utf-8")
    msg_info = mqttc.publish(TOPIC_TEMPERATURE, msg, qos=0)
    unacked_publish.add(msg_info.mid)
    sleep(7)


mqttc.disconnect()
mqttc.loop_stop()
