import time
import grovepi
import math
import requests
from grove_rgb_lcd import * 
# Connections
sound_sensor = 0        # port A0
light_sensor = 1        # port A1
temperature_sensor = 2  # port D2
led = 3                 # port D3
buzzer = 8              # port D8
# Lcd Display is connected with I2C port-3
grovepi.pinMode(buzzer,"OUTPUT")
grovepi.pinMode(led,"OUTPUT")
grovepi.analogWrite(led,255)  #turn led to max to show readiness

# Define the Thingspeak URL and API key
thingspeak_url = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update"
api_key = "ITTMCI0BNKTL9BF9"


while True:
    # Error handling in case of problems communicating with the GrovePi
    try:

        # Get value from light sensor
        light_intensity = grovepi.analogRead(light_sensor)

        # Give PWM output to LED
        grovepi.analogWrite(led,light_intensity/4)

        # Get sound level
        sound_level = grovepi.analogRead(sound_sensor)

        time.sleep(0.5)

        # Get value from temperature sensor
        [temperature,humidity]=[0,0]
        [temperature,humidity] = grovepi.dht(temperature_sensor,0)
    
        
        tweet_message= f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Light Intensity: {light_intensity}, Sound Level: {sound_level}"
	    # Define the data to be sent in the POST request
        data={"api_key":api_key,"status":tweet_message}
        # setting the lcd
        msg1= f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%"
        msg2= f"Light Inte: {light_intensity}, Sound Lvl: {sound_level}"
        setRGB(0,255,0)
        setText(msg1)
        time.sleep(1.5)
        setText_norefresh(msg2)
        #Reacting on High tempertaure
        if (temperature > 30 ):
            grovepi.digitalWrite(buzzer,1)
            print ('start')
            time.sleep(1)
            setRGB(255,0,0)
        # Send the POST request to update the status
        response = requests.post(thingspeak_url, data=data)

	# Print the response text (should be "Status updated"
        print(response.text)
        print(tweet_message)
        time.sleep(60)
        
    except IOError:
        print("Error")
    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        setRGB(0,0,0)
        setText("")
        exit()
        
    
