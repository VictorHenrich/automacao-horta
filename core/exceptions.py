class ServiceError(Exception):
    def __init__(self, service_object, description, error):
        message = (
            f"Falha no serviço {type(service_object).__name__}\n"
            + f"Descrição do erro: {description}\n"
            + f"Erro disparado: {type(error).__name__}\n"
            + f"Descrição do erro: {error}"
        )

        super().__init__(message)
