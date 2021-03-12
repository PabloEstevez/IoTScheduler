from DeviceController import on_off,get_devices
import paho.mqtt.client as mqtt

def callback_controller(client, userdata, message):
    print("%s %s" % (message.topic, message.payload.decode("utf-8")))
    on_off(message.topic,message.payload.decode("utf-8"))

mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
MQTT_TOPICS=[]
for device in get_devices():
    mqttc.message_callback_add(device, callback_controller)
    MQTT_TOPICS.append((device,0))

# Connec to MQTT Server and Subscribe to device topics
mqttc.connect("riego.local", 1883, 60)
mqttc.subscribe(MQTT_TOPICS)

mqttc.loop_forever()

