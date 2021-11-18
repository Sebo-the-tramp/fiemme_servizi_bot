import json
import os

import utils.db_utils as db

import logging, datetime, sqlite3, configparser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, Update, Bot
from telegram.ext import CallbackQueryHandler, Updater, CommandHandler, CallbackContext, Dispatcher

import telegram

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

def start(update: Update, context: CallbackContext) -> None:    
    update.message.reply_text('Benvenuto! Usa il comando /set per impostare il comune dove effettuare il promemoria')

    
def stop_notification(update: Update, context: CallbackContext):    
    chat_id = update.message.chat_id    
    remove_user(chat_id)    
    update.message.reply_text('Ok da adesso non riceverai più notifiche, a presto!')
    
def remove_user(chat_id):
    con = sqlite3.connect('bot.db')
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
    
    db.modify_user(chat_id, query.data)
            
    context_obj = {
        "chat_id": str(chat_id),
        "comune": str(query.data)
    }           
    
    #insert_user_into_db(chat_id, query.data)   

    query.edit_message_text(text=f"Comune selezionato: {COMUNI[int(query.data)]}🏘\n\nOgni giorno alle 20 ti verrà inviato un promemoria🥳\nControlla di avere le notifiche attive!🙈")
    
def insert_user_into_db(chat_id, comune):
    con = sqlite3.connect('bot.db')
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


def lambda_handler(event, context):
    
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    bot = telegram.Bot(TOKEN)

    dispatcher = Dispatcher(bot, None, use_context=True)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_reminder))
    dispatcher.add_handler(CommandHandler("stop", stop_notification))
    dispatcher.add_handler(CallbackQueryHandler(response))
    
    try:
        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), bot)
        )

    except Exception as e:
        print(e)
        return {"statusCode": 500}

    return {"statusCode": 200}