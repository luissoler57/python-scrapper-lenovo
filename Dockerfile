FROM python:3-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema, Chrome y Xvfb
RUN apt-get update && \
  apt-get install -y \
  wget \
  gnupg2 \
  curl \
  unzip \
  # Dependencias de Chrome
  libnss3 \
  libgbm1 \
  libasound2 \
  libx11-xcb1 \
  libdrm2 \
  libexpat1 \
  libxcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxext6 \
  libxfixes3 \
  libxrandr2 \
  libxtst6 \
  fonts-liberation \
  xdg-utils \
  # Xvfb y dependencias de X11
  xvfb \
  x11vnc \
  xserver-xorg-video-dummy && \
  # Instalar Chrome
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
  apt-get update && \
  apt-get install -y google-chrome-stable && \
  # Limpiar cache
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

# Configurar usuario no-root
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
  chown -R appuser /app
USER appuser

# Comando para iniciar Xvfb y ejecutar la app
# CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && python app.py"]
CMD ["python", "app.py"]