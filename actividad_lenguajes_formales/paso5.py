texto = "a1b22c"

tokens = []

# for evita el índice y conserva el orden de los dígitos.
for c in texto:
    if c.isdigit():
        tokens.append(("DIGITO", c))

print(tokens)