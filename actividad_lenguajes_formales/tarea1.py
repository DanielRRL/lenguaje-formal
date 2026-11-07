def tokenizar(texto):
    tokens = []
    i = 0
    n = len(texto)  # Se calcula una vez; el texto no cambia.

    while i < n:
        c = texto[i]

        if c.isdigit():
            inicio = i
            while i < n and texto[i].isdigit():
                i += 1
            tokens.append(("NUMERO", texto[inicio:i], inicio + 1))
        else:
            tokens.append(("SIMBOLO", c, i + 1))
            i += 1

    return tokens


print(tokenizar("20;"))
