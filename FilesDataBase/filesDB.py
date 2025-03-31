import os
import tempfile
import time
import mysql.connector
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Configuração do Banco de Dados MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "seu_usuario",
    "password": "sua_senha",
    "database": "impressao_bot"
}

# Configuração do SumatraPDF (Windows)
SUMATRA_PATH = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
PRINTER_NAME = "EPSON L3250 Series"

TOKEN = "SEU_BOT_TOKEN"

# Conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(**DB_CONFIG)

# Início do bot
async def start(update: Update, context):
    await update.message.reply_text("Olá! Envie um arquivo para armazenar.")

# Receber documentos e salvar no BD
async def handle_document(update: Update, context):
    document = update.message.document
    file_id = document.file_id
    file_name = document.file_name
    file = await context.bot.get_file(file_id)
    
    # Baixar o arquivo temporariamente
    file_bytes = await file.download_as_bytearray()

    # Salvar no banco de dados
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO arquivos (nome_arquivo, conteudo) VALUES (%s, %s)", (file_name, file_bytes))
    conn.commit()
    cur.close()
    conn.close()

    await update.message.reply_text(f"Arquivo '{file_name}' salvo no banco!")

# Comando para imprimir o último arquivo salvo
async def imprimir(update: Update, context):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nome_arquivo, conteudo FROM arquivos ORDER BY criado_em DESC LIMIT 1")
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado is None:
        await update.message.reply_text("Nenhum arquivo disponível para impressão.")
        return

    file_id, file_name, file_content = resultado

    # Criar um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        file_path = temp_file.name
        temp_file.write(file_content)

    # Enviar para impressão
    print_document(file_path)

    await update.message.reply_text(f"Arquivo '{file_name}' enviado para impressão!")

# Função para imprimir (Windows)
def print_document(file_path):
    try:
        print("Enviando para impressão...")
        subprocess.run([SUMATRA_PATH, "-print-to", PRINTER_NAME, file_path], check=True)
        time.sleep(5)
        print("Impressão enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao imprimir: {e}")

# Configuração do bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("imprimir", imprimir))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    application.run_polling()

if __name__ == '__main__':
    main()
