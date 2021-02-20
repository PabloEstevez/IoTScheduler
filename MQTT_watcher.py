from DeviceController import on_off
import paho.mqtt.subscribe as subscribe

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload.decode("utf-8")))
    on_off("motor",message.payload.decode("utf-8"))

subscribe.callback(on_message_print, "test", hostname="riego.local")