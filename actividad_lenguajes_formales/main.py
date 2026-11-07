import sys

from lexer import tokenizar
from parser import Parser
from tokens import ErrorLexico


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py programa.txt")
        sys.exit(1)

    ruta = sys.argv[1]

    try:
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta}")
        sys.exit(1)

    try:
        tokens = tokenizar(texto)
    except ErrorLexico as e:
        # ErrorLexico trae el mensaje y la posición por separado.
        print(e)
        print(f"linea = {e.linea}, columna = {e.columna}")
        sys.exit(1)

    parser = Parser(tokens)
    while True:
        token = parser.actual()
        print(token)
        if token.tipo == "EOF":
            break
        parser.avanzar()


if __name__ == "__main__":
    main()
