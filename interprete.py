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
from tokens import ErrorSemantico


def tipo_de_valor(valor):
    if type(valor) is bool:
        return "booleano"
    if type(valor) is str:
        return "texto"
    if type(valor) in (int, float):
        return "numero"
    return "desconocido"


def es_numero(valor):
    return type(valor) in (int, float)


class Entorno:
    def __init__(self, padre=None):
        self.valores = {}
        self.padre = padre

    def definir(self, nombre, tipo, valor, linea, columna):
        if nombre in self.valores:
            anterior = self.valores[nombre]["linea"]
            raise ErrorSemantico(
                f"la variable '{nombre}' ya fue declarada en la línea {anterior}",
                linea,
                columna,
            )
        self.valores[nombre] = {"tipo": tipo, "valor": valor, "linea": linea}

    def buscar(self, nombre):
        if nombre in self.valores:
            return self.valores[nombre]
        if self.padre is not None:
            return self.padre.buscar(nombre)
        return None


class Interprete:
    def __init__(self):
        self.entorno = Entorno()

    def ejecutar_programa(self, programa: Programa):
        for instruccion in programa.instrucciones:
            self.ejecutar(instruccion)

    def ejecutar_bloque(self, instrucciones):
        padre = self.entorno
        self.entorno = Entorno(padre)
        try:
            for instruccion in instrucciones:
                self.ejecutar(instruccion)
        finally:
            self.entorno = padre

    def ejecutar(self, nodo):
        if isinstance(nodo, Declaracion):
            valor = self.evaluar(nodo.valor)
            tipo = tipo_de_valor(valor)
            self.entorno.definir(
                nodo.nombre.texto,
                tipo,
                valor,
                nodo.nombre.linea,
                nodo.nombre.columna,
            )

        elif isinstance(nodo, Asignacion):
            actual = self.entorno.buscar(nodo.nombre.texto)
            if actual is None:
                raise ErrorSemantico(
                    f"la variable '{nodo.nombre.texto}' no ha sido declarada",
                    nodo.nombre.linea,
                    nodo.nombre.columna,
                )
            valor = self.evaluar(nodo.valor)
            tipo = tipo_de_valor(valor)
            if tipo != actual["tipo"]:
                raise ErrorSemantico(
                    f"no se puede guardar un {tipo} en la variable "
                    f"'{nodo.nombre.texto}' de tipo {actual['tipo']}",
                    nodo.nombre.linea,
                    nodo.nombre.columna,
                )
            actual["valor"] = valor

        elif isinstance(nodo, Mostrar):
            valores = [self.evaluar(expresion) for expresion in nodo.valores]
            print(" ".join(str(valor) for valor in valores))

        elif isinstance(nodo, Si):
            condicion = self.evaluar(nodo.condicion)
            if type(condicion) is not bool:
                raise ErrorSemantico(
                    "la condición debe ser booleana",
                    nodo.palabra.linea,
                    nodo.palabra.columna,
                )
            if condicion:
                self.ejecutar_bloque(nodo.entonces)
            elif nodo.sino is not None:
                self.ejecutar_bloque(nodo.sino)

        elif isinstance(nodo, Mientras):
            vueltas = 0
            while True:
                condicion = self.evaluar(nodo.condicion)
                if type(condicion) is not bool:
                    raise ErrorSemantico(
                        "la condición debe ser booleana",
                        nodo.palabra.linea,
                        nodo.palabra.columna,
                    )
                if not condicion:
                    break
                self.ejecutar_bloque(nodo.cuerpo)
                vueltas += 1
                if vueltas > 100000:
                    raise ErrorSemantico(
                        "el ciclo superó 100000 vueltas; "
                        "¿falta actualizar la variable de la condición?",
                        nodo.palabra.linea,
                        nodo.palabra.columna,
                    )

        else:
            raise ErrorSemantico("instrucción desconocida", 1, 1)

    def evaluar(self, nodo):
        if isinstance(nodo, Numero):
            texto = nodo.token.texto
            return float(texto) if "." in texto else int(texto)

        if isinstance(nodo, Cadena):
            return nodo.token.texto[1:-1]

        if isinstance(nodo, Booleano):
            return nodo.token.texto == "true"

        if isinstance(nodo, Variable):
            actual = self.entorno.buscar(nodo.token.texto)
            if actual is None:
                raise ErrorSemantico(
                    f"la variable '{nodo.token.texto}' no ha sido declarada",
                    nodo.token.linea,
                    nodo.token.columna,
                )
            return actual["valor"]

        if isinstance(nodo, Negativo):
            valor = self.evaluar(nodo.operando)
            if not es_numero(valor):
                raise ErrorSemantico(
                    "el signo '-' solo se puede usar con números",
                    nodo.operador.linea,
                    nodo.operador.columna,
                )
            return -valor

        if isinstance(nodo, OperacionBinaria):
            izq = self.evaluar(nodo.izq)
            der = self.evaluar(nodo.der)
            return self.operar(izq, nodo.operador, der)

        if isinstance(nodo, Comparacion):
            izq = self.evaluar(nodo.izq)
            der = self.evaluar(nodo.der)
            return self.comparar(izq, nodo.operador, der)

        if isinstance(nodo, OperacionLogica):
            izq = self.evaluar(nodo.izq)
            der = self.evaluar(nodo.der)
            if type(izq) is not bool or type(der) is not bool:
                raise ErrorSemantico(
                    "los operadores lógicos solo se pueden usar con booleanos",
                    nodo.operador.linea,
                    nodo.operador.columna,
                )
            if nodo.operador.texto == "AND":
                return izq and der
            return izq or der

        if isinstance(nodo, Not):
            valor = self.evaluar(nodo.operando)
            if type(valor) is not bool:
                raise ErrorSemantico(
                    "'NOT' solo se puede usar con booleanos",
                    nodo.operador.linea,
                    nodo.operador.columna,
                )
            return not valor

        raise ErrorSemantico("expresión desconocida", 1, 1)

    def operar(self, izq, operador, der):
        op = operador.texto
        tipo_izq = tipo_de_valor(izq)
        tipo_der = tipo_de_valor(der)

        if tipo_izq == "texto" or tipo_der == "texto":
            if op == "+" and tipo_izq == "texto" and tipo_der == "texto":
                return izq + der
            raise ErrorSemantico(
                f"no se puede usar '{op}' con textos",
                operador.linea,
                operador.columna,
            )

        if tipo_izq == "booleano" or tipo_der == "booleano":
            raise ErrorSemantico(
                f"no se puede usar '{op}' con booleanos",
                operador.linea,
                operador.columna,
            )

        if op == "+":
            return izq + der
        if op == "-":
            return izq - der
        if op == "*":
            return izq * der
        if op == "/":
            if der == 0:
                raise ErrorSemantico(
                    "división por cero", operador.linea, operador.columna
                )
            if type(izq) is int and type(der) is int:
                return izq // der
            return izq / der

        raise ErrorSemantico(
            f"operador desconocido '{op}'", operador.linea, operador.columna
        )

    def comparar(self, izq, operador, der):
        op = operador.texto
        tipo_izq = tipo_de_valor(izq)
        tipo_der = tipo_de_valor(der)

        if tipo_izq != tipo_der:
            raise ErrorSemantico(
                f"no se pueden comparar {tipo_izq} con {tipo_der}",
                operador.linea,
                operador.columna,
            )

        if op == "==":
            return izq == der
        if op == "!=":
            return izq != der

        if tipo_izq != "numero":
            raise ErrorSemantico(
                f"el operador '{op}' solo se puede usar con números",
                operador.linea,
                operador.columna,
            )

        if op == "<":
            return izq < der
        if op == "<=":
            return izq <= der
        if op == ">":
            return izq > der
        if op == ">=":
            return izq >= der

        raise ErrorSemantico(
            f"operador desconocido '{op}'", operador.linea, operador.columna
        )
