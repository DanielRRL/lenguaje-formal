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


class ErrorDeLenguaje(Exception):
    fase = "Error"

    def __init__(self, mensaje: str, linea: int, columna: int):
        # La clase base guarda el mensaje completo y la posición.
        super().__init__(f"{self.fase} en línea {linea}, columna {columna}: {mensaje}")
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna


class ErrorLexico(ErrorDeLenguaje):
    fase = "Error léxico"


class ErrorSintactico(ErrorDeLenguaje):
    fase = "Error sintáctico"
