# Gramática final de Umbral:
# programa    ::= instruccion* EOF
# instruccion ::= declaracion | asignacion | salida | condicional | ciclo
# declaracion ::= 'umbral' IDENTIFICADOR ':=' expresion ';'
# asignacion  ::= IDENTIFICADOR ':=' expresion ';'
# salida      ::= 'notificar' '(' expresion (',' expresion)* ')' ';'
# condicional ::= 'IF' condicion 'THEN' bloque ('ELSE' bloque)? 'END'
# ciclo       ::= 'WHILE' condicion 'DO' bloque 'END'
# bloque      ::= instruccion*   // termina en ELSE o END
# condicion   ::= exp_or
# exp_or      ::= exp_and ('OR' exp_and)*
# exp_and     ::= factor_logico ('AND' factor_logico)*
# factor_logico ::= 'NOT' factor_logico | comparacion
# comparacion ::= expresion (operador_relacional expresion)?
# operador_relacional ::= '==' | '!=' | '<=' | '>=' | '<' | '>'
# expresion   ::= termino (('+' | '-') termino)*
# termino     ::= factor (('*' | '/') factor)*
# factor      ::= NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | '-' factor | '(' expresion ')'

from arbol import (
    Asignacion,
    Booleano,
    Cadena,
    Comparacion,
    Declaracion,
    Mientras,
    Mostrar,
    Negativo,
    Not,
    Numero,
    OperacionBinaria,
    OperacionLogica,
    Programa,
    Si,
    Variable,
)
from tokens import ErrorSintactico, Token

COMPARADORES = {"==", "!=", "<=", ">=", "<", ">"}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def actual(self) -> Token:
        return self.tokens[self.pos]

    def avanzar(self) -> Token:
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
        if t.tipo == "RESERVADA":
            if t.texto == "IF":
                return self.condicional()
            if t.texto == "WHILE":
                return self.ciclo()
            if t.texto == "notificar":
                return self.salida()
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

    def salida(self) -> Mostrar:
        palabra = self.esperar("RESERVADA", "notificar")
        self.esperar("SIMBOLO", "(")
        valores = [self.expresion()]
        while self.actual().tipo == "SIMBOLO" and self.actual().texto == ",":
            self.avanzar()
            valores.append(self.expresion())
        self.esperar("SIMBOLO", ")")
        self.esperar("SIMBOLO", ";")
        return Mostrar(palabra, valores)

    def condicional(self) -> Si:
        palabra = self.esperar("RESERVADA", "IF")
        condicion = self.condicion()
        self.esperar("RESERVADA", "THEN")
        entonces = self.bloque(palabra.linea)
        sino = None
        if self.actual().tipo == "RESERVADA" and self.actual().texto == "ELSE":
            self.avanzar()
            sino = self.bloque(palabra.linea)
        self.esperar("RESERVADA", "END")
        return Si(palabra, condicion, entonces, sino)

    def ciclo(self) -> Mientras:
        palabra = self.esperar("RESERVADA", "WHILE")
        condicion = self.condicion()
        self.esperar("RESERVADA", "DO")
        cuerpo = self.bloque(palabra.linea)
        self.esperar("RESERVADA", "END")
        return Mientras(palabra, condicion, cuerpo)

    def bloque(self, linea_apertura: int) -> list:
        instrucciones = []
        while True:
            t = self.actual()
            if t.tipo == "RESERVADA" and t.texto in ("ELSE", "END"):
                return instrucciones
            if t.tipo == "EOF":
                raise ErrorSintactico(
                    f"falta 'END' para cerrar el bloque abierto en la línea {linea_apertura}",
                    t.linea,
                    t.columna,
                )
            instrucciones.append(self.instruccion())

    def condicion(self):
        return self.exp_or()

    def exp_or(self):
        izq = self.exp_and()
        while self.actual().tipo == "RESERVADA" and self.actual().texto == "OR":
            operador = self.avanzar()
            der = self.exp_and()
            izq = OperacionLogica(izq, operador, der)
        return izq

    def exp_and(self):
        izq = self.factor_logico()
        while self.actual().tipo == "RESERVADA" and self.actual().texto == "AND":
            operador = self.avanzar()
            der = self.factor_logico()
            izq = OperacionLogica(izq, operador, der)
        return izq

    def factor_logico(self):
        t = self.actual()
        if t.tipo == "RESERVADA" and t.texto == "NOT":
            operador = self.avanzar()
            return Not(operador, self.factor_logico())
        return self.comparacion()

    def comparacion(self):
        izq = self.expresion()
        t = self.actual()
        if t.tipo == "OPERADOR" and t.texto in COMPARADORES:
            operador = self.avanzar()
            der = self.expresion()
            return Comparacion(izq, operador, der)
        return izq

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
        if t.tipo == "BOOLEANO":
            return Booleano(self.avanzar())
        if t.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
        if t.tipo == "OPERADOR" and t.texto == "-":
            operador = self.avanzar()
            return Negativo(operador, self.factor())
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
