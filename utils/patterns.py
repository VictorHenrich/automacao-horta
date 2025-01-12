class BaseService:
    def __init__(self):
        if type(self) is BaseService:
            raise Exception("Não é possível realizar instancia de uma classe Base")

    def execute(self):
        raise NotImplementedError(
            f"Método 'execute' não foi implementado na classe '{self.__class__.__name__}'"
        )
