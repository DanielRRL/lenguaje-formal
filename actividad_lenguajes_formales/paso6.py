def digitos(texto):
    tokens = []

    i = 0

    while i < len(texto):
        if texto[i].isdigit():
            tokens.append(("DIGITO", texto[i]))

        i += 1

    return tokens


print(digitos("a1b22c"))
print(digitos("abc123"))
print(digitos("abcdef"))