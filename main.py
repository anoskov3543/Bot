import telebot
import sqlite3
from telebot import types
height=100
bot=telebot.TeleBot("5567280575:AAECZy6z5lIcjhx4IVwVW8zFa9C7OJLHfXQ")
DB_FILE_NAME = 'db.sqlite'
def create_connect():
    return sqlite3.connect(DB_FILE_NAME)
def init_db():

    with create_connect() as connect:
        connect.execute('''
            CREATE TABLE IF NOT EXISTS Message (
                id      INTEGER  PRIMARY KEY,
                user_id INTEGER  NOT NULL,
                height    INTEGER  NOT NULL
            );
        ''')

        connect.commit()
init_db()        

def add_message(user_id, message):
    with create_connect() as connect:
        connect.execute(
            'INSERT INTO Message(user_id, height) VALUES(?,?)', (user_id, message)
        )
        connect.commit()

def get_db(uid, height):
    conn = sqlite3.connect(DB_FILE_NAME)
    user = conn.execute(f'SELECT * FROM message WHERE user_id ={uid}').fetchone()

    if user is None:
        add_message(uid, heigh)
        conn.close()
        return None
    else:
        conn.close()
        row = user[0]
        user_id = user[1]
        height = user[2]
        return row, user_id, height


@bot.message_handler(commands=["start"])
def start(m,res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Вырости")
    item2=types.KeyboardButton("Мой рост")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,'Нажми: \nВырости чтобы поднять свой рост\nМой рост чтобы узнать свой текущий рост ',reply_markup=markup)
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Вырости':
        height+=10
        answer=f"Вы выросли, теперь ваш рост={height}"

        #add_message(user_id=message.chat.id, message=answer)
        
        bot.send_message(message.chat.id, answer)
        print(get_db(message.chat.id))
    if message.text.strip()=="Мой рост":
        answer=f"Ваш текущий рост={height}"
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True,interval=0)
