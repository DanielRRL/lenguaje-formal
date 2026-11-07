from tokens import Token


class Parser:
    def __init__(self, tokens: list[Token]):
        # Cada Parser guarda su propia lista y su propia posición.
        self.tokens = tokens
        self.pos = 0

    def actual(self) -> Token:
        # Devuelve el token actual sin mover la posición.
        return self.tokens[self.pos]

    def avanzar(self) -> None:
        # Se detiene en el último token (EOF) para no salir de la lista.
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
