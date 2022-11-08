import serial
import re
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM4'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 19200

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")



def main():
    packet = bytearray()
    packet.append(0x02)
    packet.append(0x03)
    packet.append(0x00)
    packet.append(0x40)

    packet.append(0x00)
    packet.append(0x02)
    packet.append(0xc5)
    packet.append(0xec)


    message = b'\x02\x06\x00\x00\x00\x02\x08\x38'
    message_a = list(message)
    message_b = bytes(message_a)
    ser = serial.Serial (SERIAL_PORT, SERIAL_RATE, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE, xonxoff=True)
    setData = ser.write(packet)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        #reading = str(ser.readline(),'utf-8','ignore')
        reading = ser.read_all()# .read(20)
        converted = list(reading)
        print(converted)
        # reading is a string...do whatever you want from here
        temp_unit = 'C'
        unit = 'pH'
        temporary = []
        for i in range(len(reading)):
            if reading[i] == 'A' and reading[i+1] == 'E':
                result = re.split(' ', reading)
                for j in range(len(result)):
                    if result[j] != '' and  result[j] != ' ' and result[j] != 'AE':
                        temporary.append(result[j])
                        
                print(temporary)
                value = temporary[0]
                if value[len(value)-1] == 'H':
                    value = float(value.split('pH')[0])
                else:
                    value = float(value.split('mV')[0])
                    unit = 'mV'
                temp = temporary[1]
                if temp[len(temp)-1] == 'C':
                    temp = float(temp.split('C')[0])
                else:
                    temp = float(temp.split('F')[0])
                    temp_unit = 'F'
                temp_device = temporary[2].rstrip()

                value_json=json.dumps({"value":value, "unit":unit, "temp": temp, "temp_unit":temp_unit, "temp_device":temp_device,"timestamp":datetime.now().timestamp()})

                client.publish("machineValues/PHmeter", value_json,qos=2,retain=True)

                print(value)
                print(unit)



#while brokerActive == True:
 #   main()


if __name__ == "__main__":
    main()