import sqlite3

conn = sqlite3.connect('database.db',
                       check_same_thread=False,
                       isolation_level=None)
cursor = conn.cursor()

cursor.execute(
  "CREATE TABLE IF NOT EXISTS user_taxi(id INTEGER PRIMARY KEY,chat_id INTIGER,user_name TEXT,user_number text,balance INT,car_name TEXT,car_color TEXT,yoli TEXT,narx INT)"
)
cursor.execute(
  "CREATE TABLE IF NOT EXISTS face_phone(id INTEGER PRIMARY KEY,phone INT)"
)
cursor.execute(
  "CREATE TABLE IF NOT EXISTS user_data(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,user_name TEXT,user_number TEXT)"
)

cursor.execute(
  "CREATE TABLE IF NOT EXISTS user_check(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,type TEXT)"
)

cursor.execute(
  "CREATE TABLE IF NOT EXISTS user_step(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,step TEXT)"
)

cursor.execute(
  "CREATE TABLE IF NOT EXISTS elonlar(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,yol TEXT)"
)

conn.commit()

