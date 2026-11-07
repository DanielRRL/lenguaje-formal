# Cada caso: (nombre, entrada, salida esperada calculada a mano).
# La salida esperada es una lista de (tipo, texto, línea, columna)
# o, si el caso es un error, el mensaje completo.
# Todas las listas de tokens terminan con el token EOF.

CASOS = [
    # ---------------- Tarea 8: delimitadores ----------------
    (
        "T8 - (a+b)*2;",
        "(a+b)*2;",
        [
            ("SIMBOLO", "(", 1, 1),
            ("IDENTIFICADOR", "a", 1, 2),
            ("OPERADOR", "+", 1, 3),
            ("IDENTIFICADOR", "b", 1, 4),
            ("SIMBOLO", ")", 1, 5),
            ("OPERADOR", "*", 1, 6),
            ("NUMERO", "2", 1, 7),
            ("SIMBOLO", ";", 1, 8),
            ("EOF", "", 1, 9),
        ],
    ),
    (
        "T8 - punto entre nombres es SIMBOLO",
        "System.out",
        [
            ("IDENTIFICADOR", "System", 1, 1),
            ("SIMBOLO", ".", 1, 7),
            ("IDENTIFICADOR", "out", 1, 8),
            ("EOF", "", 1, 11),
        ],
    ),
    (
        "T8 - punto dentro de un numero sigue siendo del numero",
        "x := 3.14;",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("SIMBOLO", ":=", 1, 3),
            ("NUMERO", "3.14", 1, 6),
            ("SIMBOLO", ";", 1, 10),
            ("EOF", "", 1, 11),
        ],
    ),
    (
        "T8 - notificar con parentesis y coma",
        'notificar("hola", 5);',
        [
            ("IDENTIFICADOR", "notificar", 1, 1),
            ("SIMBOLO", "(", 1, 10),
            ("CADENA", '"hola"', 1, 11),
            ("SIMBOLO", ",", 1, 17),
            ("NUMERO", "5", 1, 19),
            ("SIMBOLO", ")", 1, 20),
            ("SIMBOLO", ";", 1, 21),
            ("EOF", "", 1, 22),
        ],
    ),
    # ---------------- Tarea 9: operadores de dos caracteres ----------------
    (
        "T9 - x == 5 (3 tokens)",
        "x == 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "==", 1, 3),
            ("NUMERO", "5", 1, 6),
            ("EOF", "", 1, 7),
        ],
    ),
    (
        "T9 - x = = 5 (4 tokens)",
        "x = = 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "=", 1, 3),
            ("OPERADOR", "=", 1, 5),
            ("NUMERO", "5", 1, 7),
            ("EOF", "", 1, 8),
        ],
    ),
    (
        "T9 - >=",
        "a >= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", ">=", 1, 3),
            ("NUMERO", "1", 1, 6),
            ("EOF", "", 1, 7),
        ],
    ),
    (
        "T9 - <=",
        "a <= 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<=", 1, 3),
            ("NUMERO", "1", 1, 6),
            ("EOF", "", 1, 7),
        ],
    ),
    (
        "T9 - !=",
        "a != 1",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "!=", 1, 3),
            ("NUMERO", "1", 1, 6),
            ("EOF", "", 1, 7),
        ],
    ),
    (
        "T9 - < y > de un caracter",
        "a < 1 > b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<", 1, 3),
            ("NUMERO", "1", 1, 5),
            ("OPERADOR", ">", 1, 7),
            ("IDENTIFICADOR", "b", 1, 9),
            ("EOF", "", 1, 10),
        ],
    ),
    (
        "T9 - ! solo es error",
        "x ! 5",
        "Error léxico en línea 1, columna 3: carácter '!' no reconocido",
    ),
    # ---------------- Tarea 10: reservadas y booleanos ----------------
    (
        "T10 - IF reservada, IFFY y END_X identificadores",
        "IF IFFY END_X",
        [
            ("RESERVADA", "IF", 1, 1),
            ("IDENTIFICADOR", "IFFY", 1, 4),
            ("IDENTIFICADOR", "END_X", 1, 9),
            ("EOF", "", 1, 14),
        ],
    ),
    (
        "T10 - booleanos",
        "true false",
        [
            ("BOOLEANO", "true", 1, 1),
            ("BOOLEANO", "false", 1, 6),
            ("EOF", "", 1, 11),
        ],
    ),
    (
        "T10 - condicion de su lenguaje",
        "IF brillo > 80 THEN",
        [
            ("RESERVADA", "IF", 1, 1),
            ("IDENTIFICADOR", "brillo", 1, 4),
            ("OPERADOR", ">", 1, 11),
            ("NUMERO", "80", 1, 13),
            ("RESERVADA", "THEN", 1, 16),
            ("EOF", "", 1, 20),
        ],
    ),
    # ---------------- Tarea 11: comentarios de bloque ----------------
    (
        "T11 - comentario de 3 lineas entre dos declaraciones",
        "umbral a := 1; /* uno\ndos\ntres */\numbral b := 2;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "a", 1, 8),
            ("SIMBOLO", ":=", 1, 10),
            ("NUMERO", "1", 1, 13),
            ("SIMBOLO", ";", 1, 14),
            ("TIPO", "umbral", 4, 1),
            ("IDENTIFICADOR", "b", 4, 8),
            ("SIMBOLO", ":=", 4, 10),
            ("NUMERO", "2", 4, 13),
            ("SIMBOLO", ";", 4, 14),
            ("EOF", "", 4, 15),
        ],
    ),
    (
        "T11 - comentario sin cerrar",
        "umbral a := 1; /* sin cerrar",
        "Error léxico en línea 1, columna 16: comentario sin cerrar",
    ),
    (
        "T11 - comentario sin cerrar que empieza en la linea 2",
        "umbral a := 1;\n/* sin cerrar\nmas texto",
        "Error léxico en línea 2, columna 1: comentario sin cerrar",
    ),
    (
        "T11 - la division sigue siendo operador",
        "a / 2",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "/", 1, 3),
            ("NUMERO", "2", 1, 5),
            ("EOF", "", 1, 6),
        ],
    ),
    # ---------------- Tarea 12: EOF ----------------
    (
        "T12 - declaracion mas EOF",
        "umbral x := 5;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "x", 1, 8),
            ("SIMBOLO", ":=", 1, 10),
            ("NUMERO", "5", 1, 13),
            ("SIMBOLO", ";", 1, 14),
            ("EOF", "", 1, 15),
        ],
    ),
    ("T12 - texto vacio solo da EOF", "", [("EOF", "", 1, 1)]),
    (
        "T12 - texto que termina en salto de linea",
        "a\n",
        [("IDENTIFICADOR", "a", 1, 1), ("EOF", "", 2, 1)],
    ),
    # ---------------- Casos del parcial (siguen dando lo mismo) ----------------
    (
        "V1 - simple con espacios",
        "umbral umbrales := 20;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "umbrales", 1, 8),
            ("SIMBOLO", ":=", 1, 17),
            ("NUMERO", "20", 1, 20),
            ("SIMBOLO", ";", 1, 22),
            ("EOF", "", 1, 23),
        ],
    ),
    (
        "V2 - sin espacios y con operadores",
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
            ("EOF", "", 1, 21),
        ],
    ),
    (
        "V3 - dos lineas, comentario, decimal y cadena",
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
            ("EOF", "", 2, 25),
        ],
    ),
    (
        "I1 - caracter inexistente",
        "umbral x := 5 @;",
        "Error léxico en línea 1, columna 15: carácter '@' no reconocido",
    ),
    (
        "I2 - el = de Java ya es un OPERADOR valido (lo rechazara el parser)",
        "umbral x = 5;",
        [
            ("TIPO", "umbral", 1, 1),
            ("IDENTIFICADOR", "x", 1, 8),
            ("OPERADOR", "=", 1, 10),
            ("NUMERO", "5", 1, 12),
            ("SIMBOLO", ";", 1, 13),
            ("EOF", "", 1, 14),
        ],
    ),
    (
        "I3 - cadena sin cerrar en la segunda linea",
        'umbral a := 1;\numbral b := "hola;',
        "Error léxico en línea 2, columna 13: cadena sin cerrar",
    ),
    (
        "Decimal con dos puntos: 3.4 y luego . y 5",
        "3.4.5",
        [
            ("NUMERO", "3.4", 1, 1),
            ("SIMBOLO", ".", 1, 4),
            ("NUMERO", "5", 1, 5),
            ("EOF", "", 1, 6),
        ],
    ),
]
