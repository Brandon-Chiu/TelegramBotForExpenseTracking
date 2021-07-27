import os
import telebot
import telegram.ext

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

print(bot.get_me())

@bot.message_handler(commands=['test']) # reply format
def test1(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['testing']) # send format
def test2(message):
  bot.send_message(message.chat.id, "Halo!")

@bot.message_handler(commands=['add'])
def add(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 2:
    # code to show pre-exisiting category

    # code to push amount to the correct category

    bot.reply_to(message, "$" + display_amount(user_input[1]) + " added to " "{TO-FILL}")

  else:
    bot.reply_to(message, "Invalid input! Please try again.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
  cid = message.chat.id
  mid = message.message_id
  message_text = message.text
  user_id = message.from_user.id
  user_name = message.from_user.first_name
  print(message_text)


def display_amount(amount):
    if "." not in amount:
        return amount + ".00"
    index = 1
    for i in amount:
        if i == ".":
            break
        index += 1
    length=len(amount)
    if length == index + 2:
        return amount
    elif length == index + 1:
        return amount + "0"
    elif length == index:
        return amount + "00"
    else:
        return str(round(float(amount), 2))

@bot.message_handler(commands=['display'])
def display(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 1:
    # code to show breakdown of pre-exisiting category
    print("Testing")
  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['add_category'])
def display(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 2: # to make sure new category is not present
    # code to add new category
    print("Testing")
  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['view_category'])
def display(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 1:
    # code to show breakdown of pre-exisiting category
    print("Testing")
  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['remove_category'])
def display(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 2: # to make sure new category is not present
    # code to remove 1 category
    print("Testing")
  else:
    bot.reply_to(message, "Invalid input! Please try again.")

bot.polling()
