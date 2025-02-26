from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = 'Your token'

async def start(update: Update, context):
    await update.message.reply_text("Olá, sou seu bot! Como posso te ajudar?")
    
    
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
    
if __name__ == '__main__':
    main()