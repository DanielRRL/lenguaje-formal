# Tarea 11: Comentarios de bloque /* ... */
# Ejecutar: python tarea11.py

TIPOS = {"umbral"}
RESERVADAS = {"IF", "THEN", "ELSE", "END", "AND", "OR"}
BOOLEANOS = {"true", "false"}
SIMBOLOS = [":=", ";", "(", ")", "{", "}", ",", "."]
OPERADORES = ["==", "!=", "<=", ">=", "<", ">", "=", "+", "-", "*", "/"]
COMENTARIO = "#"
BLOQUE_INICIO = "/*"
BLOQUE_FIN = "*/"


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
                raise error("comentario sin cerrar", linea_inicio, columna_inicio)
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
            if palabra in TIPOS:
                tipo = "TIPO"
            elif palabra in RESERVADAS:
                tipo = "RESERVADA"
            elif palabra in BOOLEANOS:
                tipo = "BOOLEANO"
            else:
                tipo = "IDENTIFICADOR"
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
        "T11 - comentario de 3 lineas entre dos declaraciones",
        "umbral a := 1; /* uno\ndos\ntres */\numbral b := 2;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "a", 1, 8),
            ("SIMBOLO", ":=", 1, 10),
            ("NUMERO", "1", 1, 13),
            ("SIMBOLO", ";", 1, 14),
            ("TIPO", "umbral", 4, 1),
            ("IDENTIFICADOR", "b", 4, 8),
            ("SIMBOLO", ":=", 4, 10),
            ("NUMERO", "2", 4, 13),
            ("SIMBOLO", ";", 4, 14),
        ],
    )
    probar(
        "T11 - comentario sin cerrar",
        "umbral a := 1; /* sin cerrar",
        "Error léxico en línea 1, columna 16: comentario sin cerrar",
    )
    probar(
        "T11 - comentario sin cerrar que empieza en la linea 2",
        "umbral a := 1;\n/* sin cerrar\nmas texto",
        "Error léxico en línea 2, columna 1: comentario sin cerrar",
    )
    probar(
        "T11 - la division sigue siendo operador",
        "a / 2",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "/", 1, 3),
            ("NUMERO", "2", 1, 5),
        ],
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