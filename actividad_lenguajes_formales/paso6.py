def digitos(texto):
    # La comprensión filtra y construye la lista en una sola pasada.
    return [("DIGITO", c) for c in texto if c.isdigit()]


print(digitos("a1b22c"))
print(digitos("abc123"))
print(digitos("abcdef"))