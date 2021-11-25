import serial
import mysql.connector
import pymysql.cursors
import re
import binascii
import time


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM10'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE,bytesize = serial.EIGHTBITS, parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_ONE, rtscts =True, dsrdtr =True)

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

        connection = pymysql.connect(host='localhost',
                                            user='root',
                                            password='password',
                                            database='skellig_uns_lab_equipment',
                                            cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `printer_records` (`weight`, `unit`) VALUES (%s, %s)"
                cursor.execute(sql, (weight, unit))
            connection.commit()

if __name__ == "__main__":
    main()