import io
from contextlib import redirect_stdout

from arbol import (
    Asignacion,
    Declaracion,
    Numero,
    OperacionBinaria,
    Programa,
    Variable,
    mostrar_arbol,
)
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje, ErrorSintactico


def parsear(texto):
    return Parser(tokenizar(texto)).programa()


def probar_arbol_resta():
    programa = parsear("umbral r := 10 - 3 - 2;")
    assert isinstance(programa, Programa)
    assert len(programa.instrucciones) == 1

    decl = programa.instrucciones[0]
    assert isinstance(decl, Declaracion)
    assert decl.tipo.texto == "umbral"
    assert decl.nombre.texto == "r"

    resta = decl.valor
    assert isinstance(resta, OperacionBinaria)
    assert resta.operador.texto == "-"
    assert isinstance(resta.izq, OperacionBinaria)
    assert resta.izq.operador.texto == "-"
    assert isinstance(resta.izq.izq, Numero)
    assert resta.izq.izq.token.texto == "10"
    assert isinstance(resta.izq.der, Numero)
    assert resta.izq.der.token.texto == "3"
    assert isinstance(resta.der, Numero)
    assert resta.der.token.texto == "2"

    print("Árbol de resta: OK")


def probar_precedencia():
    programa = parsear("umbral total := 1 + 2 * 3;")
    suma = programa.instrucciones[0].valor

    assert isinstance(suma, OperacionBinaria)
    assert suma.operador.texto == "+"
    assert isinstance(suma.izq, Numero)
    assert suma.izq.token.texto == "1"

    multiplicacion = suma.der
    assert isinstance(multiplicacion, OperacionBinaria)
    assert multiplicacion.operador.texto == "*"
    assert isinstance(multiplicacion.izq, Numero)
    assert multiplicacion.izq.token.texto == "2"
    assert isinstance(multiplicacion.der, Numero)
    assert multiplicacion.der.token.texto == "3"

    print("Precedencia: OK")


def probar_asignacion():
    programa = parsear("umbral a := 3; a := a + 1;")
    assert len(programa.instrucciones) == 2
    assert isinstance(programa.instrucciones[0], Declaracion)

    asignacion = programa.instrucciones[1]
    assert isinstance(asignacion, Asignacion)
    assert asignacion.nombre.texto == "a"

    suma = asignacion.valor
    assert isinstance(suma, OperacionBinaria)
    assert suma.operador.texto == "+"
    assert isinstance(suma.izq, Variable)
    assert suma.izq.token.texto == "a"
    assert isinstance(suma.der, Numero)
    assert suma.der.token.texto == "1"

    print("Asignación: OK")


def probar_mostrar_arbol():
    programa = parsear("umbral r := 10 - 3 - 2;")
    salida = io.StringIO()

    with redirect_stdout(salida):
        mostrar_arbol(programa)

    esperado = (
        "Programa\n"
        "  Declaracion umbral r\n"
        "    OperacionBinaria -\n"
        "      OperacionBinaria -\n"
        "        Numero 10\n"
        "        Numero 3\n"
        "      Numero 2\n"
    )
    assert salida.getvalue() == esperado
    print("Mostrar árbol: OK")


def probar_error(entrada, mensaje, linea, columna):
    try:
        parsear(entrada)
    except ErrorSintactico as e:
        assert e.mensaje == mensaje
        assert e.linea == linea
        assert e.columna == columna
        assert str(e) == f"Error sintáctico en línea {linea}, columna {columna}: {mensaje}"
        return
    raise AssertionError(f"No se lanzó ErrorSintactico para: {entrada!r}")


def probar_errores():
    probar_error(
        "umbral x := 5",
        "se esperaba ';' y llegó el fin del archivo",
        1,
        14,
    )
    probar_error(
        "umbral y := 4 + * 2;",
        "se esperaba un número, una variable o '(' y llegó '*'",
        1,
        17,
    )
    probar_error(
        "umbral z := (1 + 2;",
        "se esperaba ')' y llegó ';'",
        1,
        19,
    )
    probar_error(
        "umbral := 5;",
        "se esperaba un IDENTIFICADOR y llegó ':='",
        1,
        8,
    )
    probar_error(
        "umbral x = 5;",
        "se esperaba ':=' y llegó '='",
        1,
        10,
    )
    print("Errores sintácticos: OK")


def probar_error_base():
    try:
        parsear("umbral x := 5")
    except ErrorDeLenguaje as e:
        assert isinstance(e, ErrorSintactico)
        print("ErrorDeLenguaje atrapa ErrorSintactico: OK")
        return
    raise AssertionError("No se lanzó ErrorDeLenguaje")


if __name__ == "__main__":
    probar_arbol_resta()
    probar_precedencia()
    probar_asignacion()
    probar_mostrar_arbol()
    probar_errores()
    probar_error_base()
    print("Todas las pruebas del parser pasaron")
