from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

arr = ['1','2']
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    if not len(context_value) <= 0:
        if not context_value in arr:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are not a Member of Inovus Labs Discord"
            )
        else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Welcome {context_value}"
            )



if __name__ == '__main__':
    application = ApplicationBuilder().token(config('TOKEN')).build()
    
    start_handler = CommandHandler('start', start)
    # caps_handler = CommandHandler('caps', caps)

    application.add_handler(start_handler)
    # application.add_handler(caps_handler)

    application.run_polling()