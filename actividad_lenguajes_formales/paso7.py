def digitos(texto):
    tokens = []

    i = 0

    while i < len(texto):
        c = texto[i]

        if c.isdigit():
            tokens.append(("DIGITO", c))

        elif c.isalpha():
            pass

        else:
            raise SyntaxError(f"Carácter inesperado '{c}'")

        i += 1

    return tokens


try:
    print(digitos("a1b"))
except SyntaxError as e:
    print(e)

try:
    print(digitos("a1@"))
except SyntaxError as e:
    print(e)