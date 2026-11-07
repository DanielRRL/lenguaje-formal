from tarea6_3 import ErrorLexico, tokenizar


casos = [
    {
        "nombre": "Válido 1: declaración simple con espacios",
        "entrada": "umbral umbrales := 20;",
        "esperado": [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "umbrales", 1, 8),
            ("SIMBOLO", ":=", 1, 17),
            ("NUMERO", "20", 1, 20),
            ("SIMBOLO", ";", 1, 22),
        ],
    },
    {
        "nombre": "Válido 2: sin espacios y con operadores",
        "entrada": "umbral total:=a+5*2;",
        "esperado": [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "total", 1, 8),
            ("SIMBOLO", ":=", 1, 13),
            ("IDENTIFICADOR", "a", 1, 15),
            ("OPERADOR", "+", 1, 16),
            ("NUMERO", "5", 1, 17),
            ("OPERADOR", "*", 1, 18),
            ("NUMERO", "2", 1, 19),
            ("SIMBOLO", ";", 1, 20),
        ],
    },
    {
        "nombre": "Válido 3: dos líneas, comentario, decimal y cadena",
        "entrada": 'umbral precio := 3.14; # comentario\numbral nombre := "hola";',
        "esperado": [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "precio", 1, 8),
            ("SIMBOLO", ":=", 1, 15),
            ("NUMERO", "3.14", 1, 18),
            ("SIMBOLO", ";", 1, 22),
            ("TIPO", "umbral", 2, 1),
            ("IDENTIFICADOR", "nombre", 2, 8),
            ("SIMBOLO", ":=", 2, 15),
            ("CADENA", '"hola"', 2, 18),
            ("SIMBOLO", ";", 2, 24),
        ],
    },
    {
        "nombre": "Inválido 1: carácter inexistente",
        "entrada": "umbral x := 5 @;",
        "esperado": "ERROR: Carácter inesperado '@' en línea 1, columna 15",
    },
    {
        "nombre": "Inválido 2: declaración al estilo Java",
        "entrada": "umbral x = 5;",
        "esperado": "ERROR: Carácter inesperado '=' en línea 1, columna 10",
    },
    {
        "nombre": "Inválido 3: cadena sin cerrar en la segunda línea",
        "entrada": 'umbral a := 1;\numbral b := "hola;',
        "esperado": "ERROR: Cadena sin cerrar que empieza en línea 2, columna 13",
    },
]


coinciden = 0

for caso in casos:
    print("=" * 60)
    print(caso["nombre"])
    print("Entrada:", repr(caso["entrada"]))

    try:
        real = tokenizar(caso["entrada"])
    except ErrorLexico as e:
        real = f"ERROR: {e}"

    print("Esperado:", caso["esperado"])
    print("Real:    ", real)

    if real == caso["esperado"]:
        print("¿Coincide?: SÍ")
        coinciden += 1
    else:
        print("¿Coincide?: NO")

print("=" * 60)
print(f"{coinciden}/{len(casos)} casos coinciden")
