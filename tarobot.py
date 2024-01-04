{\rtf1\ansi\ansicpg1251\cocoartf2757
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import telebot\
from telebot import types\
import openai\
from dotenv import load_dotenv\
import os\
\
# \uc0\u1047 \u1072 \u1075 \u1088 \u1091 \u1079 \u1082 \u1072  \u1087 \u1077 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1099 \u1093  \u1086 \u1082 \u1088 \u1091 \u1078 \u1077 \u1085 \u1080 \u1103  \u1080 \u1079  .env \u1092 \u1072 \u1081 \u1083 \u1072 \
load_dotenv()\
\
# \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1077  \u1090 \u1086 \u1082 \u1077 \u1085 \u1086 \u1074  \u1080 \u1079  \u1087 \u1077 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1099 \u1093  \u1086 \u1082 \u1088 \u1091 \u1078 \u1077 \u1085 \u1080 \u1103 \
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')\
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')\
\
# \uc0\u1059 \u1089 \u1090 \u1072 \u1085 \u1086 \u1074 \u1082 \u1072  \u1082 \u1083 \u1102 \u1095 \u1072  API \u1076 \u1083 \u1103  OpenAI\
openai.api_key = OPENAI_TOKEN\
\
# \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1073 \u1086 \u1090 \u1072 \
bot = telebot.TeleBot(TELEGRAM_TOKEN)\
\
# \uc0\u1057 \u1083 \u1086 \u1074 \u1072 \u1088 \u1100  \u1076 \u1083 \u1103  \u1093 \u1088 \u1072 \u1085 \u1077 \u1085 \u1080 \u1103  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1077 \u1081 \
users = \{\} \
\
@bot.message_handler(commands=['start'])\
def start(message):\
    bot.send_message(message.chat.id, "\uc0\u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1071  \u1073 \u1086 \u1090 -\u1087 \u1088 \u1077 \u1076 \u1089 \u1082 \u1072 \u1079 \u1072 \u1090 \u1077 \u1083 \u1100 . \u1063 \u1090 \u1086 \u1073 \u1099  \u1087 \u1086 \u1083 \u1091 \u1095 \u1080 \u1090 \u1100  \u1087 \u1088 \u1077 \u1076 \u1089 \u1082 \u1072 \u1079 \u1072 \u1085 \u1080 \u1077 , \u1074 \u1074 \u1077 \u1076 \u1080  \u1089 \u1074 \u1086 \u1080  \u1076 \u1072 \u1085 \u1085 \u1099 \u1077  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1086 \u1081  /register.")\
\
@bot.message_handler(commands=['register'])\
def register(message):\
    msg = bot.send_message(message.chat.id, "\uc0\u1042 \u1074 \u1077 \u1076 \u1080  \u1089 \u1074 \u1086 \u1077  \u1080 \u1084 \u1103 :")\
    bot.register_next_step_handler(msg, process_name_step)\
\
def process_name_step(message):\
    user_id = message.chat.id\
    name = message.text\
    users[user_id] = \{'name': name\}\
    \
    msg = bot.send_message(message.chat.id, "\uc0\u1042 \u1074 \u1077 \u1076 \u1080  \u1089 \u1074 \u1086 \u1081  \u1079 \u1085 \u1072 \u1082  \u1079 \u1086 \u1076 \u1080 \u1072 \u1082 \u1072 :")\
    bot.register_next_step_handler(msg, process_zodiac_step, user_id)\
\
def process_zodiac_step(message, user_id):\
    zodiac = message.text\
    users[user_id]['zodiac'] = zodiac\
\
    msg = bot.send_message(message.chat.id, "\uc0\u1054 \u1090 \u1087 \u1088 \u1072 \u1074 \u1100  \u1092 \u1086 \u1090 \u1086  \u1089 \u1074 \u1086 \u1077 \u1081  \u1083 \u1072 \u1076 \u1086 \u1085 \u1080  \u1076 \u1083 \u1103  \u1090 \u1072 \u1088 \u1086  \u1087 \u1088 \u1077 \u1076 \u1089 \u1082 \u1072 \u1079 \u1072 \u1085 \u1080 \u1103 :")\
    bot.register_next_step_handler(msg, process_photo_step, user_id)\
    \
def process_photo_step(message, user_id):\
    # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1092 \u1086 \u1090 \u1086 \u1075 \u1088 \u1072 \u1092 \u1080 \u1080  \u1083 \u1072 \u1076 \u1086 \u1085 \u1080 \
    # ...\
\
# \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1100 \u1090 \u1077  \u1079 \u1076 \u1077 \u1089 \u1100  \u1076 \u1088 \u1091 \u1075 \u1080 \u1077  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080  \u1080  \u1086 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1080 \
\
# \uc0\u1047 \u1072 \u1087 \u1091 \u1089 \u1082  \u1073 \u1086 \u1090 \u1072 \
bot.polling()\
}
