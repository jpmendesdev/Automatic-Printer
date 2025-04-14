from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from UTILS.printerConfigs import PRINTER_NAME, TOKEN
from DAO.dao import create_document
#Update funciona como uma espécie de log no telegram, ele atualiza as ações referente a mensagens que aconteceram, ações de usuários.



async def salvar_docs(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    document: Document = update.message.document
    update.message.reply_text("Arraste os documentos para que sejam salvos!")
    file = await context.bot.get_file(document.file_id)
    file_bytes = await file.download_as_bytearray()
    file_name = document.file_name
    create_document(file_name,file_bytes)
    if create_document:
        await update.message.reply_text(f"Documento salvo com sucesso")
    else:
        await update.message.reply_text(f"Erro ao tentar salvar documento")
    
if __name__ == '__main__':   
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.Document.ALL, salvar_docs))
    print("Rodando...")
    app.run_polling()