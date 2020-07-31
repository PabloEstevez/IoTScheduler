import RPi.GPIO as gpio
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
        gpio_setup(id)
        if status == "true":
            gpio.output(config["devices"][id]["pin"],True)
            pass
        else:
            gpio.output(config["devices"][id]["pin"],False)
            pass
        gpio_status(id)
    elif config["devices"][id]["type"] == "i2c":
        print("I2C activated!")

    if use_mqtt:
        client = mqtt.Client()
        client.connect(config["mqtt"]["server"], config["mqtt"]["port"], config["mqtt"]["keepalive"])
        client.publish(id, status)


def gpio_status(id):
    gpio_setup(id)
    print(gpio.input(config["devices"][id]["pin"]), end='')


def gpio_setup(id):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(config["devices"][id]["pin"], gpio.OUT)
###


## DEFINITIONS ##


###


## MAIN ##

def main():
    parser = argparse.ArgumentParser(description="IoTScheduler hardware controller.")
    parser.add_argument("--id", help="ID of the device to controll.", required=True)
    parser.add_argument("--set", help="SET=[true/false] Set the device on/off.", required=False)
    parser.add_argument("--status", dest="status", action="store_true", help="ID of the device to controll.", required=False)
    args = parser.parse_args()
    global use_mqtt
    use_mqtt = True
    if args.set != None:
        on_off(args.id, args.set)
    if args.status:
        gpio_status(args.id)

if __name__ == "__main__":
    main()

