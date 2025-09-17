FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar curses
RUN apt-get update && apt-get install -y libncurses5-dev libncursesw5-dev && rm -rf /var/lib/apt/lists/*

COPY filosofos_estoicos.py filosofos_tablero.py ./

CMD ["python", "filosofos_estoicos.py"]
