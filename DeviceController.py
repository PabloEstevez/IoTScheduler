from gpiozero import LED
import json

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
###


## DEFINITIONS ##

###
