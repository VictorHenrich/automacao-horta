from services.manager import ServiceManager
from services.infrared_sensor import InfraredSensorService
from services.water_sensor import WaterSensorService
from services.soil_sensor import SoilSensorService
from services.humidity_and_temperature_sensor import HumidityAndTemperatureSensorService


gerden_service_manager = ServiceManager(
    InfraredSensorService(),
    WaterSensorService(),
    SoilSensorService(),
    HumidityAndTemperatureSensorService(),
)


while True:
    gerden_service_manager.execute()
