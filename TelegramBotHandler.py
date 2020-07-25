import telebot
import json
import CronScheduler
import DeviceController
import os

## CONFIGURATION ##
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
###


## DEFINITIONS ##
bot = telebot.TeleBot(config["telegram_bot"]["token"])
helpMessage = """
/help: Muestra esta ayuda.
/run: Ejecuta el comando que pongas a continuacion.
"""
inicio = duracion = comentario = device = None 
###


## FUNCTIONS ##
def check_device(device):
    for i in config["devices"]:
        if i == device:
            return True
    return False

def get_devices():
    dev = []
    for i in config["devices"]:
        dev.append(i)
    return dev

def get_tasks():
    tasks = CronScheduler.get_tasks()
    formated = "TAREAS:\n"
    for i in range(len(tasks)):
        job = tasks[i].split("#")
        if len(job) < 2:
            break
        task = job[0].split(" ")
        comment = job[1]
        if "_Inicio" in comment:
            formated += "→ " + comment.replace("_Inicio","") + ": " + task[1] + ":" + task[0] 
        elif "_Final" in comment:
            formated += " - " + task[1] + ":" + task[0] + "\n"
    return formated

def devices2str():
    formated = "DISPOSITIVOS:\n"
    for i in config["devices"]:
        formated += "→ " + i + ": " + config["devices"][i]["description"] + "\n"
    return formated




def input_schedule(message):
    global inicio 
    inicio = message.text
    sent = bot.send_message(message.from_user.id, "Durante cuanto tiempo va a estar encendido? (en minutos)")
    bot.register_next_step_handler(sent, input_duration)
def input_duration(message):
    global duracion 
    duracion = int(message.text)
    sent = bot.send_message(message.from_user.id, "Dime un identificador para la tarea")
    bot.register_next_step_handler(sent, input_comment)
def input_comment(message):
    global comentario
    comentario = message.text
    schedule()
    bot.send_message(message.from_user.id, "Listo!")

def schedule():
    global device
    command_init = "python " + os.getcwd() + "/DeviceController.py --id " + device + " --status on"
    command_final = "python " + os.getcwd() + "/DeviceController.py --id " + device + " --status off"
    CronScheduler.set_task(command_init, command_final, inicio, duracion, comentario, False)
###


## HANDLERS ##
@bot.message_handler(commands=['schedule','programa'])
def handle_schedule(message):
    global device
    text = message.text.split(" ")
    if len(text) > 1:
        device = text[1]
    if check_device(device):
        sent = bot.send_message(message.from_user.id, "Dime la hora de inicio")
        bot.register_next_step_handler(sent, input_schedule)
    else:
        bot.send_message(message.from_user.id, devices2str())

@bot.message_handler(commands=['start','enciende'])
def handle_start(message):
    global device
    text = message.text.split(" ")
    print(text)
    if len(text) > 1:
        device = text[1]
    if check_device(device):
        sent = bot.send_message(message.from_user.id, "Dime la hora de inicio")
        bot.register_next_step_handler(sent, input_schedule)
    else:
        bot.send_message(message.from_user.id, "Los dispositivos disponibles son: " + str(get_devices()))

@bot.message_handler(commands=['tasks', 'tareas'])
def handle_tasks(message):
    bot.send_message(message.from_user.id, get_tasks())

@bot.message_handler(commands=['devices', 'dispositivos'])
def handle_devices(message):
    bot.send_message(message.from_user.id, devices2str)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, helpMessage)
###


print("Bot listening...")
bot.polling()