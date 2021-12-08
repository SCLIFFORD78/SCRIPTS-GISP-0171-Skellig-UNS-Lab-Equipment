# If you don't want to see the outputs/print of your training program, 
#     add @ECHO OFF to the start. If you want to see them, remove the @ECHO OFF
@ECHO OFF

# Without "start" before the script to run your training program,
#     the batch file will wait until the training program finishes
python "path\to\your\training_program.py"
ECHO training program completed

# Adding "start" opens it in a new window, and processes the next line
#     without waiting for the program to finish running
start python "readCOMportPrinter.py"
ECHO Running program1
start python "readCOMportShaker.py"
ECHO Running program2
start python "readCOMportPH.py"
ECHO Running program3
start python "readCOMportConductivityMeter.py"
ECHO Running program4
start python "readCOMportViscometer.py"
ECHO Running program5




# Adding "PAUSE" makes the script wait for you manually type a key to continue,
#     but it is not required. You can add PAUSE anywhere in the script
PAUSE





