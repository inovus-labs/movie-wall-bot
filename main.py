from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
# Test List
arr = ['1','2']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    print(update)
    if not len(context_value) <= 0:
        if not context_value[0] in arr:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are not a Member of Inovus Labs Discord"
            )
        else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Welcome {context_value[0]}"
            )



if __name__ == '__main__':
    application = ApplicationBuilder().token(config('TOKEN')).build()
    
    start_handler = CommandHandler('start', start)


    application.add_handler(start_handler)

    application.run_polling()