# Conway's Game of Life

Este proyecto es una simulación en C++ por consola del "Juego de la Vida" (Conway's Game of Life), que es un autómata celular que evoluciona en una malla bidimensional.

## ¿Qué hace el programa?

1. **Generación del Tablero:**
   Al iniciar, el programa te pedirá definir el tamaño de la cuadrícula (con un mínimo de 10x10 y máximo de 100x100). Luego, generará aleatoriamente un tablero donde algunas células estarán vivas (representadas con el número `1`) y otras muertas (representadas con el número `0`).

2. **Reglas del Juego:**
   - Una célula viva con 2 o 3 vecinas vivas sigue viva.
   - Una célula viva con menos de 2 o más de 3 vecinas vivas muere (por soledad o superpoblación).
   - Una célula muerta con exactamente 3 vecinas vivas revive.
   - Las células consideran 8 vecinos (incluyendo diagonales).

3. **Proceso de Simulación:**
   En cada generación, el programa aplica las reglas del juego y muestra la evolución del tablero. Puedes continuar con más generaciones o detener la simulación en cualquier momento.

4. **Interacción:**
   Si aún quedan células vivas en el tablero, el programa preguntará si deseas continuar la simulación. El proceso puede repetirse hasta que todas las células mueran o decidas detenerlo.

5. **Historial de Cambios:**
   A lo largo del proceso, el sistema guarda cada generación del tablero. Al finalizar el programa, se imprimirá un historial completo de todas las generaciones agrupadas en bloques. Esto te permite visualizar paso a paso cómo evolucionó el tablero.

## Compilación y Ejecución

Para compilar el proyecto usando `g++`, abre una terminal en el directorio del proyecto y ejecuta:

```bash
g++ main.cpp -o game_of_life
```

Para ejecutar el programa recién compilado:

```bash
./game_of_life
```

## Estructura del Código

- **GameBoard.h**: Gestiona el tablero, las células y la aplicación de las reglas del juego.
- **GameValidator.h**: Valida la entrada del usuario para el tamaño del tablero.
- **GameSimulator.h**: Controla la simulación y la interacción con el usuario.
- **Utilities.h**: Contiene funciones de utilidad y la cola de cambios de generaciones.
- **main.cpp**: Punto de entrada del programa.
