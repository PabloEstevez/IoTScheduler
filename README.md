# IoTScheduler

## Tips

- If you are using MQTT, consider stablishing a default value for your devices publishing a message with the flag "retain" on; so if the program crashes, you have a power outage or any other kind of unexpected event, you are sure that your system will go back to a "default" state that you know it is safe. For example, I set all my actuators off.