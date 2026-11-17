"""Camada Model (MVC): regras de negócio e persistência."""


class ValidacaoError(Exception):
    """Erro de regra de negócio/validação, exibido ao usuário."""

    def __init__(self, erros):
        if isinstance(erros, str):
            erros = [erros]
        self.erros = list(erros)
        super().__init__("; ".join(self.erros))
