import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from bot import (
    consultar_estado_wsfev,
    consultar_estado_wsfexv,
    consultar_estado_padron,
    consultar_estado_padronA4,
    facturacion,
    facturacionExportacion,
    padron,
    padronA4,
)

# Test para funciones SOAP
@patch("bot.soap_client_wsfev.service.FEDummy")
def test_consultar_estado_wsfev(mock_fedummy):
    # Caso exitoso
    mock_fedummy.return_value = MagicMock(
        AppServer="OK", DbServer="OK", AuthServer="OK"
    )
    resultado = consultar_estado_wsfev()
    assert "AppServer: OK" in resultado
    assert "DbServer: OK" in resultado
    assert "AuthServer: OK" in resultado

    # Caso con excepción
    mock_fedummy.side_effect = Exception("Error en el servicio")
    resultado = consultar_estado_wsfev()
    assert "⚠️ Error al consultar ARCA: Error en el servicio" in resultado


@patch("bot.soap_client_wsfexv.service.FEXDummy")
def test_consultar_estado_wsfexv(mock_fexdummy):
    # Caso exitoso
    mock_fexdummy.return_value = MagicMock(
        AppServer="OK", DbServer="OK", AuthServer="OK"
    )
    resultado = consultar_estado_wsfexv()
    assert "AppServer: OK" in resultado
    assert "DbServer: OK" in resultado
    assert "AuthServer: OK" in resultado

    # Caso con excepción
    mock_fexdummy.side_effect = Exception("Error en el servicio")
    resultado = consultar_estado_wsfexv()
    assert "⚠️ Error al consultar ARCA: Error en el servicio" in resultado


@patch("bot.soap_client_padron.service.dummy")
def test_consultar_estado_padron(mock_dummy):
    # Caso exitoso
    mock_dummy.return_value = MagicMock(
        appserver="OK", authserver="OK", dbserver="OK"
    )
    resultado = consultar_estado_padron()
    assert "AppServer: OK" in resultado
    assert "AuthServer: OK" in resultado
    assert "DbServer: OK" in resultado

    # Caso con excepción
    mock_dummy.side_effect = Exception("Error en el servicio")
    resultado = consultar_estado_padron()
    assert "⚠️ Error al consultar el servicio del padrón: Error en el servicio" in resultado


@patch("bot.soap_client_padron_a4.service.dummy")
def test_consultar_estado_padronA4(mock_dummy):
    # Caso exitoso
    mock_dummy.return_value = MagicMock(
        appserver="OK", authserver="OK", dbserver="OK"
    )
    resultado = consultar_estado_padronA4()
    assert "AppServer: OK" in resultado
    assert "AuthServer: OK" in resultado
    assert "DbServer: OK" in resultado

    # Caso con excepción
    mock_dummy.side_effect = Exception("Error en el servicio")
    resultado = consultar_estado_padronA4()
    assert "⚠️ Error al consultar el servicio del padrón A4: Error en el servicio" in resultado


# Test para comandos de Telegram
@pytest.mark.asyncio
async def test_facturacion():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Caso exitoso
    with patch("bot.consultar_estado_wsfev", return_value="Estado OK"):
        await facturacion(update, context)
        update.message.reply_text.assert_called_once_with("Estado OK")

    # Caso con excepción
    with patch("bot.consultar_estado_wsfev", side_effect=Exception("Error en el comando")):
        await facturacion(update, context)
        update.message.reply_text.assert_called_with("⚠️ Error al consultar ARCA: Error en el comando")


@pytest.mark.asyncio
async def test_facturacionExportacion():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Caso exitoso
    with patch("bot.consultar_estado_wsfexv", return_value="Estado Exportación OK"):
        await facturacionExportacion(update, context)
        update.message.reply_text.assert_called_once_with("Estado Exportación OK")

    # Caso con excepción
    with patch("bot.consultar_estado_wsfexv", side_effect=Exception("Error en el comando")):
        await facturacionExportacion(update, context)
        update.message.reply_text.assert_called_with("⚠️ Error al consultar ARCA: Error en el comando")


@pytest.mark.asyncio
async def test_padron():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Caso exitoso
    with patch("bot.consultar_estado_padron", return_value="Estado Padrón OK"):
        await padron(update, context)
        update.message.reply_text.assert_called_once_with("Estado Padrón OK")

    # Caso con excepción
    with patch("bot.consultar_estado_padron", side_effect=Exception("Error en el comando")):
        await padron(update, context)
        update.message.reply_text.assert_called_with("⚠️ Error al consultar el servicio del padrón: Error en el comando")


@pytest.mark.asyncio
async def test_padronA4():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Caso exitoso
    with patch("bot.consultar_estado_padronA4", return_value="Estado Padrón A4 OK"):
        await padronA4(update, context)
        update.message.reply_text.assert_called_once_with("Estado Padrón A4 OK")

    # Caso con excepción
    with patch("bot.consultar_estado_padronA4", side_effect=Exception("Error en el comando")):
        await padronA4(update, context)
        update.message.reply_text.assert_called_with("⚠️ Error al consultar el servicio del padrón A4: Error en el comando")
