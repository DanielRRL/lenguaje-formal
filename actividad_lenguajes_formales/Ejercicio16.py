# Tarea 16: Programa de ejemplo (Ejemplo.txt)
# Ejecutar: python Ejercicio16.py [archivo]   (por defecto lee Ejemplo.txt)

from dataclasses import dataclass
import sys

# Un solo diccionario clasifica la palabra en O(1).
# NOT se incluye porque aparece en BNF.txt.
PALABRAS = {
    "umbral": "TIPO",
    "IF": "RESERVADA", "THEN": "RESERVADA", "ELSE": "RESERVADA",
    "END": "RESERVADA", "AND": "RESERVADA", "OR": "RESERVADA",
    "NOT": "RESERVADA",
    "true": "BOOLEANO", "false": "BOOLEANO",
}
# Tabla única (texto, tipo) con los más largos primero.
FIJOS = (
    (":=", "SIMBOLO"),
    ("==", "OPERADOR"), ("!=", "OPERADOR"), ("<=", "OPERADOR"), (">=", "OPERADOR"),
    (";", "SIMBOLO"), ("(", "SIMBOLO"), (")", "SIMBOLO"),
    ("{", "SIMBOLO"), ("}", "SIMBOLO"), (",", "SIMBOLO"), (".", "SIMBOLO"),
    ("<", "OPERADOR"), (">", "OPERADOR"), ("=", "OPERADOR"),
    ("+", "OPERADOR"), ("-", "OPERADOR"), ("*", "OPERADOR"), ("/", "OPERADOR"),
)
COMENTARIO = "#"
BLOQUE_INICIO = "/*"
BLOQUE_FIN = "*/"


@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):
        return f"{self.tipo}({self.texto!r}) en {self.linea}:{self.columna}"


class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        super().__init__(
            f"Error léxico en línea {linea}, columna {columna}: {mensaje}"
        )
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    inicio_linea = 0
    n = len(texto)  # Se calcula una vez; el texto no cambia.

    while i < n:
        c = texto[i]

        if c == "\n":
            linea += 1
            i += 1
            inicio_linea = i

        elif c.isspace():
            i += 1

        # COMENTARIO es de un carácter; comparar c evita startswith.
        elif c == COMENTARIO:
            while i < n and texto[i] != "\n":
                i += 1

        elif texto.startswith(BLOQUE_INICIO, i):
            linea_inicio = linea
            columna_inicio = i - inicio_linea + 1
            i += len(BLOQUE_INICIO)
            cerrado = False
            while i < n:
                if texto.startswith(BLOQUE_FIN, i):
                    i += len(BLOQUE_FIN)
                    cerrado = True
                    break
                if texto[i] == "\n":
                    linea += 1
                    inicio_linea = i + 1
                i += 1
            if not cerrado:
                raise ErrorLexico("comentario sin cerrar", linea_inicio, columna_inicio)

        elif c.isdigit():
            inicio = i
            while i < n and texto[i].isdigit():
                i += 1
            if i + 1 < n and texto[i] == "." and texto[i + 1].isdigit():
                i += 1
                while i < n and texto[i].isdigit():
                    i += 1
            tokens.append(Token("NUMERO", texto[inicio:i], linea, inicio - inicio_linea + 1))

        elif c == '"':
            inicio = i
            columna_inicio = i - inicio_linea + 1
            i += 1
            while i < n and texto[i] != '"' and texto[i] != "\n":
                i += 1
            if i >= n or texto[i] == "\n":
                raise ErrorLexico("cadena sin cerrar", linea, columna_inicio)
            i += 1
            tokens.append(Token("CADENA", texto[inicio:i], linea, columna_inicio))

        elif c.isalpha():
            inicio = i
            while i < n and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            tipo = PALABRAS.get(palabra, "IDENTIFICADOR")
            tokens.append(Token(tipo, palabra, linea, inicio - inicio_linea + 1))

        else:
            reconocido = False

            # Una sola tabla evita comprobar símbolos y operadores por separado.
            for fijo, tipo in FIJOS:
                if texto.startswith(fijo, i):
                    tokens.append(Token(tipo, fijo, linea, i - inicio_linea + 1))
                    i += len(fijo)
                    reconocido = True
                    break

            if not reconocido:
                raise ErrorLexico(f"carácter {c!r} no reconocido", linea, i - inicio_linea + 1)

    tokens.append(Token("EOF", "", linea, i - inicio_linea + 1))
    return tokens


def mostrar_tabla(tokens):
    print(f"{'LINEA':<7}{'COL':<6}{'TIPO':<15}TEXTO")
    for t in tokens:
        print(f"{t.linea:<7}{t.columna:<6}{t.tipo:<15}{t.texto}")


# Tokens de las 3 primeras líneas de Ejemplo.txt, calculados a mano
# (la línea 1 es un comentario y no genera tokens)
ESPERADO_3_LINEAS = [
    ("TIPO", "umbral", 2, 1),
    ("IDENTIFICADOR", "limite_brillo", 2, 8),
    ("SIMBOLO", ":=", 2, 22),
    ("NUMERO", "80", 2, 25),
    ("SIMBOLO", ";", 2, 27),
    ("TIPO", "umbral", 3, 1),
    ("IDENTIFICADOR", "brillo_minimo", 3, 8),
    ("SIMBOLO", ":=", 3, 22),
    ("NUMERO", "15.5", 3, 25),
    ("SIMBOLO", ";", 3, 29),
]


if __name__ == "__main__":
    # El nombre real del archivo es Ejemplo.txt (Linux distingue mayúsculas).
    ruta = sys.argv[1] if len(sys.argv) > 1 else "Ejemplo.txt"

    try:
        # with cierra el archivo aunque falle la lectura.
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta}")
        sys.exit(1)

    try:
        tokens = tokenizar(texto)
    except ErrorLexico as e:
        print(e)
        sys.exit(1)

    mostrar_tabla(tokens)

    # comparación con lo calculado a mano
    real = [(t.tipo, t.texto, t.linea, t.columna) for t in tokens if t.linea <= 3]
    print()
    print("Primeras 3 líneas contra lo calculado a mano:", "SI" if real == ESPERADO_3_LINEAS else "NO")
