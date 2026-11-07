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
