# Umbral

Lenguaje de reglas para dispositivos móviles, extendido a un lenguaje de
programación con variables, expresiones, condiciones, ciclos y salida.

## 1. Integrantes

- REINA
- ALMEIDA
- AMORTEGUI
- ARIAS

## 2. Cómo ejecutar

```bash
python main.py programa.txt
```

También se puede abrir el modo interactivo:

```bash
python main.py
```

Para salir del modo interactivo se escribe `salir` o se presiona `Ctrl+D`.

El proyecto requiere Python 3.10 o superior.

## 3. Ficha del lenguaje

### Nombre

**Umbral**. Se llama así porque la declaración de variables usa la palabra
`umbral` y el lenguaje nació para controlar umbrales del dispositivo, como el
brillo, el volumen o la batería.

### Tabla de traducción desde Java

| Concepto | Java | Umbral |
|---|---|---|
| Tipo de variable | `int`, `double`, `String`, `boolean` | `umbral` con tipo inferido |
| Asignación | `=` | `:=` |
| Fin de instrucción | `;` | `;` |
| Salida | `System.out.println(...)` | `notificar(...);` |
| Condicional | `if (cond) { ... } else { ... }` | `IF cond THEN ... ELSE ... END` |
| Ciclo | `while (cond) { ... }` | `WHILE cond DO ... END` |
| Comentario | `//` y `/* ... */` | `#` y `/* ... */` |

### Decisión de diseño

La asignación se escribe `:=` y no `=`. Así se distingue claramente de la
comparación de igualdad `==`. Además, `umbral` declara una variable y el tipo
se infiere del valor: número, texto o booleano. Una variable no puede cambiar
de tipo después de declararse.

## 4. Gramática final en EBNF

```ebnf
programa    ::= instruccion* EOF
instruccion ::= declaracion | asignacion | salida | condicional | ciclo
declaracion ::= 'umbral' IDENTIFICADOR ':=' expresion ';'
asignacion  ::= IDENTIFICADOR ':=' expresion ';'
salida      ::= 'notificar' '(' expresion (',' expresion)* ')' ';'
condicional ::= 'IF' condicion 'THEN' bloque ('ELSE' bloque)? 'END'
ciclo       ::= 'WHILE' condicion 'DO' bloque 'END'
bloque      ::= instruccion*          // termina en ELSE o END
condicion   ::= exp_or
exp_or      ::= exp_and ('OR' exp_and)*
exp_and     ::= factor_logico ('AND' factor_logico)*
factor_logico ::= 'NOT' factor_logico | comparacion
comparacion ::= expresion (operador_relacional expresion)?
operador_relacional ::= '==' | '!=' | '<=' | '>=' | '<' | '>'
expresion   ::= termino (('+' | '-') termino)*
termino     ::= factor (('*' | '/') factor)*
factor      ::= NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | '-' factor | '(' expresion ')'
```

## 5. Reglas de operaciones entre tipos

| Operación | Regla |
|---|---|
| `+` entre números | Suma. |
| `+` entre textos | Concatenación. |
| `+` entre número y texto | Error semántico. |
| `-`, `*`, `/` entre números | Operación numérica. |
| `/` entre enteros | División entera. |
| `/` con al menos un decimal | División real. |
| División por cero | Error semántico. |
| `-`, `*`, `/` con textos | Error semántico. |
| `AND`, `OR`, `NOT` | Solo booleanos. |
| `==` y `!=` | Mismo tipo: números, textos o booleanos. |
| `<`, `<=`, `>`, `>=` | Solo números. |
| Variable de tipo número | Acepta enteros y decimales. |
| Variable de tipo texto | Acepta textos. |
| Variable de tipo booleano | Acepta `true` y `false`. |

`umbral` infiere el tipo en la declaración. Una variable no puede cambiar de
tipo después.

## 6. Requerimientos electivos

### 6.1 Tipo booleano

El lenguaje acepta `true` y `false` como valores y permite variables booleanas.

```text
umbral listo := true;
IF listo THEN
    notificar("listo");
END
```

Salida:

```text
listo
```

### 6.2 Modo interactivo

Al ejecutar `python main.py` sin archivo se abre un prompt que ejecuta
instrucciones línea por línea y conserva las variables.

```text
> umbral a := 2;
> notificar(a);
2
> salir
```

## 7. Estructura del repositorio

```text
README.md
tokens.py
lexer.py
arbol.py
parser.py
interprete.py
main.py
programa.txt
factorial.txt
promedio.txt
```

## 8. Programas de muestra

### 8.1 Tabla del 3

Archivo `programa.txt`:

```text
umbral n := 1;
WHILE n <= 5 DO
    notificar(n * 3);
    n := n + 1;
END
```

Ejecución:

```bash
python main.py programa.txt
```

Salida:

```text
3
6
9
12
15
```

### 8.2 Factorial de 5

Archivo `factorial.txt`:

```text
umbral n := 5;
umbral resultado := 1;
WHILE n > 1 DO
    resultado := resultado * n;
    n := n - 1;
END
notificar(resultado);
```

Ejecución:

```bash
python main.py factorial.txt
```

Salida:

```text
120
```

### 8.3 Promedio de tres notas

Archivo `promedio.txt`:

```text
umbral promedio := (3.0 + 4.0 + 5.0) / 3.0;
notificar(promedio);
IF promedio >= 3.0 THEN
    notificar("aprueba");
ELSE
    notificar("reprueba");
END
```

Ejecución:

```bash
python main.py promedio.txt
```

Salida:

```text
4.0
aprueba
```

## 9. Requerimientos obligatorios

### 9.1 Alcance de bloques

Cada bloque de `IF` y `WHILE` tiene su propio entorno. Una variable declarada
dentro de un bloque no existe fuera.

```text
IF 1 < 2 THEN
    umbral x := 5;
END
notificar(x);
```

Salida:

```text
Error semántico en línea 4, columna 11: la variable 'x' no ha sido declarada
notificar(x);
          ^
linea = 4, columna = 11
```

### 9.2 Operadores lógicos

```text
umbral n := 7;
IF n >= 1 AND n <= 10 THEN
    notificar("en rango");
END
```

Salida:

```text
en rango
```

### 9.3 Números negativos

```text
umbral x := -5;
umbral y := -(x + 2);
notificar(y);
```

Salida:

```text
3
```

### 9.4 Errores que señalan el código

`main.py` imprime el mensaje, la línea del programa y un `^` debajo de la
columna del error.

```text
umbral a := 5;
notificar(a);
notificar(b);
```

Salida:

```text
5
Error semántico en línea 3, columna 11: la variable 'b' no ha sido declarada
notificar(b);
          ^
linea = 3, columna = 11
```

## 10. Comentarios

Se admiten comentarios de línea con `#` y comentarios de bloque con
`/* ... */`.

```text
# esto es un comentario
/* esto también
   es un comentario */
```
