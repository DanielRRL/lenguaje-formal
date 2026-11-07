texto = "a1b22c"

tokens = []

i = 0

while i < len(texto):
    if texto[i].isdigit():
        tokens.append(("DIGITO", texto[i]))

    i += 1

print(tokens)