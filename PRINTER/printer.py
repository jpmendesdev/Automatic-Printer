import os
import subprocess
from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from UTILS.printerConfigs import PRINTER_NAME, TOKEN
from UTILS.sumatra import SUMATRA_PATH, DOWNLOAD_PATH
from DAO.dao import create_document, read_document, cursor, conexao

#Update funciona como uma espécie de log no telegram, ele atualiza as ações referente a mensagens que aconteceram, ações de usuários.


# Cria a pasta de downloads se não existir
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def print_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type == "application/pdf":
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOWNLOAD_PATH, document.file_name)
        
        # Baixar o arquivo
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"Documento {document.file_name} recebido. Enviando para impressão...")

        # Comando para imprimir usando o SumatraPDF
        try:
            subprocess.run([
                SUMATRA_PATH,
                "-print-to-default",
                "-silent",
                file_path
            ], check=True)
            await update.message.reply_text("Impressão enviada com sucesso!")
        except subprocess.CalledProcessError as e:
            await update.message.reply_text(f"Erro ao imprimir: {e}")
    else:
        await update.message.reply_text("Por favor, envie um arquivo PDF.")

 
    
    
if __name__ == '__main__':   
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.ALL, print_document))
    app.run_polling()