from telebot.types import  *
import telebot
from database import *

USER_NUMBER = {}
USER_NAME = {}
CAR_AGE = {}
CAR_COLOR = {}
CAR_NAME = {}
A_MAP = {}
B_MAP = {}
LOCATION= {}
LOCATION_ID= {}
ADMIN_ID = 789945598

NEW_B = {}

bot = telebot.TeleBot("7173804946:AAHE0uh331nnJOUeugxhLqfWC6OYA3zGfDU",parse_mode='html')
provider_token = "371317599:TEST:1703133501220"


def user_register_menu():
    key = InlineKeyboardMarkup()
    key.add(
        InlineKeyboardButton(text="🚖 Haydovchi",callback_data='register-taxi'),
        InlineKeyboardButton(text="👤 Yo'lovchi", callback_data='register-user')
    )
    return key
def viloyat_menu():
  key = InlineKeyboardMarkup()
  key.add(
      InlineKeyboardButton(text="Boshlash",callback_data='xorazim'),

  )
  return key

tumanlar =[
 "Andijon viloyati",
 "Buxoro viloyati",
 "Farg'ona viloyati",
 "Jizzax viloyati",
 "Xorazm viloyati",
 "Namangan viloyati",
 "Navoiy viloyati",
 "Qashqadaryo viloyati",
 "Samarqand viloyati",
 "Sirdaryo viloyati",
 "Surxondaryo viloyati",
 "Toshkent viloyati",
 "Qoraqalpog'iston Respublikasi",
 "Toshkent shahri",
]


prices = [LabeledPrice(label='Taxi uchun', amount=1000000)]

shipping_options = [
]



def number_menu():
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(KeyboardButton("☎ Telefon raqam",request_contact=True))
    return key

def user_step(cid):
    cursor.execute(f"SELECT * FROM user_step WHERE chat_id={cid}")
    return cursor.fetchone()[2]


def tumanlar_menu():
    key = InlineKeyboardMarkup(row_width=2)
    m = []
    for i in tumanlar:
        m.append(InlineKeyboardButton(text=str(i),callback_data="map-"+str(i)))
    return key.add(*m)

def tuman_menu():
  try:
    m= []
    for i in  tumanlar:
      m.append(InlineKeyboardButton(text=str(i),callback_data="a-"+str(i)))
    key = InlineKeyboardMarkup(row_width=2).add(*m)
    return key
  except Exception as e:
    print(e)
    
def tuman_menu1(txt):
    key = InlineKeyboardMarkup(row_width=2)
    tum = tumanlar
    m = []
    for i in  tum:
        if i!=txt:
          m.append(InlineKeyboardButton(text=str(i),callback_data="b-"+str(i)))
    return key.add(*m)



def tumanlar_menu1(txt):
    tum = tumanlar
    key = InlineKeyboardMarkup(row_width=2)
    m = []
    for i in tum:
      if i!=txt:
        m.append(InlineKeyboardButton(text=str(i),callback_data="c-"+str(i)))
    return key.add(*m)


def del_menu():
  key = InlineKeyboardMarkup()
  key.add(InlineKeyboardButton(text="✅ Ha",callback_data='ha'),InlineKeyboardButton(text="❌ Yoq",callback_data='yoq'))
  return key
def admin_menu():
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton(text="🧑‍💻 Qo'llab quvatlash",url=f'tg://user?id={ADMIN_ID}'),InlineKeyboardButton(text="🗑 O'chirish",callback_data=f'del'))
    return key.add(InlineKeyboardButton(text="➕ Hisob to'ldirish",callback_data='card'))

def admin_menu1():
  key = InlineKeyboardMarkup()
  key.add(InlineKeyboardButton(text="🧑‍💻 Qo'llab quvatlash",url=f'tg://user?id={ADMIN_ID}'),InlineKeyboardButton(text="🗑 O'chirish",callback_data=f'del'))
  return key
def admin_menu2():
  key = InlineKeyboardMarkup()
  key.add(InlineKeyboardButton(text="🧑‍💻 Qo'llab quvatlash",url=f'tg://user?id={ADMIN_ID}'))
  return key



def user_menu():
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(
        KeyboardButton("🔍 Taxi izlash"),
        KeyboardButton("➕ Elon joylash")
    )
    key.add(
        KeyboardButton("📊 Statistika"),
        KeyboardButton("👤 Kabinet"),
    )
    return key

def taxi_menu():
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(
        KeyboardButton("➕ Elon berish"),
        KeyboardButton("📔 Elonlar")
    )
    key.add(
      KeyboardButton("📊 Statistika"),
      KeyboardButton("👤 Kabinet"),
    )
    return key
def admin_panel():
  key = ReplyKeyboardMarkup(resize_keyboard=True)

  key.add(
    KeyboardButton("✉ Oddiy xabar"),
    KeyboardButton("✉ Forward xabar"),
  )
  key.add(
    KeyboardButton("➕ Pul qo'shish"),
    KeyboardButton("➖ Pul ayirish"),
  )
  key.add(
    KeyboardButton("📁 Baza yuklash"),
      KeyboardButton("◀ Bosh menu")
  )
  return key

def oddiy_xabar(msg):
  success = 0
  error = 0
  stat = cursor.execute("SELECT chat_id FROM user_check").fetchall()
  for i in stat:
    print(i[0])
    try:
      success+=1
      bot.send_message(i[0],msg.text)
    except:
      error+=1
  bot.send_message(ADMIN_ID,f"<b>Xabar yuborildi!\n\n✅Yuborildi: {success}\n❌ Yuborilmadi: {error}</b>",reply_markup=admin_panel())

def add_money(msg):
  data = msg.text.split("=")
  taxi_id = data[0]
  money = data[1]
  check = cursor.execute(f"SELECT * FROM user_taxi WHERE chat_id={taxi_id}").fetchone()
  if check is None:
    bot.send_message(ADMIN_ID,"<b>❌ Kechirasiz bunday haydovchi mavjud emas!</b>")
  else:
    try:
      sums = check[4]+int(money)
      cursor.execute(f"UPDATE user_taxi SET balance={int(sums)} WHERE chat_id={int(taxi_id)}")
      conn.commit()
      bot.send_message(taxi_id,f"<b>✅ Sizning hisobingizga: {money} uzs qo'shildi!</b>")              
      bot.send_message(ADMIN_ID,f"<b>✅ Foydalanuvchi hisobiga: {money} uzs qo'shildi!</b>")
    except:
      bot.send_message(ADMIN_ID,"<b>❌ Kechirasiz xatolik!</b>",reply_markup=admin_panel())
def minus_money(msg):
  data = msg.text.split("=")
  taxi_id = data[0]
  money = data[1]
  check = cursor.execute(f"SELECT * FROM user_taxi WHERE chat_id={taxi_id}").fetchone()
  if check is None:
    bot.send_message(ADMIN_ID,"<b>❌ Kechirasiz bunday haydovchi mavjud emas!</b>")
  else:
    try:
      sums = check[4]-int(money)
      cursor.execute(f"UPDATE user_taxi SET balance={int(sums)} WHERE chat_id={int(taxi_id)}")
      conn.commit()
      bot.send_message(taxi_id,f"<b>✅ Sizning hisobingizdan: {money} uzs ayrildi!</b>")              
      bot.send_message(ADMIN_ID,f"<b>✅ Foydalanuvchi hisobidan: {money} uzs ayrildi!</b>")
    except:
      bot.send_message(ADMIN_ID,"<b>❌ Kechirasiz xatolik!</b>",reply_markup=admin_panel())

def forward_xabar(msg):
  success = 0
  error = 0
  stat = cursor.execute("SELECT chat_id FROM user_check").fetchall()
  for i in stat:
    print(i[0])
    try:
      success+=1
      bot.forward_message(i[0], ADMIN_ID, msg.message_id)
    except:
      error+=1
  bot.send_message(ADMIN_ID,f"<b>Xabar yuborildi!\n\n✅Yuborildi: {success}\n❌ Yuborilmadi: {error}</b>",reply_markup=admin_panel())
  
def user_elon(msg):
  cid = msg.chat.id
  text = msg.text
  if len(msg.text)>5:
    cursor.execute(f"INSERT INTO elonlar(chat_id,yol) VALUES({cid},'{text}')")
    bot.reply_to(msg,"✅ Elon muvaffaqiyatli qo'shildi!")
  else:
    bot.reply_to(msg,"<b>❌ Manzil xato kiritilgan!</b>")
  
def cars_menu():
    key = InlineKeyboardMarkup()
    key.add(
        InlineKeyboardButton(text='Damas',callback_data='car-Damas'),
        InlineKeyboardButton(text='Nexia',callback_data='car-Nexia')
    )
    key.add(
        InlineKeyboardButton(text='Cobalt',callback_data='car-Cobalt'),
        InlineKeyboardButton(text='Matiz',callback_data='car-Matiz')
    )
    key.add(
        InlineKeyboardButton(text='Gentra',callback_data='car-Gentra'),
        InlineKeyboardButton(text='Spark',callback_data='car-Spark'),
    )
    key.add(
        InlineKeyboardButton(text='Tracker',callback_data='car-Tracker'),
        
    )
    return key
def color_menu():
    key = InlineKeyboardMarkup()
    key.add(
        InlineKeyboardButton(text='Qora', callback_data='color-Qora'),
        InlineKeyboardButton(text='Oq', callback_data='color-Oq')
    )
    key.add(
        InlineKeyboardButton(text='Yashil', callback_data='color-Yashil'),
        InlineKeyboardButton(text='Qizil', callback_data='color-Qizil')
    )
    key.add(
        InlineKeyboardButton(text='Sariq', callback_data='color-Sariq'),
        InlineKeyboardButton(text='Ko\'k', callback_data='color-Ko\k'),
    )
    return key
# tracker 2
def car_age():
    key = InlineKeyboardMarkup(row_width=1)
    key.add(
        InlineKeyboardButton(text='2000-2007', callback_data='age-2000-2007'),
        InlineKeyboardButton(text='2008-2015', callback_data='age-2008-2015'),
        InlineKeyboardButton(text='2016-2020', callback_data='age-2016-2020'),
        InlineKeyboardButton(text='2021-2023', callback_data='age-2021-2023')
    )
    return key
