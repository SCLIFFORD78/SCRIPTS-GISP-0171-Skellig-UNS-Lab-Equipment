import serial
import mysql.connector
import pymysql.cursors
import re


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM12'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 1200


def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = str(ser.readline(),'utf-8','ignore')
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
                # Connect to the database
                connection = pymysql.connect(host='localhost',
                                            user='root',
                                            password='password',
                                            database='skellig_uns_lab_equipment',
                                            cursorclass=pymysql.cursors.DictCursor)
                with connection:
                    with connection.cursor() as cursor:
                        # Create a new record
                        sql = "INSERT INTO `ph_records` (`value`, `unit`, `temp`, `temp_unit`, `temp_device`) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (value, unit, temp, temp_unit, temp_device ))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
                print(value)
                print(unit)


if __name__ == "__main__":
    main()