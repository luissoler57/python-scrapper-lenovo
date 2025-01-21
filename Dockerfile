# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema para Chrome y Selenium
RUN apt-get update && \
  apt-get install -y \
  wget \
  gnupg2 \
  curl \
  unzip \
  # Dependencias esenciales para Chrome
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
  xdg-utils && \
  # Xvfb y dependencias de X11
  xvfb \
  # Instalar Chrome
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
  apt-get update && \
  apt-get install -y google-chrome-stable && \
  # Limpiar cache
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

# Configurar usuario no-root
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
  chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden
# CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && python app.py"]
CMD ["python", "app.py"]