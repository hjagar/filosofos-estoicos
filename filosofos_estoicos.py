import threading
import time
import random
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Número de filósofos / tenedores
N = 5

# Un lock por cada tenedor
tenedores = [threading.Lock() for _ in range(N)]

# Camarero: solo permite que N-1 filósofos intenten comer
camarero = threading.Semaphore(N - 1)

# Funciones "estoicas"
def aceptar_destino(i):
    print(Fore.CYAN + f"Filósofo {i} dice: El universo decidió que no coma ahora. Y estoy bien con eso.")
    time.sleep(random.uniform(1, 2))

def meditar_sobre_la_virtud(i):
    print(Fore.MAGENTA + f"Filósofo {i} medita: La virtud basta para ser feliz. El hambre es indiferente.")
    time.sleep(random.uniform(1, 2))

# Acción principal de cada filósofo
def filosofo(i):
    izq = i
    der = (i + 1) % N

    while True:
        print(Fore.YELLOW + f"🤔 Filósofo {i} está pensando...")
        time.sleep(random.uniform(1, 2))

        camarero.acquire()
        tomado_izq = tenedores[izq].acquire(blocking=False)
        tomado_der = tenedores[der].acquire(blocking=False)

        if tomado_izq and tomado_der:
            print(Fore.GREEN + f"🍝 Filósofo {i} está comiendo serenamente...")
            time.sleep(random.uniform(2, 3))
            tenedores[izq].release()
            tenedores[der].release()
            print(Fore.BLUE + f"Filósofo {i} terminó de comer y los suelta con desapego.")
        else:
            if tomado_izq:
                tenedores[izq].release()
            if tomado_der:
                tenedores[der].release()
            aceptar_destino(i)
            meditar_sobre_la_virtud(i)

        camarero.release()

# Crear y lanzar hilos
def main():
    filosofos = []
    for i in range(N):
        t = threading.Thread(target=filosofo, args=(i,), daemon=True)
        filosofos.append(t)
        t.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(Style.BRIGHT + Fore.RED + "\nSimulación interrumpida. Los filósofos se despiden con ecuanimidad.")

if __name__ == "__main__":
    main()
