import tokens
from towfm import Wiki, CreateTree, _TextError
import telebot

bot = telebot.TeleBot(tokens.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Welcome user {message.from_user.first_name}, I am a bot that can create a tree from word meanings. Type a random word and the result will be.')

@bot.message_handler(content_types=['text'])
def CWT(message):
    if not(';' in message.text or ':' in message.text or '.' in message.text):
        bot.send_message(message.chat.id, 'Please wait loading.')
        a = CreateTree(message.text)
        b = Wiki(quantity=10)
        b.search(message.text)
        a.add(b.seed, b.list, 'seed')
        for i in a.history_of_knowledge[0]:
            try:
                b.search(i)
                a.add(b.seed, b.list, 'seed')
            except AttributeError:
                continue
        bot.send_message(message.chat.id, f"Here's the result:\nMax level:{a.max_level()}\nMax index:{a.max_index()}\namount of knowledge: {len(a.knowledge)}\nword count: {len(a.tree)}\n")
        bot.send_message(message.chat.id, f'And yes, here is a tree with the NDT type)\n{a.tree_NDT()}')
    else:
        bot.send_message(message.chat.id, _TextError._ValueError1(message.text))

bot.polling(none_stop=True)
