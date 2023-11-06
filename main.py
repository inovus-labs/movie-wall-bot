from decouple import config
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,CallbackQueryHandler
import firebase_admin
from firebase_admin import firestore,credentials
from decouple import config 
from google.cloud.firestore_v1.base_query import FieldFilter
import requests
import json
import tmdbsimple as tmdb
import time
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

tmdb.API_KEY = config('TMDB_API')

arr = ['1','2']

# Use a service account.
cred = credentials.Certificate(config('FIREBASE_CREDENTIALS'))

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred)

db = firestore.client()
user_collection = db.collection("Users")
movie_collection = db.collection("Movie")
watch_log_collection = db.collection("WatchLog")

# user_collection.add({"Discord ID":"hello","Name":"56","Thumbnail":"india","Telegram ID":"Telegra ID"})

# user = movie_collection.get()

# HERE NEEDS TO GET THE API FOR USERS
x = requests.get('https://dummyjson.com/users').text

a = json.loads(x)
# print(a['users'][0]["id"])
# print(str(x.content["id"]))
# sample = list(docs)
# for i  in sample:
#     print(i.to_dict()["place"])
# for doc in docs:
#     #  print(dict(doc[0]))
#     # print(f"{doc.id} => {doc.to_dict()[]}")
#     sample = doc.to_dict()["age"]



# This is a  sample image fetching 

# search = tmdb.Search()
# response = search.movie(query='the journey to the center of the earth ')
# # print(type(response))
# # print(movie)
# for i in search.results:
#     print(i["backdrop_path"])
# 88751
# 'backdrop_path': '/zGLN7ohWaBxDtRmFagq73BXDCMd.jpg',
# 'poster_path': '/e2PTTF3iGyumCVGEqE3fvp7Us64.jpg', '
# https://image.tmdb.org/t/p/original/Adlc8JMVEXOelFO6hYpIYcGBx2T.jpg

url = "https://api.themoviedb.org/3/movie/88751/images"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer "+config('TMDB_READ_ACCESS_TOKEN')
    }

response = requests.get(url, headers=headers)

# print(response.text)



# url = "https://api.themoviedb.org/3/authentication"

# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YTFhNWVjMjAyNGYzNjk0MzViMWQzZmM0ZGMwYTI1MSIsInN1YiI6IjY1MzM3MmQ0OGNmY2M3MDEyYjNmMzQ3OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.xH_Oy-Xw1iREDOW9B3nUZw-sh86IgD-UUxUbC0rXZa4"
# }

# response = requests.get(url, headers=headers)

# print(response.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    print(update.message.chat.id)
    # print(update.text)
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
            InlineKeyboardButton("Option 3", callback_data="2"),
        ],
        [InlineKeyboardButton("None of the above", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your option:", reply_markup=reply_markup)
    # HERE NEEDS TO VERIFY THE USER IS A MEMEMBER OF INOVUS LABS DISCORD
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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    # user_telegram_id = update.message.chat.id
    generator_expr = (str(element) for element in context_value)
    separator = ' '
    result_string = separator.join(generator_expr)
    # print(result_string)
    # Here check weather the user is in the db or not in later (IF CONDITION)

    # movie = tmdb.Movies(result_string).info()
    # response = movie.info()
    search = tmdb.Search()
    response = search.movie(query=result_string)
    # print(type(response))
    # print(movie)
    for i in search.results[:3]:
        # print("Background:",i["backdrop_path"],"Overview:",i["overview"],"Release Date:",i["release_date"],"Original Date:",i['original_title'])
        # print(i["poster_path"])
        if not i["backdrop_path"] == None:
            url = "https://image.tmdb.org/t/p/original"+i["poster_path"]
            overview = i["overview"]
            release_date = i["release_date"]
            original_title = i["original_title"]
            # print(url)
            # await update.message.reply_text(text=f"{url}{overview}{release_date}{original_title}")
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="**Overview**\n"+overview+"\n**Released Date**\n"+release_date+"\n**Original Title**\n"+original_title+"\n"+url)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config('TELEGRAM_TOKEN')).read_timeout(30).write_timeout(30).build()
    start_handler = CommandHandler('start', start)
    add_movie_handler = CommandHandler('add_movie', add_movie)


    application.add_handler(start_handler)
    application.add_handler(add_movie_handler)
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)