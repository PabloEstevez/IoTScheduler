#!/bin/bash

pip3 install -r requirements.txt

cat <<EOT >> /etc/systemd/system/iotscheduler.service
[Unit]
Description= IoT Scheduler.
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $(pwd)/MQTT_watcher.py >> $(pwd)/mqtt_watcher.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable iotscheduler.service
systemctl start iotscheduler.service

echo "Installation Successful!"
