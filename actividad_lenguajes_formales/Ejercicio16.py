# Tarea 16: Programa de ejemplo (ejemplo.txt)
# Ejecutar: python tarea16.py   (lee ejemplo.txt)

from dataclasses import dataclass
import sys

TIPOS = {"umbral"}
RESERVADAS = {"IF", "THEN", "ELSE", "END", "AND", "OR"}
BOOLEANOS = {"true", "false"}
SIMBOLOS = [":=", ";", "(", ")", "{", "}", ",", "."]
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


def mostrar_tabla(tokens):
    print(f"{'LINEA':<7}{'COL':<6}{'TIPO':<15}TEXTO")
    for t in tokens:
        print(f"{t.linea:<7}{t.columna:<6}{t.tipo:<15}{t.texto}")


# Tokens de las 3 primeras líneas de ejemplo.txt, calculados a mano
# (la línea 1 es un comentario y no genera tokens)
ESPERADO_3_LINEAS = [
    ("TIPO", "umbral", 2, 1),
    ("IDENTIFICADOR", "limite_brillo", 2, 8),
    ("SIMBOLO", ":=", 2, 22),
    ("NUMERO", "80", 2, 25),
    ("SIMBOLO", ";", 2, 27),
    ("TIPO", "umbral", 3, 1),
    ("IDENTIFICADOR", "brillo_minimo", 3, 8),
    ("SIMBOLO", ":=", 3, 22),
    ("NUMERO", "15.5", 3, 25),
    ("SIMBOLO", ";", 3, 29),
]


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "ejemplo.txt"

    try:
        texto = open(ruta, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta}")
        sys.exit(1)

    try:
        tokens = tokenizar(texto)
    except ErrorLexico as e:
        print(e)
        sys.exit(1)

    mostrar_tabla(tokens)

    # comparación con lo calculado a mano
    real = [(t.tipo, t.texto, t.linea, t.columna) for t in tokens if t.linea <= 3]
    print()
    print("Primeras 3 líneas contra lo calculado a mano:", "SI" if real == ESPERADO_3_LINEAS else "NO")