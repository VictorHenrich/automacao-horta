from services.infrared_sensor import InfraredSensorService
from utils import config


infrared_sensor_service = InfraredSensorService(port=config.INFRARED_SENSOR_PORT)

while True:
    infrared_sensor_service.execute()
