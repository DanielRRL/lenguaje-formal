# Tarea 14: Excepcion propia ErrorLexico
# Ejecutar: python tarea14.py

from dataclasses import dataclass

TIPOS = {"umbral"}
RESERVADAS = {"IF", "THEN", "ELSE", "END", "AND", "OR"}
BOOLEANOS = {"true", "false"}
SIMBOLOS = [":=", ";", "(", ")", "{", "}", ",", "."]
# los mas largos primero: asi == se reconoce antes que =
OPERADORES = ["==", "!=", "<=", ">=", "<", ">", "=", "+", "-", "*", "/"]
COMENTARIO = "#"
BLOQUE_INICIO = "/*"
BLOQUE_FIN = "*/"


@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):
        return f"{self.tipo}({self.texto!r}) en {self.linea}:{self.columna}"


class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        super().__init__(
            f"Error léxico en línea {linea}, columna {columna}: {mensaje}"
        )
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    inicio_linea = 0

    while i < len(texto):
        c = texto[i]

        if c == "\n":
            linea += 1
            i += 1
            inicio_linea = i

        elif c.isspace():
            i += 1

        elif texto.startswith(COMENTARIO, i):
            while i < len(texto) and texto[i] != "\n":
                i += 1

        elif texto.startswith(BLOQUE_INICIO, i):
            linea_inicio = linea
            columna_inicio = i - inicio_linea + 1
            i += len(BLOQUE_INICIO)
            cerrado = False
            while i < len(texto):
                if texto.startswith(BLOQUE_FIN, i):
                    i += len(BLOQUE_FIN)
                    cerrado = True
                    break
                if texto[i] == "\n":
                    linea += 1
                    inicio_linea = i + 1
                i += 1
            if not cerrado:
                raise ErrorLexico("comentario sin cerrar", linea_inicio, columna_inicio)
        elif c.isdigit():
            inicio = i
            while i < len(texto) and texto[i].isdigit():
                i += 1
            if i + 1 < len(texto) and texto[i] == "." and texto[i + 1].isdigit():
                i += 1
                while i < len(texto) and texto[i].isdigit():
                    i += 1
            tokens.append(Token("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c == '"':
            inicio = i
            columna_inicio = i - inicio_linea + 1
            i += 1
            while i < len(texto) and texto[i] != '"' and texto[i] != "\n":
                i += 1
            if i >= len(texto) or texto[i] == "\n":
                raise ErrorLexico("cadena sin cerrar", linea, columna_inicio)
            i += 1
            tokens.append(Token("CADENA", texto[inicio:i], linea, columna_inicio))

        elif c.isalpha():
            inicio = i
            while i < len(texto) and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            if palabra in TIPOS:
                tipo = "TIPO"
            elif palabra in RESERVADAS:
                tipo = "RESERVADA"
            elif palabra in BOOLEANOS:
                tipo = "BOOLEANO"
            else:
                tipo = "IDENTIFICADOR"
            tokens.append(Token(tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            reconocido = False

            for simbolo in SIMBOLOS:
                if texto.startswith(simbolo, i):
                    tokens.append(Token("SIMBOLO", simbolo, linea, i - inicio_linea + 1))
                    i += len(simbolo)
                    reconocido = True
                    break

            if not reconocido:
                for op in OPERADORES:
                    if texto.startswith(op, i):
                        tokens.append(Token("OPERADOR", op, linea, i - inicio_linea + 1))
                        i += len(op)
                        reconocido = True
                        break
            if not reconocido:
                raise ErrorLexico(f"carácter {c!r} no reconocido", linea, i - inicio_linea + 1)

    tokens.append(Token("EOF", "", linea, i - inicio_linea + 1))
    return tokens


if __name__ == "__main__":
    entrada = "umbral a := 1;\numbral b := 2 @"
    try:
        tokenizar(entrada)
    except ErrorLexico as e:
        print("e.linea   =", e.linea)
        print("e.columna =", e.columna)
        print("mensaje   =", e)
        esperado = (2, 15, "Error léxico en línea 2, columna 15: carácter '@' no reconocido")
        print("Coincide:", "SI" if (e.linea, e.columna, str(e)) == esperado else "NO")