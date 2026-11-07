TIPOS = {"umbral"}
SIMBOLOS = [":=", ";"]
COMENTARIO = "#"


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
                raise ValueError(f"Carácter inesperado {c!r}")

    return tokens


print(tokenizar("umbral x := 5; # esto se ignora\numbral y := 6;"))
