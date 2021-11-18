import datetime
import os

from telegram import ParseMode
import telegram
import utils.db_utils as db

TOKEN = os.getenv('TELEGRAM_TOKEN')

DATA = {
    "0": {
        "nome": "Carano",
        "vetro": 1,
        "mondizie": ["", "", "UMIDO,CARTA,PLASTICA", "", "", "SECCO,UMIDO,VETRO", ""],
    },
    "1": {
        "nome": "Capriana",
        "vetro": 0,
        "mondizie": ["", "CARTA", "UMIDO", "VETRO", "SECCO,PLASTICA", "UMIDO", ""],
    },
    "2": {
        "nome": "Castello Molina di Fiemme",
        "vetro": 1,
        "mondizie": ["", "UMIDO,VETRO", "", "SECCO,CARTA", "UMIDO,PLASTICA", "", ""],
    },
    "3": {
        "nome": "Cavalese",
        "vetro": 1,
        "mondizie": ["UMIDO,PLASTICA", "", "SECCO", "UMIDO,CARTA", "VETRO", "", ""],
    },
    "4": {
        "nome": "Daiano",
        "vetro": 1,
        "mondizie": ["", "", "UMIDO,CARTA,PLASTICA", "VETRO", "", "SECCO,UMIDO", ""],
    },
    "5": {
        "nome": "Panchià",
        "vetro": 1,
        "mondizie": ["", "UMIDO,CARTA,VETRO", "", "PLASTICA", "SECCO,UMIDO", "", ""],
    },
    "6": {
        "nome": "Tesero",
        "vetro": 0,
        "mondizie": ["", "UMIDO", "", "", "UMIDO,CARTA", "SECCO,VETRO,PLASTICA", ""],
    },
    "7": {
        "nome": "Predazzo",
        "vetro": 0,
        "mondizie": ["SECCO,CARTA", "UMIDO,PLASTICA", "", "", "UMIDO,VETRO", "", ""],
    },
    "8": {
        "nome": "Valfloriana",
        "vetro": 0,
        "mondizie": ["", "CARTA", "UMIDO", "VETRO", "SECCO,PLASTICA", "UMIDO", ""],
    },
    "9": {
        "nome": "Varena",
        "vetro": 1,
        "mondizie": ["", "", "UMIDO,CARTA,PLASTICA", "VETRO", "", "SECCO,UMIDO", ""],
    },
    "10": {
        "nome": "Ziano diFiemme",
        "vetro": 1,
        "mondizie": ["UMIDO", "CARTA,VETRO", "", "UMIDO,PLASTICA", "SECCO", "", ""],
    },
}


def send_reminder() -> None:
    """Send the alarm message."""

    bot = telegram.Bot(TOKEN)
    users = db.read_all_users()

    # format of the data
    # [{'comune': {'N': '2'}, 'chat_id': {'N': '777722458'}}, {'comune': {'N': '2'}, 'chat_id': {'N': '123456789'}}]

    for user in users:
        send_message(user["chat_id"]["N"], user["comune"]["N"], bot)


def send_message(chat_id, comune, bot):

    message_to_send = get_text(comune)

    if(message_to_send):
        bot.send_message(chat_id, text=message_to_send,
                         parse_mode=ParseMode.MARKDOWN)

def get_text(comune):
    text = ""

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    day_of_week = tomorrow.weekday()

    list_mondizie = DATA[comune]["mondizie"][day_of_week]

    # if mondizie presenti
    if(list_mondizie):
        if("VETRO" in list_mondizie):
            day_month = int(tomorrow.strftime("%d"))
            # get the number of the week and check if the modulo 2 is odd or even and assert it with the
            # same data in VETRO data structure
            is_not_VETRO_week = not (
                (day_month-1)//7+1) % 2 != DATA[str(comune)]["vetro"]
            if(is_not_VETRO_week):
                list_mondizie = list_mondizie.replace(",VETRO", "")
                list_mondizie = list_mondizie.replace("VETRO", "")

        text += "🔔 Promemoria! 🔔\n\n"
        text += "Domani mattina nel comune di *" + \
            str(DATA[comune]["nome"]) + \
            "* verrà effettuata la raccolta dei seguenti rifiuti:\n\n"

        for mondizie in list_mondizie.split(","):
            text += "- " + mondizie + "\n"

    return text

def lambda_handler(event, context):
    send_reminder()
