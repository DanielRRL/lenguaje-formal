from dataclasses import dataclass

from tokens import Token


@dataclass
class Numero:
    token: Token


@dataclass
class Cadena:
    token: Token


@dataclass
class Variable:
    token: Token


@dataclass
class OperacionBinaria:
    izq: object
    operador: Token
    der: object


@dataclass
class Declaracion:
    tipo: Token
    nombre: Token
    valor: object


@dataclass
class Asignacion:
    nombre: Token
    valor: object


@dataclass
class Programa:
    instrucciones: list


def mostrar_arbol(nodo, nivel=0):
    # Dos espacios por nivel para que se vea la jerarquía del árbol.
    sangria = "  " * nivel

    if isinstance(nodo, Programa):
        print(f"{sangria}Programa")
        for instruccion in nodo.instrucciones:
            mostrar_arbol(instruccion, nivel + 1)

    elif isinstance(nodo, Declaracion):
        print(f"{sangria}Declaracion {nodo.tipo.texto} {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, Asignacion):
        print(f"{sangria}Asignacion {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, OperacionBinaria):
        print(f"{sangria}OperacionBinaria {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)

    elif isinstance(nodo, Numero):
        print(f"{sangria}Numero {nodo.token.texto}")

    elif isinstance(nodo, Variable):
        print(f"{sangria}Variable {nodo.token.texto}")

    elif isinstance(nodo, Cadena):
        print(f"{sangria}Cadena {nodo.token.texto}")
