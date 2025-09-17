import threading
import time
import random
import curses

# Número de filósofos / tenedores
N = 5
tenedores = [threading.Lock() for _ in range(N)]
camarero = threading.Semaphore(N - 1)

# Estados de los filósofos
estados = ["🤔"] * N
lock_estado = threading.Lock()

def actualizar_estado(i, nuevo_estado):
    with lock_estado:
        estados[i] = nuevo_estado

def filosofo(i):
    izq = i
    der = (i + 1) % N

    while True:
        actualizar_estado(i, "🤔")  # Pensando
        time.sleep(random.uniform(1, 2))

        camarero.acquire()
        tomado_izq = tenedores[izq].acquire(blocking=False)
        tomado_der = tenedores[der].acquire(blocking=False)

        if tomado_izq and tomado_der:
            actualizar_estado(i, "🍝")  # Comiendo
            time.sleep(random.uniform(2, 3))
            tenedores[izq].release()
            tenedores[der].release()
        else:
            if tomado_izq:
                tenedores[izq].release()
            if tomado_der:
                tenedores[der].release()
            actualizar_estado(i, "🧘")  # Acepta destino
            time.sleep(random.uniform(1, 2))

        camarero.release()

def dibujar_tablero(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    filosofos = []
    for i in range(N):
        t = threading.Thread(target=filosofo, args=(i,), daemon=True)
        filosofos.append(t)
        t.start()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "🧘‍♂️ Simulación de Filósofos Estoicos 🍝")
        stdscr.addstr(1, 2, "Ctrl+C para salir\n")

        with lock_estado:
            # Dibujar en forma circular
            stdscr.addstr(3, 10, f" {estados[0]} ")
            stdscr.addstr(5, 20, f" {estados[1]} ")
            stdscr.addstr(9, 16, f" {estados[2]} ")
            stdscr.addstr(9, 4,  f" {estados[3]} ")
            stdscr.addstr(5, 0,   f" {estados[4]} ")

        stdscr.refresh()
        time.sleep(0.5)

def main():
    curses.wrapper(dibujar_tablero)

if __name__ == "__main__":
    main()
