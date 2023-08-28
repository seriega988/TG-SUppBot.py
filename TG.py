import telebot
import sys,os
import smtplib
import time
from charset_normalizer import md__mypyc
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email
import email.mime.application
from telebot import types
global i
######################BOT ID#####################################
bot = telebot.TeleBot('')
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋Здравствуйте. Вас приветствует бот-помощник."
                                           "Здесь вы сможете оставить свою проблему/вопрос и получить обратную связь", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text=="👋 Поздороваться":
        markIN = types.ReplyKeyboardMarkup(resize_keyboard=True)
        INNbtn = types.KeyboardButton("Отправить данные")
        markIN.add(INNbtn)
        bot.send_message(message.from_user.id, "Как к вам обращаться?Введите данные для связи(телефон/почта)", reply_markup=markIN)
        bot.register_next_step_handler(message, checkINN)
def butINN(message):
    if message.text=="Отправить данные":
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Quesbtn = types.KeyboardButton("Отправить запрос")
        mark.add(Quesbtn)
        bot.send_message(message.from_user.id, "Теперь опишите, пожалуйста, ваш вопрос или проблему."
                                               "Также здесь можно указать дополнительные данные, если что-то забыли", reply_markup=mark)
        bot.register_next_step_handler(message, checkQ)
    elif message.text=="/start":
        start(message)
    else:
        bot.send_message(message.from_user.id, "Данные уже в памяти, намжмите кнопку или напишите /start для перезагрузки")
        bot.register_next_step_handler(message, butINN)
def checkQ(message):
    global Question
    if message.text == "Отправить запрос":
        bot.send_message(message.from_user.id, "Fail,go again")
        bot.register_next_step_handler(message, checkQ)
    elif message.text=="/start":
        start(message)
    else:
        bot.send_message(message.from_user.id, "Ваш запрос принят, нажмите кнопку 'Отправить запрос' или напишите /start для перезагрузки")
        Question = message.text
        print(Question)
        i=IDe
        bot.register_next_step_handler(message, priznak)
def priznak(message):
    PrBtn = types.KeyboardButton("Отправить")
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark.add(PrBtn)
    bot.send_message(message.from_user.id, "Напоследок введите пожалуйтса ИНН организации, или признак(физлицо/ИП)"
                                         , reply_markup=mark)
    bot.register_next_step_handler(message, Prcheck)
def Prcheck(message):
    global Priznak
    if message.text=="Отправить":
        bot.send_message(message.from_user.id, "Данные не введены")
        bot.register_next_step_handler(message,Prcheck)
    elif message.text=="/start":
        start(message)
    else:
        Priznak = message.text
        bot.send_message(message.from_user.id, "Данные приняты, нажмите 'Отправить' или напишите /start для перезагрузки")
        bot.register_next_step_handler(message, End)
def End(message):
    if message.text=="Отправить":
        EndBtn = types.KeyboardButton("Повторить запрос")
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(EndBtn)
        with open(f"Заявка-{Priznak}.txt","w") as file:
            file.write(f'Данные для связи-{IDe},Запрос клиента-{Question},ИНН/признак организации-{Priznak}')
        send(IDe,Question,Priznak)
        bot.send_message(message.from_user.id, "Ожидайте нашего ответа, для нового запроса нажмите кнопку "
                                               "'Повторить запрос'",reply_markup=mark)
        bot.register_next_step_handler(message, EndMs)
    elif message.text=="/start":
        start(message)
    else:
        bot.send_message(message.from_user.id, "Команда не распознана")
        bot.register_next_step_handler(message, End)
def EndMs(message):
    if message.text == "Повторить запрос" or message.text == "/start":
        start(message)
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Для нового запроса напишите /start или нажмите "
                                               "'Повторить запрос'. Или ожидайте обратной связи")
        bot.register_next_step_handler(message, EndMs)
def checkINN(message):
    global IDe
    print(message.text)
    if message.text == "Отправить данные":
        bot.send_message(message.from_user.id, "Данные не были введены")
        bot.register_next_step_handler(message, checkINN)
    elif message.text=="/start":
        start(message)
    else:
        IDe = message.text
        bot.send_message(message.from_user.id, "Данные приняты, жмите кнопку 'Отправить данные' или напишите /start для перезагрузки")
        bot.register_next_step_handler(message, butINN)
def send(IDe,Question,Priznak):
    ###########################################MAIL#####################################
    EMAIL_ADDRESS = ''
    EMAIL_PASSWORD = ''

    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = 'Сообщение от бота ТГ'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ""

    body = email.mime.text.MIMEText("""Новая заявка!Информация во вложении!!Сообщение отправлено из бота Телеграмм""")
    msg.attach(body)

    filename = f'Заявка-{Priznak}.txt'
    fp = open(filename, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(), _subtype="txt")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)

    smtpObj = smtplib.SMTP('', 587)
    smtpObj.starttls()
    smtpObj.login('', '')
    smtpObj.sendmail('','',msg.as_string())
    smtpObj.quit()


@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    if call.data == "resetData":
        bot.delete_message(call.message.chat.id, call.message.message_id)



if __name__ == '__main__':
    ###########################################MAIL#####################################
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = ''
    msg['From'] = ''
    msg['To'] = ''
    body = email.mime.text.MIMEText(
        """Бот запущен""")
    msg.attach(body)
    smtpObj = smtplib.SMTP('', 587)
    smtpObj.starttls()
    smtpObj.login('', '')
    smtpObj.sendmail('', '', msg.as_string())
    smtpObj.quit()
    while True:
        try:
            bot.polling(none_stop=True)
            ###########################################MAIL#####################################
            msg = email.mime.multipart.MIMEMultipart()
            msg['Subject'] = ''
            msg['From'] = ''
            msg['To'] = ''
            body = email.mime.text.MIMEText(
                """Бот запущен""")
            msg.attach(body)
            smtpObj = smtplib.SMTP('', 587)
            smtpObj.starttls()
            smtpObj.login('', '')
            smtpObj.sendmail('', '', msg.as_string())
            smtpObj.quit()
        except Exception as e:
            ###########################################MAIL#####################################
            msg = email.mime.multipart.MIMEMultipart()
            msg['Subject'] = ''
            msg['From'] = ''
            msg['To'] = ''
            body = email.mime.text.MIMEText(
                """Бот упал""")
            msg.attach(body)
            smtpObj = smtplib.SMTP('', 587)
            smtpObj.starttls()
            smtpObj.login('', '')
            smtpObj.sendmail('', '', msg.as_string())
            smtpObj.quit()
            time.sleep(3)
            print(e)


