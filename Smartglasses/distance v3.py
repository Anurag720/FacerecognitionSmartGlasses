"""File: echo_loop.py"""
# Import necessary libraries.
from Bluetin_Echo import Echo
import time
from espeak import espeak

# Define GPIO pin constants.
TRIGGER_PIN = 27
ECHO_PIN = 22
# Initialise Sensor with pins, speed of sound.
speed_of_sound = 315
echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
# Measure Distance 5 times, return average.

# Take multiple measurements.
while True:
    result = echo.read()
    # Print result.
    print(result, 'cm')
    if result < 15.0 :
        espeak.set_voice("whisper")
        espeak.set_voice("f5")
        espeak.synth("कोई नजदीक आ रहा है अश्विनी कुमार सिन्हा")
        #espeak.synth("helloै")
    

if __name__ == '__main__':
    print ("Starting distance measurement! Press Ctrl+C to stop this script.")
    time.sleep(1)



