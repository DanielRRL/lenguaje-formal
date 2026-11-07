from casos import CASOS
from lexer import tokenizar
from parser import Parser
from tokens import ErrorLexico, Token


def a_tuplas(tokens):
    # Adapta los objetos Token al formato de las pruebas anteriores.
    return [(t.tipo, t.texto, t.linea, t.columna) for t in tokens]


def probar_token():
    t = Token("NUMERO", "5", 1, 9)
    assert t.tipo == "NUMERO"
    assert t.texto == "5"
    assert t.linea == 1
    assert t.columna == 9
    assert str(t) == "NUMERO('5') en 1:9"
    print("Token: OK")


def probar_error_lexico():
    try:
        tokenizar("umbral x := 5 @")
    except ErrorLexico as e:
        assert e.mensaje == "carácter '@' no reconocido"
        assert e.linea == 1
        assert e.columna == 15
        assert str(e) == "Error léxico en línea 1, columna 15: carácter '@' no reconocido"
        print("ErrorLexico: OK")
    else:
        raise AssertionError("ErrorLexico: no se lanzó")


def probar_parser():
    tokens = tokenizar("umbral x := 5;")
    p1 = Parser(tokens)
    p2 = Parser(tokens)

    assert p1.actual().tipo == "TIPO"
    assert p2.actual().tipo == "TIPO"

    p1.avanzar()
    assert p1.actual().tipo == "IDENTIFICADOR"
    assert p2.actual().tipo == "TIPO"

    while p1.actual().tipo != "EOF":
        p1.avanzar()

    assert p1.actual().tipo == "EOF"
    p1.avanzar()
    assert p1.actual().tipo == "EOF"

    p3 = Parser(tokenizar("umbral y := 2;"))
    assert p3.actual().texto == "umbral"
    assert p1.actual().tipo == "EOF"

    print("Parser: OK")


def probar_casos():
    fallos = 0

    for nombre, entrada, esperada in CASOS:
        try:
            real = a_tuplas(tokenizar(entrada))
        except ErrorLexico as e:
            real = str(e)

        if real == esperada:
            continue

        fallos += 1
        print("FALLO:", nombre)
        print("  esperado:", esperada)
        print("  real:    ", real)

    print(f"{len(CASOS) - fallos}/{len(CASOS)} casos coinciden")
    assert fallos == 0


if __name__ == "__main__":
    probar_token()
    probar_error_lexico()
    probar_parser()
    probar_casos()
