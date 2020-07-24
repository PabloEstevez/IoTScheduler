import telebot
import json
import CronScheduler

## CONFIGURATION ##
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
###

## FUNCTIONS ##
def build_command(text):
    command = text.split(" ")
    del(command[0])
    return command
###


## DEFINITIONS ##
bot = telebot.TeleBot(config["telegram_bot"]["token"])
helpMessage = """
/help: Muestra esta ayuda.
/run: Ejecuta el comando que pongas a continuacion.
"""
###


## HANDLERS ##
@bot.message_handler(commands=['schedule','programa'])
def handle_schedule(message):
	pass

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, helpMessage)
###

print("Bot listening...")
bot.polling()