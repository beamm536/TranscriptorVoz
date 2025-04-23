# Usa imagen ligera con Python
FROM python:3.10-slim

# Evita prompts interactivos al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias de Python
# (usa Whisper + versión CPU de Torch)
# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Instala primero Flask y Whisper desde GitHub
RUN pip install --no-cache-dir flask \
    git+https://github.com/openai/whisper.git

# Instala PyTorch y sus componentes desde el índice CPU oficial
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu
# Expone el puerto del servidor Flask
EXPOSE 5000

# Comando para iniciar la app Flask
CMD ["python", "app.py"]
