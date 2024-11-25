import telebot
import sqlite3
from telebot import types
from time import sleep

bot = telebot.TeleBot('7393369674:AAEo6bYOsL5tawUo4BRcoIE28t0FBrQnd8E')
name = None
start_message_id = None
start_chat_id = None
contact_info = {}
user_messages = {}

@bot.message_handler(func=lambda message: message.text == 'Заполнить данные 📃')
def handle_fill_data(message):

    bot.send_message(message.chat.id, "Введите ваше имя и номер телефона (в формате: +XXXXXXXXXXX):")

    bot.register_next_step_handler(message, confirm_data)



def confirm_data(message):

    user_data = message.text

    confirmation_message = f"Ваши данные: {user_data}\n\nДанные верны?"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_btn = types.KeyboardButton("Данные верны ✅")
    edit_btn = types.KeyboardButton("Нет, хочу исправить ❌")
    markup.add(confirm_btn, edit_btn)

    bot.send_message(message.chat.id, confirmation_message, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["Данные верны ✅", "Нет, хочу исправить ❌"])
def handle_confirmation(message):
    if message.text == "Данные верны ✅":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться в главное меню')
        markup.add(btn1)
        bot.send_message(message.chat.id, "Спасибо, данные подтверждены! В ближайшее время мы свяжемся с вами.", reply_markup=markup)
    elif message.text == "Нет, хочу исправить ❌":
        bot.send_message(message.chat.id, "Введите ваше имя и номер телефона (в формате: +XXXXXXXXXXX):")
        bot.register_next_step_handler(message, confirm_data)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton('На открытом воздухе 🌳')
    btn2 = types.KeyboardButton('В арендованном помещении 🏢')
    btn3 = types.KeyboardButton('Выезд на дом 🏠')
    markup.add(btn1, btn2, btn3)
    bot.send_photo(message.chat.id, 'https://sun9-63.userapi.com/impg/5tZ63IVN5MIwTTcv8yyaX41VdvAZ9r8EzmOYEw/dEqH0tUIZOg.jpg?size=720x544&quality=96&sign=bad489983a2d719d7e48f73e6015c4a2&type=album', caption='Привет {0.first_name}! Я помогу организовать вам праздник.' .format(message.from_user), reply_markup=markup)

    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()

    cur.execute( 'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Сначала вам необходимо авторизоваться. Введите свой логин:')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    bot.send_message(message.chat.id, 'Давайте выберем место проведения мероприятия:')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users ORDER BY id DESC LIMIT 5')
    users = cur.fetchall()


    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'На открытом воздухе 🌳':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Праздники 🌳')
            btn2 = types.KeyboardButton('Реквизит 💡')
            btn3 = types.KeyboardButton('Персонал 🎩')
            btn4 = types.KeyboardButton('Бронирование ✅')
            back1 = types.KeyboardButton('Выбрать другое место')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'Организация праздника на открытом воздухе имеет множество преимуществ, которые делают такие мероприятия особенно привлекательными и запоминающимися.')
            sleep(2)
            bot.send_message(message.chat.id,'Природная красота и свежий воздух создают приятную и расслабляющую атмосферу для гостей. В окружении зелени, цветов и открытого неба участники могут наслаждаться природными красотами и полноценно отдыхать от повседневной суеты.')
            bot.send_photo(message.chat.id,'https://персонаж.рф/wp-content/uploads//2021/05/6844701e5116210b0a19b9e6798e8780-800x533.jpg')
            sleep(2)
            bot.send_message(message.chat.id,'Также стоит отметить, что проведение праздника на открытом воздухе способствует физической активности и здоровому образу жизни. Гости могут наслаждаться активными развлечениями, заниматься спортом и проводить время на свежем воздухе, что благоприятно сказывается на их физическом и психическом здоровье.')
            sleep(2)
            bot.send_message(message.chat.id,'Для организаторов таких мероприятий также существует ряд преимуществ. Открытая природа обычно предлагает большое пространство, что позволяет свободно разместить всех гостей и создать удобные условия для проведения праздника.')
            sleep(2)
            bot.send_message(message.chat.id,'Кроме того, праздники на открытом воздухе часто ассоциируются с экологической ответственностью и уважением к окружающей среде. Такие мероприятия могут проводиться с учетом принципов устойчивого развития и использования экологически чистых материалов.', reply_markup=markup)

        elif message.text == 'Праздники 🌳':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Корпоратив 🎉')
            btn2 = types.KeyboardButton('Детский праздник 🎊')
            btn3 = types.KeyboardButton('Свадьба 💫')
            back1 = types.KeyboardButton('Назад 🌳')
            markup.add(btn1, btn2, btn3, back1)

            bot.send_message(message.chat.id, 'Выберите праздник:', reply_markup=markup)

        elif message.text == 'Назад 🌳':
            bot.send_message(message.chat.id,'Организация праздника на открытом воздухе имеет множество преимуществ, которые делают такие мероприятия особенно привлекательными и запоминающимися.')
            bot.send_message(message.chat.id,'Природная красота и свежий воздух создают приятную и расслабляющую атмосферу для гостей. В окружении зелени, цветов и открытого неба участники могут наслаждаться природными красотами и полноценно отдыхать от повседневной суеты.')
            bot.send_photo(message.chat.id,'https://персонаж.рф/wp-content/uploads//2021/05/6844701e5116210b0a19b9e6798e8780-800x533.jpg')
            bot.send_message(message.chat.id,'Также стоит отметить, что проведение праздника на открытом воздухе способствует физической активности и здоровому образу жизни. Гости могут наслаждаться активными развлечениями, заниматься спортом и проводить время на свежем воздухе, что благоприятно сказывается на их физическом и психическом здоровье.')
            bot.send_message(message.chat.id,'Для организаторов таких мероприятий также существует ряд преимуществ. Открытая природа обычно предлагает большое пространство, что позволяет свободно разместить всех гостей и создать удобные условия для проведения праздника.')
            bot.send_message(message.chat.id,'Кроме того, праздники на открытом воздухе часто ассоциируются с экологической ответственностью и уважением к окружающей среде. Такие мероприятия могут проводиться с учетом принципов устойчивого развития и использования экологически чистых материалов.')
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Праздники 🌳')
            btn2 = types.KeyboardButton('Реквизит 💡')
            btn3 = types.KeyboardButton('Персонал 🎩')
            btn4 = types.KeyboardButton('Бронирование ✅')
            back1 = types.KeyboardButton('Выбрать другое место')
            markup.add(btn1, btn2, btn3, btn4, back1)

            bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

        elif message.text == 'Корпоратив 🎉':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Корпоратив 🌳')
            back1 = types.KeyboardButton('Назад 🌳')
            btn1 = types.KeyboardButton('Справочная информация 🔤')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*Организация корпоратива на открытом воздухе представляет собой уникальную возможность создать яркое и незабываемое событие для компании. Такие мероприятия становятся популярными среди бизнес-сообщества благодаря своей оригинальности и нестандартности.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id, 'https://catering-muscat.ru/img/blog/blog_corporate_out-1.jpg')
            bot.send_message(message.chat.id, 'Пример организации корпоратива на открытом воздухе',  reply_markup=markup)

        elif message.text == 'Выбрать другое место':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('На открытом воздухе 🌳')
            btn2 = types.KeyboardButton('В арендованном помещении 🏢')
            btn3 = types.KeyboardButton('Выезд на дом 🏠')
            markup.add(btn1, btn2, btn3)

            bot.send_message(message.chat.id,'Выбрать другое место 🌳:', reply_markup=markup)

        elif message.text == 'Реквизит 💡':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Шарики')
            btn2 = types.KeyboardButton('Мыльные пузыри')
            btn3 = types.KeyboardButton('Праздничные колпаки')
            btn4 = types.KeyboardButton('Ничего')
            back1 = types.KeyboardButton('Назад 🌳')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляются реквизиты, такие как шарики, праздничные колпаки и мыльные пузыри. Пользователи могут выбирать из различных размеров, цветов и типов, чтобы создать желаемую атмосферу для своего мероприятия.\nКаждый реквизит сопровождается информацией о ценах, наличии и вариантах доставки или самовывоза. Вся информация уточняется по телефону после бронирования заказа.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Реквизит ⚱️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Шарики')
            btn2 = types.KeyboardButton('Мыльные пузыри')
            btn3 = types.KeyboardButton('Праздничные колпаки')
            btn4 = types.KeyboardButton('Ничего')
            back1 = types.KeyboardButton('Назад 🏢')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляются реквизиты, такие как шарики, праздничные колпаки и мыльные пузыри. Пользователи могут выбирать из различных размеров, цветов и типов, чтобы создать желаемую атмосферу для своего мероприятия.\nКаждый реквизит сопровождается информацией о ценах, наличии и вариантах доставки или самовывоза. Вся информация уточняется по телефону после бронирования заказа.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Реквизит 💎':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Шарики')
            btn2 = types.KeyboardButton('Мыльные пузыри')
            btn3 = types.KeyboardButton('Праздничные колпаки')
            btn4 = types.KeyboardButton('Ничего')
            back1 = types.KeyboardButton('Назад 🏠')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляются реквизиты, такие как шарики, праздничные колпаки и мыльные пузыри. Пользователи могут выбирать из различных размеров, цветов и типов, чтобы создать желаемую атмосферу для своего мероприятия.\nКаждый реквизит сопровождается информацией о ценах, наличии и вариантах доставки или самовывоза. Вся информация уточняется по телефону после бронирования заказа.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Персонал 🎩':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Певцы')
            btn2 = types.KeyboardButton('Фотографы')
            btn3 = types.KeyboardButton('Ведущие')
            btn4 = types.KeyboardButton('Никто')
            back1 = types.KeyboardButton('Назад 🌳')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляется персонал, включающий в себя певцов, фотографов и ведущих. Пользователи могут выбирать профессионалов в соответствии с их предпочтениями и требованиями к мероприятию.\nКаждый член персонала представлен с информацией о их опыте, портфолио и стоимости услуг. Подробности уточняются по телефону.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Персонал 🕵️‍♂️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Певцы')
            btn2 = types.KeyboardButton('Фотографы')
            btn3 = types.KeyboardButton('Ведущие')
            btn4 = types.KeyboardButton('Никто')
            back1 = types.KeyboardButton('Назад 🏢')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляется персонал, включающий в себя певцов, фотографов и ведущих. Пользователи могут выбирать профессионалов в соответствии с их предпочтениями и требованиями к мероприятию.\nКаждый член персонала представлен с информацией о их опыте, портфолио и стоимости услуг. Подробности уточняются по телефону.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Персонал 👨‍🏫':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Певцы')
            btn2 = types.KeyboardButton('Фотографы')
            btn3 = types.KeyboardButton('Ведущие')
            btn4 = types.KeyboardButton('Никто')
            back1 = types.KeyboardButton('Назад 🏠')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'*Для праздника предоставляется персонал, включающий в себя певцов, фотографов и ведущих. Пользователи могут выбирать профессионалов в соответствии с их предпочтениями и требованиями к мероприятию.\nКаждый член персонала представлен с информацией о их опыте, портфолио и стоимости услуг. Подробности уточняются по телефону.*', reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Назад ⬅️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Праздники 🌳')
            btn2 = types.KeyboardButton('Реквизит 💡')
            btn3 = types.KeyboardButton('Персонал')
            btn4 = types.KeyboardButton('Бронирование ✅')
            back1 = types.KeyboardButton('Выбрать другое место')
            markup.add(btn1, btn2, btn3, btn4, back1)
            bot.send_message(message.chat.id,'Организация праздника на открытом воздухе имеет множество преимуществ, которые делают такие мероприятия особенно привлекательными и запоминающимися.')
            sleep(2)
            bot.send_message(message.chat.id,'Природная красота и свежий воздух создают приятную и расслабляющую атмосферу для гостей. В окружении зелени, цветов и открытого неба участники могут наслаждаться природными красотами и полноценно отдыхать от повседневной суеты.')
            bot.send_photo(message.chat.id,'https://персонаж.рф/wp-content/uploads//2021/05/6844701e5116210b0a19b9e6798e8780-800x533.jpg')
            sleep(2)
            bot.send_message(message.chat.id,'Также стоит отметить, что проведение праздника на открытом воздухе способствует физической активности и здоровому образу жизни. Гости могут наслаждаться активными развлечениями, заниматься спортом и проводить время на свежем воздухе, что благоприятно сказывается на их физическом и психическом здоровье.')
            sleep(2)
            bot.send_message(message.chat.id,'Для организаторов таких мероприятий также существует ряд преимуществ. Открытая природа обычно предлагает большое пространство, что позволяет свободно разместить всех гостей и создать удобные условия для проведения праздника.')
            sleep(2)
            bot.send_message(message.chat.id,'Кроме того, праздники на открытом воздухе часто ассоциируются с экологической ответственностью и уважением к окружающей среде. Такие мероприятия могут проводиться с учетом принципов устойчивого развития и использования экологически чистых материалов.',reply_markup=markup)

        elif message.text == 'Детский праздник 🎊':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Детский праздник 🎊')
            back1 = types.KeyboardButton('Назад 🌳')
            btn1 = types.KeyboardButton('Справочная информация 🔛')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*Детский праздник на свежем воздухе - это замечательная возможность сделать праздник вашего ребенка еще более ярким и веселым. Дети будут активно развлекаться и наслаждаться играми на свежем воздухе.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id,'https://lh3.googleusercontent.com/proxy/4Y2csov3SOslVZSNZZ6M2MRqiO9N2BNqwG2BU5Fx2EAsB8LOQEUwdiXwyiQaxDrmMRHEgqiTcyOdSWVS2ImJpXtgyEdsYYca0FLkNHmN2oN_2rxGnchi0GFMj8UyoDQ4d3cZa3-zr15tfEmXtdg')
            bot.send_message(message.chat.id, 'Пример организации детского праздника на открытом воздухе', reply_markup=markup)

        elif message.text == 'Свадьба 💫':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Свадьбу 💫')
            back1 = types.KeyboardButton('Назад 🌳')
            btn1 = types.KeyboardButton('Справочная информация 🔤')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*Свадьба - это особенное событие в жизни каждого человека. Организация свадьбы на открытом воздухе позволит сделать ваше торжество ярким, неповторимым и запоминающимся.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id,'https://static.tildacdn.com/tild3131-6562-4665-b537-666332383633/outdoor-wedding.jpg')
            bot.send_message(message.chat.id, 'Пример организации свадьбы на открытом воздухе', reply_markup=markup)

        elif message.text == 'В арендованном помещении 🏢':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Праздники 🏢')
                btn2 = types.KeyboardButton('Реквизит ⚱️')
                btn3 = types.KeyboardButton('Персонал 🕵️‍♂️')
                btn4 = types.KeyboardButton('Бронирование ✅')
                back1 = types.KeyboardButton('Выбрать другое место')
                markup.add(btn1, btn2, btn3, btn4, back1)
                bot.send_message(message.chat.id,'Организация праздника в арендованном помещении обладает рядом преимуществ, делающих такие мероприятия привлекательными и удобными для гостей и организаторов.')
                sleep(2)
                bot.send_message(message.chat.id,'Арендованное помещение предоставляет контролируемую и комфортную обстановку для проведения мероприятий. Здесь можно обеспечить удобства для гостей, такие как обогрев или кондиционирование воздуха, что особенно важно в случае непредсказуемых погодных условий.')
                sleep(2)
                bot.send_message(message.chat.id,'Кроме того, наличие помещения позволяет свободно планировать и организовывать различные развлечения и активности вне зависимости от времени года или погоды. В помещении можно провести как тематическую вечеринку, так и более формальное мероприятие, подстроив его под нужды и предпочтения гостей.')
                bot.send_photo(message.chat.id, 'https://opis-cdn.tinkoffjournal.ru/mercury/svadba-v-dome-21.kh7wf7abflca.jpg')
                sleep(2)
                bot.send_message(message.chat.id,'Также стоит отметить, что арендованное помещение часто обладает всем необходимым оборудованием и инфраструктурой для проведения мероприятий. Это включает в себя звуковое и осветительное оборудование, мебель, кухонные принадлежности и прочее, что существенно облегчает подготовку и проведение праздника.')
                sleep(2)
                bot.send_message(message.chat.id,'Для организаторов плюсом является также возможность контролировать атмосферу и ход мероприятия в помещении. Это позволяет более гибко реагировать на изменения планов и предпочтений гостей, обеспечивая им максимальный комфорт и удовольствие от проведенного времени.', reply_markup=markup)

        elif message.text == 'Праздники 🏢':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Юбилей 💍')
            btn2 = types.KeyboardButton('Детский праздник 🎁')
            btn3 = types.KeyboardButton('День рождения 🎂')
            back1 = types.KeyboardButton('Назад 🏢')
            markup.add(btn1, btn2, btn3, back1)

            bot.send_message(message.chat.id, 'Выберите праздник:', reply_markup=markup)

        elif message.text == 'Назад 🏢':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Праздники 🏢')
                btn2 = types.KeyboardButton('Реквизит ⚱️')
                btn3 = types.KeyboardButton('Персонал 🕵️‍♂️')
                btn4 = types.KeyboardButton('Бронирование ✅')
                back1 = types.KeyboardButton('Выбрать другое место')
                markup.add(btn1, btn2, btn3, btn4, back1)
                bot.send_message(message.chat.id,'Организация праздника в арендованном помещении обладает рядом преимуществ, делающих такие мероприятия привлекательными и удобными для гостей и организаторов.')
                bot.send_message(message.chat.id,'Арендованное помещение предоставляет контролируемую и комфортную обстановку для проведения мероприятий. Здесь можно обеспечить удобства для гостей, такие как обогрев или кондиционирование воздуха, что особенно важно в случае непредсказуемых погодных условий.')
                bot.send_message(message.chat.id,'Кроме того, наличие помещения позволяет свободно планировать и организовывать различные развлечения и активности вне зависимости от времени года или погоды. В помещении можно провести как тематическую вечеринку, так и более формальное мероприятие, подстроив его под нужды и предпочтения гостей.')
                bot.send_photo(message.chat.id, 'https://opis-cdn.tinkoffjournal.ru/mercury/svadba-v-dome-21.kh7wf7abflca.jpg')
                bot.send_message(message.chat.id,'Также стоит отметить, что арендованное помещение часто обладает всем необходимым оборудованием и инфраструктурой для проведения мероприятий. Это включает в себя звуковое и осветительное оборудование, мебель, кухонные принадлежности и прочее, что существенно облегчает подготовку и проведение праздника.')
                bot.send_message(message.chat.id,'Для организаторов плюсом является также возможность контролировать атмосферу и ход мероприятия в помещении. Это позволяет более гибко реагировать на изменения планов и предпочтений гостей, обеспечивая им максимальный комфорт и удовольствие от проведенного времени.', reply_markup=markup)

        elif message.text == 'Юбилей 💍':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Юбилей 💍')
            back1 = types.KeyboardButton('Назад 🏢')
            btn1 = types.KeyboardButton('Справочная информация 🔤')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*Юбилей - это особенное событие, которое заслуживает запоминающейся и оригинальной организации. Юбилей в арендованном помещении позволит создать атмосферу торжества и радости в уютной обстановке.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id,'https://4party.ua/upload/medialibrary/287/vecherinka-na-prirode.jpg')
            bot.send_message(message.chat.id, 'Пример организации юбилея в арендованном помещении', reply_markup=markup)

        elif message.text == 'Детский праздник 🎁':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Детский праздник 🎁')
            back1 = types.KeyboardButton('Назад 🏢')
            btn1 = types.KeyboardButton('Справочная информация 🔛')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*Детский праздник в арендованном помещении - это отличный выбор для проведения веселого и безопасного праздника для детей любого возраста. Здесь можно организовать множество интересных игр и развлечений.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id,'https://st.przx.ru/files/content/articles/ekb/show/program.jpg')
            bot.send_message(message.chat.id, 'Пример организации детского праздника в арендованном помещении', reply_markup=markup)

        elif message.text == 'День рождения 🎂':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать День рождения 🎂')
            back1 = types.KeyboardButton('Назад 🏢')
            btn1 = types.KeyboardButton('Справочная информация 🔛')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'*День рождения - это особенное событие, которое нужно отмечать ярко и весело!\nОрганизация дня рождения в арендованном помещении позволит создать атмосферу веселья и праздника для вас и ваших гостей.*', parse_mode='Markdown')
            bot.send_photo(message.chat.id,'https://www.wmj.ru/thumb/1500x0/filters:quality(75):no_upscale()/imgs/2016/12/05/02/818624/d1200a5dac0a9ece3dff3ab48197e85ce014c30b.jpg')
            bot.send_message(message.chat.id, 'Пример организации дня рождения в арендованном помещении', reply_markup=markup)


        elif message.text == 'Выезд на дом 🏠':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Праздники 🏠')
                btn2 = types.KeyboardButton('Реквизит 💎')
                btn3 = types.KeyboardButton('Персонал 👨‍🏫')
                btn4 = types.KeyboardButton('Бронирование ✅')
                back1 = types.KeyboardButton('Выбрать другое место')
                markup.add(btn1, btn2, btn3, btn4, back1)
                bot.send_message(message.chat.id,'Организация праздника с выездом на дом предоставляет ряд преимуществ, которые делают такой формат мероприятия удобным и привлекательным как для гостей, так и для организаторов.')
                sleep(2)
                bot.send_message(message.chat.id,'Проведение праздника прямо у вас дома обеспечивает максимальный комфорт и удобство для всех участников. Гости могут чувствовать себя как дома, что создает особенно теплую и приятную атмосферу.')
                sleep(2)
                bot.send_message(message.chat.id,'Кроме того, проведение мероприятия в домашней обстановке позволяет существенно сэкономить время и усилия на подготовку. Нет необходимости беспокоиться о транспортировке гостей или аренде помещения - все происходит у вас дома, что делает организацию максимально удобной и беззаботной.')
                bot.send_photo(message.chat.id,'https://annalegenda.ru/wp-content/uploads/2020/03/img-holiday-skew-2-1024x682.jpg')
                sleep(2)
                bot.send_message(message.chat.id,'Также стоит отметить, что праздник с выездом на дом позволяет полностью персонализировать мероприятие под ваши пожелания и предпочтения. Вы вольны выбирать тему, меню, декорации и развлечения в соответствии с вашими вкусами и потребностями, что делает праздник по-настоящему уникальным и индивидуальным.')
                sleep(2)
                bot.send_message(message.chat.id,'Для организаторов такого мероприятия плюсом является также возможность полного контроля над процессом и атмосферой мероприятия. Вы можете свободно распределять задачи, координировать работу персонала и обеспечивать комфорт и удовлетворение гостей на протяжении всего праздника.', reply_markup=markup)

        elif message.text == 'Праздники 🏠':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Новый год 🎅')
            btn2 = types.KeyboardButton('День рождения 🍕')
            back1 = types.KeyboardButton('Назад 🏠')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id, 'Выберите праздник:', reply_markup=markup)

        elif message.text == 'Назад 🏠':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Праздники 🏠')
            btn2 = types.KeyboardButton('Реквизит 💎')
            btn3 = types.KeyboardButton('Персонал 👨‍🏫')
            back1 = types.KeyboardButton('Выбрать другое место')
            markup.add(btn1, btn2, btn3, back1)
            bot.send_message(message.chat.id,'Организация праздника с выездом на дом предоставляет ряд преимуществ, которые делают такой формат мероприятия удобным и привлекательным как для гостей, так и для организаторов.')
            bot.send_message(message.chat.id,'Проведение праздника прямо у вас дома обеспечивает максимальный комфорт и удобство для всех участников. Гости могут чувствовать себя как дома, что создает особенно теплую и приятную атмосферу.')
            bot.send_message(message.chat.id,'Кроме того, проведение мероприятия в домашней обстановке позволяет существенно сэкономить время и усилия на подготовку. Нет необходимости беспокоиться о транспортировке гостей или аренде помещения - все происходит у вас дома, что делает организацию максимально удобной и беззаботной.')
            bot.send_photo(message.chat.id,'https://annalegenda.ru/wp-content/uploads/2020/03/img-holiday-skew-2-1024x682.jpg')
            bot.send_message(message.chat.id,'Также стоит отметить, что праздник с выездом на дом позволяет полностью персонализировать мероприятие под ваши пожелания и предпочтения. Вы вольны выбирать тему, меню, декорации и развлечения в соответствии с вашими вкусами и потребностями, что делает праздник по-настоящему уникальным и индивидуальным.')
            bot.send_message(message.chat.id,'Для организаторов такого мероприятия плюсом является также возможность полного контроля над процессом и атмосферой мероприятия. Вы можете свободно распределять задачи, координировать работу персонала и обеспечивать комфорт и удовлетворение гостей на протяжении всего праздника.', reply_markup=markup)

        elif message.text == 'Новый год 🎅':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать Новый год 🎅')
            back1 = types.KeyboardButton('Назад 🏠')
            btn1 = types.KeyboardButton('Справочная информация 🔛')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'Новый год с выездом на дом - это отличный способ встретить праздник прямо у вас дома в уютной обстановке вместе с близкими и друзьями. Наслаждайтесь праздником без лишних хлопот и забот!')
            bot.send_photo(message.chat.id,'https://www.zabava63.ru/upload/iblock/42f/42f9abc79af14bbecaa1582f61566351.jpg')
            bot.send_message(message.chat.id, 'Пример организации нового года с выездом на дом', reply_markup=markup)

        elif message.text == 'День рождения 🍕':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton('Выбрать День рождения 🍕')
            back1 = types.KeyboardButton('Назад 🏠')
            btn1 = types.KeyboardButton('Справочная информация 🔛')
            markup.add(btn1, btn2, back1)

            bot.send_message(message.chat.id,'День рождения с выездом на дом - это удобный и комфортный вариант организации праздника прямо у вас дома. Вам не нужно беспокоиться о том, как добраться до места проведения, все происходит у вас дома!')
            bot.send_photo(message.chat.id,'https://sushi-catering.ru/files/user/shapka-3.jpg')
            bot.send_message(message.chat.id, 'Пример организации дня рождения с выездом на дом', reply_markup=markup)

        elif message.text == 'Справочная информация 🔛':
            bot.send_message(message.chat.id, 'Среднее время проведения от 3 до 7 часов.')
            sleep(1)
            bot.send_message(message.chat.id, 'Отмена или изменение расписания мероприятия запрещено.')
            sleep(1)
            bot.send_message(message.chat.id, 'Рекомендуемое количество участников: от 5 до 15 человек.')
            sleep(1)
            bot.send_message(message.chat.id, 'Наличие тематической одежды или костюмов: по желанию организатора.')
            sleep(1)
            bot.send_message(message.chat.id, 'Платное/Бесплатное участие: обсуждается и согласуется по телефону.')
            sleep(1)
            bot.send_message(message.chat.id, 'Проведение мероприятия доступно для людей с ограниченными возможностями.')

        elif message.text == 'Справочная информация 🔤':
            bot.send_message(message.chat.id,'Наличие перерывов.')
            sleep(1)
            bot.send_message(message.chat.id,'Среднее время проведения от 6 до 10 часов.')
            sleep(1)
            bot.send_message(message.chat.id,'Рекомендуемое количество участников: от 10 до 25 человек.')
            sleep(1)
            bot.send_message(message.chat.id,'Наличие правил отмены или изменения расписания мероприятия.')
            sleep(1)
            bot.send_message(message.chat.id,'Наличие тематической одежды или костюмов: по желанию организатора.')
            sleep(1)
            bot.send_message(message.chat.id,'Платное/Бесплатное участие: обсуждается и согласуется по телефону.')
            sleep(1)
            bot.send_message(message.chat.id,'Проведение мероприятия доступно для людей с ограниченными возможностями.')

        elif message.text == 'Бронирование ✅':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Заполнить данные 📃')
            btn2 = types.KeyboardButton('Бонусная программа 💸')
            back1 = types.KeyboardButton('Выбрать другое место')
            markup.add(btn1, btn2, back1)
            bot.send_message(message.chat.id,'Выберите действие:', reply_markup=markup)

        elif message.text == 'Вернуться в главное меню':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('На открытом воздухе 🌳')
            btn2 = types.KeyboardButton('В арендованном помещении 🏢')
            btn3 = types.KeyboardButton('Выезд на дом 🏠')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите место проведения мероприятия:', reply_markup=markup)

        elif message.text == 'Бонусная программа 💸':
            bot.send_message(message.chat.id,'За первую регистрацию вам начисленно: *1000 Баллов*', parse_mode='Markdown')
            bot.send_message(message.chat.id, 'При оформлении праздника 10% от стоимости готового праздника переходят на ваш следующий заказ.\n*Цены и баллы уточняются по телефону.*', parse_mode='Markdown')

        elif message.text == 'Шарики':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Мыльные пузыри':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Праздничные колпаки':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Ничего':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Певцы':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Фотографы':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Ведущие':
            bot.send_message(message.chat.id, 'Выбор учтен.')

        elif message.text == 'Никто':
            bot.send_message(message.chat.id, 'Выбор учтен.')


bot.polling(none_stop=True, interval=0)