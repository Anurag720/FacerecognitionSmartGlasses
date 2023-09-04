import time
from espeak import espeak
# Function that reads distance from the sensor
def read_distance():
    # Initialize the GPIO pins
    import RPi.GPIO as GPIO         # Import the Raspberry Pi GPIO library
    GPIO.setmode(GPIO.BCM)          # Use Broadcom GPIO pin numbering
    TRIG = 27                        # GPIO pin 02
    ECHO = 22                       # GPIO pin 03
    GPIO.setup(TRIG, GPIO.OUT)      # Set TRIG pin as output
    GPIO.setup(ECHO, GPIO.IN)       # Set ECHO pin as input
    GPIO.output(TRIG, GPIO.LOW)     # Initialize TRIG output as LOW

    # Send a HIGH signal to TRIG in order to trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)    # Send a HIGH pulse to TRIG
    time.sleep(0.00001)             # Wait 10 microseconds to trigger sensor
    GPIO.output(TRIG, GPIO.LOW)     # Set TRIG back to LOW

    # Once the sensor is triggered, it will send an ultrasonic pulse and set
    # the ECHO signal to HIGH. As soon as the receiver detects the original
    # ultrasonic pulse, the sensor will set ECHO back to LOW.

    # We need capture the duration between ECHO HIGH and LOW to measure how
    # long the ultrasonic pulse took on its round-trip.

    pulse_start = time.time()               # Record the pulse start time
    while GPIO.input(ECHO) != GPIO.HIGH:    # Continue updating the start time
        pulse_start = time.time()           # until ECHO HIGH is detected

    pulse_end = pulse_start                 # Record the pulse end time
    while time.time() < pulse_start + 0.1:  # Continue updating the end time
        if GPIO.input(ECHO) == GPIO.LOW:    # until ECHO LOW is detected
            pulse_end = time.time()
            break

    GPIO.cleanup()                  # Done with the GPIO, so let's clean it up

    # The difference (pulse_end - pulse_start) will tell us the duration that
    # the pulse travelled between the transmitter and receiver.
    pulse_duration = pulse_end - pulse_start

    # We know that sound moves through air at 343m/s or 34,300cm/s. We can now
    # use d=vÃ—t to calculate the distance. We need to divide by 2, since we only
    # want the one-way distance to the object, not the round-trip distance that
    # the pulse took.
    distance = 34300 * pulse_duration / 2

    # The sensor is not rated to measure distances over 4m (400cm), so if our
    # calculation results in a distance too large, let's ignore it.
    if distance <= 400:
        return distance
    else:
        return None

# If this script is executed directly, run the read_distance function in a loop
if __name__ == '__main__':
    print ("Starting distance measurement! Press Ctrl+C to stop this script.")
    time.sleep(1)

    while True:
        # Track the current time so we an loop at regular intervals
        loop_start_time = time.time()

        # Read the distance and output the result
        distance = read_distance()
        if distance:
            print ("Distance: %.1f cm" % (distance))
            if distance <= 18:
                #espeak.synth("obstacle is near by distance")
                #espeak.synth(str(round (distance,1)))
                #espeak.set_voice("whisper")
                #espeak.set_voice("f5")
                #espeak.synth("कोई नजदीक आ रहा है अश्विनी कुमार सिन्हा")
                espeak.set_voice("en")
                espeak.set_voice("whisper")
                espeak.synth("Obstacle is nearby")
                espeak.synth(str(round (distance,1)))
                #you can change the voice and language by uncommenting the lines in code
                
                
                
            

        # Find out how much time to wait until we should loop again, so that
        # each loop lasts 1 second
        time_to_wait = loop_start_time + 1 - time.time()
        if time_to_wait > 0:
            time.sleep(time_to_wait)
