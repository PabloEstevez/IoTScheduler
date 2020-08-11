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
###

## FUNCTIONS ##

def on_off(id, status):
    if config["devices"][id]["type"] == "gpio":
        gpio_setup(id)
        if status == "1":
            gpio.output(config["devices"][id]["pin"],True)
            pass
        else:
            gpio.output(config["devices"][id]["pin"],False)
            pass
        gpio_status(id)
    elif config["devices"][id]["type"] == "i2c":
        print("I2C activated!")

    if args.mqtt:
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
    parser.add_argument("--set", help="SET=[1/0] Set the device on/off.", required=False)
    parser.add_argument("--status", dest="status", action="store_true", help="Print status of the device.", required=False)
    parser.add_argument("--mqtt", dest="mqtt", action="store_true", help="Notify status via MQTT.", required=False)
    parser.set_defaults(status=False, mqtt=False)
    global args
    args = parser.parse_args()
    if args.set != None:
        on_off(args.id, args.set)
    if args.status:
        gpio_status(args.id)

if __name__ == "__main__":
    main()

