from machine import Pin, I2C
from libs.lcd.i2c_lcd import I2cLcd
from core import config


class LCDDisplay(I2cLcd):
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

        self.__number_of_columns = number_of_columns

        self.__number_of_lines = number_of_lines

        super().__init__(i2c, component_address, number_of_lines, number_of_columns)

        self.backlight_on()

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

    def print_message(self, message):
        self.clear()

        text_parts = []

        if "\n" in message:
            broken_message = message.split("\n")

            text_parts = [
                text_part[: self.__number_of_columns] for text_part in broken_message
            ]

        else:
            text_parts = [
                message[index : index + self.__number_of_columns]
                for index in range(0, len(message), self.__number_of_columns)
            ]

        for text_row, text_part in enumerate(text_parts[: self.__number_of_lines]):
            self.move_to(0, text_row)

            self.putstr(text_part)
