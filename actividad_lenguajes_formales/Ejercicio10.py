# Tarea 10: Palabras reservadas de control y booleanos
# Ejecutar: python Ejercicio10.py

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

        elif c.isdigit():
            inicio = i
            while i < n and texto[i].isdigit():
                i += 1
            if i + 1 < n and texto[i] == "." and texto[i + 1].isdigit():
                i += 1
                while i < n and texto[i].isdigit():
                    i += 1
            tokens.append(("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c == '"':
            inicio = i
            columna_inicio = i - inicio_linea + 1
            i += 1
            while i < n and texto[i] != '"' and texto[i] != "\n":
                i += 1
            if i >= n or texto[i] == "\n":
                raise error("cadena sin cerrar", linea, columna_inicio)
            i += 1
            tokens.append(("CADENA", texto[inicio:i], linea, columna_inicio))

        elif c.isalpha():
            inicio = i
            while i < n and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            tipo = PALABRAS.get(palabra, "IDENTIFICADOR")
            tokens.append((tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            reconocido = False

            # Una sola tabla evita comprobar símbolos y operadores por separado.
            for fijo, tipo in FIJOS:
                if texto.startswith(fijo, i):
                    tokens.append((tipo, fijo, linea, i - inicio_linea + 1))
                    i += len(fijo)
                    reconocido = True
                    break

            if not reconocido:
                raise error(f"carácter {c!r} no reconocido", linea, i - inicio_linea + 1)

    return tokens


def probar(nombre, entrada, esperada):
    try:
        real = tokenizar(entrada)
    except ErrorLexico as e:
        real = str(e)
    print("=" * 60)
    print(nombre)
    print("Entrada :", repr(entrada))
    print("Esperada:", esperada)
    print("Real    :", real)
    print("Coincide:", "SI" if real == esperada else "NO")


# Los casos se agrupan y se recorren; evita repetir llamadas.
CASOS = [
    (
        "T10 - IF reservada, IFFY y END_X identificadores",
        "IF IFFY END_X",
        [
            ("RESERVADA", "IF", 1, 1),
            ("IDENTIFICADOR", "IFFY", 1, 4),
            ("IDENTIFICADOR", "END_X", 1, 9),
        ],
    ),
    (
        "T10 - booleanos",
        "true false",
        [
            ("BOOLEANO", "true", 1, 1),
            ("BOOLEANO", "false", 1, 6),
        ],
    ),
    (
        "T10 - condicion de su lenguaje",
        "IF brillo > 80 THEN",
        [
            ("RESERVADA", "IF", 1, 1),
            ("IDENTIFICADOR", "brillo", 1, 4),
            ("OPERADOR", ">", 1, 11),
            ("NUMERO", "80", 1, 13),
            ("RESERVADA", "THEN", 1, 16),
        ],
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
        ],
    ),
]


if __name__ == "__main__":
    for nombre, entrada, esperada in CASOS:
        probar(nombre, entrada, esperada)
