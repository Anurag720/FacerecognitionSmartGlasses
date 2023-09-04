from hcsr04sensor import sensor
from espeak import espeak
# Created by Al Audet
# MIT License
value =0



trig_pin = 27
echo_pin = 22

   
while True:
    value = sensor.Measurement(trig_pin, echo_pin)
    raw_measurement = value.raw_distance(sample_size=5, sample_wait=0.03)

    # Calculate the distance in centimeters
    print("The Distance = {} centimeters".format(round(raw_measurement, 1)))
    if raw_measurement <= 15:
        espeak.synth("obstacle is near by distance")
        espeak.synth(str(format(round(raw_measurement, 1))))
        
                



if __name__ == "__main__":
    main()
