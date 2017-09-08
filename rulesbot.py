
# coding: utf-8

import telebot
from telebot import types
import requests
import random
import logging
import operator


TOKEN = "<BOT-TOKEN>"
bot = telebot.TeleBot(TOKEN)
rules_dict = {'rule': None, 'user': None}
#telebot.logger.setLevel(logging.DEBUG)
#arreglar que sea exactamente la palabra
user_dict = {}



class Rules():
    def __init__(self):
        self.Prohibidas = []
        self.Recomendables = []
        self.Usuarios = {}



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hola grupo. Este es el bot de osfo a todas")
    rules = Rules()
    chat_id = message.chat.id
    user_dict[chat_id] = rules



@bot.message_handler(commands=['newrule'])
def new_rule(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Prohibido', 'Permitido', 'Recomendable')
    msg = bot.reply_to(message, '¿Que regla quieres aplicar?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_rule_selection)

def process_rule_selection(message):
    chat_id = message.chat.id
    rule = message.text
    rules_dict['rule'] = rule
    rules_dict['user'] = message.from_user.first_name
    chat_type = message.chat.type
    if chat_type == u'group':
        selective = True
    else:
        selective = False
    
    if rule == u'Prohibido':
        msg = bot.send_message(chat_id, '¿que palabra vas a prohibir?',reply_markup=types.ReplyKeyboardRemove(selective=selective))
        bot.register_next_step_handler(msg, process_rules)
        return
    if rule == u'Permitido':
        msg = bot.send_message(chat_id, '¿que palabra vas a permitir?',reply_markup=types.ReplyKeyboardRemove(selective=selective))
        bot.register_next_step_handler(msg, remove_rules)
        return
    if rule == u'Recomendable':
        msg = bot.send_message(chat_id, '¿que palabra es recomendable usar?',reply_markup=types.ReplyKeyboardRemove(selective=selective))
        bot.register_next_step_handler(msg, process_rules)
        return
    
def process_rules(message):
    try:
        if str(message.from_user.first_name) == str(rules_dict['user']):
            chat_id = message.chat.id
            rules = user_dict[chat_id]
            word = message.text
            bot.reply_to(message, 'Vale, entendido',reply_markup=types.ReplyKeyboardRemove(selective=False))
            if rules_dict['rule'] == "Prohibido":
                rules.Prohibidas.append(word)
            if rules_dict['rule'] == "Recomendable":
                rules.Recomendables.append(word)
        else:
            msg = bot.reply_to(message, 'No te cueles, que lo diga {}'.format(rules_dict['user']), reply_markup=types.ReplyKeyboardRemove(selective=False))
            bot.register_next_step_handler(msg, process_rule)
            return
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Please, use /start command before', parse_mode='Markdown')

def remove_rule(message):
    chat_id = message.chat.id
    word = message.text
    try:
        Prohibidas.remove(word)
    except:
        bot.reply_to(message, 'Esa palabra no está prohibida')
    bot.reply_to(message, 'Vale, entendido')


@bot.message_handler(commands=['rules'])
def getRules(message):
    try:
        chat_id = message.chat.id
        rules = user_dict[chat_id]
        rlist = "*Prohibidas*: \n"
        for rule in rules.Prohibidas:
            rlist += "- " + rule + "\n"
        rlist += "\n*Recomendables*: \n"
        for rule in rules.Recomendables:
            rlist += "- " + rule + "\n"
        bot.send_message(chat_id, rlist, parse_mode='Markdown')
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Please, use /start command before', parse_mode='Markdown')



@bot.message_handler(commands=['rank'])
def getRank(message):
    try:
        chat_id = message.chat.id
        rules = user_dict[chat_id]
        rlist = "*Ranking*: \n"
        sorted_rules = sorted(rules.Usuarios.items(), key=operator.itemgetter(1), reverse=True)
        for user in sorted_rules:
            rlist += user[0] + " --->  " + str(user[1]) + "\n"
        bot.send_message(chat_id, rlist, parse_mode='Markdown')
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Please, use /start command before', parse_mode='Markdown')



@bot.message_handler(func=lambda message: True)
def rules_in_message(message):
    try:
        chat_id = message.chat.id
        rules = user_dict[chat_id]
        user = message.from_user.first_name
        for rule in rules.Prohibidas:
            if rule.lower() in message.text.lower():
                bot.reply_to(message, "Prohibida. -1")
                if not user in rules.Usuarios:
                    rules.Usuarios[user] = 0
                rules.Usuarios[user] += -1
        for rule in rules.Recomendables:
            if rule.lower() in message.text.lower():
                bot.reply_to(message, "Es bien. +1")
                if not user in rules.Usuarios:
                    rules.Usuarios[user] = 0
                rules.Usuarios[user] += +1
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Please, use /start command before', parse_mode='Markdown')


bot.polling()




