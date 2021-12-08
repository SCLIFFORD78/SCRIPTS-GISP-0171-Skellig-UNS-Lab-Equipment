import serial
import mysql.connector
import pymysql.cursors
import re
from datetime import datetime


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM8'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600
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
        Z = datetime.time(datetime.strptime(Z, '%H:%M:%S'))

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='password',
                                    database='skellig_uns_lab_equipment',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `viscometer_records` (`rpm`,`M`, `cP`, `D_CM2`, `1_SEC`, `temperature`, `temp_unit`, `Z`, `percentage`, `S`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (rpm, M, cP, d_CM2, one_sec, temperature, temp_unit, Z, percentage, S ))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()




if __name__ == "__main__":
    main()