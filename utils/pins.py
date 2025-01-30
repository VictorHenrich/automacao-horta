from machine import Pin, ADC


class PinTypes:
    IN = Pin.IN

    OUT = Pin.OUT

    PULL_DOWN = Pin.PULL_DOWN


class DigitalPin(Pin):
    def __init__(self, port, type=PinTypes.IN, *args):
        super().__init__(port, type, *args)


class AnalogPin(ADC):
    def __init__(self, port, type=PinTypes.IN, **kwargs):
        pin = Pin(port, type)

        super().__init__(pin, atten=ADC.ATTN_11DB, **kwargs)
