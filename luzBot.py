import configparser

# from matplotlib.pyplot import text
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import (
    InlineKeyboardButton,
    BotCommandScopeChat,
    BotCommandScopeChatAdministrators,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
    Update
)
import logging
'''from auxiliar import (
    enviar,
    build_command_list
)'''
import datetime
import json
import os
import time
from crontab import CronTab
from crearImaxe import createImage


# Set up the logging
logging.basicConfig(filename='log.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')


config = configparser.ConfigParser()
config.read('config.ini')


updater = Updater(config['CONFIG']['TOKEN'], use_context=True)

# Revisar esta función, xa que non deberia facer falta crear a foto


def preciosHoxe(update: Update, context: CallbackContext):
    day = -1
    try:
        modTimesinceEpoc = os.path.getmtime(config['IMAGES']['TODAY'])
        day = time.strftime('%d', time.localtime(modTimesinceEpoc))
    except FileNotFoundError:
        createImage(config['IMAGES']['TODAY'])

        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(config['IMAGES']['TODAY'], 'rb'),
                               caption="Precios Hoxe:")
        return
    today = datetime.datetime.now()
    if int(today.day) != int(day):
        createImage(config['IMAGES']['TODAY'])

    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open(config['IMAGES']['TODAY'], 'rb'),
                           caption="Precios Hoxe:")


def preciosManha(update: Update, context: CallbackContext):
    ''


def start(update: Update, context: CallbackContext):
    logging.info(
        f'User ({update.message.chat.username}) with ID: ({str(update.message.chat.id)}) entered the bot')
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
                /help to see the commands available.")
    if update.message.chat.id != int(config['ADMINS']['admin']):
        update.bot.send_message(chat_id=config['ADMINS']['admin'], text="Novo usuario conectado ao bot!!\n  ID: " +
                                update.message.chat.id + "\n  Username: " + update.message.chat.username)


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Avaliable Commands :-
        /help - Mostrar a lista de comandos dispoñibles
        /info - Mostrar resumo de dispositivos conectados
        """)


def unknown(update: Update, context: CallbackContext):

    logging.info(
        f'User ({update.message.chat.id}) says: {str(update.message.text).lower()}')

    # update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s' verificacion" % update.message.text)


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


def crearDispatchers():
    # Comandos
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('hoxe', preciosHoxe))
    # Así funciona para todos os chats:
    '''updater.bot.set_my_commands(
        build_command_list(),
        scope=BotCommandScopeAllPrivateChats()
    )
    updater.bot.set_my_commands(
        build_command_list(admins=True),
        scope=BotCommandScopeChat(config['ADMINS'].getint('admin'))
    )'''

    # Mirar se é o tipo apropiado xa que creo que non, deberia ser un comando, non?
    updater.dispatcher.add_handler(CallbackQueryHandler(help, pattern='help'))

    # Mensaxes
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))

    # Comando irrecoñecible # Filters out unknown commands
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Erros
    updater.dispatcher.add_error_handler(error)


def iniciar():
    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()


def eliminarTraballos():
    cron = CronTab(user=True)
    cron.remove_all()
    cron.write()


def actualizarImaxes():
    # user=True denotes the current user
    cron = CronTab(user=True)
    job = cron.new(
        command='/usr/bin/python3 /mnt/c/Users/danim/MEGA/Varios/pyhton/luzBot/today.py')
    job.setall("00 00 * * *")
    job = cron.new(
        command='/usr/bin/python3 /mnt/c/Users/danim/MEGA/Varios/pyhton/luzBot/tomorrow.py')
    #job.setall("18 20 * * *")
    job.setall("54 13 * * *")

    if cron[0].is_valid() and cron[1].is_valid():  # If syntax is valid, write to crontab
        print(cron[0].is_enabled(), cron[1].is_enabled())
        cron.write()
    else:
        print("Houbo un erro!")


crearDispatchers()
iniciar()
eliminarTraballos()
actualizarImaxes()
updater.bot.send_message(
    chat_id=config['ADMINS']['admin'], text='Tamoh ready!')
