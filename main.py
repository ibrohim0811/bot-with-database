import asyncio
import logging
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import types


TOKEN = "8260223409:AAEJsckweSzRwJHW9ElLaAy1u_4lP5yen4U"
bot = Bot(token=TOKEN)

dp = Dispatcher()
PATH = 'bot/users.db'

def create():
    conn = sqlite3.connect(PATH)
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(500),
    username VARCHAR(100) UNIQUE,
    telegram_id INT,
    time DATE
)
                """)
    conn.commit()
    conn.close()

def save(firstname, username, t_id, time):
    conn = sqlite3.connect(PATH)
    cur = conn.cursor()
    
    try:
        query = "INSERT INTO users(first_name, username,  telegram_id, time) VALUES ( ?, ?, ?, ?)"
        cur.execute(query,(firstname, username,  t_id, time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return None      
    
def delete_(username):
    conn = sqlite3.connect(PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?",(username, ))
    conn.commit()
    conn.close()
        
create()
@dp.message(CommandStart())
async def start(msg: types.Message):
    firstname = msg.from_user.first_name
    username = msg.from_user.username
    u_id = msg.from_user.id
    sucsess = save(firstname, username, u_id, datetime.now())
    
    if sucsess:
        await msg.answer(f"Salom 👋 {username} siz bazaga qoshildingiz ✅")
    else:
        await msg.answer(f" @{msg.from_user.username} Allaqachon bazada mavjud 🙂")
        
@dp.message(Command("delete"))
async def delete(msg: types.Message):
    username = msg.from_user.username
    delete_(username)
    await msg.answer("Siz bazadan o'chirildiz 🗑️")

async def main() -> None:
    

    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot ishga tushdi...")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
