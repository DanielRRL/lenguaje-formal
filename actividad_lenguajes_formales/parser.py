# Gramática del parser (checkpoint 14 de noviembre):
# programa    ::= instruccion* EOF
# instruccion ::= declaracion | asignacion
# declaracion ::= TIPO IDENTIFICADOR ':=' expresion ';'
# asignacion  ::= IDENTIFICADOR ':=' expresion ';'
# expresion   ::= termino (('+' | '-') termino)*
# termino     ::= factor (('*' | '/') factor)*
# factor      ::= NUMERO | CADENA | IDENTIFICADOR | '(' expresion ')'

from arbol import (
    Asignacion,
    Cadena,
    Declaracion,
    Numero,
    OperacionBinaria,
    Programa,
    Variable,
)
from tokens import ErrorSintactico, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        # Cada Parser guarda su propia lista y su propia posición.
        self.tokens = tokens
        self.pos = 0

    def actual(self) -> Token:
        # Devuelve el token actual sin mover la posición.
        return self.tokens[self.pos]

    def avanzar(self) -> Token:
        # Devuelve el token que deja atrás y se detiene en EOF.
        token = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def esperar(self, tipo: str, texto: str | None = None) -> Token:
        t = self.actual()
        if t.tipo != tipo or (texto is not None and t.texto != texto):
            quiero = f"'{texto}'" if texto else f"un {tipo}"
            llego = "el fin del archivo" if t.tipo == "EOF" else f"'{t.texto}'"
            raise ErrorSintactico(
                f"se esperaba {quiero} y llegó {llego}", t.linea, t.columna
            )
        return self.avanzar()

    def programa(self) -> Programa:
        instrucciones = []
        while self.actual().tipo != "EOF":
            instrucciones.append(self.instruccion())
        return Programa(instrucciones)

    def instruccion(self):
        t = self.actual()
        if t.tipo == "TIPO":
            return self.declaracion()
        if t.tipo == "IDENTIFICADOR":
            return self.asignacion()
        raise ErrorSintactico(
            f"se esperaba el inicio de una instrucción y llegó '{t.texto}'",
            t.linea,
            t.columna,
        )

    def declaracion(self) -> Declaracion:
        tipo = self.esperar("TIPO")
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("SIMBOLO", ":=")
        valor = self.expresion()
        self.esperar("SIMBOLO", ";")
        return Declaracion(tipo, nombre, valor)

    def asignacion(self) -> Asignacion:
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("SIMBOLO", ":=")
        valor = self.expresion()
        self.esperar("SIMBOLO", ";")
        return Asignacion(nombre, valor)

    def expresion(self):
        izq = self.termino()
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("+", "-"):
            operador = self.avanzar()
            der = self.termino()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def termino(self):
        izq = self.factor()
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("*", "/"):
            operador = self.avanzar()
            der = self.factor()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def factor(self):
        t = self.actual()
        if t.tipo == "NUMERO":
            return Numero(self.avanzar())
        if t.tipo == "CADENA":
            return Cadena(self.avanzar())
        if t.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
        if t.tipo == "SIMBOLO" and t.texto == "(":
            self.avanzar()
            dentro = self.expresion()
            self.esperar("SIMBOLO", ")")
            return dentro
        raise ErrorSintactico(
            f"se esperaba un número, una variable o '(' y llegó '{t.texto}'",
            t.linea,
            t.columna,
        )
