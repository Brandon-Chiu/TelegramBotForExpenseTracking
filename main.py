import os
import telebot
import mysql.connector
import datetime

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
  bot.reply_to(message, "Welcome! :)")
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
  is_category_present = False
  user_input = message.text.split()
  if len(user_input) == 3:
    # code to push amount to the correct category
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_result = my_cursor.fetchall()
    for i in my_result:
        if i[0].lower() == user_input[2].lower():
            is_category_present = True
            break
    else:
        bot.reply_to(message, "Category selected is not present in the database! Kindly add the new category before proceeding to add new expenses.")

    if is_category_present:
        my_cursor.execute("Insert into expenses values (%s, %s, %s, %s)", (datetime.datetime.now(), float(display_amount(user_input[1])), user_input[2], message.from_user.id))
        my_db.commit()
        bot.reply_to(message, "$" + display_amount(user_input[1]) + " added to " + user_input[2])

  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['remove'])
def add(message):
  is_category_present = False
  user_input = message.text.split()
  if len(user_input) == 3:
    # code to push amount to the correct category
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_result = my_cursor.fetchall()
    for i in my_result:
        if i[0].lower() == user_input[2].lower():
            is_category_present = True
            break
    else:
        bot.reply_to(message, "Category selected is not present in the database! Kindly add the new category before proceeding to add new expenses.")

    if is_category_present:
        my_cursor.execute("Insert into expenses values (%s, %s, %s, %s)", (datetime.datetime.now(), -float(display_amount(user_input[1])), user_input[2], message.from_user.id))
        my_db.commit()
        bot.reply_to(message, "$" + display_amount(user_input[1]) + " removed from " + user_input[2])

  else:
    bot.reply_to(message, "Invalid input! Please try again.")

@bot.message_handler(commands=['add_category'])
def test1(message):
    user_input = message.text.split()
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

@bot.message_handler(commands=['remove_category'])
def test1(message):
    user_input = message.text.split()
    if len(user_input) == 2:
        my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
        my_result = my_cursor.fetchall()
        my_cursor.execute("Delete From categories Where userId = (%s) And category = (%s)", (message.from_user.id, user_input[1]))
        my_db.commit()
        removed = False
        for i in my_result:
            for k in i:
                if k.lower() == user_input[1].lower():
                    removed = True
                    break
        if removed:
            bot.reply_to(message, user_input[1] + " removed from category")

            bot.reply_to(message, "Fetching all categories. Please wait!")
            my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
            my_result = my_cursor.fetchall()
            output = ""
            for i in my_result:
                output += i[0] + "; "
            output = output[:-2]
            bot.reply_to(message, "Current list of categories: " + output)
        else:
            bot.reply_to(message, user_input[1] + " not present in category")

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


@bot.message_handler(commands=['display_all'])
def test1(message):
    my_cursor.execute("Select * From expenses where userId = (%s)", (message.from_user.id,))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_amount_breakdown(my_result, my_category)
    bot.reply_to(message, "Breakdown of total expenses: \n" + output)

@bot.message_handler(commands=['display_current_week'])
def test1(message):
    current_day = datetime.datetime.today().weekday()
    my_cursor.execute("Select * From expenses where userId = (%s) and time >= (%s)", (message.from_user.id, get_starting_date_for_week(current_day)))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_amount_breakdown(my_result, my_category)
    bot.reply_to(message, "Breakdown of current week expenses: \n" + output)

@bot.message_handler(commands=['display_current_month'])
def test1(message):
    current_date = datetime.datetime.now()
    my_cursor.execute("Select * From expenses where userId = (%s) and time >= (%s)", (message.from_user.id, datetime.datetime(current_date.year, current_date.month, 1)))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_amount_breakdown(my_result, my_category)
    bot.reply_to(message, "Breakdown of current month expenses: \n" + output)

@bot.message_handler(commands=['display_all_log'])
def test1(message):
    my_cursor.execute("Select * From expenses where userId = (%s)", (message.from_user.id,))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_log(my_result, my_category)
    bot.reply_to(message, "Expenses history: \n" + output)

@bot.message_handler(commands=['display_current_month_log'])
def test1(message):
    current_date = datetime.datetime.now()
    my_cursor.execute("Select * From expenses where userId = (%s) and time >= (%s)", (message.from_user.id, datetime.datetime(current_date.year, current_date.month, 1)))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_log(my_result, my_category)
    bot.reply_to(message, "Expenses history: \n" + output)

@bot.message_handler(commands=['display_current_week_log'])
def test1(message):
    current_day = datetime.datetime.today().weekday()
    my_cursor.execute("Select * From expenses where userId = (%s) and time >= (%s)", (message.from_user.id, get_starting_date_for_week(current_day)))
    my_result = my_cursor.fetchall()
    my_cursor.execute("Select category From categories where userId = (%s)", (message.from_user.id,))
    my_category = my_cursor.fetchall()
    output = display_log(my_result, my_category)
    bot.reply_to(message, "Expenses history: \n" + output)

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

def caps_first_letter(word):
    return word[0].upper() + word[1:]

def get_starting_date_for_week(num):
    current_time = datetime.datetime.today()
    if current_time.day - num > 0:
        return datetime.datetime(current_time.year, current_time.month, current_time.day - num)
    elif current_time.month - 1 > 0:
        num -= current_time.day
        return datetime.datetime(current_time.year, current_time.month - 1, number_of_days(current_time.year, current_time.month - 1) - num)
    else:
        num -= current_time.day
        return datetime.datetime(current_time.year - 1, 12, number_of_days(current_time.year - 1, 12) - num)

def number_of_days(y, m):
    leap = 0
    if y% 400 == 0:
        leap = 1
    elif y % 100 == 0:
        leap = 0
    elif y% 4 == 0:
        leap = 1
    if m==2:
        return 28 + leap
    list = [1,3,5,7,8,10,12]
    if m in list:
        return 31
    return 30

def display_log(my_result, my_category):
    result = {}
    amount = {}
    for i in my_category:
        result[i[0].lower()] = "\n"
        amount[i[0].lower()] = 0
    for i in my_result:
        result[i[2].lower()] += "Date: " + i[0].strftime("%d/%m/%y") + "; Category: " + i[
            2] + "; Amount: " + display_amount(str(i[1])) + "\n"
        amount[i[2].lower()] += i[1]
    total_amount = 0
    for values in amount.values():
        total_amount += values
    output = "Total amount: $" + display_amount(str(total_amount)) + "\n"
    for key, value in result.items():
        output += "\n***" + caps_first_letter(key) + "***" + str(value) + "Total: " + display_amount(
            str(amount[key])) + "\n"
    return output

def display_amount_breakdown(my_result, my_category):
    result = {}
    for i in my_category:
        result[i[0].lower()] = 0
    for i in my_result:
        result[i[2].lower()] += i[1]
    total_amount = 0
    for values in result.values():
        total_amount += values
    output = "Total amount: $" + display_amount(str(total_amount)) + "\n\n"
    for key, value in result.items():
        output += caps_first_letter(key) + ": " + str(value) + "\n"
    return output

bot.polling()