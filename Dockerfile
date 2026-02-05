# Imagen base
FROM python:3.11.0-slim-bullseye

# Zona horaria
ENV TZ=America/Mexico_City
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    apache2 \
    libmariadb-dev \
    libapache2-mod-wsgi-py3 \
    pkg-config \
    gcc \
    iputils-ping \
    net-tools \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libopenblas-dev \
    liblapack-dev \
    python3-dev \
    build-essential \
    && apt-get clean


# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias de python 
COPY requirements.txt . 
#"." de directorio actual = /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Se copia el resto del código
COPY . .

# Se expone el puerto y se utiliza el comando de arranque
EXPOSE 8000
CMD [ "apachectl", "-DFOREGROUND" ]