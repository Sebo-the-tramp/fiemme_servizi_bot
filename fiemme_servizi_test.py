#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, datetime, sqlite3, csv, configparser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import CallbackQueryHandler, Updater, CommandHandler, CallbackContext, JobQueue

from datetime import time
from pytz import timezone

parser = configparser.ConfigParser()
parser.read("config/.config")

TOKEN = str(parser.get("config", "TOKEN_TEST"))

test = datetime.datetime.now() + datetime.timedelta(seconds=2)

_hour = int(test.strftime("%H"))
_minute = int(test.strftime("%M"))
_seconds = int(test.strftime("%S"))
print(_seconds)

TIME = datetime.time(hour=_hour, minute=_minute, second=_seconds, tzinfo=timezone('Europe/Rome'))

KEYBOARD = [
        [InlineKeyboardButton("Carano", callback_data='0')],
        [InlineKeyboardButton("Capriana", callback_data='1')],
        [InlineKeyboardButton("Castello Molina di Fiemme", callback_data='2')],
        [InlineKeyboardButton("Cavalese", callback_data='3')],
        [InlineKeyboardButton("Daiano", callback_data='4')],
        [InlineKeyboardButton("Panchià", callback_data='5')],
        [InlineKeyboardButton("Tesero", callback_data='6')],
        [InlineKeyboardButton("Predazzo", callback_data='7')],
        [InlineKeyboardButton("Valfloriana", callback_data='8')],
        [InlineKeyboardButton("Varena", callback_data='9')],
        [InlineKeyboardButton("Ziano di Fiemme", callback_data='10')],
    ]

COMUNI = [
    "Carano",
    "Capriana",
    "Castello Molina di Fiemme",
    "Cavalese",
    "Daiano",
    "Panchià",
    "Tesero",
    "Predazzo",
    "Valfloriana",
    "Varena",
    "Ziano di Fiemme"
]

# If 0 -> prima e la terza settimana (dati dai vari calendari)
# Else 1 -> Seconda e quarta settimana

VETRO = {
    "0": 1,
    "1": 0,
    "2": 0,
    "3": 1,
    "4": 1,
    "5": 1,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 1,
    "10": 1
}

MONDIZIE = {
    "0": ["","","UMIDO,CARTA,PLASTICA","","","SECCO,UMIDO,VETRO",""],
    "1": ["","CARTA","UMIDO","VETRO","SECCO,PLASTICA","UMIDO",""],
    "2": ["","UMIDO,VETRO","","SECCO,CARTA","UMIDO,PLASTICA","",""],
    "3": ["UMIDO,PLASTICA","","SECCO","UMIDO,CARTA","VETRO","",""],
    "4": ["","","UMIDO,CARTA,PLASTICA","VETRO","","SECCO,UMIDO",""],
    "5": ["","UMIDO,CARTA,VETRO","","PLASTICA","SECCO,UMIDO","",""],
    "6": ["","UMIDO","","","UMIDO,CARTA","SECCO,VETRO,PLASTICA",""],
    "7": ["SECCO,CARTA","UMIDO,PLASTICA","","","UMIDO,VETRO","",""],
    "8": ["","CARTA","UMIDO","VETRO","SECCO,PLASTICA","UMIDO",""],
    "9": ["","","UMIDO,CARTA,PLASTICA","VETRO","","SECCO,UMIDO",""],
    "10":["UMIDO","CARTA,VETRO","","UMIDO,PLASTICA","SECCO","",""],
}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def start(update: Update, context: CallbackContext) -> None:    
    update.message.reply_text('Benvenuto! Usa il comando /set per impostare il comune dove effettuare il promemoria')

def send_reminder(context: CallbackContext) -> None:
    """Send the alarm message."""    
    job = context.job
    chat_id = job.context["chat_id"]
    comune = job.context["comune"]    
    message_to_send = get_text(comune)    
    if(message_to_send):    
        context.bot.send_message(chat_id, text=message_to_send, parse_mode=ParseMode.MARKDOWN)        
    else:
        print("nothing")

def get_text(comune):
    text = "" 
            
    tomorrow = datetime.datetime.now() - datetime.timedelta(days=3)        
    day_of_week = tomorrow.weekday()
    print("week_day", day_of_week)
    
    list_mondizie = MONDIZIE[comune][day_of_week]
    print(list_mondizie)
    
    # if mondizie presenti
    if(list_mondizie):
        if("VETRO" in list_mondizie):            
            day_month = int(tomorrow.strftime("%d"))
            # get the number of the week and check if the modulo 2 is odd or even and assert it with the
            # same data in VETRO data structure
            is_not_vetro_week = not ((day_month-1)//7+1)%2 != VETRO[comune]
            if(is_not_vetro_week):
                list_mondizie = list_mondizie.replace("VETRO","")

        text += "🔔 Promemoria! 🔔\n\n"
        text += "Domani mattina nel comune di *" + str(COMUNI[int(comune)]) + "* verrà effettuata la raccolta dei seguenti rifiuti:\n\n"        
        
        for mondizie in list_mondizie.split(","):
            text += "- " + mondizie + "\n"
            
    return text
    
def stop_notification(update: Update, context: CallbackContext):    
    chat_id = update.message.chat_id
    remove_job_if_exists(str(chat_id), context)
    remove_user(chat_id)    
    update.message.reply_text('Ok da adesso non riceverai più notifiche, a presto!')
    
def remove_user(chat_id):
    con = sqlite3.connect('bot_test.db')
    cur = con.cursor()    
    cur.execute("DELETE FROM users WHERE chat_id = " + str(chat_id))        
    con.commit()
    con.close()
        
def set_reminder(update: Update, context: CallbackContext) -> None:   
    reply_markup = InlineKeyboardMarkup(KEYBOARD)
    update.message.reply_text('Perfavore seleziona il tuo comune:', reply_markup=reply_markup)         

def response(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query    
    chat_id = update.callback_query.message.chat_id
    query.answer()        
            
    context_obj = {
        "chat_id": str(chat_id),
        "comune": str(query.data)
    }           
    
    insert_user_into_db(chat_id, query.data)
    
    job_removed = remove_job_if_exists(str(chat_id), context)
    
    print("test", update.callback_query.from_user.first_name)
    
    if job_removed:            
        context.job_queue.run_daily(send_reminder, TIME, days=[0,1,2,3,4,5,6], context=context_obj, name=str(chat_id))

    query.edit_message_text(text=f"Comune Selezionato: {COMUNI[int(query.data)]}🏘\n\nOgni giorno alle 20 ti verrà inviato un promemoria🥳\nControlla di avere le notifiche attive!🙈")
    
def insert_user_into_db(chat_id, comune):
    con = sqlite3.connect('bot_test.db')
    cur = con.cursor()
      
    cur.execute("SELECT * FROM users WHERE chat_id = " + str(chat_id))    
    res = cur.fetchone()
    
    # If the user does not exist
    if(res is None):
        cur.execute("INSERT INTO users VALUES(" + str(chat_id) + "," + str(comune) + ")")    
    # If the choice is the same
    elif(int(res[1]) == int(comune)):
        pass
    else:
        cur.execute("UPDATE users SET comune = " + str(comune) + " WHERE chat_id = " + str(chat_id))

    con.commit()
    con.close()

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def read_saved_users(job_queue):    
    con = sqlite3.connect('bot_test.db')
    cur = con.cursor()
        
    cur.execute('''CREATE TABLE IF NOT EXISTS users (chat_id integer primary key, comune text)''')    
    con.commit()
    
    for row in con.execute("select * from users"):        
        create_job_and_add_to_schedule(row[0], row[1], job_queue)
    
    con.close()
    
def create_job_and_add_to_schedule(chat_id, comune, job_queue):
    
    context_obj = {
        "chat_id": str(chat_id),
        "comune": str(comune)
    }       
        
    job_queue.run_daily(callback=send_reminder, time=TIME, days=[0,1,2,3,4,5,6], context=context_obj, name=str(chat_id))


def main() -> None:
    
    """Run bot."""        
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    """Read previous data"""
    read_saved_users(updater.job_queue)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_reminder))
    dispatcher.add_handler(CommandHandler("stop", stop_notification))
    dispatcher.add_handler(CallbackQueryHandler(response))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
