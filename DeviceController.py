from gpiozero import LED
import json
import argparse

## CONFIGURATION ##
config_file = open("config.json", "r")
config_str = config_file.read()
config = json.loads(config_str)
config_file.close()
###

## FUNCTIONS ##

def on_off(id, status):
    if config["devices"][id]["type"] == "gpio":
        """led = LED(config["devices"][id]["pin"])
        if status == True:
            led.on()
        else:
            led.off()"""
        print("GPIO activated!")
    elif config["devices"][id]["type"] == "i2c":
        print("I2C activated!")
###


## DEFINITIONS ##


###


## MAIN ##

def main():
    parser = argparse.ArgumentParser(description="IoTScheduler hardware controller.")
    parser.add_argument("--id", help="ID of the device to controll.", required=True)
    parser.add_argument("--status", help="STATUS=[on/off] Set the device on/off.", required=True)
    args = parser.parse_args()
    on_off(args.id, args.status)

if __name__ == "__main__":
    main()

