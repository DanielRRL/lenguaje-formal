texto = "a1b22c"

# for recorre el texto sin manejar el índice a mano; mismo resultado.
for c in texto:
    if c.isdigit():
        print(c)