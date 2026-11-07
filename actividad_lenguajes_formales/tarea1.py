def tokenizar(texto):
    tokens = []
    i = 0

    while i < len(texto):
        c = texto[i]

        if c.isdigit():
            inicio = i
            while i < len(texto) and texto[i].isdigit():
                i += 1
            tokens.append(("NUMERO", texto[inicio:i], inicio + 1))
        else:
            tokens.append(("SIMBOLO", c, i + 1))
            i += 1

    return tokens


print(tokenizar("20;"))
