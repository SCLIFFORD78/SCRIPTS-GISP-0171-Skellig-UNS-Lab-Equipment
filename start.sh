#!/bin/bash 

#nohup python3 readCOMportPH.py .py > readCOMportPH  &
#nohup python3 readCOMportShaker.py> readCOMportShaker &
#nohup python3 readCOMportViscometer.py> readCOMportViscometer &

#parallel ::: "python3 readCOMportPrinter.py" "python3 readCOMportShaker.py"
#python3 readCOMportPrinter.py &
lxterminal -e 'python3 readCOMportShaker.py' &
lxterminal -e 'python3 readCOMportViscometer.py' &
lxterminal -e 'python3 readCOMportPH.py' &
lxterminal -e 'python3 readCOMportConductivityMeter.py' &
lxterminal -e 'python3 readCOMportPrinter.py' &
#python3 readCOMportShaker.py &
#python3 readCOMportPH.py &
#python3 "readCOMportConductivityMeter.py"
#python3 readCOMportViscometer.py &

#gnome-terminal -x sh -c "python3 readCOMportViscometer.py; bash"

#lxterminal -e 'bash -c "cd Desktop/SCRIPTS-GISP-0171-Skellig-UNS-Lab-Equipment && python3 readCOMportViscometer.py; read x'&
#lxterminal -e 'bash -c "cd Desktop/SCRIPTS-GISP-0171-Skellig-UNS-Lab-Equipment && python3 readCOMportPH.py ; read x" '&