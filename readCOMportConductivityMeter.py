import serial
import mysql.connector
import pymysql.cursors
import re
from datetime import datetime
import paho.mqtt.client as mqtt
import json


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM13'
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
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, parity=serial.PARITY_NONE, xonxoff=True)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = str(ser.readline(),'utf-8','ignore')
        # reading is a string...do whatever you want from here
        print(reading)
        secondaryUnit = 'C'
        unit = 'pH'
        temporary = []
        try:
            for i in range(len(reading)):
                if (reading[i] == '0' and reading[i+1] == '0' and reading[i+2] == '0'):
                    result = re.split(' ', reading)
                    for j in range(len(result)):
                        if result[j] != '' and  result[j] != ' ' and result[j] != '000' and result[j] != '\x00000':
                            temporary.append(result[j].rstrip())
                    value = temporary[0]
                    if len(temporary)==5:
                        value = float(value.split('M')[0])
                        unit = 'M'
                    else:
                        if value[len(value)-1] == 'l':
                            value = float(value.split('mg/l')[0])
                            unit = 'mg/l'
                        elif value[len(value)-1] == 'S':
                            value = float(value.split('uS')[0])
                            unit = 'uS'
                        elif value[len(value)-1] == 'M':
                            value = float(value.split('M')[0])
                            unit = 'M'
                    if len(temporary)==5:
                        secondary = temporary[2]
                    else:
                        secondary = temporary[1]
                    if secondary[len(secondary)-1] == 'C':
                        secondary = float(secondary.split('`C')[0])
                    elif secondary[len(secondary)-1] == 'F':
                        secondary = float(secondary.split('`F')[0])
                        secondaryUnit = 'F'
                    else:
                        secondary = float(secondary.split('g/l')[0])
                        secondaryUnit = 'g/l'
                    if len(temporary)==5:
                        date_logged = temporary[3]+' '+temporary[4]
                    else:
                        date_logged = temporary[2]+' '+temporary[3]
                    date_logged = str(datetime.strptime(date_logged, '%H:%M:%S %d/%m/%y'))
                    
                    value_json=json.dumps({"date_logged":date_logged, "value":value, "unit": unit, "secondary_value":secondary, "secondary_unit":secondaryUnit,"timestamp":datetime.now().timestamp()})
                    
                    client.publish("machineValues/ConductivityMeter", value_json,qos=2,retain=True)


        except:
            print('Error processing data')

while  connection() == False:
    print("CONDUCTIVITYMETER attempting to connect to broker")

#while brokerActive == True:
 #   main()


if __name__ == "__main__":
    main()