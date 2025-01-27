from umqtt.simple import MQTTClient
import json
import time
from core import config


class MQTTIntegration(MQTTClient):
    def __init__(
        self, host=config.MQTT_HOST, port=config.MQTT_PORT, message_callback=None
    ):
        client_id = f"{config.DEFAULT_CLIENT_ID}_{time.time()}"

        super().__init__(client_id, host, port)

        if message_callback:
            self.set_callback(message_callback)

    def publish(self, topic, message):
        data = message

        if isinstance(data, dict):
            data = json.dumps(data)

        super().publish(topic, data)
