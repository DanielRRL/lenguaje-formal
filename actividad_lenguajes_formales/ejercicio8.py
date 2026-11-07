# Tarea 8: Delimitadores: ( ) { } , .
# Ejecutar: python tarea8.py
 
TIPOS = {"umbral"}
SIMBOLOS = [":=", ";", "(", ")", "{", "}", ",", "."]
OPERADORES = {"+", "-", "*"}
COMENTARIO = "#"
 
 
class ErrorLexico(Exception):
    pass
 
 
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
                raise ErrorLexico(
                    f"Cadena sin cerrar que empieza en línea {linea}, columna {columna_inicio}"
                )
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
 
            if not reconocido and c in OPERADORES:
                tokens.append(("OPERADOR", c, linea, i - inicio_linea + 1))
                i += 1
                reconocido = True
            if not reconocido:
                raise ErrorLexico(
                    f"Carácter inesperado {c!r} en línea {linea}, columna {i - inicio_linea + 1}"
                )
 
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
        "T8 - (a+b)*2;",
        "(a+b)*2;",
        [
            ("SIMBOLO", "(", 1, 1),
            ("IDENTIFICADOR", "a", 1, 2),
            ("OPERADOR", "+", 1, 3),
            ("IDENTIFICADOR", "b", 1, 4),
            ("SIMBOLO", ")", 1, 5),
            ("OPERADOR", "*", 1, 6),
            ("NUMERO", "2", 1, 7),
            ("SIMBOLO", ";", 1, 8),
        ],
    )
    probar(
        "T8 - punto entre nombres es SIMBOLO",
        "System.out",
        [
            ("IDENTIFICADOR", "System", 1, 1),
            ("SIMBOLO", ".", 1, 7),
            ("IDENTIFICADOR", "out", 1, 8),
        ],
    )
    probar(
        "T8 - punto dentro de un numero sigue siendo del numero",
        "x := 3.14;",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("SIMBOLO", ":=", 1, 3),
            ("NUMERO", "3.14", 1, 6),
            ("SIMBOLO", ";", 1, 10),
        ],
    )
    probar(
        "T8 - notificar con parentesis y coma",
        "notificar(\"hola\", 5);",
        [
            ("IDENTIFICADOR", "notificar", 1, 1),
            ("SIMBOLO", "(", 1, 10),
            ("CADENA", "\"hola\"", 1, 11),
            ("SIMBOLO", ",", 1, 17),
            ("NUMERO", "5", 1, 19),
            ("SIMBOLO", ")", 1, 20),
            ("SIMBOLO", ";", 1, 21),
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
 