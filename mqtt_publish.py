import paho.mqtt.client as mqtt
from datetime import datetime
import json
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
client.connect("40.118.124.87", 1883, 60)

# send a message to the raspberry/topic every 1 second, 5 times in a row
for i in range(5):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    #client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    value_json=json.dumps({"value":23.7, "unit":"pH", "temp": 19.2, "temp_unit":"c", "temp_device":"ATC","t_stamp":datetime.now().timestamp()})
    value1_json=json.dumps({"scales":563.2, "timestamp":datetime.now().timestamp()})
    client.publish("machineValues/PHmeter", value_json,qos=2,retain=False)
    client.publish("machineValues/scales", value1_json,qos=2,retain=False)

    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_forever()
