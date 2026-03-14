import logging

BROKER_HOST = "broker.mqtt-dashboard.com"
BROKER_PORT = 1883
CHAT_TOPIC = "luisresende/q9/chat/"

class PromptToolkitHandler(logging.StreamHandler):
    def emit(self, record):
        from prompt_toolkit import print_formatted_text
        try:
            print_formatted_text(self.format(record))
        except Exception:
            self.handleError(record)

handler = PromptToolkitHandler()
handler.setFormatter(logging.Formatter('%(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False