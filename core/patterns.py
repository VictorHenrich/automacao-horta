class BaseService:
    def __init__(self):
        if type(self) is BaseService:
            raise Exception("Não é possível realizar instancia de uma classe Base")

    def execute(self):
        raise NotImplementedError(
            f"Método 'execute' não foi implementado na classe '{self.__class__.__name__}'"
        )


class ServiceResponse:
    def __init__(self, mqtt_topic=None, mqtt_data=None, display_message=None):
        self.__mqtt_topic = mqtt_topic

        self.__mqtt_data = mqtt_data

        self.__display_message = display_message

    @property
    def mqtt_topic(self):
        return self.__mqtt_topic

    @property
    def mqtt_data(self):
        return self.__mqtt_data

    @property
    def display_message(self):
        return self.__display_message
