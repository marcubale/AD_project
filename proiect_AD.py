import time

import RPi.GPIO as IO    #calling for header file which helps in using GPIOs of PI


string_of_characters = 0 
LED_PIN = 14
 #led pin green 
LED_PIN_RED = 15



IO.setwarnings(False)    #do not show any warnings

IO.setmode (IO.BCM)      #programming the GPIO by BCM pin numbers. (like PIN29 as GPIO5)

IO.setup(17,IO.OUT)      #initialize GPIO17,27,24,23,18,26,5,6,13,19,21 as an output

IO.setup(27,IO.OUT)

IO.setup(24,IO.OUT)

IO.setup(23,IO.OUT)

IO.setup(18,IO.OUT)

IO.setup(26,IO.OUT)

IO.setup(5,IO.OUT)

IO.setup(6,IO.OUT)

IO.setup(13,IO.OUT)

IO.setup(19,IO.OUT)

IO.setup(21,IO.OUT)

IO.setup(16,IO.IN)      #initialize GPIO16 as an input

IO.setup(LED_PIN, IO.OUT)
IO.setup(LED_PIN_RED, IO.OUT)

distance_threshhold = 30

#IO.output(LED_PIN_RED, IO.LOW)
#IO.output(LED_PIN, IO.LOW)

def turn_on_led():
    IO.output(LED_PIN_RED, IO.LOW)
    IO.output(LED_PIN, IO.HIGH)
    
def turn_on_red():
    IO.output(LED_PIN, IO.LOW)
    IO.output(LED_PIN_RED, IO.HIGH)



def send_a_command (command):  #steps for sending a command to 16x2 LCD

    pin=command

    PORT(pin);

    IO.output(17,0)

    #PORTD&= ~(1<<RS);

    IO.output(27,1)

    #PORTD|= (1<<E);

    time.sleep(0.001)

    #_delay_ms(50);

    IO.output(27,0)

    #PORTD&= ~(1<<E);

    pin=0

    PORT(pin); 


def send_a_character (character):  #steps for sending a character to 16x2 LCD

    pin=character

    PORT(pin);

    IO.output(17,1)

    #PORTD|= (1<<RS);

    IO.output(27,1)

    #PORTD|= (1<<E);

    time.sleep(0.001)

    #_delay_ms(50);

    IO.output(27,0)

    #PORTD&= ~(1<<E);

    pin=0

    PORT(pin);


def PORT(pin):                    #assigning level for PI GPIO for sending data to LCD through D0-D7

    if(pin&0x01 == 0x01):

        IO.output(24,1)

    else:

        IO.output(24,0)

    if(pin&0x02 == 0x02):

        IO.output(23,1)

    else:

        IO.output(23,0)

    if(pin&0x04 == 0x04):

        IO.output(18,1)

    else:

        IO.output(18,0)

    if(pin&0x08 == 0x08):

        IO.output(26,1)

    else:

        IO.output(26,0)    

    if(pin&0x10 == 0x10):

        IO.output(5,1)

    else:

        IO.output(5,0)

    if(pin&0x20 == 0x20):

        IO.output(6,1)

    else:

        IO.output(6,0)

    if(pin&0x40 == 0x40):

        IO.output(13,1)

    else:

        IO.output(13,0)

    if(pin&0x80 == 0x80):

        IO.output(19,1)

    else:

        IO.output(19,0)


def send_a_string(string_of_characters):

  string_of_characters = string_of_characters.ljust(16," ")

  for i in range(16):

    send_a_character(ord(string_of_characters[i]))  #send characters one by one through data port

    

while 1:
    # turn_on_led()

    send_a_command(0x38);  #16x2 line LCD

    send_a_command(0x0E);  #screen and cursor ON

    send_a_command(0x01);  #clear screen

    time.sleep(0.001)                #sleep for 100msec

    

    IO.setup(21,1)

    time.sleep(0.00001)

    IO.setup(21,0)           #sending trigger pulse for sensor to measure the distance

        

    while (IO.input(16)==0):

        start = time.time()  #store the start time of pulse output         

            

    while (IO.input(16)==1):

        stop = time.time()   #store the stop time 

      

            

    distance = ((stop - start)*17150)  #calculate distance from time

    distance = round(distance,2)       #round up the decimal values

    if(distance<400):                  #if distance is less than 400 cm, display the result on LCD 

        send_a_command(0x80 + 0);

        send_a_string ("Dist=%s cm"% (distance));

        time.sleep(0.15)

        

    if(distance>400):                  #If distance is more than 400cm, just print 400+ on LCD

        send_a_command(0x80 + 0);

        send_a_string ("Dist= 400+ cm");

        time.sleep(0.15)
    
    if(distance > distance_threshhold):
       turn_on_red()
    elif(distance < distance_threshhold):
       turn_on_led()
        
#IO.cleanup()
