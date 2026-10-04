import sys
import time

import sys
import msvcrt
import os
import random  # ¡NUEVO! Importamos random para elegir colores al azar

# ==========================================
# CONFIGURACIÓN Y ESTILOS
# ==========================================

# Símbolos visuales.
SIMBOLO_SUELO = "' "
SIMBOLO_JUGADOR = "■ "

# Matriz principal
matriz = [[SIMBOLO_SUELO]*80 for x in range(80)]

# Matriz secundaria
matriz_dos = [[SIMBOLO_SUELO]*80 for x in range(80)]
# Lista de colores.
COLORES_HEX = ["0969da", "eda73b", "8b9bb4", "e43b44"]

# ==========================================
# COMANDOS DE CONSOLA
# ==========================================

def cls_imprimir(texto):
    """Imprime texto inmediatamente en pantalla sin hacer salto de línea."""
    sys.stdout.write(texto)
    sys.stdout.flush()

def cls_mover_cursor(fila, columna):
    """Mueve el cursor a una posición específica de la terminal."""
    cls_imprimir(f"\033[{fila};{columna}H")

def cls_ocultar_cursor():
    """Oculta el cursor parpadeante."""
    cls_imprimir("\033[?25l")

def cls_mostrar_cursor():
    """Muestra nuevamente el cursor."""
    cls_imprimir("\033[?25h")

def cls_limpiar_pantalla():
    """Borra todo el contenido de la consola."""
    cls_imprimir("\033[2J\033[H")

def cls_restaurar_colores():
    """Vuelve a los colores por defecto de la terminal."""
    cls_imprimir("\033[0m")

def cls_establecer_color_hex(hex_color):
    """
    Toma un color hexadecimal y aplica color 'True Color' (24 bits)
    al texto de la consola usando el código ANSI: \033[38;2;R;G;Bm
    """
    # 1. Convertir Hex (base 16) a RGB (base 10).
    # [0:2] toma los primeros dos caracteres, int(..., 16) lo convierte a entero base 10
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 2. Aplicar el código ANSI True Color.
    cls_imprimir(f"\033[38;2;{r};{g};{b}m")

def cls_leer_tecla():
    """
    Lee la tecla y la traduce.
    """
    if not msvcrt.kbhit(): # Esperar a que el usuario presione alguna tecla.
        pass 
    
    tecla = msvcrt.getch()

    # Detectar ENTER.
    if tecla == b'\r':
        return "ENTER"

    # Detectar Flechas (son códigos de dos bytes).
    if tecla in (b'\x00', b'\xe0'):
        flecha = msvcrt.getch()
        if flecha == b'H': return "ARRIBA"
        if flecha == b'P': return "ABAJO"
        if flecha == b'M': return "DERECHA"
        if flecha == b'K': return "IZQUIERDA"

    # Detectar SALIR.
    if tecla.lower() == b'q' or tecla == b'\x1b':
        return "SALIR"

    if tecla == b' ':
        return "ESPACIO"

    return "OTRA"


# ==========================================
# LÓGICA DEL JUEGO
# ==========================================

def dibujar_tablero():
    """Dibuja la cuadrícula vacía."""
    cls_limpiar_pantalla()
    # Asegurar que el suelo se dibuje con el color por defecto
    cls_restaurar_colores() 
    cls_mover_cursor(1,1)
    
    # Titulo
    cls_mover_cursor(1,57)
    cls_establecer_color_hex("87CEEB")
    print("Game Of Life - John Horton Conway")
    cls_restaurar_colores()
    
    # Imprimir la matriz
    cls_mover_cursor(2,1)
    for i in range(80):
        for h in range(80):
            cls_mover_cursor(i + 2, (h * 2) + 1)
            cls_imprimir(matriz[i][h])
    cls_mover_cursor(82, 1)
    print("Controles: Flechas (Mover), ENTER (Colocar/Borrar celula), ESPACIO (Iniciar/Terminar iteraciones), Q (Salir)")


def dibujar_personaje(fila, columna, color_hex):
    """Calcula la posición visual, aplica el color y dibuja al personaje."""
    columna_visual = (columna * 2) - 1
    cls_mover_cursor(fila, columna_visual)
    
    # 1. Activamos el color especial antes de imprimir.
    cls_establecer_color_hex(color_hex)
    
    # 2. Imprimimos el personaje.
    cls_imprimir(SIMBOLO_JUGADOR)
    
    # 3. Es importante restaurar colores inmediatamente para no "pintar" el resto de los caracteres en consola.
    cls_restaurar_colores()

def borrar_rastro(fila, columna):
    """Dibuja un bloque de suelo normal donde estaba el personaje."""
    columna_visual = (columna * 2) - 1
    cls_mover_cursor(fila, columna_visual)
    cls_restaurar_colores() # Asegurar color por defecto para el suelo
    valorx = columna - 1
    valory = fila - 2
    cls_imprimir(matriz[valory][valorx])
    
def celula_vecinos(y, x):

    vecinos = 0

    for fila in range(y-1, y+2):
        for columna in range(x-1, x+2):

            if fila == y and columna == x:
                continue

            if fila >= 0 and fila < 80 and columna >= 0 and columna < 80:

                if matriz[fila][columna] == SIMBOLO_JUGADOR:
                    vecinos += 1

    return vecinos

def siguiente_iteracion():

    for y in range(80):
        for x in range(80):

            vecinos = celula_vecinos(y, x)

            if matriz[y][x] == SIMBOLO_JUGADOR:

                if vecinos < 2:
                    matriz_dos[y][x] = SIMBOLO_SUELO

                elif vecinos > 3:
                    matriz_dos[y][x] = SIMBOLO_SUELO

                else:
                    matriz_dos[y][x] = SIMBOLO_JUGADOR

            else:

                if vecinos == 3:
                    matriz_dos[y][x] = SIMBOLO_JUGADOR

                else:
                    matriz_dos[y][x] = SIMBOLO_SUELO
                    
# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def iniciar_juego():
    valorx = 0
    valory = 0
    
    # Borrar pantalla
    os.system('cls')
    # Preparación
    os.system("") 
    cls_ocultar_cursor()
    
    # Estado inicial
    fila = 2
    columna = 1
    # Elegimos un color inicial aleatorio de la lista
    color = random.choice(COLORES_HEX)
    
    
    dibujar_tablero()
    cls_mover_cursor(2,1)
    dibujar_personaje(fila, columna, color)

    try:
        while True:
            comando = cls_leer_tecla()
            iteracion = False

            if comando == "SALIR":
                break
            
            # LÓGICA DEL COLOR.
            if comando == "ENTER":
                # Ingresar celula en la matriz
                if matriz[valory][valorx] == SIMBOLO_JUGADOR:
                    matriz[valory][valorx] = SIMBOLO_SUELO
                else:
                    matriz[valory][valorx] = SIMBOLO_JUGADOR
                # Volvemos a dibujar el personaje en el mismo lugar pero con nuevo color.
                #volver a dibujar
                dibujar_personaje(fila, columna, color)
                dibujar_tablero()
                continue # Saltamos el resto del ciclo.

            # Comando para empezar las iteraciones
            if comando == "ESPACIO":
                iteracion = True
            
            # Empezar iteraciones si el comando es ESPACIO
            while iteracion == True:
                # Esto es para que termine las iteraciones al dar q solo que se tiene que timear para que funcione
                if msvcrt.kbhit():
                    tecla = msvcrt.getch()
                    
                    if tecla.lower() == b' ':
                        break
                    
                siguiente_iteracion()
                # Que las iteraciones terminen cuando no hayan cambios
                if matriz == matriz_dos:
                    break
                for y in range(80):
                    for x in range(80):
                        matriz[y][x] = matriz_dos[y][x]
                dibujar_tablero()
                dibujar_personaje(fila, columna, color)
                time.sleep(0.2)
                continue
                
            # LÓGICA DE MOVIMIENTO.
            fila_ant, col_ant = fila, columna

            if comando == "ARRIBA":
                fila = max(2, fila - 1)

            elif comando == "ABAJO":
                fila = min(81, fila + 1)

            elif comando == "DERECHA":
                columna = min(80, columna + 1)

            elif comando == "IZQUIERDA": 
                columna = max(1, columna - 1)

            valorx = columna - 1
            valory = fila - 2

            if fila != fila_ant or columna != col_ant:
                borrar_rastro(fila_ant, col_ant)
                dibujar_personaje(fila, columna, color)
                
                

    finally:
        # Limpieza final.
        cls_restaurar_colores() # Importante: quitar colores antes de salir.
        cls_mostrar_cursor()
        cls_mover_cursor(83, 1)
        print("Juego cerrado.")
        

if __name__ == "__main__":
    iniciar_juego()