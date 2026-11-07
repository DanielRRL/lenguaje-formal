# @dataclass genera el constructor y la representación automáticamente.
from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):
        # Formato legible pedido: NUMERO('5') en 1:9
        return f"{self.tipo}({self.texto!r}) en {self.linea}:{self.columna}"


class ErrorLexico(Exception):
    def __init__(self, mensaje: str, linea: int, columna: int):
        # super().__init__ guarda el mensaje completo del error.
        super().__init__(f"Error léxico en línea {linea}, columna {columna}: {mensaje}")
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
