TIPOS = {"umbral"}


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

        elif c.isdigit():
            inicio = i
            while i < len(texto) and texto[i].isdigit():
                i += 1
            tokens.append(("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c.isalpha():
            inicio = i
            while i < len(texto) and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]

            if palabra in TIPOS:
                tipo = "TIPO"
            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            tokens.append(("SIMBOLO", c, linea, i - inicio_linea + 1))
            i += 1

    return tokens


print(tokenizar("umbral edad"))
print(tokenizar("umbrales"))
