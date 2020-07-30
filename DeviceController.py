from gpiozero import LED
import json
import argparse
import os
import paho.mqtt.client as mqtt

## CONFIGURATION ##
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
use_mqtt = False
###

## FUNCTIONS ##

def on_off(id, status):
    if config["devices"][id]["type"] == "gpio":
        #led = LED(config["devices"][id]["pin"])
        if status == "true":
            #led.on()
            pass
        else:
            #led.off()
            pass
        print(status)
    elif config["devices"][id]["type"] == "i2c":
        print("I2C activated!")

    if use_mqtt:
        client = mqtt.Client()
        client.connect(config["mqtt"]["server"], config["mqtt"]["port"], config["mqtt"]["keepalive"])
        client.publish(id, status)
###


## DEFINITIONS ##


###


## MAIN ##

def main():
    parser = argparse.ArgumentParser(description="IoTScheduler hardware controller.")
    parser.add_argument("--id", help="ID of the device to controll.", required=True)
    parser.add_argument("--status", help="STATUS=[true/false] Set the device on/off.", required=True)
    args = parser.parse_args()
    on_off(args.id, args.status)

if __name__ == "__main__":
    global use_mqtt
    use_mqtt = True
    main()

