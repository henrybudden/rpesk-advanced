# sunrise_alarm.py
# Written for the Electronics Starter Kit for the Raspberry Pi by MonkMakes.com with help from Henry Budden (@pi_tutor)
from Tkinter import *
import RPi.GPIO as GPIO
import time, math

GPIO.cleanup()

# Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin positions
GPIO.setmode(GPIO.BCM)


# Set sunrise limit. This works for testing in a light room when torch aimed at LDR. Use 30 for accurate sunrise detection.
sunrise = 50

# Pin a charges the capacitor through a fixed 1k resistor and the thermistor in series
# pin b discharges the capacitor through a fixed 1k resistor 
a_pin = 18
b_pin = 23

# Setup pins as outputs for the buzzer and the two LEDs
buzzer_pin = 24
red_pin1 = 27
red_pin2 = 22

GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(red_pin1, GPIO.OUT)
GPIO.setup(red_pin2, GPIO.OUT)

# empty the capacitor ready to start filling it up
def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.01)

# return the time taken for the voltage on the capacitor to count as a digital input HIGH
# than means around 1.65V
def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    GPIO.output(a_pin, True)
    t1 = time.time()
    while not GPIO.input(b_pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 1000000

# Take an analog readin as the time taken to charge after first discharging the capacitor
def analog_read():
    discharge()
    return charge_time()

# Convert the time taken to charge the cpacitor into a value of resistance
# To reduce errors, do it 100 times and take the average.
def read_resistance():
    n = 20
    total = 0;
    for i in range(1, n):
        total = total + analog_read()
    reading = total / float(n)
    resistance = reading * 6.05 - 939
    return resistance

def light_from_r(R):
    # Log the reading to compress the range
    return math.log(1000000.0/R) * 10.0 

while True:
    GPIO.output(red_pin1, False)
    GPIO.output(red_pin2, False)
    light = light_from_r(read_resistance())
    print light
    x = 0
    if light > sunrise:
        GPIO.output(red_pin1, True)     # True means that LED turns on
        GPIO.output(red_pin2, False)    # False means that LED turns off
        while True:
            x = x + 1
            GPIO.output(buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(buzzer_pin, False)
            time.sleep(0.001)
            if x == 250:
                x = 0
                break            
        GPIO.output(red_pin1, False)
        GPIO.output(red_pin2, True)
        while True:
            x = x + 1
            GPIO.output(buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(buzzer_pin, False)
            time.sleep(0.001)
            if x == 250:
                x = 0
                break
