"""Module providingFunction of telegram hash bot"""
import os
import subprocess
import telebot
from telebot import types
# capfile = False
DIRECTORY = 'E:/1'
TARGET = '1.hccapx'
bot = telebot.TeleBot('1063868677:AAGfaq8tqOG4Z_kAiAhS3WNviczNBJG02dY')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Module providingFunction of tbot messaging"""
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет,сегодня.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Цель установлена")
        ttt = open('target.txt', 'w', encoding="utf-8")
        ttt.write(DIRECTORY + '/' + message.text)
        ttt.close()
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого знака зодиака
    key_oven = types.InlineKeyboardButton(text='передать .cap',
                                          callback_data='capfile')
    keyboard.add(key_oven)
    key_oven = types.InlineKeyboardButton(text='список файлов',
                                          callback_data='filelist')
    keyboard.add(key_oven)
    key_oven = types.InlineKeyboardButton(text='анализ файла',
                                          callback_data='filecrack')
    keyboard.add(key_oven)
    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text='Меню обработки:',
                     reply_markup=keyboard)
# Обработчик нажатий на кнопки


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """Module providingFunction of tbot button press"""
    if call.data == "capfile":
        bot.send_message(call.message.chat.id, 'ожидаю файл')
        # capfile = True
    if call.data == "filelist":
        msg = ''
        files = os.listdir(DIRECTORY)
        for i in files:
            msg = msg + '\n' + i
        bot.send_message(call.message.chat.id, msg)
    if call.data == "filecrack":
        ttt = open('target.txt', 'r', encoding="utf-8")
        target = ttt.readline()
        ttt.close()
        args = ['C:/Users/User/Desktop/hashcat-6.1.1/hashcat.exe', '-a', '3',
                '-m', '2500', '--quiet', target, '?d?d?d?d?d?d?d?d']
        child = subprocess.Popen(args, cwd='C:/Users/User/Desktop/hashcat-6.1.1',
                                 stdout=subprocess.PIPE, encoding='utf8')
        data = child.communicate()
        while child.poll() is None:
            for line in data:
                print(line)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    """Module providingFunction of tbot file load"""
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'E:/1/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except OSError as os_error:
        bot.reply_to(message, os_error)


bot.polling(none_stop=True, interval=0)
