from config import *
from flask import *


#cursor.execute(f"UPDATE user_taxi SET balance=10000 WHERE chat_id=674312616")
conn.commit()

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def webhook():
  if request.method == 'POST':
    data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(data)])
    return "OK"
  else:
    return "Hello, this is your Telegrambot's webhook!"




@bot.message_handler(commands=['start'])
def welcome(msg):
    cid = msg.chat.id
    text = msg.text
    b = cursor.execute(f"SELECT * FROM user_check WHERE chat_id={msg.chat.id}")
    if b.fetchone() is None:
        try:
            cursor.execute(f"INSERT INTO user_step(chat_id,step) VALUES({cid},'0')")
            conn.commit()
        except:
            pass
        cursor.execute(f"UPDATE user_step SET step ='null' WHERE chat_id={cid}")
        conn.commit()
        bot.send_message(cid,f"<b>👋 {msg.from_user.first_name} Taxi 607 xush kelibsiz!</b>",reply_markup=viloyat_menu())
    else:
        cursor.execute(f"SELECT * FROM user_check WHERE chat_id={msg.chat.id}")
        user = cursor.fetchone()[2]
        if user=='taxi':
            bot.send_message(cid,f"<b>👋 {msg.from_user.first_name} xush kelibsiz!</b>",reply_markup=taxi_menu())
        else:
            bot.send_message(cid,f"<b>👋 {msg.from_user.first_name} xush kelibsiz!</b>",reply_markup=user_menu())



@bot.message_handler(content_types=['text','contact'])
def custom(msg):
  cid = msg.chat.id
  text = msg.text
  step = user_step(cid)
  try:
    if text=="✉ Oddiy xabar" and cid==ADMIN_ID:
      a = bot.send_message(cid,"<b>Xabar matnini kiriting: </b>")
      bot.register_next_step_handler(a,oddiy_xabar)
    elif text=="✉ Forward xabar" and cid==ADMIN_ID:
      a = bot.send_message(cid,"<b>Xabar matnini yuboring: </b>")
      bot.register_next_step_handler(a,forward_xabar)
    elif text=="➕ Pul qo'shish" and cid==ADMIN_ID:
      a = bot.send_message(cid,f"<b>Hisob to'ldirish uchun: {cid}=5000</b>")
      bot.register_next_step_handler(a,add_money)
    elif text=="➖ Pul ayirish" and cid==ADMIN_ID:
      a = bot.send_message(cid,f"<b>Hisob ayirish uchun: {cid}=5000</b>")
      bot.register_next_step_handler(a,minus_money)
    elif text=="◀ Bosh menu":
      cursor.execute(f"SELECT * FROM user_check WHERE chat_id={msg.chat.id}")
      user = cursor.fetchone()[2]
      if user=='taxi':
          bot.send_message(cid,f"<b>👋 {msg.from_user.first_name} xush kelibsiz!</b>",reply_markup=taxi_menu())
      else:
          bot.send_message(cid,f"<b>👋 {msg.from_user.first_name} xush kelibsiz!</b>",reply_markup=user_menu())
    elif text=='📁 Baza yuklash':
     bot.send_document(cid,open('database.db','rb'))
    
  except Exception as e:
    print(e)
    
  try:
    if text=='/panel' and cid==ADMIN_ID:
      bot.send_message(cid,"<b>Admin panelga xush kelibsiz!</b>",reply_markup=admin_panel())
    if text == "🔍 Taxi izlash":
        bot.send_message(cid,"<b>👇 Siz qayerdasiz? </b>",reply_markup=tuman_menu())
    if text=="📊 Statistika":
      taxi = cursor.execute("SELECT COUNT(chat_id) FROM user_taxi").fetchone()[0]      
      user = cursor.execute("SELECT COUNT(chat_id) FROM user_data").fetchone()[0]
      txt = f"""<b>
📊 Foydalanuvchilar soni: {taxi+user}ta

🚖 Haydovchilar: {taxi}ta
👤 Yolovchilar: {user}ta

<i>🔥 Eng tezkor va ishonchi taxi partal!</i>
</b>
      """ 
      bot.send_message(cid,txt,reply_markup=admin_menu2())
    if text=="👤 Kabinet":
        cursor.execute(f'SELECT * FROM user_check WHERE chat_id={cid}')
        json = cursor.fetchone()[2]
        if json=='user':
            cursor.execute(f"SELECT * FROM user_data WHERE chat_id={cid}")
            i = cursor.fetchone()
            text = f"<b>🆔 User id: {i[0]}\n👤 Ismingiz: {i[2]}\n☎ Raqamingiz: +{i[3]}\n\nSavol va taklif uchun 👇</b>"
            bot.send_message(cid,text,reply_markup=admin_menu1())
        else:
            cursor.execute(f"SELECT * FROM user_taxi WHERE chat_id={cid}")
            i = cursor.fetchone()
            txt = F"""<b>
🆔 Taxi id: {i[0]}
👤 Ismingiz: {i[2]}
☎ Raqamingiz: +{i[3]}
💵 Hisobingiz: {i[4]} uzs

🚖 Avtomabil haqida
🖼 Modeli: {i[5]}
🟥 Rangi : {i[6]}


↗ Yo'nalish: {i[7]}

Savol va taklif uchun 👇</b>
"""
          
      
  

              
        bot.send_message(cid,txt,reply_markup=admin_menu())
    if text=="➕ Elon berish":
      cursor.execute(f"SELECT * FROM user_taxi WHERE chat_id={cid}")
      if(cursor.fetchone()[7]=="Nomalum"):
        bot.send_message(cid,"<b>Siz qaysi viloyatdan yo'lovchi olmoqchisiz?</b>",reply_markup=tumanlar_menu())
      else:
        bot.send_message(cid,"<b>☹️ Sizda faol elon mavjud!</b>",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🗑 Eloni o'chirish",callback_data=f'elon-del')))
    if text=="➕ Elon joylash":
      cursor.execute(f"SELECT * FROM elonlar WHERE chat_id={cid}")
      if(cursor.fetchone() is None):
        b = bot.send_message(cid,"<b>Qayerga borishingizni yozib yuboring!\n\nNaumna : Urganch sh 🔜 Yangiariq</b>")
        bot.register_next_step_handler(b,user_elon)
      else:
        bot.send_message(cid,"<b>☹️ Sizda faol elon mavjud!</b>",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🗑 Eloni o'chirish",callback_data=f'delelon')))
    if text=="📔 Elonlar":
      alll = cursor.execute(f"SELECT * FROM elonlar").fetchall()
      #print(alll)
      if(len(alll)==0):
        bot.reply_to(msg,"😔 Yo'lovchilar elon joylamagan!")
      else:
        for i in alll:
          try:
            b = cursor.execute(f"SELECT * FROM user_data WHERE chat_id={i[1]}").fetchone()
            
          
          
            bot.send_message(cid,f"""
<b>🆔 Userid: {b[0]}
👤 Ismi: {b[2]}
☎️ Raqami: +{b[3]}

↗️ Borishi kerak: {i[2]}
</b>
""")
          except Exception as e:
            print(e)
          
    if step=='taxi-name':
        if len(text.split())!=2:
            bot.send_message(cid,"<b>🚫 Kechirasiz ismingiz qoniqarsiz!\n\nNamuna: <i>Aliyev Vali</i></b>")
        else:
            USER_NAME[str(cid)]=text
            cursor.execute(f"UPDATE user_step SET step ='taxi-number' WHERE chat_id={cid}")
            conn.commit()
            bot.send_message(cid,"<b>✅ Raxmat ismingiz qabul qilindi!\n\n👇 Endi telefon raqamingizni yuboring!</b>",reply_markup=number_menu())
    if step=='user-name':
        if len(text.split())!=2:
            bot.send_message(cid,"<b>🚫 Kechirasiz ismingiz qoniqarsiz!\n\nNamuna: <i>Aliyev Vali</i></b>")
        else:
            USER_NAME[str(cid)]=text
            cursor.execute(f"UPDATE user_step SET step ='user-number' WHERE chat_id={cid}")
            conn.commit()
            bot.send_message(cid,"<b>✅ Raxmat ismingiz qabul qilindi!\n\n👇 Endi telefon raqamingizni yuboring!</b>",reply_markup=number_menu())
    if step=='taxi-number':
        if msg.contact:
            num = str(msg.contact.phone_number).replace("+","")
            USER_NUMBER[str(cid)]=num
            bot.send_message(cid,"<b>✅ Raxmat raqam qabul qilindi!\n\n👇 Endi avtomabil model tanlang!</b>",reply_markup=cars_menu())
        else:
            bot.send_message(cid,"<b>👇 Kechirasiz pastdagi tugmadan foydalaning!</b>",reply_markup=number_menu())

    if step=='user-number':
        if msg.contact:
            num = msg.contact.phone_number
            name = USER_NAME[str(cid)]
            name = name.replace("'", "''")
            bot.send_message(cid,"<b>✅ Siz muofaqiyatli ro'yxatdan o'tdingiz!!\n</b>",reply_markup=user_menu())
            cursor.execute(f"UPDATE user_step SET step ='null' WHERE chat_id={cid}")
            cursor.execute(f"INSERT INTO user_check(chat_id,type) VALUES({cid},'user')")
            cursor.execute(f"""INSERT INTO user_data(chat_id,user_name,user_number) VALUES({cid},"{name}",'{num}')""")
            conn.commit()
        else:
            bot.send_message(cid,"<b>👇 Kechirasiz pastdagi tugmadan foydalaning!</b>",reply_markup=number_menu())
  except Exception as e:
    print(e)
            


def set_narx(msg):
  cid = msg.chat.id
  b = NEW_B[str(cid)]
  a = A_MAP[str(cid)]
  m = str(a+" | "+b).replace("'","")
  if(msg.text.isdigit() and int(msg.text)>3):
    try:
      cursor.execute(f"UPDATE user_taxi SET yoli='{m}' WHERE chat_id={cid}")
      cursor.execute(f"UPDATE user_taxi SET narx={int(msg.text)} WHERE chat_id={cid}")
      conn.commit()
      bot.reply_to(msg,f"<b>✅ {a} - {b} e'lon berildi!</b>",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🗑 Eloni o'chirish",callback_data=f'elon-del')))
    except Exception as e:
      print(e)
      bot.reply_to(msg,"<b>Siz xato qiymat kiritingiz!</b>",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🗑 Eloni o'chirish",callback_data=f'elon-del')))


@bot.message_handler(content_types=['location'])
def location(msg):
  taxi_id = LOCATION[str(msg.chat.id)]  
  mid = LOCATION_ID[str(msg.chat.id)]
  lat,long = msg.location.latitude, msg.location.longitude
  bot.reply_to(msg,"<b>Raxmat qabul qildindi!</b>",reply_markup=user_menu())
  try:
    bot.send_location(taxi_id,lat,long,reply_to_message_id=mid)
  except Exception as e:
    print(e)
  


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    cid = call.message.chat.id
    data = call.data
    mid  = call.message.id
    print(data)
    if data=='card':
    
      txt = """<b>
📋 To'lov tizimi: CARD

💳 Hamyonlar:


Humo: <code>TEST NO CARD</code>
Uzcard: <code>TEST NO CARD</code>

Hamyon egasi: <code> TEST NO NAME</code>

To'lov chekini : @Akhatkulov'ga yuboring!
⚠️ To'lovingiz 15-25 daqiqa ichida ko'rib chiqiladi.</b>
"""
    try:
      bot.edit_message_text(txt,cid,mid,reply_markup=admin_menu1())
    except Exception as e:
      print(e)

    if 'register' in data:
        user_type = data.split('-')[1]
        if user_type=='taxi':
            cursor.execute(f"UPDATE user_step SET step ='taxi-name' WHERE chat_id={cid}")
            conn.commit()
            bot.edit_message_text("<b>Iltimos ismingizni yuboring!\n\nNamuna: <i>Aliyev Vali</i></b>",cid,mid)
        else:
            cursor.execute(f"UPDATE user_step SET step ='user-name' WHERE chat_id={cid}")
            conn.commit()
            bot.edit_message_text("<b>Iltimos ismingizni yuboring!\n\nNamuna: <i>Aliyev Vali</i></b>",cid,mid)
    elif 'car' in data:
        car = data.split('-')[1]
        CAR_NAME[str(cid)]=car
        bot.edit_message_text(f"<b>✅ {car} qabul qilindi!\n\n<i>Endi rangini tanlang!</i></b>",cid,mid,reply_markup=color_menu())
    elif 'color' in data:
        color = data.split('-')[1]
        CAR_COLOR[str(cid)]=color

        num = USER_NUMBER[str(cid)]
        name = USER_NAME[str(cid)]
        color = CAR_COLOR[str(cid)]
        car  = CAR_NAME[str(cid)]
        yol  = "Nomalum"
        try:
          cmoney = cursor.execute(f"SELECT * FROM face_phone WHERE phone={num}").fetchone()
        except Exception as e:
          print(e)
        if cmoney is None:
          money = 10000
          cursor.execute(f"INSERT INTO face_phone(phone) VALUES({num})")
          conn.commit()
          bot.send_message(cid,"<b>🎁 Siz birinchi botga tashrif buyurganingiz uchun 10.000 uzs hisobingizga qo'shildi!</b>")
        else:
          bot.send_message(cid,"<b>✅ Siz oldin ro'yxatdan otgansiz !</b>")
          money = 0
        cursor.execute(f"UPDATE user_step SET step ='null' WHERE chat_id={cid}")
        cursor.execute(f"INSERT INTO user_check(chat_id,type) VALUES({cid},'taxi')")
        cursor.execute(f"""INSERT INTO user_taxi(chat_id,user_name,user_number,balance,car_name,car_color,yoli,narx) VALUES({cid},"{name}",'{num}',{money},'{car}','{color}',"{yol}",{0})""")
        conn.commit()
        bot.delete_message(cid,mid)
        bot.send_message(cid,f"<b>✅ Haydovchi siz ro'yxatdan o'tdingiz!!</b>",reply_markup=taxi_menu())
    elif 'map-' in data:
        joy = data.split('-')[1]
        A_MAP[str(cid)]=joy
        bot.edit_message_text(f"<b>✅ {joy} qabul qilindi!\n\n<i>Siz qaysi tumanga borasiz ?</i></b>",cid,mid,reply_markup=tumanlar_menu1(joy))
    elif 'success-' in data:
      taxi_info = cursor.execute(f"SELECT * FROM user_taxi WHERE chat_id={cid}").fetchone()
      if taxi_info[4]>=500:
        sums = taxi_info[4]-500
        cursor.execute(f"UPDATE user_taxi SET balance={sums} WHERE chat_id={cid}")
        conn.commit()
        okey = data.split('-')[1]
        bot.delete_message(cid,mid)
        user_info = cursor.execute(f"SELECT * FROM user_data WHERE chat_id={okey}").fetchone()
       
        # print(taxi_info)
        try:
          bot.send_message(taxi_info[1],f"<b>🔔 Sizga yangi buyurtma! \n\nIsmi: {user_info[2]}\nRaqami:  +{user_info[3]}\nYo'nalish: {taxi_info[-1]}</b>",reply_markup=taxi_menu())
        except Exception as e:
          print(e)
        bot.send_message(okey,f"<b>✅ Haydovchi qabul qildi!</b>",reply_markup=user_menu())
      else:
        bot.answer_callback_query(call.id,"Kechirasiz sizningi hisobingiz yetarli emas!",show_alert=True)
    elif 'not-' in data:
      bot.delete_message(cid,mid)
      okey = data.split('-')[1]
      bot.send_message(okey,f"<b>❌ Haydovchi bekor qildi!</b>",reply_markup=user_menu())
  
    elif data=="delelon":
      bot.edit_message_text("<b>✅ Eloningiz o'chirildi!</b>",cid,mid)
      cursor.execute(f"DELETE FROM elonlar WHERE chat_id={cid}")
      conn.commt()
    elif data=='xorazim':
      try:
        bot.edit_message_text(f"<b>👋 {call.message.from_user.first_name}  xush kelibsiz!\n\n<i>Iltimos ro'yxatdan o'ting!</i></b>",cid,mid,reply_markup=user_register_menu())
      except Exception as e:
        print(e)
    elif 'order' in data:
      id = data.split('-')[1]
      bot.delete_message(cid,mid)
      bot.send_message(cid,f"<b>✅ Haydovchiga malumot yuborildi!\n\nIltimos locatsiya ham yuboring!</b>",reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("📍 Yuborish",request_location=True)))
      
      user_info = cursor.execute(f"SELECT * FROM user_data WHERE chat_id={cid}").fetchone()
      taxi_info = cursor.execute(f"SELECT * FROM user_taxi WHERE id={id}").fetchone()
      print(taxi_info)
      try:
        B = bot.send_message(taxi_info[1],f"<b>🔔 Sizga yangi buyurtma! \n\nIsmi: {user_info[2]}\nRaqami:  +998xxxxxx\nYo'nalish: {taxi_info[7]}</b>\n<i>Qabul qilganingizdan keyin sizga raqami yuboriladi!</i>",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Qabul qilish",callback_data=f'success-{cid}'),InlineKeyboardButton("❌ Bekor qilish",callback_data=f'not-{cid}'))).message_id
        LOCATION[str(cid)]=taxi_info[1]
        LOCATION_ID[str(cid)]=B
      except Exception as e:
        print(e)
    elif 'c-' in data:
        NEW_B[str(cid)] = data.split('-')[1]
        b = bot.edit_message_text(f"<b>✅ Iltimos yo'l haqini yuboring!\nNamuna: 10000</b>",cid,mid)
        bot.register_next_step_handler(b,set_narx)
        
  
    elif 'a-' in data :
        a = data.split('-')[1]
        A_MAP[str(cid)]=a
        bot.edit_message_text(f"<b>✅ {a} qabul qilindi!\n\n<i>Bormoqchi bo'lgan joy ?</i></b>",cid,mid,reply_markup=tuman_menu1(a))
    
    elif 'b-' in data :
        b = data.split('-')[1]
        a = A_MAP[str(cid)]
        m = str(a+" | "+b).replace("'","")
        cursor.execute(f""" SELECT * FROM user_taxi WHERE yoli="{m}" """)
        json = cursor.fetchall()
        if len(json)<1:
            bot.answer_callback_query(call.id,"😥 Kechirasiz haydovchilar mavjud emas!",show_alert=True)
        else:
            key = InlineKeyboardMarkup()
            for k in json:
                print(json)
                cursor.execute(f"SELECT * FROM user_taxi WHERE id={k[0]}")
                i = cursor.fetchone()
                print(i)
                txt = F"""<b>
🆔 Taxi id: {i[0]}
👤 Ismi : {i[2]}
☎ Raqami : +{i[3]}

🚖 Avtomabil haqida
🖼 Modeli: {i[5]}
🟥 Rangi : {i[6]}
💰 Yo'l xaqi: {i[8]} uzs

↗ Yo'nalish: {i[7]}
</b>
                """
                bot.send_message(cid,txt,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Buyurtma berish",callback_data=f'order-{i[0]}')))
  
    elif data=='del':
      bot.edit_message_text("<b>Malumotingiz o'chirilsinmi? </b>",cid,mid,reply_markup=del_menu())
    elif data=='elon-del':
      bot.delete_message(cid,mid)
      bot.send_message(cid,"<b>✅ Sizning eloningiz o'chirildi!\n\nSiz yana elon berishingiz mumkun!</b>")
      cursor.execute(f"UPDATE user_taxi SET yoli='Nomalum' WHERE chat_id={cid}")
      conn.commit()
    elif data=='ha':
      try:
        cursor.execute(f"DELETE FROM user_taxi WHERE chat_id={cid}")
      except:
        pass
      try:
        cursor.execute(f"DELETE FROM user_data WHERE chat_id={cid}")
      except:
        pass
      try:
        cursor.execute(f"DELETE FROM user_step WHERE chat_id={cid}")
      except Exception as e:
        print(e)
      try:
        cursor.execute(f"DELETE FROM user_check WHERE chat_id={cid}")
      except Exception as e:
        print(e)
      
      conn.commit()
      bot.delete_message(cid,mid)
      bot.send_message(cid,"<b>Ma'lumotingiz o'chirildi!\n\nstart /start</b>",reply_markup=ReplyKeyboardRemove())

try:
  
  @bot.shipping_query_handler(func=lambda query: True)
  def shipping(shipping_query):
      print(shipping_query)
      bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')
  
  
  @bot.pre_checkout_query_handler(func=lambda query: True)
  def checkout(pre_checkout_query):
      bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                    error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                  " try to pay again in a few minutes, we need a small rest.")
  
  
  @bot.message_handler(content_types=['successful_payment'])
  def got_payment(message):
      bot.send_message(message.chat.id,
                       'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                       'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                           message.successful_payment.total_amount / 100, message.successful_payment.currency),
                       parse_mode='Markdown')
  
except Exception as e:
  print(e)
print(bot.get_me())
try:
  bot.infinity_polling()
except:
  bot.polling()
#app.run(host='0.0.0.0',port=81)
