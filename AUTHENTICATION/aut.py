import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from UTILS.bot_password import BOT_PASSWORD
from UTILS.sumatra import DOWNLOAD_PATH


# Dicionário para armazenar usuários autenticados
authorized_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text("Você já está autenticado. Pode enviar o PDF.")
    else:
        await update.message.reply_text("🔐 Olá! Envie a senha para acessar o bot.")

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        return  # Já autenticado, ignora

    if update.message.text == BOT_PASSWORD:
        authorized_users.add(user_id)
        await update.message.reply_text("✅ Senha correta! Agora você pode enviar PDFs para imprimir.")
    else:
        await update.message.reply_text("❌ Senha incorreta. Tente novamente.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in authorized_users:
        await update.message.reply_text("🔐 Acesso negado. Envie a senha primeiro.")
        return

    document = update.message.document
    if document.mime_type == "application/pdf":
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOWNLOAD_PATH, document.file_name)
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"📄 Documento recebido. Enviando para impressão...")