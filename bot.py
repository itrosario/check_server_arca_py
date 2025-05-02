from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from zeep import Client, Transport
import requests
import ssl
import urllib3
import os
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

WSFEV_WSDL_URL = 'https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL'
PADRON_WSDL_URL = 'https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL'

context = ssl.create_default_context()
context.set_ciphers("DEFAULT:@SECLEVEL=1")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

session = requests.Session()
adapter = requests.adapters.HTTPAdapter()
session.mount('https://', adapter)
session.verify = False
adapter.init_poolmanager(connections=10, maxsize=10, ssl_context=context)

transport = Transport(session=session)

soap_client_wsfev = Client(WSFEV_WSDL_URL, transport=transport)
soap_client_padron = Client(PADRON_WSDL_URL, transport=transport)

def consultar_estado_wsfev():
    try:
        response = soap_client_wsfev.service.FEDummy()
        resultado = response
        return (
            f"🧾 Estado del servicio ARCA:\n"
            f"📡 AppServer: {resultado.AppServer}\n"
            f"💾 DbServer: {resultado.DbServer}\n"
            f"🔐 AuthServer: {resultado.AuthServer}"
        )
    except Exception as e:
        return f"⚠️ Error al consultar ARCA: {str(e)}"

def consultar_estado_padron():
    try:
        response = soap_client_padron.service.dummy()
        resultado = response
        return (
            f"📊 Estado del servicio del Padrón:\n"
            f"📡 AppServer: {resultado.appserver}\n"
            f"🔐 AuthServer: {resultado.authserver}\n"
            f"💾 DbServer: {resultado.dbserver}"
        )
    except Exception as e:
        return f"⚠️ Error al consultar el servicio del padrón: {str(e)}"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Usa /help para ver los comandos disponibles.")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/facturacion - Consulta el estado del servicio de facturación ARCA\n"
        "/padron - Consulta el estado del servicio del padrón\n"
        "/todos - Consulta el estado de ambos servicios\n"
        "/help - Muestra este mensaje de ayuda\n"
    )

# /facturacion
async def facturacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    estado_afip = consultar_estado_wsfev()
    await update.message.reply_text(estado_afip)

# /padron
async def padron(update: Update, context: ContextTypes.DEFAULT_TYPE):
    estado_padron = consultar_estado_padron()
    await update.message.reply_text(estado_padron)

#/todos
async def todos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    estado_afip = consultar_estado_wsfev()
    estado_padron = consultar_estado_padron()
    await update.message.reply_text(
        f"Estado del servicio de Facturacion de ARCA:\n{estado_afip}\n\n"
        f"Estado del servicio del Padrón:\n{estado_padron}"
    )

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("facturacion", facturacion))
    app.add_handler(CommandHandler("padron", padron))
    app.add_handler(CommandHandler("todos", todos))

    app.run_polling()
    
if __name__ == '__main__':
    main()
