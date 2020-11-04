import telebot
import os
import subprocess
from telebot import types
capfile = False
directory = 'E:/1'
target = ''
bot = telebot.TeleBot('1063868677:AAGfaq8tqOG4Z_kAiAhS3WNviczNBJG02dY')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Цель установлена")
        target = message.text
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого знака зодиака
    key_oven = types.InlineKeyboardButton(text='передать .cap', callback_data='capfile')
    keyboard.add(key_oven)
    key_oven = types.InlineKeyboardButton(text='список файлов', callback_data='filelist')
    keyboard.add(key_oven)
    key_oven = types.InlineKeyboardButton(text='анализ файла', callback_data='filecrack')
    keyboard.add(key_oven)
    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text='Меню обработки', reply_markup=keyboard)
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
  # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "capfile": 
        bot.send_message(call.message.chat.id, 'ожидаю файл')
        capfile = True
    if call.data == "filelist":
        msg = ''
        files = os.listdir(directory)
        for i in files:
            msg = msg + '\n' + i
        bot.send_message(call.message.chat.id, msg)
    if call.data == "filecrack":
        args = ['C:/Users/User/Desktop/hashcat-6.1.1/hashcat.exe','-t','32', '--quiet', '--status', '-a', '7', 'example0.hash', '?a?a?a?a', 'example.dict']
        child = subprocess.Popen(args, cwd='C:/Users/User/Desktop/hashcat-6.1.1', stdout=subprocess.PIPE, encoding='utf8')
        data = child.communicate()
        
            #for line in data:
            #bot.send_message(call.message.chat.id, line)
            #print(line)
        while child.poll() is None:
            print (data)
        
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        #chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'E:/1/' + message.document.file_name 
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)
bot.polling(none_stop=True, interval=0)