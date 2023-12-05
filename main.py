from decouple import config
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,CallbackQueryHandler,MessageHandler
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

# This is a sample test array for validating /start command for testing purpose 
arr = ['1','2']

# Use a service account.
cred = credentials.Certificate(config('FIREBASE_CREDENTIALS'))

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred)

db = firestore.client()
user_collection = db.collection("Users")
movie_collection = db.collection("Movie")
watch_log_collection = db.collection("WatchLog")

# user_collection.add({"Discord_ID":"hello","Name":"56","Thumbnail":"india","Telegram_ID":"Telegra ID"})
# user_collection.add({"Discord_ID":"hello","Name":"56","Thumbnail":"india","Telegram_ID":"Telegra ID"})
# user_collection.add({"Discord_ID":"hello","Name":"56","Thumbnail":"india","Telegram_ID":"Telegra ID"})
# movie_collection.add({"Movie_ID":"12345","Movie_Name":"avatar","Thumbnail_Url":"india","User":["sample"]})



# user = movie_collection.get()

# HERE NEEDS TO GET THE API FOR USERS
# x = requests.get('https://dummyjson.com/users').text

# a = json.loads(x)
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

# docs = user_collection.stream()

# for doc in docs:
#     print(f"{doc.id} => {doc.to_dict()}")


# doc_ref = user_collection.document("1177818025")

# doc = doc_ref.get()
# if doc.exists:
#     print(f"Document data: {doc.to_dict()}")
# else:
#     print("No such document!")


# collections = user_collection.document("1177818025").collections()
# for collection in collections:
#     for doc in collection.stream():
#         print(f"{doc.id} => {doc.to_dict()}")


# announce_docs = user_collection.stream()

# # for doc in announce_docs:
# #         print(doc.to_dict())
# # print(announce_docs)
# for doc in announce_docs:
#    print(f"{doc.id} => {doc.to_dict()}")


# docs = (
#     user_collection
#     .where(filter=FieldFilter("Name", "==", "Arjun "))
#     .get()
# )
# if docs:
#     for doc in docs:
#         print(f"{doc.id} => {doc.to_dict()}")
# else:
#     print("not found")


# city = {"Discord ID": "093845098", "Name": "Alan","Thumbnail":"7545934958327","Telegram ID":"1177818025"}
# city = {"Discord ID": "093845098", "Name": "Nithin Daniel","Thumbnail":"23452345235","Telegram ID":"23424523424"}
# city = {"Discord ID": "1177818025", "Name": "Badhusha","Thumbnail":"0988765","Telegram ID":"2345365356"}
# update_time, city_ref = user_collection.add(city)
# print(f"Added document with id {city_ref.id}")

movie_name = ''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    print(update.message.chat.id)
    # print(update.text)

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
    current_user = query.from_user.id
    if not query.data == 'None' and not query.data == "NotAvailable":
        # Here the query data for saving data to database
        # print(query.data)
        movie_id = query.data.split()[0]
        movie_language = query.data.split()[1]
        # print(movie_language)
        # Here the where condition for user is in the database
        user_validation = (user_collection.where(filter=FieldFilter("Telegram_ID", "==", current_user)).stream())
        # Here the where condition for movie is in the database
        movie_validation = (
        movie_collection
        .where(filter=FieldFilter("Movie_ID", "==", movie_id))
        .stream()
        )

        # Here the API get all the movie details with movie_id and movie_language 
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language={movie_language}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer "+config('TMDB_READ_ACCESS_TOKEN')
        }

        response = requests.get(url, headers=headers)
        # print(response.json()["adult"])
        response_movie_title = response.json()["title"]
        response_movie_id = response.json()["id"]
        response_movie_poster_path = response.json()["poster_path"]
        # This validation checks weather the user is exist of not in the database
        # print(movie_id)
        if user_validation:
                movie_collection_id = ""
                movie = movie_collection.where(filter=FieldFilter("Movie_ID", "!=", movie_id))
                query_results = movie.get()
                for document in query_results:
                    if document.to_dict()['Movie_ID'] == int(movie_id):
                        document_id = document.id 
                        break
                    else:
                        print("not avalilable")
                        break
            # else:
                # movie_collection.add({"Movie_ID":response_movie_id,"Movie_Name":response_movie_title,"Thumbnail_Url":response_movie_poster_path,"User":[current_user]})
        else:
            await query.edit_message_text(text=f"You are not a member of Inovus Labs IEDC Discord")   
    elif query.data == 'NotAvailable':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No movie found with "+movie_name
            )
    else:
        search = tmdb.Search()
        response = search.movie(query=movie_name)
        if search.results:
            # print(search.results)
            # first_callback = search.results[0]['id']
            # print(first_callback)
            global keyboard
            keyboard = []
            option_count = 1
            for i in search.results[3:9]:
                if  i["overview"]:
                    url = "https://image.tmdb.org/t/p/original"+str(i["poster_path"])
                    overview = i["overview"]
                    release_date = i["release_date"]
                    original_title = i["original_title"]
                    # print(original_title)
                    await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="**Overview**\n"+overview+"\n**Released Date**\n"+release_date+"\n**Original Title**\n"+original_title+"\n"+url)
                
                # The keyboard list will  insert each  InlineKeyboardButton
                # The appending is working in Option and we assign a local variable already for the count and it will increment and callback_data is the `id` from the TMDB server
                keyboard.append([InlineKeyboardButton("Option "+str(option_count), callback_data=str(i['id'])+"  "+str(i['original_language']))])
                # It will increment the counter number for callback_data
                option_count += 1
        # We need the this button last of the all the buttons so we appeded this here
        keyboard.pop()
        keyboard.append([InlineKeyboardButton("None of the above", callback_data="NotAvailable")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.effective_chat.send_message("Choose your option:", reply_markup=reply_markup)

async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_value = context.args
    # user_telegram_id = update.message.chat.id
    generator_expr = (str(element) for element in context_value)
    separator = ' '
    result_string = separator.join(generator_expr)
    global movie_name
    movie_name +=result_string
    # Here check weather the user is in the db or not in later (IF CONDITION)

    # movie = tmdb.Movies(result_string).info()
    # response = movie.info()
    search = tmdb.Search()
    response = search.movie(query=result_string)
    if search.results:
        # first_callback = search.results[0]['id']
        # print(first_callback)
        keyboard = []
        option_count = 1
        for i in search.results[:3]:
            if not i["backdrop_path"] == None:
                url = "https://image.tmdb.org/t/p/original"+i["poster_path"]
                overview = i["overview"]
                release_date = i["release_date"]
                original_title = i["original_title"]
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="**Overview**\n"+overview+"\n**Released Date**\n"+release_date+"\n**Original Title**\n"+original_title+"\n"+url)
              
            # The keyboard list will  insert each  InlineKeyboardButton
            # The appending is working in Option and we assign a local variable already for the count and it will increment and callback_data is the `id` from the TMDB server
            keyboard.append([InlineKeyboardButton("Option "+str(option_count), callback_data=str(i['id'])+"  "+str(i['original_language']))])
            # It will increment the counter number for callback_data
            option_count += 1
        # We need the this button last of the all the buttons so we appeded this here
        keyboard.append([InlineKeyboardButton("None of the above", callback_data="None")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose your option:", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="No movie found with "+result_string)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config('TELEGRAM_TOKEN')).read_timeout(30).write_timeout(30).build()
    start_handler = CommandHandler('start', start)
    add_movie_handler = CommandHandler('add_movie', add_movie)


    application.add_handler(start_handler)
    application.add_handler(add_movie_handler)
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)