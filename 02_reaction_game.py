#02_reaction_game.py
# Written for Simon Monk's Electronics Starter Kit for the Raspberry Pi by Henry Budden (@pi_tutor)

#Thanks to Ben Nuttall from the Raspberry Pi Foundation for the GPIO Zero library

#Import relevant libraries
from gpiozero import *
from time import sleep
import random

#Set pin numbers
led_1 = LED(22)
led_2 = LED(4)
rgb = RGBLED(red=14, green=17, blue=27)
button_1 = Button(24)
button_2 = Button(2)

#Input player names
player_1 = raw_input("Enter the name of Player 1: ")
player_2 = raw_input("Enter the name of Player 2: ")

#Initialise score variables
player_1_score = 0
player_2_score = 0

#Initialise round number variable
round_num = 0

#Start the game
while True:

    trick = False   #Set trick mode
    round_num = round_num +1 #Increment round number by one for each iteration
    
    wait = 0

    time = random.uniform(0, 10)        #Randomly generate time delay between 0 and 10 seconds
    color_2 = random.uniform(0, 1)      #Randomly generate green colour value (on or off)
    color_3 = random.uniform(0, 1)      #Randomly generate blue colour value (on or off)

    fix = random.randint(0,3)           #Randomly generate number for trick question between 0 and 3 inclusive

    if color_2 == 0 and color_3 == 0:   #If all colours are off by chance
        color_2 = 1                     #Set green pixel to on

    print " "                               #Print blank line for better formatting
    print "Round", str(round_num) + ":"     #Print round number
    print "Get Ready!"
    
    sleep(time)     #Wait for random amount of time

    if fix == 3:                #Approx 25% of the time
        trick = True            #Set trick mode
        rgb.color = (1, 0, 0)   #Make RGB LED Red
    else:
        rgb.color = (0, color_2, color_3) #Turn on RGB LED to random colour

    while True:
        if button_1.is_pressed and trick == False:                      #If player 1 button is pressed
            print player_1, "wins!"                                     #Display winning message
            player_1_score = player_1_score + 1                         #Increment score by one
            rgb.color = (0,0,0)                                         #Turn LED off
            print player_1, ":", player_1_score                         #Display scores
            print player_2, ":", player_2_score
            wait = 0                                                    #Reset wait value
            break
        elif button_1.is_pressed and trick == True:
            print player_1, "Oh dear!"                                  #Display winning message
            player_1_score = player_1_score - 1                         #Increment score by one
            rgb.color = (0,0,0)                                         #Turn LED off
            print player_1, ":", player_1_score                         #Display scores
            print player_2, ":", player_2_score
            wait = 0 
            break
        
        if button_2.is_pressed and trick == False:
            print player_2, "wins!"
            player_2_score = player_2_score + 1
            rgb.color = (0,0,0)
            print player_1, ":", player_1_score
            print player_2, ":", player_2_score
            wait = 0 
            break
        elif button_2.is_pressed and trick == True:
            print player_2, "Oh dear!"
            player_2_score = player_2_score - 1
            rgb.color = (0,0,0)
            print player_1, ":", player_1_score
            print player_2, ":", player_2_score
            wait = 0 
            break

        if trick == True and wait == 100000:                            #If on trick question time out after approx 5 seconds
            print "Well Done"
            rgb.color = (0,0,0)
            print player_1, ":", player_1_score
            print player_2, ":", player_2_score
            wait = 0
            break
        
        wait = wait + 1                                                 #Increment wait value by one
        
    if player_1_score > player_2_score:     #If player one is winning overall
        led_1.on()                          #Turn on player one LED and turn player two LED off
        led_2.off()
    elif player_2_score > player_1_score:
        led_2.on()
        led_1.off()
    else:                                   #If they are drawing
        led_1.on()                          #Turn both LEDs on
        led_2.on()

    
