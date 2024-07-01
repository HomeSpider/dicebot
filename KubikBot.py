import telebot, random, sqlite3
from telebot import types
bot = telebot.TeleBot("2011166017:AAFM2SNAKqnbsAXvC1UvQc_-rrQAfTqv0lM")

worklist = []
changelist = []
adminlist = []

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="""Ну поехали!\nТыкни /create чтобы создать персонажа,\n/change чтобы исправить характеристики\n и /roll чтобы бросить кубик.""")

@bot.message_handler(commands=["roll"])
def roll(message):
    keys=types.ReplyKeyboardMarkup()
    keys.add("D4", "D6", "D8", "D10", "D12", "D20", "D20 + модиф")
    keys.resize_keyboard
    quest = bot.send_message(message.chat.id, text="Выбери кубик, солнышко", reply_markup=keys)
    bot.register_next_step_handler(quest, roll2)

def roll2(message):
    if message.text == "D20":
        num = random.randint(1, 20) 
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D12":
        num = random.randint(1, 12)
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D10":
        num = random.randint(1, 10)
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D8":
        num = random.randint(1, 8)
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D6":
        num = random.randint(1, 6)
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D4":
        num = random.randint(1, 4)
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
    elif message.text == "D20 + модиф":
        keys=types.ReplyKeyboardMarkup()
        keys.add("STR", "DEX", "CON", "INT", "WIS", "CHAR")
        keys.resize_keyboard
        quest = bot.send_message(message.chat.id, text="Котик, выбери модификатор", reply_markup=keys)
        bot.register_next_step_handler(quest, roll20)
    try:
        bot.register_next_step_handler(quest, roll2)
    except:
        print("Help!")

def roll20(message):
    conn=sqlite3.connect("tables.db")
    cursor=conn.cursor()
    id=str(message.from_user.id)
    try:
        sql=cursor.execute("""SELECT {} FROM Heroes
                        WHERE Id="{}" """.format(message.text, message.from_user.id))
        for i in sql.fetchall():
            for j in i:
                if j==1:
                    num2=-5
                elif j==2 or j==3:
                    num2=-4
                elif j==4 or j==5:
                    num2=-3
                elif j==6 or j==7:
                    num2=-2
                elif j==8 or j==9:
                    num2=-1
                elif j==10 or j==11:
                    num2=0
                elif j==12 or j==13:
                    num2=1
                elif j==14 or j ==15:
                    num2=2
                elif j==16 or j==17:
                    num2=3
                elif j==18 or j==19:
                    num2=4
                elif j==20 or j==21:
                    num2=5
                elif j==22 or j==23:
                    num2=6
                elif j==24 or j==25:
                    num2=7
                elif j==26 or j==27:
                    num2=8
                elif j==28 or j==29:
                    num2=9
                elif j==30:
                    num2=10
        num = random.randint(1, 20)+num2
        quest = bot.send_message(message.chat.id, text=num, reply_to_message_id=message.id)
        try:
            bot.register_next_step_handler(quest, roll20)
        except:
            print("Help!\n"+message.text)
    except:
        roll(message)
        
@bot.message_handler(commands=["create"])
def create(message):
    id=str(message.from_user.id)
    worklist.append(id)
    print(worklist)
    quest = bot.send_message(message.chat.id, text="Напиши имя своего персонажа, котик", reply_to_message_id=message.id)
    bot.register_next_step_handler(quest, create2)

def create2(message):
    worklist.append(str(message.text))
    print(worklist)
    bot.send_message(message.chat.id, text="Теперь напиши мне свои параметры через запятую!", reply_to_message_id=message.id)
    quest = bot.send_message(message.chat.id, text="Вот порядок:\nСила, Ловкость, Телосложение, Интеллект, Мудрость, Харизма")
    bot.register_next_step_handler(quest, create3)

def create3(message):
    for i in message.text.split(","):
        worklist.append(i)
    print(worklist)
    bot.send_message(message.chat.id, text="Отлично, ты у меня умничка!", reply_to_message_id=message.id)
    conn=sqlite3.connect("tables.db")
    cursor=conn.cursor()
    sql=cursor.execute(""" create table if not exists Heroes (Id Integer, Name Text, STR Integer, DEX Inteder, CON Integer, INT Integer, WIS Integer, CHAR Integer)""")
    conn.commit()
    try:
        sql=cursor.execute(""" INSERT INTO Heroes(Id, Name, STR, DEX, CON, INT, WIS, CHAR) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}") """.format(worklist[0], worklist[1], worklist[2], worklist[3],worklist[4],worklist[5],worklist[6],worklist[7]))
        conn.commit()
        bot.send_message(message.chat.id, text="У меня всё готово, можно начинать")
    except: 
        print(worklist)
        bot.send_message(message.chat.id, text=message.from_user.last_name+", мы всё сломали. Вообще всё...", reply_to_message_id=message.id)
    worklist.clear()

@bot.message_handler(commands=["change"])
def change(message):
    keys=types.ReplyKeyboardMarkup()
    keys.add("STR", "DEX", "CON", "INT", "WIS", "CHAR", "Name")
    keys.resize_keyboard
    quest = bot.send_message(message.chat.id, text="Что хочешь изменить?", reply_markup=keys)
    bot.register_next_step_handler(quest, change2)

def change2(message):
    quest = bot.send_message(message.chat.id, text="Введи новое значение для характеристики")
    bot.register_next_step_handler(quest, change3)
    changelist.append(message.text)

def change3(message):
    conn=sqlite3.connect("tables.db")
    cursor=conn.cursor()
    id=str(message.from_user.id)
    try:
        sql=cursor.execute("""UPDATE Heroes
                                    SET {}="{}"
                                    WHERE Id="{}" """.format(changelist[0], message.text, id))
        conn.commit()
        bot.send_message(message.chat.id, text="Окей, всё готово!", reply_to_message_id=message.id)
        changelist.clear()
    except:
        print("У нас что-то сломалось.")
        print(Exception)
        bot.send_message(message.chat.id, text=message.from_user.last_name+", мы всё сломали. Вообще всё...", reply_to_message_id=message.id)

@bot.message_handler(commands=["delete"])
def delete(message):
    keys=types.ReplyKeyboardMarkup()
    keys.add("Удаляй!", "Нет, не надо...")
    keys.resize_keyboard
    quest = bot.send_message(message.chat.id, text="Правда хочешь удалить?", reply_markup=keys)
    bot.register_next_step_handler(quest, delete2)

def delete2(message):
    conn=sqlite3.connect("tables.db")
    cursor=conn.cursor()
    id=str(message.from_user.id)
    if message.text=="Удаляй!":
        try:
            sql=cursor.execute("""DELETE FROM Heroes WHERE Id="{}" """.format(id))
            conn.commit()
            bot.send_message(message.chat.id, text="Пока-пока, персонаж!", reply_to_message_id=message.id)
        except:
            print("У нас что-то сломалось.")
            bot.send_message(message.chat.id, text=message.from_user.last_name+", мы всё сломали. Вообще всё...", reply_to_message_id=message.id)
    elif message.text=="Нет, не надо...":
        bot.send_message(message.chat.id, text="Ладно тогда.", reply_to_message_id=message.id)



bot.polling()