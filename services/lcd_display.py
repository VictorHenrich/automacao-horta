from machine import Pin, I2C
from i2c_lcd import I2cLcd
from utils.exceptions import ServiceError
from utils.patterns import BaseService
from utils import config


class LCDDisplayService(BaseService):
    def __init__(
        self,
        i2c_sda_port=config.LCD_DISPLAY_SDA_PORT,
        i2c_scl_port=config.LCD_DISPLAY_SCL_PORT,
        i2c_address=config.LCD_DISPLAY_ADDRESS,
        number_of_lines=config.LCD_NUMBER_OF_LINES,
        number_of_columns=config.LCD_NUMBER_OF_COLUMNS,
    ):
        i2c = I2C(0, sda=Pin(i2c_sda_port), scl=Pin(i2c_scl_port))

        self.__lcd = I2cLcd(i2c, i2c_address, number_of_lines, number_of_columns)

        self.__message = ""

    def set_message(self, message):
        if isinstance(self.__message, str):
            raise TypeError(f"Valor da mensagem precisa ser caracterer!")

        self.__message = message

        return self

    def execute(self):
        try:
            self.__lcd.clean()

            messages = (self.__message or "").split("\n")

            for message_index in range(len(messages)):
                self.__lcd.move_to(0, message_index)

                self.__lcd.putstr(messages[message_index])

        except Exception as error:
            raise ServiceError(self, "Falha ao mostrar mensagem ao display", error)
