from machine import Pin, ADC


class PinAttenuityTypes:
    ATTN_11DB = ADC.ATTN_11DB

    ATTN_2_5DB = ADC.ATTN_2_5DB

    ATTN_0DB = ADC.ATTN_0DB

    ATTN_6DB = ADC.ATTN_6DB


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

        super().__init__(pin, atten=PinAttenuityTypes.ATTN_11DB, **kwargs)
