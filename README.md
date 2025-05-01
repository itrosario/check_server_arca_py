# Telegram Bot para Consultas de ARCA

Este proyecto es un bot de Telegram que permite consultar el estado de los servicios de facturación electrónica y padrón de ARCA utilizando SOAP.

## Requisitos

- Python 3.11 o superior
- Docker (opcional, para ejecutar el bot en un contenedor)

## Instalación

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:
```bash
git clone https://github.com/itrosario/check_server_arca_py.git
cd check_server_arca_py
```

### 2. Crear un archivo `.env`
Crea un archivo `.env` en el directorio raíz del proyecto y agrega tu token del bot de Telegram:
```plaintext
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

Reemplaza `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ` con el token que obtuviste de [BotFather](https://t.me/BotFather).

### 3. Crear un entorno virtual (opcional)
Si deseas ejecutar el bot localmente, crea un entorno virtual e instala las dependencias:
```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
# source .venv/bin/activate  # En Linux/Mac

pip install -r requirements.txt
```

### 4. Ejecutar el bot localmente
Ejecuta el bot con:
```bash
python bot.py
```

## Uso con Docker

### 1. Construir la imagen de Docker
Construye la imagen de Docker utilizando el archivo `Dockerfile` incluido:
```bash
docker build -t telegram-bot .
```

### 2. Ejecutar el contenedor
Ejecuta el contenedor pasando el token del bot como una variable de entorno:
```bash
docker run -e BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ telegram-bot
```

### 3. Opcional: Usar un archivo `.env` con Docker
Si prefieres usar un archivo `.env` para pasar el token, puedes hacerlo con:
```bash
docker run --env-file .env telegram-bot
```

## Comandos del Bot

- `/start`: Inicia el bot y muestra un mensaje de bienvenida.
- `/help`: Muestra los comandos disponibles.
- `/facturacion`: Consulta el estado del servicio de facturación electrónica de ARCA.
- `/padron`: Consulta el estado del servicio del padrón de ARCA.
- `/todos`: Consulta el estado de ambos servicios.

## Licencia

Este software fue creado por **Juan Martin Villanueva** y está bajo la licencia [MIT](LICENSE).