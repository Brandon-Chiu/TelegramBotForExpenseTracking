import os
import telebot
import mysql.connector

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)
my_db = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), passwd=os.getenv('mySQL'), database=os.getenv('database'))


# Check if connections are established
print(bot.get_me())
print(my_db)

if (my_db):
    print("GOOD!")
else:
    print("FAILED")

# Creating cursor for MySQL
my_cursor=my_db.cursor()


@bot.message_handler(commands=['test']) # reply format
def test1(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['testing']) # send format
def test2(message):
  bot.send_message(message.chat.id, "Halo!")

@bot.message_handler(commands=['start'])
def test1(message):
  bot.reply_to(message, "Welcome!")
  my_cursor.execute("Select userId From users")
  my_result=my_cursor.fetchall()


  for i in my_result:
      if i[0] == message.from_user.id:
          bot.send_message(message.chat.id, "You are an existing user!")
          break
  else:
      my_cursor.execute("Insert into users values (%s)", (message.from_user.id,))
      my_db.commit()
      bot.send_message(message.chat.id, "You are new user!")

@bot.message_handler(commands=['add'])
def add(message):
  echo_message(message)
  user_input = message.text.split()
  if len(user_input) == 2:

    # code to push amount to the correct category

    bot.reply_to(message, "$" + display_amount(user_input[1]) + " added to " "{TO-FILL}")

  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['add_category'])
def test1(message):
    user_input = message.text.split()
    print(user_input)
    if len(user_input) == 2:
        # make sure new category is not present
        my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
        my_result = my_cursor.fetchall()
        for i in my_result:
            if i[0] == user_input[1]:
                bot.reply_to(message, user_input[1] + " category is already present!")
                break
        # code to add new category
        else:
            my_cursor.execute("Insert into categories values (%s, %s)", (message.from_user.id, user_input[1]))
            my_db.commit()
            bot.reply_to(message, user_input[1] + " category added successfully!")

            # Display category
            bot.reply_to(message, "Fetching all categories. Please wait!")
            my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
            my_result = my_cursor.fetchall()
            output = ""
            for i in my_result:
                output += i[0] + "; "
            output = output[:-2]
            bot.reply_to(message, "Current list of categories: " + output)
    else:
        bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['view_category'])
def test1(message):
    bot.reply_to(message, "Fetching all categories. Please wait!")
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_result = my_cursor.fetchall()
    output= ""
    for i in my_result:
        output += i[0] + "; "
    output= output[:-2]
    bot.reply_to(message, "Current list of categories: " + output)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
  cid = message.chat.id
  mid = message.message_id
  message_text = message.text
  user_id = message.from_user.id
  user_name = message.from_user.first_name
  print(message_text)
  print(user_id)


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

bot.polling()
