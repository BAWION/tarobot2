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

def get_prediction(prompt, max_tokens=300):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def send_partial_response(chat_id, prediction):
    partial_response = prediction[:int(len(prediction) * 0.4)]
    bot.send_message(chat_id, partial_response)
    bot.send_message(chat_id, "Чтобы получить полный ответ, отправьте 50 рублей. [Ссылка на оплату]")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-предсказатель. Чтобы получить предсказание, зарегистрируйся командой /register")

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

    msg = bot.send_message(message.chat.id, "Какой у тебя знак зодиака?")
    bot.register_next_step_handler(msg, process_zodiac_step, user_id)


