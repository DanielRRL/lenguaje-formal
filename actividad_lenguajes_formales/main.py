import sys

from arbol import mostrar_arbol
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje


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
        programa = Parser(tokenizar(texto)).programa()
        mostrar_arbol(programa)
    except ErrorDeLenguaje as e:
        # La clase base atrapa errores léxicos y sintácticos.
        print(e)
        print(f"linea = {e.linea}, columna = {e.columna}")
        sys.exit(1)


if __name__ == "__main__":
    main()
