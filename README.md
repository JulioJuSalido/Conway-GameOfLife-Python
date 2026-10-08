# Juego de la Vida de Conway - Python
Implementación del **Juego de la Vida de Conway** desarrollada en Python y ejecutada directamente desde la terminal.

El programa permite colocar y eliminar células en un tablero de 80 × 80 y posteriormente iniciar las iteraciones para observar cómo evoluciona la población siguiendo las reglas del Juego de la Vida.


## Descripción
El Juego de la Vida es un autómata celular creado por el matemático **John Horton Conway**. El estado de cada célula depende de las células que se encuentran a su alrededor.

En este proyecto, el usuario puede crear una configuración inicial colocando células en el tablero y después iniciar las iteraciones para observar su evolución.

## Reglas del juego
Cada célula puede estar viva o muerta y se consideran sus **8 vecinos**.

Las reglas utilizadas son:

* Una célula viva con menos de 2 vecinos vivos muere por falta de población.
* Una célula viva con más de 3 vecinos vivos muere por sobrepoblación.
* Una célula viva con 2 o 3 vecinos permanece viva.
* Una célula muerta con exactamente 3 vecinos vivos se convierte en una célula viva.

## Controles
| Tecla       | Acción                            |
| ----------- | --------------------------------- |
| `↑`         | Mover hacia arriba                |
| `↓`         | Mover hacia abajo                 |
| `←`         | Mover hacia la izquierda          |
| `→`         | Mover hacia la derecha            |
| `ENTER`     | Colocar o eliminar una célula     |
| `ESPACIO`   | Iniciar o detener las iteraciones |
| `Q` / `ESC` | Salir del juego                   |

## Tecnologías utilizadas
* **Python**
* `msvcrt` para la lectura de teclas.
* `os` para controlar la consola.
* `random` para seleccionar colores.
* `time` para controlar la velocidad de las iteraciones.
* Códigos **ANSI** para colores y posicionamiento del cursor.

## Requisitos

Se necesita tener instalado:

* Python 3.x
* Sistema Windows, debido al uso de `msvcrt`.

No se requieren librerías externas.


