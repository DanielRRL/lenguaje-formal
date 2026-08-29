# Lenguaje de reglas para dispositivos móviles

## Integrantes

- REINA
- ALMEIDA
- AMORTEGUI
- ARIAS

## 1. Dominio o contexto del sistema

El lenguaje desarrollado está orientado al manejo de reglas para dispositivos
móviles, principalmente teléfonos celulares.

El sistema permitirá definir reglas que evalúen diferentes características
del dispositivo, como el nivel de batería, temperatura, almacenamiento,
volumen, brillo, señal, uso de datos móviles, memoria RAM y estado de
diferentes funciones.

Las reglas permitirán que el dispositivo ejecute determinadas acciones
cuando se cumplan una o varias condiciones.

## 2. Reglas en lenguaje natural

1. IF bateria < 20 THEN activar_ahorro

2. IF temperatura > 40 THEN apagar_celular

3. IF almacenamiento < 10 THEN mostrar_advertencia

4. IF volumen > 80 THEN reducir_volumen

5. IF brillo > 90 THEN reducir_brillo

6. IF señal < 30 THEN mostrar_alerta_senal

7. IF bateria < 20 AND cargando = false THEN activar_ahorro_de_energía

8. IF tiempo_de_pantalla > 6 AND modo_hora_de_dormir = false THEN activar_bienestar_digital

9. IF almacenamiento_utilizado > 90 AND limpieza_automática = false THEN activar_alerta_de_almacenamiento

10. IF ram >= 8 AND almacenamiento >= 64 THEN puede_jugar

11. IF bateria == 80 OR bateria >= 90 THEN carga_alta

12. IF bateria <= 20 AND cargando = true THEN mostrar_alerta_de_carga

13. IF temperatura_de_la_batería > 40 AND refrigeración_activa = false THEN activar_refrigeración

14. IF uso_de_datos_móviles > 80 AND wifi_conectado = false THEN mostrar_advertencia_de_datos

15. IF aplicaciones_abiertas > 10 THEN cerrar_aplicaciones


## 3. Cumplimiento de requisitos

### Reglas con una sola condición

Las reglas 1, 2, 3, 4, 5, 6 y 15 contienen una sola condición.

### Reglas con condiciones compuestas

Las reglas 7, 8, 9, 10, 12, 13 y 14 utilizan condiciones compuestas
mediante el operador lógico AND.

La regla 11 utiliza el operador lógico OR.

### Reglas que combinan diferentes tipos de datos

Las reglas 7, 8, 9, 12, 13 y 14 combinan variables numéricas y booleanas.

Por ejemplo:

IF bateria < 20 AND cargando = false THEN activar_ahorro

En esta regla:

- bateria es numérica.
- cargando es booleana.
- AND es un operador lógico.


## 4. Clasificación de variables

| Variable | Tipo Java | Ejemplo |
|---|---|---|
| bateria | int | 80 |
| temperatura | double | 38.5 |
| almacenamiento | int | 8 |
| volumen | int | 70 |
| brillo | int | 85 |
| señal | int | 50 |
| cargando | boolean | true |
| tiempo_de_pantalla | double | 6.5 |
| modo_hora_de_dormir | boolean | false |
| almacenamiento_utilizado | int | 92 |
| limpieza_automática | boolean | false |
| ram | int | 8 |
| temperatura_de_la_batería | double | 41.5 |
| refrigeración_activa | boolean | false |
| uso_de_datos_móviles | double | 85.5 |
| wifi_conectado | boolean | true |
| aplicaciones_abiertas | int | 12 |


## 5. Sintaxis general

La sintaxis general de las reglas será:

IF <condicion> [AND|OR <condicion>] THEN <accion>

<condicion> ::= <variable> <operador> <valor>

<operador> ::= > | < | >= | <= | == | =

<variable> ::= identificador_en_minusculas

<valor> ::= numero | true | false | "texto"

<accion> ::= identificador_en_minusculas


## 6. Palabras reservadas

El lenguaje utilizará las siguientes palabras reservadas:

| Palabra | Significado | Categoría |
|---|---|---|
| IF | Indica el inicio de una condición | Palabra clave |
| THEN | Indica la acción que se ejecutará | Palabra clave |
| AND | Permite unir dos condiciones que deben cumplirse | Operador lógico |
| OR | Permite establecer una alternativa entre condiciones | Operador lógico |
| TRUE | Representa un valor verdadero | Literal booleano |
| FALSE | Representa un valor falso | Literal booleano |


## 7. Convención de escritura

Para mantener una estructura uniforme se establecen las siguientes reglas:

- Las palabras reservadas se escriben en mayúsculas.
- Las variables se escriben en minúsculas.
- Las variables compuestas utilizan guion bajo.
- Las acciones se escriben en minúsculas.
- Los valores booleanos se escriben como true o false.
- Los operadores de comparación permitidos son >, <, >=, <=, == y =.
- Las reglas deben comenzar con IF.
- Las condiciones deben estar ubicadas antes de THEN.
- Las acciones deben aparecer después de THEN.