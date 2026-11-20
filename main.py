import sys

from interprete import Interprete
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje


def mostrar_error(error, lineas):
    print(error)
    if 1 <= error.linea <= len(lineas):
        print(lineas[error.linea - 1])
        print(" " * (error.columna - 1) + "^")
    print(f"linea = {error.linea}, columna = {error.columna}")


def ejecutar_texto(texto, interprete):
    programa = Parser(tokenizar(texto)).programa()
    interprete.ejecutar_programa(programa)


def modo_archivo(ruta):
    try:
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta}")
        return 1

    try:
        ejecutar_texto(texto, Interprete())
    except ErrorDeLenguaje as error:
        mostrar_error(error, texto.splitlines())
        return 1

    return 0


def modo_interactivo():
    interprete = Interprete()
    print("Umbral interactivo. Escribe 'salir' para terminar.")

    while True:
        try:
            linea = input("> ")
        except EOFError:
            print()
            break

        if linea.strip() == "salir":
            break
        if not linea.strip():
            continue

        try:
            ejecutar_texto(linea, interprete)
        except ErrorDeLenguaje as error:
            mostrar_error(error, linea.splitlines())


def main():
    if len(sys.argv) > 1:
        sys.exit(modo_archivo(sys.argv[1]))
    modo_interactivo()


if __name__ == "__main__":
    main()
