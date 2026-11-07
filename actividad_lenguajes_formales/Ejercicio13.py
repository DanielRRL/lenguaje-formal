# Tarea 13: Clase Token
# Ejecutar: python Ejercicio13.py

from dataclasses import dataclass

# Un solo diccionario clasifica la palabra en O(1).
# NOT se incluye porque aparece en BNF.txt.
PALABRAS = {
    "umbral": "TIPO",
    "IF": "RESERVADA", "THEN": "RESERVADA", "ELSE": "RESERVADA",
    "END": "RESERVADA", "AND": "RESERVADA", "OR": "RESERVADA",
    "NOT": "RESERVADA",
    "true": "BOOLEANO", "false": "BOOLEANO",
}
# Tabla única (texto, tipo) con los más largos primero.
FIJOS = (
    (":=", "SIMBOLO"),
    ("==", "OPERADOR"), ("!=", "OPERADOR"), ("<=", "OPERADOR"), (">=", "OPERADOR"),
    (";", "SIMBOLO"), ("(", "SIMBOLO"), (")", "SIMBOLO"),
    ("{", "SIMBOLO"), ("}", "SIMBOLO"), (",", "SIMBOLO"), (".", "SIMBOLO"),
    ("<", "OPERADOR"), (">", "OPERADOR"), ("=", "OPERADOR"),
    ("+", "OPERADOR"), ("-", "OPERADOR"), ("*", "OPERADOR"), ("/", "OPERADOR"),
)
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
    pass


def error(mensaje, linea, columna):
    return ErrorLexico(f"Error léxico en línea {linea}, columna {columna}: {mensaje}")


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    inicio_linea = 0
    n = len(texto)  # Se calcula una vez; el texto no cambia.

    while i < n:
        c = texto[i]

        if c == "\n":
            linea += 1
            i += 1
            inicio_linea = i

        elif c.isspace():
            i += 1

        # COMENTARIO es de un carácter; comparar c evita startswith.
        elif c == COMENTARIO:
            while i < n and texto[i] != "\n":
                i += 1

        elif texto.startswith(BLOQUE_INICIO, i):
            linea_inicio = linea
            columna_inicio = i - inicio_linea + 1
            i += len(BLOQUE_INICIO)
            cerrado = False
            while i < n:
                if texto.startswith(BLOQUE_FIN, i):
                    i += len(BLOQUE_FIN)
                    cerrado = True
                    break
                if texto[i] == "\n":
                    linea += 1
                    inicio_linea = i + 1
                i += 1
            if not cerrado:
                raise error("comentario sin cerrar", linea_inicio, columna_inicio)

        elif c.isdigit():
            inicio = i
            while i < n and texto[i].isdigit():
                i += 1
            if i + 1 < n and texto[i] == "." and texto[i + 1].isdigit():
                i += 1
                while i < n and texto[i].isdigit():
                    i += 1
            tokens.append(Token("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c == '"':
            inicio = i
            columna_inicio = i - inicio_linea + 1
            i += 1
            while i < n and texto[i] != '"' and texto[i] != "\n":
                i += 1
            if i >= n or texto[i] == "\n":
                raise error("cadena sin cerrar", linea, columna_inicio)
            i += 1
            tokens.append(Token("CADENA", texto[inicio:i], linea, columna_inicio))

        elif c.isalpha():
            inicio = i
            while i < n and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            tipo = PALABRAS.get(palabra, "IDENTIFICADOR")
            tokens.append(Token(tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            reconocido = False

            # Una sola tabla evita comprobar símbolos y operadores por separado.
            for fijo, tipo in FIJOS:
                if texto.startswith(fijo, i):
                    tokens.append(Token(tipo, fijo, linea, i - inicio_linea + 1))
                    i += len(fijo)
                    reconocido = True
                    break

            if not reconocido:
                raise error(f"carácter {c!r} no reconocido", linea, i - inicio_linea + 1)

    tokens.append(Token("EOF", "", linea, i - inicio_linea + 1))
    return tokens


def a_texto(tokens):
    return [str(t) for t in tokens]


def a_tupla(tokens):
    return [(t.tipo, t.texto, t.linea, t.columna) for t in tokens]


def probar(nombre, entrada, esperada, convertir):
    real = convertir(tokenizar(entrada))
    print("=" * 60)
    print(nombre)
    print("Entrada :", repr(entrada))
    print("Esperada:", esperada)
    print("Real    :", real)
    print("Coincide:", "SI" if real == esperada else "NO")


# Los casos se agrupan y se recorren; evita repetir llamadas.
CASOS = [
    (
        "T13 - __str__ legible",
        "x := 5;",
        [
            "IDENTIFICADOR('x') en 1:1",
            "SIMBOLO(':=') en 1:3",
            "NUMERO('5') en 1:6",
            "SIMBOLO(';') en 1:7",
            "EOF('') en 1:8",
        ],
        a_texto,
    ),
    (
        "V2 - sin espacios y con operadores",
        "umbral total:=a+5*2;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "total", 1, 8),
            ("SIMBOLO", ":=", 1, 13),
            ("IDENTIFICADOR", "a", 1, 15),
            ("OPERADOR", "+", 1, 16),
            ("NUMERO", "5", 1, 17),
            ("OPERADOR", "*", 1, 18),
            ("NUMERO", "2", 1, 19),
            ("SIMBOLO", ";", 1, 20),
            ("EOF", "", 1, 21),
        ],
        a_tupla,
    ),
]


if __name__ == "__main__":
    # un token por línea, como pide la tarea
    for t in tokenizar("x := 5;"):
        print(t)

    for nombre, entrada, esperada, convertir in CASOS:
        probar(nombre, entrada, esperada, convertir)
