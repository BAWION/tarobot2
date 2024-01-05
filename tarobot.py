import os
import telebot
import openai
import re
from telebot import types

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')

# Убедитесь, что токены были правильно загружены
if not TELEGRAM_TOKEN or not OPENAI_TOKEN:
    raise ValueError("Не удалось загрузить токены. Проверьте настройки переменных окружения.")

# Установка API ключа для OpenAI
openai.api_key = OPENAI_TOKEN

# Инициализация бота Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

users = {}

def safe_send_message(chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except telebot.apihelper.ApiTelegramException as e:
        if e.result.status_code == 403:
            print(f"Не удалось отправить сообщение пользователю {chat_id}: пользователь заблокировал бота")
        else:
            raise e

def get_prediction(prompt, max_tokens=300):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

@bot.message_handler(commands=['start'])
def start(message):
    safe_send_message(message.chat.id, "Привет! Я бот-предсказатель. Чтобы получить предсказание, зарегистрируйся командой /register")

@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.send_message(message.chat.id, "Как тебя зовут?")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    user_id = message.chat.id
    name = message.text
    if not re.match("^[а-яА-ЯёЁa-zA-Z]+$", name):
        msg = bot.send_message(message.chat.id, "Пожалуйста, введи корректное имя.")
        bot.register_next_step_handler(msg, process_name_step)
        return
    users[user_id] = {'name': name}
    safe_send_message(message.chat.id, "Какой у тебя знак зодиака?")
    bot.register_next_step_handler_by_chat_id(user_id, process_zodiac_step)

def process_zodiac_step(message):
    user_id = message.chat.id
    zodiac = message.text
    if not re.match("^[а-яА-ЯёЁa-zA-Z]+$", zodiac):
        msg = bot.send_message(message.chat.id, "Пожалуйста, введи корректный знак зодиака.")
        bot.register_next_step_handler(msg, process_zodiac_step)
        return
    users[user_id]['zodiac'] = zodiac
    safe_send_message(message.chat.id, "Отправь фото своей левой ладони для предсказания")
    bot.register_next_step_handler_by_chat_id(user_id, process_photo_step)

def process_photo_step(message):
    user_id = message.chat.id
    if not message.photo:
        msg = bot.send_message(message.chat.id, "Пожалуйста, отправь фото левой ладони.")
        bot.register_next_step_handler(msg, process_photo_step)
        return
    photo_id = message.photo[-1].file_id
    users[user_id]['photo'] = photo_id  

    user = users[user_id]
    prompt = f"Сделайте астрологическое предсказание и предсказание по карте Таро для {user['name']} со знаком зодиака {user['zodiac']} на основе фотографии ладони: {user['photo']}"
    full_prediction = get_prediction(prompt, max_tokens=900) # Увеличиваем количество токенов для более полного ответа
    safe_send_message(message.chat.id, full_prediction)

bot.polling()
