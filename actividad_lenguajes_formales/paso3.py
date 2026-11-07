c = ";"

# Diccionario en vez de if/elif: una búsqueda y menos ramas.
mensajes = {" ": "espacio", ";": "punto y coma"}
print(mensajes.get(c, "otra cosa"))
