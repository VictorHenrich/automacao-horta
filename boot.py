from core.manager import ServiceManager
from services.infrared_sensor import InfraredSensorService
from services.water_sensor import WaterSensorService
from services.soil_sensor import SoilSensorService
from services.photoresistor_sensor import PhotoresistorSensorService
from services.humidity_and_temperature_sensor import HumidityAndTemperatureSensorService
from services.temperature_sensor import TemperatureSensorService


gerden_service_manager = ServiceManager(
    InfraredSensorService(),
    WaterSensorService(),
    SoilSensorService(),
    HumidityAndTemperatureSensorService(),
    PhotoresistorSensorService(),
    TemperatureSensorService(),
    send_to_mqtt=True,
    display_execution_time=None,
    service_execution_time=None,
    show_message_in_console=True,
    show_message_in_display=True,
)


gerden_service_manager.execute()
