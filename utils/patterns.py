class BaseService:
    def __init__(self):
        if type(self) is BaseService:
            raise Exception("Não é possível realizar instancia de uma classe Base")

    def execute(self):
        raise NotImplementedError(
            f"Método 'execute' não foi implementado na classe '{self.__class__.__name__}'"
        )


class ServiceResponse:
    def __init__(self, topic, data):
        self.__topic = topic

        self.__data = data

    @property
    def topic(self):
        return self.__topic

    @property
    def data(self):
        return self.__data
