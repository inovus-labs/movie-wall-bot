from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import firebase_admin
from firebase_admin import firestore,credentials
from decouple import config 
from google.cloud.firestore_v1.base_query import FieldFilter


arr = ['1','2']

# Use a service account.
cred = credentials.Certificate(config('FIREBASE_CREDENTIALS'))

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred)

db = firestore.client()
movie_collection = db.collection("Movie")
user_collection = db.collection("Users")
watch_log_collection = db.collection("WatchLog")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    print(update.message.chat.id)
    # print(update.text)
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
    application = ApplicationBuilder().token(config('TELEGRAM_TOKEN')).build()
    
    start_handler = CommandHandler('start', start)


    application.add_handler(start_handler)

    application.run_polling()