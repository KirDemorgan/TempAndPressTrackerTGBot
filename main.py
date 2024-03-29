#                      _           _               ______
#                     | |         | |              |  _  \
#  _ __ ___   __ _  __| | ___     | |__  _   _     | | | |___ _ __ ___   ___  _ __ __ _  __ _ _ __
# | '_ ` _ \ / _` |/ _` |/ _ \    | '_ \| | | |    | | | / _ \ '_ ` _ \ / _ \| '__/ _` |/ _` | '_ \
# | | | | | | (_| | (_| |  __/    | |_) | |_| |    | |/ /  __/ | | | | | (_) | | | (_| | (_| | | | |
# |_| |_| |_|\__,_|\__,_|\___|    |_.__/ \__, |    |___/ \___|_| |_| |_|\___/|_|  \__, |\__,_|_| |_|
#                                        __/ |                                    __/ |
#                                       |___/                                    |___/

import sqlite3
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bottoken import TOKEN
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
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
                          pressure TEXT,
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
        'Привет! Бот создан для отвлеживания температуры и давления.')


def add_pressure(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    message_text = update.message.text
    pressureinf = message_text.split(' ', 1)[1]  # get the part of the message after the command
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # get current date and time
    conn_press = create_connection_pressure()
    cur = conn_press.cursor()
    cur.execute("INSERT INTO pressure (user_id, pressure, date_time) VALUES (?, ?, ?)", (user_id, pressureinf, date_time))
    conn_press.commit()
    conn_press.close()
    update.message.reply_text(f'Давление добавлено в базу данных')

def add_temp(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    message_text = update.message.text
    tempinf = message_text.split(' ', 1)[1]  # get the part of the message after the command
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # get current date and time
    conn_press = create_connection_pressure()
    cur = conn_press.cursor()
    cur.execute("INSERT INTO temperatures (user_id, temperature, date_time)  VALUES (?, ?, ?)", (user_id, tempinf, date_time))
    conn_press.commit()
    conn_press.close()
    update.message.reply_text(f'Температура добавлено в базу данных')


def print_pressure(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    conn_press = create_connection_pressure()
    cur = conn_press.cursor()
    cur.execute("SELECT pressure, date_time FROM pressure WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            update.message.reply_text(f'Давление: {row[0]} Дата: {row[1]}')
    else:
        update.message.reply_text('Нет записей о давлении для этого пользователя.')
    conn_press.close()


def print_temp(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    conn_temp = create_connection_temperature()
    cur = conn_temp.cursor()
    cur.execute("SELECT temperature, date_time FROM temperatures WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            update.message.reply_text(f'Температура: {row[0]} Дата: {row[1]}')
    else:
        update.message.reply_text('Нет записей о температуре для этого пользователя.')
    conn_temp.close()


def ask_for_confirmation(update: Update, context: CallbackContext, delete_type: str) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Подтвердить", callback_data=f'confirm_{delete_type}'),
            InlineKeyboardButton("Отменить", callback_data='cancel')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Вы уверены, что хотите удалить?', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'confirm_pressure':
        delete_pressure(update, context)
        query.edit_message_text(text="Давление удалено")
    elif query.data == 'confirm_temp':
        delete_temp(update, context)
        query.edit_message_text(text="Температура удалена")
    else:
        query.edit_message_text(text="Удаление отменено")


def delete_pressure(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    conn_press = create_connection_pressure()
    cur = conn_press.cursor()
    cur.execute("DELETE FROM pressure WHERE user_id=?", (user_id,))
    conn_press.commit()
    conn_press.close()
    update.callback_query.message.reply_text(f'Давление удалено из базы данных')


def delete_temp(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    conn_temp = create_connection_temperature()
    cur = conn_temp.cursor()
    cur.execute("DELETE FROM temperatures WHERE user_id=?", (user_id,))
    conn_temp.commit()
    conn_temp.close()
    update.callback_query.message.reply_text(f'Температура удалена из базы данных')


def main() -> None:
    conn_press = create_connection_pressure()
    create_table_pressure(conn_press)
    conn_temp = create_connection_temperature()
    create_table_temp(conn_temp)

    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    print("Bot active")

    dispatcher.add_handler(
        CommandHandler("deletePressure", lambda update, context: ask_for_confirmation(update, context, 'pressure')))
    dispatcher.add_handler(
        CommandHandler("deleteTemp", lambda update, context: ask_for_confirmation(update, context, 'temp')))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("addPressure", add_pressure))
    dispatcher.add_handler(CommandHandler("addTemp", add_temp))
    dispatcher.add_handler(CommandHandler("printPressure", print_pressure))
    dispatcher.add_handler(CommandHandler("printTemp", print_temp))

    updater.start_polling()

    updater.idle()

    conn_temp.close()
    conn_press.close()


if __name__ == '__main__':
    main()