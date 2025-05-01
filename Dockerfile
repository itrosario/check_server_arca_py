# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY bot.py /app/
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

ENV BOT_TOKEN=""

# Comando para ejecutar el bot
CMD ["python", "bot.py"]
