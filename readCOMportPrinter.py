from struct import error
import serial
import re
import binascii
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/ttyUSB0'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE,bytesize = serial.EIGHTBITS, parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_ONE, rtscts =True, dsrdtr =True)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
brokerActive = False
def connection():
    try:
        client.connect("52.233.241.139", 1883, 60)
        brokerActive = True
        return brokerActive
    except Exception as e:
        print(e)
        return False

def main():
    active = False
    while True:
        temporary = []
        weight = 0.0
        unit = 'g'
        

        reading = str(ser.readline(),'utf-8').rstrip()
        result = re.split(' ',reading)
        for i in range(len(result)):
            if result[i] != '' and result[i] != 'N':
                temporary.append(result[i])
        print(temporary)
        if len(temporary) == 3:
            weight = float(temporary[0]+temporary[1])
            unit = temporary[2]
        else:
            weight = float(temporary[0])
            unit = temporary[1]
        print(unit)
        print (weight)
        
        value_json=json.dumps({"weight":weight, "unit":unit,"timestamp":datetime.now().timestamp()})
        
        client.publish("machineValues/Scales", value_json,qos=0,retain=True)


while  connection() == False:
    print("Viscometer attempting to connect to broker")

#while brokerActive == True:
 #   main()


if __name__ == "__main__":
    main()