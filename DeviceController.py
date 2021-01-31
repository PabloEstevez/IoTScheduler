import RPi.GPIO as gpio
import json
import argparse
import os
import time
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_pub

## CONFIGURATION ##
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
###

## FUNCTIONS ##

def on_off(id, status):
    #print("Status: " + status)
    if config["devices"][id]["type"] == "gpio":
        gpio_setup(id)
        if id == "motor":
            if status == "1":
                gpio.output(config["devices"]["motor"]["pin"],True)
            else:
                gpio.output(config["devices"]["motor"]["pin"],False)
        elif config["devices"][id]["motor"] == 1:
            if status == "1":
                gpio.output(config["devices"][id]["pin"],True)
                #time.sleep(0.2)
                gpio_setup("motor")
                gpio.output(config["devices"]["motor"]["pin"],True)
            else:
                if not check_using("motor", id):
                    gpio_setup("motor")
                    gpio.output(config["devices"]["motor"]["pin"],False)
                    time.sleep(5) # To let the solenoid valve drain the remaining pressure
                gpio_setup(id)
                gpio.output(config["devices"][id]["pin"],False)
        gpio_status(id)
    elif config["devices"][id]["type"] == "i2c":
        print("I2C activated!")
    
    try:
        if args.mqtt:
            #client = mqtt.Client()
            #client.connect(config["mqtt"]["server"], config["mqtt"]["port"], config["mqtt"]["keepalive"])
            #client.publish(id, status)
            mqtt_pub.single(id, status, retain=True, hostname=config["mqtt"]["server"], port=config["mqtt"]["port"], keepalive=config["mqtt"]["keepalive"])
    except: pass
    return(status)


def gpio_status(id):
    gpio_setup(id)
    status = gpio.input(config["devices"][id]["pin"])
    print(status, end='')
    return status


def gpio_setup(id):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(config["devices"][id]["pin"], gpio.OUT)

def check_using(id, exception):
    for device in config["devices"]:
        if (device != id) and (device != exception) and (config["devices"][device][id] == 1):
            gpio_setup(device)
            if gpio.input(config["devices"][device]["pin"]) == 1:
                return True
    return False

def get_devices():
    return config["devices"]

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

