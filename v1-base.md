 FROM python:3.10-slim

 RUN apt-get update && apt-get install -y \
 ffmpeg \
 git \
 && rm -rf /var/lib/apt/lists/*
 RUN apt-get update
 RUN apt-get install -y ffmpeg git

 WORKDIR /app

 COPY . /app
# 1. Instala Flask desde el índice normal de PyPI
 RUN pip install --no-cache-dir flask

# 2. Instala PyTorch desde su índice CPU oficial - quitamos torchvision / torchaudio -solo dejamos torch
 RUN pip install --no-cache-dir torch
 #RUN pip install --no-cache-dir \
     #torch --index-url https://download.pytorch.org/whl/cpu


 # 3. Instala Whisper desde GitHub
 RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

 EXPOSE 5000

 CMD ["python", "app.py"]