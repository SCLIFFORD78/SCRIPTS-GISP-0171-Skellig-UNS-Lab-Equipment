import serial
import mysql.connector
import pymysql.cursors
import re
import binascii
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM11'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
client.connect("40.118.124.87", 1883, 60)

speed = 0.0
active = False

def main():
    active = False
    while True:
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE,bytesize = serial.SEVENBITS, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE, rtscts =True)
        #value = 'OUT_SP_4 60 \r\n'.encode("utf-8")
        #value1 = 'START_4 \r\n'.encode("utf-8")
        value2 = 'IN_PV_4 \r\n'.encode("utf-8")
        #value = b'IN_PV_4\r\n'
        #ser.write(value)
        #ser.write(value1)
        ser.write(value2)
        reading = str(ser.readline(),'utf-8').rstrip()
        speed = float(re.split(' ',reading)[0])
        print(speed)
        ser.close()
        time.sleep(1)
        if speed > 0.0:
            active = True
            value_json=json.dumps({"speed":speed, "unit":'RPM',"timestamp":datetime.now().timestamp()})
            
            client.publish("machineValues/Shaker", value_json,qos=2,retain=True)

        if active == True and speed == 0.0:
            
            value_json=json.dumps({"speed":speed, "unit":'RPM',"timestamp":datetime.now().timestamp()})
            
            client.publish("machineValues/Shaker", value_json,qos=2,retain=True)

            active = False

        

if __name__ == "__main__":
    main()