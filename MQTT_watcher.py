from DeviceController import on_off,get_devices
import paho.mqtt.client as mqtt
import json,os, time

## CONFIGURATION ##
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
###

def callback_controller(client, userdata, message):
    print("%s %s" % (message.topic, message.payload.decode("utf-8")))
    on_off(message.topic,message.payload.decode("utf-8"))

mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
MQTT_TOPICS=[]
for device in get_devices():
    if device != "motor":
        mqttc.message_callback_add(device, callback_controller)
        MQTT_TOPICS.append((device,0))

# Connec to MQTT Server and Subscribe to device topics
check = True
while check:
    try:
        mqttc.connect(config["mqtt"]["server"], config["mqtt"]["port"], config["mqtt"]["keepalive"])
        mqttc.subscribe(MQTT_TOPICS)
        mqttc.loop_forever()
        check=False
    except:
        print("Unable to connect to MQTT broker, retrying...")
        time.sleep(1)

