#============IMPORT LIBLARIEYS
from telebot import TeleBot, types
from telebot.types import Update
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import uuid
from flask import Flask, request
#============IMPORT FROM FILES
from config import bot_token, admin
from keyboards import *
from db import init_db, add_1_count_url, add_user, get_count_url, get_count_money, get_all, update_money_plus, update_money_minus, get_count_all_money,update_all_money_plus
import parser_t
from parser_t import id_out
# open Chrome
try:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    dr = webdriver.Chrome(options=options)
except:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    dr = webdriver.Firefox(options = options)

# main bot
b = TeleBot(bot_token)

# db
init_db()

links_out = []

##########===WITHDRAW LIST===######################
temp_with_id = []
temp_wit = {'id':'','name':'','rekv':'','sum':'','urls_rented':''}
class Withdraw:
    list = []

#############===WAITING LIST===####################
list_id = []
temp = {'id':'','name':'','exp':'','from':'','time':''}
class Waiting:
    list = []
def add_to_waiting(id,username,experience,from_,time):
    Waiting.list.append({'id': id,
                        'name': username,
                        'exp': experience,
                        'from': from_,
                        'time': time
                         })
#####################################################

###########==CONDITION OF RENTING==##################
class Rules:
    domen = ['staemcammunily.ru']
    min_videos = 15
    min_watches = 4
    min_total_watch = 1500
    sum = 40
    name = 'Misha'
    all = 100188628
#####################################################

def run_bot():
    try:
        b.remove_webhook()
        print("bot started")
        b.polling(none_stop=True, interval=10)

    except Exception as err:
        print("run bot error:", err)


@b.message_handler(content_types=['text'])
def get_text_msg(message):
    print(50*'*')
    print(message.from_user.id)
    print('Message: '+ message.text)
    print(50 * '*')
    if (message.text.__contains__("start")) and (message.chat.type == 'private') and (message.from_user.id not in admin) and message.from_user.id not in list_id:
        if get_all(message.from_user.id):
            b.send_message(message.from_user.id, 'Вы уже запускали бота, нажимайте на кнопки ;)', reply_markup=main_user())
        else:
            #add_to_waiting(1256629898, 'name', 'exp', 'from', 'time')
            m = b.send_message(message.chat.id, '😎Для начала работы заполните анкету. Был ли опыт в спаме ТТ?')
            b.register_next_step_handler(m, get_exp)

    if (message.text == "Заявки на вступления"):
        for i in Waiting.list:
            b.send_message(message.chat.id, f'ID пользователя: {i["id"]} '+'\n'+f'Ник: {i["name"]} '+'\n'+f'Опыт работы: {i["exp"]} '+'\n'+f'Кто пригласил: {i["from"]} '+'\n'+f'Сколько времени готов уделять: {i["time"]}', reply_markup=act_apply(i["id"]))
    if message.text == "Заявки на вывод":
        for i in Withdraw.list:
            b.send_message(message.chat.id, f'ID пользователя: {i["id"]} ' + '\n' + f'Ник: {i["name"]} ' + '\n' + f'Реквизиты: {i["rekv"]}' + '\n' + f'Сумма вывода: {i["sum"]}' + '\n' + f'Всего добавленно ссылок: {i["urls_rented"]}', reply_markup=act_withdraw(i["id"]))
    if message.text == Rules.name:
        add_user(message.from_user.id)
        admin.append(message.from_user.id)
    if message.text == "Сменить условия":
        b.send_message(message.from_user.id, 'Сейчас:'+'\n'+f'Домены: {" ".join(Rules.domen)}'+'\n'+f'Мин. к-во видео: {Rules.min_videos}'+'\n'+ f'Мин. к-во просмотром на видео: {Rules.min_watches}'+'\n'+f'Загальное к-во просмотров: {Rules.min_total_watch}'+'\n'+f'Выплата за 1 акк: {Rules.sum}'+'\n'+'Что именно сменнить?', reply_markup=condition())
    if '/admin'== message.text and message.from_user.id in admin:
        b.send_message(message.chat.id,'Приветствую, Босс! Что делаем?',reply_markup=main_admin())
    if 'Добавить ссылку' in message.text:
        m = b.send_message(message.chat.id, 'Отправьте ссылку ТТ в любом формате:')
        b.register_next_step_handler(m, add_url)
    if 'Профиль' in message.text:
        if message.from_user.username:
            b.send_message(message.chat.id, f'⚙ Логин Telegram: {message.from_user.username}'+'\n'+
                                            f'🆔 Telegram ID: {message.from_user.id}'+'\n'+
                                            f'💵 Текущая ставка: {Rules.sum} руб за аккаунт'+'\n'+
                                            f'🧨 Проверено ссылок: {get_count_url(message.from_user.id)[0]}'+'\n'+
                                            f'💰 Сумма выплат проекта: {Rules.all} руб.'+'\n'+
                                            f'💸 Вы заработали: {get_count_all_money(message.from_user.id)[0]}' + '\n' +
                                            f'🤑 Доступно к выводу: {get_count_money(message.from_user.id)[0]} руб.' + '\n', reply_markup=main_user())
        else:
            b.send_message(message.chat.id, f'⚙ Логин Telegram: {message.from_user.first_name}' + '\n' +
                                            f'🆔 Telegram ID: {message.from_user.id}' + '\n' +
                                            f'💵 Текущая ставка: {Rules.sum} руб за аккаунт' + '\n' +
                                            f'🧨 Проверено ссылок: {get_count_url(message.from_user.id)[0]}' + '\n' +
                                            f'💰 Сумма выплат проекта: {Rules.all} руб.'+'\n'+
                                            f'💸 Вы заработали: {get_count_all_money(message.from_user.id)[0]}' + '\n' +
                                            f'🤑 Доступно к выводу: {get_count_money(message.from_user.id)[0]} руб.' + '\n', reply_markup=main_user())
        print(get_all(message.chat.id))
    if 'Вывод средств' in message.text:
        b.send_message(message.chat.id, f'Ваш баланс: {get_count_money(message.from_user.id)[0]}', reply_markup=wallet())
    if message.text == '+m' and message.from_user.id in admin:
        update_money_plus(message.from_user.id, int(Rules.sum))
    if message.text == '+s' and message.from_user.id in admin:
        add_1_count_url(message.from_user.id)
    if 'Проверка ссылки' in message.text:
        m = b.send_message(message.chat.id, 'Отправьте ссылку ТТ в любом формате:')
        b.register_next_step_handler(m, get_test)
    if 'Помощь' in message.text:
        b.send_message(message.chat.id, "Статьи:" + '\n' + '\n'+"<a href='https://lolz.guru/threads/2050246/'>📑Тема для отзывов</a>"+'\n'+'\n'+f"""<a href='https://telegra.ph/Pravila-raboty-01-03'>🛠Правила работы</a>"""+'\n'+'\n'+f"""<a href='https://t.me/spamtiktokcash'>💳Канал выплат</a>"""+'\n'+'\n'+f"""<a href='https://telegra.ph/Vsem-privet-segodnya-ya-rasskazhu-kak-spamit-v-Tiktok-12-06'>❗Мануал</a>""", parse_mode="HTML", reply_markup=main_user())


def get_test(message):
    b.send_message(message.chat.id, '⚙Проверка ссылки..⚙')
    res = parser_t.parser_test(message.text, Rules.domen, int(Rules.min_videos), int(Rules.min_watches), int(Rules.min_total_watch))
    b.send_message(message.chat.id, res, reply_markup=main_user())

@b.callback_query_handler(func=lambda call: True)
def get_call(call):
    print(call.data)
    if 'rem' in call.data:
        id = call.data.split('_')
        id = id[-1]
        for i in Waiting.list:
            if i["id"] == int(id):
                Waiting.list.remove(i)
                b.delete_message(call.from_user.id, call.message.message_id)

    elif 'add' in call.data:
        id = call.data.split('_')
        id = id[-1]
        add_user(int(id))
        b.send_message(int(id), 'Вашу заявку рассмотрели, вы приняты. Ссылка на беседу - https://t.me/joinchat/FM00KjlXvfY256B-', reply_markup=main_user())
        list_id.remove(int(id))
        add_user(int(id))
        for i in Waiting.list:
            if i["id"] == int(id):
                Waiting.list.remove(i)
                b.delete_message(call.from_user.id, call.message.message_id)

    elif 'payed' in call.data:
        id = call.data.split('_')
        id = id[-1]
        for i in Withdraw.list:
            if i["id"] == int(id):
                Withdraw.list.remove(i)
                b.delete_message(call.from_user.id, call.message.message_id)
                Rules.all += int(i["sum"])
        b.send_message(int(id), '🎉Поздравляем, средства перечислены на ваш кошелек🎉',
                       reply_markup=main_user())
    elif 'back' == call.data:
        b.delete_message(call.from_user.id, call.message.message_id)
        b.send_message(call.message.chat.id, 'Главное меню', reply_markup=main_admin())

    elif 'back_u' == call.data:
        b.delete_message(call.from_user.id, call.message.message_id)
        b.send_message(call.message.chat.id, 'Главное меню', reply_markup=main_user())

    elif call.data == 'withdraw':
        if int(get_count_money(call.message.chat.id)[0]) == 0:
            b.send_message(call.message.chat.id, 'Вывод невозможен, так как у вас на счету 0 руб', reply_markup=main_user())
        elif call.message.chat.id in temp_with_id:
            b.send_message(call.message.chat.id,'Вывод невозможен, так как вы уже подавали заявку')
        else:
            m = b.send_message(call.message.chat.id, '💵Укажите сумму для вывода::',reply_markup=back())
            b.register_next_step_handler(m, withdraw_sum)

    elif call.data == 'edit_domen':
        m = b.send_message(call.message.chat.id, 'Уведите нужный домен:', reply_markup=back())
        b.register_next_step_handler(m, edit_domen)

    elif call.data == 'edit_videos':
        m = b.send_message(call.message.chat.id, 'Уведите мин. к-во видео:', reply_markup=back())
        b.register_next_step_handler(m, edit_videos)

    elif call.data == 'edit_watches':
        m = b.send_message(call.message.chat.id, 'Уведите мин. к-во просмотров на видео:', reply_markup=back())
        b.register_next_step_handler(m, edit_watches)

    elif call.data == 'edit_total_watches':
        m = b.send_message(call.message.chat.id, 'Уведите всего просмотров на акаунте:', reply_markup=back())
        b.register_next_step_handler(m, edit_total_watches)

    elif call.data == 'edit_sum':
        m = b.send_message(call.message.chat.id, 'Уведите сумму для выплат:', reply_markup=back())
        b.register_next_step_handler(m, edit_sum)

def edit_sum(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_admin())
        return 'back'
    Rules.sum = int(message.text)
    b.send_message(message.from_user.id, 'Успешно изменено', reply_markup=main_admin())

def edit_total_watches(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_admin())
        return 'back'
    Rules.min_total_watch = int(message.text)
    b.send_message(message.from_user.id, 'Успешно изменено', reply_markup=main_admin())

def edit_watches(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_admin())
        return 'back'
    Rules.min_watches = int(message.text)
    b.send_message(message.from_user.id, 'Успешно изменено', reply_markup=main_admin())

def edit_videos(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_admin())
        return 'back'
    Rules.min_videos = int(message.text)
    b.send_message(message.from_user.id, 'Успешно изменено', reply_markup=main_admin())

def edit_domen(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_admin())
        return 'back'
    Rules.domen.append(message.text)
    b.send_message(message.from_user.id, 'Успешно изменено', reply_markup=main_admin())

def get_exp(message):
    temp['id'] = message.from_user.id
    temp['name']= message.from_user.first_name
    temp['exp'] = message.text
    m = b.send_message(message.chat.id,
                       'Укажите ссылку на профиль lolzteam🤓')
    b.register_next_step_handler(m, get_from)
def get_from(message):
    temp['from'] = message.text
    m = b.send_message(message.chat.id,
                       '💻Сколько готовы уделять времени?')
    b.register_next_step_handler(m, get_time)
def get_time(message):
    temp['time'] = message.text
    b.send_message(message.chat.id,
                   '🎉Заявка подана! Ожидайте, наш менеджер скоро проверит заявку.🎉')
    list_id.append(message.from_user.id)
    add_to_waiting(temp['id'],temp['name'],temp['exp'],temp['from'],temp['time'])
    print('Пользователь добавлен в комнату ожидание: '+str(temp['id']),temp['name'],temp['exp'],temp['from'],temp['time'])


def add_url(message):
    b.send_message(message.chat.id, '⚙Проверка ссылки..⚙')
    if message.text in links_out:
        b.send_message(message.chat.id, '⛔Акаунт уже был здан⛔', reply_markup=main_user())
        return 'pass'
    res = parser_t.parser(message.text, Rules.domen, int(Rules.min_videos), int(Rules.min_watches), int(Rules.min_total_watch))
    if res == '✅Ссылка успешно добавлена✅':
        b.send_message(message.chat.id, res, reply_markup=main_user())
        add_1_count_url(message.from_user.id)
        update_money_plus(message.from_user.id, int(Rules.sum))
        update_all_money_plus(message.from_user.id, int(Rules.sum))
    else:
        b.send_message(message.chat.id, '⛔Ссылка не подходит. Для уточнения обратиться к администрации⛔', reply_markup=main_user())

def withdraw_sum(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_user())
        return 'back'
    if int(message.text) > int(get_count_money(message.from_user.id)[0]):
        b.send_message(message.from_user.id, 'Недостаточно средств в кошельке', reply_markup=main_user())
        return 'Denied'
    m = b.send_message(message.from_user.id,'💳Напишите реквизиты(Qiwi или Яндекс. Деньги)', reply_markup=back())
    b.register_next_step_handler(m, withdraw_rekv)
    temp_wit["id"] = message.from_user.id
    if message.from_user.username:
        temp_wit["name"] = message.from_user.username
    else:
        temp_wit["name"] = message.from_user.first_name
    temp_wit["sum"] = message.text
    temp_wit['urls_rented'] = get_count_url(message.from_user.id)[0]

def withdraw_rekv(message):
    if message.text == 'Назад':
        b.send_message(message.from_user.id, 'Главное меню', reply_markup=main_user())
        return 'back'
    b.send_message(message.from_user.id, '🎉Заявка подана! Ожидайте, наш менеджер скоро проверит заявку.🎉', reply_markup=main_user())
    temp_wit["rekv"] = message.text
    temp_with_id.append(message.from_user.id)
    Withdraw.list.append(temp_wit)
    update_money_minus(message.from_user.id, int(temp_wit["sum"]))

