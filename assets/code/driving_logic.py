import RPi.GPIO as GPIO
import time
import json
import os

SERVO_R = os.environ.get("SERVO_R")
SERVO_L = os.environ.get("SERVO_L")


class Robot:
    def __init__(self, servo_pin1=SERVO_R, servo_pin2=SERVO_L, pwm_freq=50, duty_cycle=0):
        self.servo_pin1 = servo_pin1
        self.servo_pin2 = servo_pin2
        self.pwm_freq = pwm_freq
        self.duty_cycle = duty_cycle
        self.start_time = None
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.servo_pin1, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.servo_pin1, self.pwm_freq)
        self.pwm1.start(self.duty_cycle)

        GPIO.setup(self.servo_pin2, GPIO.OUT)
        self.pwm2 = GPIO.PWM(self.servo_pin2, self.pwm_freq)
        self.pwm2.start(self.duty_cycle)

    def drive_straight(self, seconds=2):
        self.pwm1.ChangeDutyCycle(5)
        self.pwm2.ChangeDutyCycle(10)
        self.how_long(seconds)
    
    def drive_backwards(self, seconds=2):
        self.pwm1.ChangeDutyCycle(10)
        self.pwm2.ChangeDutyCycle(5)
        self.how_long(seconds)

    def turn_left(self, degree=90):
        self.pwm1.ChangeDutyCycle(5)
        self.how_long(1.2*degree/90.0)
    
    def turn_right(self, degree=90):
        self.pwm2.ChangeDutyCycle(10)
        self.how_long(1.2*degree/90.0)

    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        end_time = time.time()
        print("Time elapsed: ", end_time - self.start_time)

    def cleanup(self):
        self.pwm1.stop()
        self.pwm2.stop()
        self.__init__(self.servo_pin1, self.servo_pin2, self.pwm_freq, self.duty_cycle)
        GPIO.cleanup()


    def how_long(self, seconds):
        self.start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= seconds:
                self.stop()
                break
    
    def execute_instructions(self, instructions_file):
        with open(instructions_file, 'r') as f:
            instructions = json.load(f)
        for instruction in instructions['instructions']:
            action = instruction['action']
            print("Executing action: ", action)
            if action == 'drive_straight':
                self.drive_straight(instruction['seconds'])
            elif action == 'drive_backwards':
                self.drive_backwards(instruction['seconds'])
            elif action == 'turn_left':
                self.turn_left(instruction['degree'])
            elif action == 'turn_right':
                self.turn_right(instruction['degree'])
            time.sleep(1)