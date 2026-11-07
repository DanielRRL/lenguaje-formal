texto = "a1b22c"

#i = 0

#while i < len(texto):
#   print(i, texto[i])
#  i += 1
    
#texto = "a1b22c"

i = 0

while i < len(texto):
    if texto[i].isdigit():
        print(texto[i])

    i += 1