import telebot
import json
import CronScheduler
import DeviceController
import os
import datetime

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
    sent = bot.send_message(message.from_user.id, "¿Quieres que funcione una sola vez?")
    bot.register_next_step_handler(sent, input_ott)
def input_ott(message):
    if message.text.upper() == "YES" or message.text.upper() == "SI":
        ott = True
    else:
        ott = False
    schedule(ott)
    bot.send_message(message.from_user.id, "Listo!")

def schedule(ott):
    global inicio, duracion, comentario, device
    command_init = "python " + os.getcwd() + "/DeviceController.py --id " + device + " --status on"
    command_final = "python " + os.getcwd() + "/DeviceController.py --id " + device + " --status off"
    CronScheduler.set_task(command_init, command_final, inicio, duracion, comentario, ott)
    inicio = duracion = comentario = device = None 
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
    if len(text) > 1:
        device = text[1]
    if check_device(device):
        DeviceController.on_off(device, True)
        bot.send_message(message.from_user.id, "El dispositivo " + device + " se ha encendido")
    else:
        bot.send_message(message.from_user.id, devices2str)

@bot.message_handler(commands=['stop','apaga'])
def handle_stop(message):
    global device
    text = message.text.split(" ")
    if len(text) > 1:
        device = text[1]
    if check_device(device):
        DeviceController.on_off(device, False)
        bot.send_message(message.from_user.id, "El dispositivo " + device + " se ha apagado")
    else:
        bot.send_message(message.from_user.id, devices2str)

@bot.message_handler(commands=['tasks', 'tareas'])
def handle_tasks(message):
    bot.send_message(message.from_user.id, get_tasks())

@bot.message_handler(commands=['ott'])
def handle_ott(message):
    global device, duracion, inicio, comentario
    text = message.text.split(" ")
    if len(text) > 3:
        device = text[1]
        duracion = int(text[2])
        comentario = text[3]
    if check_device(device):
        time = datetime.datetime.now()
        inicio = str(time.hour) + ":" + str(time.minute)
        DeviceController.on_off(device, True)
        bot.send_message(message.from_user.id, "El dispositivo " + device + " se ha encendido y se apagará dentro de " + str(duracion) + " minutos")
        schedule(True)
    else:
        bot.send_message(message.from_user.id, helpMessage)

@bot.message_handler(commands=['devices', 'dispositivos'])
def handle_devices(message):
    bot.send_message(message.from_user.id, devices2str)

@bot.message_handler(commands=['remove', 'delete', 'borra', 'elimina'])
def handle_remove(message):
    text = message.text.split(" ")
    if len(text) < 2:
        bot.send_message(message.from_user.id, get_tasks())
    else:
        id = text[1]
        CronScheduler.remove_task(id)
        bot.send_message(message.from_user.id, get_tasks())

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, helpMessage)
###


print("Bot listening...")
try:
    bot.polling()
except:
    bot.send_message(config["telegram_bot"]["my_id"], "The bot crashed :(")