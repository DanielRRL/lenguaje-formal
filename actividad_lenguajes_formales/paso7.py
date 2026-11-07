def digitos(texto):
    tokens = []

    # Se recorre una sola vez: dígitos se guardan, letras se ignoran.
    for c in texto:
        if c.isdigit():
            tokens.append(("DIGITO", c))
        elif not c.isalpha():
            raise SyntaxError(f"Carácter inesperado '{c}'")

    return tokens


# Un solo bucle evita repetir el try/except para cada entrada.
for entrada in ("a1b", "a1@"):
    try:
        print(digitos(entrada))
    except SyntaxError as e:
        print(e)