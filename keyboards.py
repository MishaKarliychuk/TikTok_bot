from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
# one_time_keyboard=True, resize_keyboard=True

def back():
    key = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key.add(KeyboardButton("Назад"))

def main_admin():
    key = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key.add(KeyboardButton("Заявки на вступления"),
            KeyboardButton("Заявки на вывод"),
            KeyboardButton("Сменить условия"))
    return key

def act_apply(id):
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton("Добавить", callback_data=f"add_{id}"),
            InlineKeyboardButton("Удалить", callback_data=f"rem_{id}"))
    return key

def act_withdraw(id):
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton("Оплачено", callback_data=f"payed_{id}"))
    return key


def main_user():
    key = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key.add(KeyboardButton("🤠Профиль"),
            KeyboardButton("📬Добавить ссылку"),
            KeyboardButton("🔍Проверка ссылки"),
            KeyboardButton("💸Вывод средств"),
            KeyboardButton("🖇Помощь"))
    return key

def wallet():
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton("Вывести", callback_data="withdraw"),
            InlineKeyboardButton("Назад", callback_data="back_u")
            )
    return key

def condition():
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton("Домен", callback_data="edit_domen"),
            InlineKeyboardButton("Мин. к-во видео", callback_data="edit_videos"),
            InlineKeyboardButton("Мин. к-во просмотров на видео", callback_data="edit_watches"),
            InlineKeyboardButton("Всего просмотров", callback_data="edit_total_watches"),
            InlineKeyboardButton("Сумма выплат", callback_data="edit_sum"),
            InlineKeyboardButton("Назад", callback_data="back"))
    return key
