import logging

BROKER_HOST = "broker.mqtt-dashboard.com"
BROKER_PORT = 1883
TOPIC_TEMPERATURE = "luisresende/q10/temperature/"
TOPIC_HUMIDITY = "luisresende/q10/humidity/"
TOPIC_LIGHT = "luisresende/q10/light/"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)