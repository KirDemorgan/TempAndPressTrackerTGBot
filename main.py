#                      _           _               ______
#                     | |         | |              |  _  \
#  _ __ ___   __ _  __| | ___     | |__  _   _     | | | |___ _ __ ___   ___  _ __ __ _  __ _ _ __
# | '_ ` _ \ / _` |/ _` |/ _ \    | '_ \| | | |    | | | / _ \ '_ ` _ \ / _ \| '__/ _` |/ _` | '_ \
# | | | | | | (_| | (_| |  __/    | |_) | |_| |    | |/ /  __/ | | | | | (_) | | | (_| | (_| | | | |
# |_| |_| |_|\__,_|\__,_|\___|    |_.__/ \__, |    |___/ \___|_| |_| |_|\___/|_|  \__, |\__,_|_| |_|
#                                        __/ |                                    __/ |
#                                       |___/                                    |___/

import sqlite3
from bottoken import TOKEN
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from sqlite3 import Error


def create_connection_pressure():
    conn = None
    try:
        conn_press = sqlite3.connect('pressure.db')
    except Error as e:
        print(e)

    return conn_press


def create_connection_temperature():
    conn = None
    try:
        conn_temp = sqlite3.connect('temp.db')
    except Error as e:
        print(e)

    return conn_temp


def create_table_pressure(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS pressure
                         (user_id INTEGER,
                          temperature TEXT,
                           date_time TEXT)'''
        conn.execute(sql)
        conn.commit()
    except Error as e:
        print(e)


def create_table_temp(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS temperatures
                         (user_id INTEGER,
                          temperature TEXT,
                           date_time TEXT)'''
        conn.execute(sql)
        conn.commit()
    except Error as e:
        print(e)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Напиши мне любой год в диапозоне от 2000 до 2020, а я расскажу тебе об основных событиях.')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    print("Bot active")

    dispatcher.add_handler(CommandHandler("start", start))


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

conn_press = create_connection_pressure()
create_table_pressure(conn_press)

conn_temp = create_connection_temperature()
create_table_temp(conn_temp)

conn_temp.close()
conn_press.close()