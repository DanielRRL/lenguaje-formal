# Tarea 9: Operadores de dos caracteres: == != <= >= < >
# Ejecutar: python tarea9.py

TIPOS = {"umbral"}
SIMBOLOS = [":=", ";", "(", ")", "{", "}", ",", "."]
# los mas largos primero: asi == se reconoce antes que =
OPERADORES = ["==", "!=", "<=", ">=", "<", ">", "=", "+", "-", "*", "/"]
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

        elif c.isdigit():
            inicio = i
            while i < len(texto) and texto[i].isdigit():
                i += 1
            if i + 1 < len(texto) and texto[i] == "." and texto[i + 1].isdigit():
                i += 1
                while i < len(texto) and texto[i].isdigit():
                    i += 1
            tokens.append(("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c == '"':
            inicio = i
            columna_inicio = i - inicio_linea + 1
            i += 1
            while i < len(texto) and texto[i] != '"' and texto[i] != "\n":
                i += 1
            if i >= len(texto) or texto[i] == "\n":
                raise error("cadena sin cerrar", linea, columna_inicio)
            i += 1
            tokens.append(("CADENA", texto[inicio:i], linea, columna_inicio))

        elif c.isalpha():
            inicio = i
            while i < len(texto) and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            tipo = "TIPO" if palabra in TIPOS else "IDENTIFICADOR"
            tokens.append((tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            reconocido = False

            for simbolo in SIMBOLOS:
                if texto.startswith(simbolo, i):
                    tokens.append(("SIMBOLO", simbolo, linea, i - inicio_linea + 1))
                    i += len(simbolo)
                    reconocido = True
                    break

            if not reconocido:
                for op in OPERADORES:
                    if texto.startswith(op, i):
                        tokens.append(("OPERADOR", op, linea, i - inicio_linea + 1))
                        i += len(op)
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


if __name__ == "__main__":
    probar(
        "T9 - x == 5 (3 tokens)",
        "x == 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "==", 1, 3),
            ("NUMERO", "5", 1, 6),
        ],
    )
    probar(
        "T9 - x = = 5 (4 tokens)",
        "x = = 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "=", 1, 3),
            ("OPERADOR", "=", 1, 5),
            ("NUMERO", "5", 1, 7),
        ],
    )
    probar(
        "T9 - >=",
        "a >= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", ">=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    )
    probar(
        "T9 - <=",
        "a <= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    )
    probar(
        "T9 - !=",
        "a != 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "!=", 1, 3),
            ("NUMERO", "1", 1, 6),
        ],
    )
    probar(
        "T9 - < y > de un caracter",
        "a < 1 > b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<", 1, 3),
            ("NUMERO", "1", 1, 5),
            ("OPERADOR", ">", 1, 7),
            ("IDENTIFICADOR", "b", 1, 9),
        ],
    )
    probar(
        "T9 - ! solo es error",
        "x ! 5",
        "Error léxico en línea 1, columna 3: carácter '!' no reconocido",
    )
    probar(
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
    )