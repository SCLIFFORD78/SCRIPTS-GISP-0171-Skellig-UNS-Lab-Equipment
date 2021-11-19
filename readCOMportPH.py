import serial


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM8'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 1200


def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = str(ser.readline(),'utf-8','ignore')
        # reading is a string...do whatever you want from here
        print(reading)
        for i in range(len(reading)):
            if reading[i] == 'A' and reading[i+1] == 'E':
                print(reading.split(' ', 3))
                ph = reading.split(' ', 3)
                print(ph[1].split('pH'))
                num = float(ph[1].split('pH')[0])
                print(num)


if __name__ == "__main__":
    main()