import paho.mqtt.client as mqtt
from datetime import datetime
import json
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
while True:

    value_json=json.dumps({"value":23.7, "unit":"pH", "temp": 19.2, "temp_unit":"c", "temp_device":"ATC","timestamp":datetime.now().timestamp()})
    value1_json=json.dumps({"scales":563.2, "timestamp":datetime.now().timestamp()})
    try:
        client.connect("40.118.124.87", 1883, 10)

        # send a message to the raspberry/topic every 1 second, 5 times in a row
        for i in range(5):
            # the four parameters are topic, sending content, QoS and whether retaining the message respectively
            #client.publish('raspberry/topic', payload=i, qos=0, retain=False)
            
            client.publish("machineValues/PHmeter", value_json,qos=2,retain=False)
            client.publish("machineValues/scales", value1_json,qos=2,retain=False)

            print(f"send {i} to raspberry/topic")
            time.sleep(2)
        client.loop_forever()   
    except:
        with open('test.txt','a') as text_file:
            text_file.write(value_json)
            text_file.write("\n")
            
        with open('test.txt', 'r') as text_file:
            readBack = text_file.readlines()
            for line in readBack:
                js = json.loads(line)

