import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from rembg import remove
from PIL import Image
import openai

TOKEN = os.getenv("8222329548:AAHU1S0samdiNvDtT3B4I64SMU6lEKDQ8zA")
OPENAI_KEY = os.getenv("k-proj-xLfv8aT4JJHJ5QV0mYt9wWuhR1KTAdyJZeF0m54YCSV7k5aLjBhhvCx947mVBqEwYXF-KRI8jmT3BlbkFJ11sdK-l32plJHLw-kuGCFOrW09GfatSbhLlNFq3uBHDcJAF3zi94GuUlNEXBDULI0l_VpruhQA")
openai.api_key = OPENAI_KEY

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo to remove background or ask me anything!")

# Chatbot
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": update.message.text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

# Background Remover
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive("input.png")

    img = Image.open("input.png")
    out = remove(img)
    out.save("output.png")

    await update.message.reply_photo(open("output.png","rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.add_handler(MessageHandler(filters.PHOTO, photo))


app.run_polling()
