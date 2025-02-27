from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import MessageHandler, filters
import os
import tempfile
import subprocess
import time

TOKEN = 'Your telegram bot token'
PRINTER_NAME = "Your printer model"

async def start(update: Update, context):
    await update.message.reply_text("Olá, sou seu bot! Como posso te ajudar?")
    
async def imprimir(update: Update, context):
    await update.message.reply_text("Envie o documento que deseja imprimir!")
    
async def handle_document(update: Update, context):
    document = update.message.document
    file_id = document.file_id
    file = await context.bot.get_file(file_id)    
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        file_path = temp_file.name
        file_bytes = await file.download_as_bytearray()
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
    print_document(file_path)
    
    await update.message.reply_text("Documento enviado para impressão!")
    
 
def print_document(file_path):
    sumatra_path = r"Path to Sumatra in your desktop"
    try:
        print("Enviando para impressão...")
        subprocess.run([sumatra_path, "-print-to", PRINTER_NAME, file_path], check=True)
        time.sleep(5)
        print("Impressão enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao imprimir: {e}")
    
    
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("imprimir", imprimir))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.run_polling()
    
if __name__ == '__main__':
    main()