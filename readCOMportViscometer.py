import serial
import mysql.connector
import pymysql.cursors
import re
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM8'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
def connection():
    try:
        client.connect("52.233.241.139", 1883, 60)
        return True
    except Exception as e:
        print(e)
        return False

def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, parity=serial.PARITY_NONE, xonxoff=False)
    temp_unit = 'C'
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = str(ser.readline(),'utf-8','ignore').lstrip()
        # reading is a string...do whatever you want from here
        print(reading)
        temporary = []
        result = re.split(' ', reading)
        for j in range(len(result)):
            result[j].rstrip()
            if result[j] != '' and  result[j] != ' ':
                temporary.append(result[j].rstrip())
        rpm = float(re.split('=', temporary[0])[1])
        M = str(re.split('=', temporary[1])[1])
        S = float(re.split('=', temporary[2])[1])
        percentage = float(re.split('=', temporary[3])[1])
        cP = re.split('=', temporary[4])[1]
        if cP[len(cP)-1] != '-':
            cP = float(re.split('=', temporary[4])[1])
        else:
            cP = 0.0
        d_CM2 = re.split('=', temporary[5])[1]
        if d_CM2[len(d_CM2)-1] != '-':
            d_CM2 = float(re.split('=', temporary[5])[1])
        else:
            d_CM2 = 0.0
        one_sec = float(re.split('=', temporary[6])[1])
        temperature = float(re.split('C', re.split('=', temporary[7])[1])[0])
        Z = '00:'+ re.split('Z', temporary[8])[1]
        Z = str(datetime.time(datetime.strptime(Z, '%H:%M:%S')))
        
        value_json=json.dumps({"rpm":rpm, "M":M, "cP": cP, "D_CM2":d_CM2, "1_SEC":one_sec, "Z":Z, "temperature":temperature, "temp_unit":temp_unit, "percentage":percentage, "S": S })

        client.publish("machineValues/Viscometer", value_json,qos=2,retain=True)


while  connection() == False:
    print("Viscometer attempting to connect to broker")

#while brokerActive == True:
 #   main()


if __name__ == "__main__":
    main()