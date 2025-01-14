from services.water_sensor import WaterSensorService
from utils import config


water_sensor_service = WaterSensorService(port=config.WATER_SENSOR_PORT)

while True:
    water_sensor_service.execute()
