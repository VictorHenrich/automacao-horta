from machine import Pin, I2C
import time
from libs.lcd.i2c_lcd import I2cLcd
from core import config


class LCDDisplay:
    def __init__(
        self,
        i2c_sda_port=config.LCD_DISPLAY_SDA_PORT,
        i2c_scl_port=config.LCD_DISPLAY_SCL_PORT,
        i2c_address=config.LCD_DISPLAY_ADDRESS,
        number_of_lines=config.LCD_NUMBER_OF_LINES,
        number_of_columns=config.LCD_NUMBER_OF_COLUMNS,
    ):
        i2c = I2C(0, sda=Pin(i2c_sda_port), scl=Pin(i2c_scl_port))

        component_address = self.__get_address(i2c, i2c_address)

        self.__lcd = I2cLcd(i2c, component_address, number_of_lines, number_of_columns)

    def __get_address(self, i2c, address_default):
        i2c_address = address_default

        if i2c_address is None:
            try:
                i2c_address = i2c.scan()[0]

            except IndexError:
                raise Exception(
                    f"Não foi possível localizar nenhum endereço para o dispositivo LCD!"
                )

        return i2c_address

    def print_message(self, *messages, execution_time=1):
        self.__lcd.clear()

        for message_index in range(len(messages)):
            self.__lcd.move_to(0, message_index)

            self.__lcd.putstr(messages[message_index])

            time.sleep(execution_time)
