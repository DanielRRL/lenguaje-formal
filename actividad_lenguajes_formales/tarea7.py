from tarea6_3 import ErrorLexico, tokenizar


casos = [
    (
        "Válido 1: declaración simple con espacios",
        "umbral umbrales := 20;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "umbrales", 1, 8),
            ("SIMBOLO", ":=", 1, 17),
            ("NUMERO", "20", 1, 20),
            ("SIMBOLO", ";", 1, 22),
        ],
    ),
    (
        "Válido 2: sin espacios y con operadores",
        "umbral total:=a+5*2;",
        [
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
    ),
    (
        "Válido 3: dos líneas, comentario, decimal y cadena",
        'umbral precio := 3.14; # comentario\numbral nombre := "hola";',
        [
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
    ),
    (
        "Inválido 1: carácter inexistente",
        "umbral x := 5 @;",
        "ERROR: Carácter inesperado '@' en línea 1, columna 15",
    ),
    (
        "Inválido 2: declaración al estilo Java",
        "umbral x = 5;",
        "ERROR: Carácter inesperado '=' en línea 1, columna 10",
    ),
    (
        "Inválido 3: cadena sin cerrar en la segunda línea",
        'umbral a := 1;\numbral b := "hola;',
        "ERROR: Cadena sin cerrar que empieza en línea 2, columna 13",
    ),
]


coinciden = 0

# Tuplas + desempaquetado: menos claves repetidas y bucle directo.
for nombre, entrada, esperado in casos:
    print("=" * 60)
    print(nombre)
    print("Entrada:", repr(entrada))

    try:
        real = tokenizar(entrada)
    except ErrorLexico as e:
        real = f"ERROR: {e}"

    print("Esperado:", esperado)
    print("Real:    ", real)

    if real == esperado:
        print("¿Coincide?: SÍ")
        coinciden += 1
    else:
        print("¿Coincide?: NO")

print("=" * 60)
print(f"{coinciden}/{len(casos)} casos coinciden")
