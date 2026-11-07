# Tarea 9: Operadores de dos caracteres: == != <= >= < >
# Ejecutar: python Ejercicio9.py

TIPOS = {"umbral"}
# Tabla única (texto, tipo) con los más largos primero:
# así == se reconoce antes que = y no se necesitan dos bucles.
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
            tipo = "TIPO" if palabra in TIPOS else "IDENTIFICADOR"
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


# Los casos se agrupan y se recorren; evita repetir ocho llamadas.
CASOS = [
    (
        "T9 - x == 5 (3 tokens)",
        "x == 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "==", 1, 3),
            ("NUMERO", "5", 1, 6),
        ],
    ),
    (
        "T9 - x = = 5 (4 tokens)",
        "x = = 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "=", 1, 3),
            ("OPERADOR", "=", 1, 5),
            ("NUMERO", "5", 1, 7),
        ],
    ),
    (
        "T9 - >=",
        "a >= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", ">=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    ),
    (
        "T9 - <=",
        "a <= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    ),
    (
        "T9 - !=",
        "a != 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "!=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    ),
    (
        "T9 - < y > de un caracter",
        "a < 1 > b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<", 1, 3),
            ("NUMERO", "1", 1, 5),
            ("OPERADOR", ">", 1, 7),
            ("IDENTIFICADOR", "b", 1, 9),
        ],
    ),
    (
        "T9 - ! solo es error",
        "x ! 5",
        "Error léxico en línea 1, columna 3: carácter '!' no reconocido",
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
