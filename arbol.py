from dataclasses import dataclass

from tokens import Token


@dataclass
class Numero:
    token: Token


@dataclass
class Cadena:
    token: Token


@dataclass
class Booleano:
    token: Token


@dataclass
class Variable:
    token: Token


@dataclass
class Negativo:
    operador: Token
    operando: object


@dataclass
class OperacionBinaria:
    izq: object
    operador: Token
    der: object


@dataclass
class Comparacion:
    izq: object
    operador: Token
    der: object


@dataclass
class OperacionLogica:
    izq: object
    operador: Token
    der: object


@dataclass
class Not:
    operador: Token
    operando: object


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
class Mostrar:
    palabra: Token
    valores: list


@dataclass
class Si:
    palabra: Token
    condicion: object
    entonces: list
    sino: list | None


@dataclass
class Mientras:
    palabra: Token
    condicion: object
    cuerpo: list


@dataclass
class Programa:
    instrucciones: list


def mostrar_arbol(nodo, nivel=0):
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

    elif isinstance(nodo, Mostrar):
        print(f"{sangria}Mostrar {nodo.palabra.texto}")
        for valor in nodo.valores:
            mostrar_arbol(valor, nivel + 1)

    elif isinstance(nodo, Si):
        print(f"{sangria}Si {nodo.palabra.texto}")
        print(f"{sangria}  Condicion")
        mostrar_arbol(nodo.condicion, nivel + 2)
        print(f"{sangria}  Entonces")
        for instruccion in nodo.entonces:
            mostrar_arbol(instruccion, nivel + 2)
        if nodo.sino is not None:
            print(f"{sangria}  Sino")
            for instruccion in nodo.sino:
                mostrar_arbol(instruccion, nivel + 2)

    elif isinstance(nodo, Mientras):
        print(f"{sangria}Mientras {nodo.palabra.texto}")
        print(f"{sangria}  Condicion")
        mostrar_arbol(nodo.condicion, nivel + 2)
        print(f"{sangria}  Hacer")
        for instruccion in nodo.cuerpo:
            mostrar_arbol(instruccion, nivel + 2)

    elif isinstance(nodo, OperacionBinaria):
        print(f"{sangria}OperacionBinaria {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)

    elif isinstance(nodo, Comparacion):
        print(f"{sangria}Comparacion {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)

    elif isinstance(nodo, OperacionLogica):
        print(f"{sangria}OperacionLogica {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)

    elif isinstance(nodo, Not):
        print(f"{sangria}Not {nodo.operador.texto}")
        mostrar_arbol(nodo.operando, nivel + 1)

    elif isinstance(nodo, Negativo):
        print(f"{sangria}Negativo {nodo.operador.texto}")
        mostrar_arbol(nodo.operando, nivel + 1)

    elif isinstance(nodo, Numero):
        print(f"{sangria}Numero {nodo.token.texto}")

    elif isinstance(nodo, Variable):
        print(f"{sangria}Variable {nodo.token.texto}")

    elif isinstance(nodo, Cadena):
        print(f"{sangria}Cadena {nodo.token.texto}")

    elif isinstance(nodo, Booleano):
        print(f"{sangria}Booleano {nodo.token.texto}")
