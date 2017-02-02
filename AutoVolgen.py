import RPi.GPIO as GPIO 
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7
pinTrigger = 17
pinEcho = 18
pinLedA = 24
pinLedB = 23
Frequency = 35
DutyCycleA = 30
DutyCycleB = 30
Stop = 0

GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)


GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)      


GPIO.setup(pinLedA, GPIO.OUT) 
GPIO.setup(pinLedB, GPIO.OUT)  


pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)


pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)


def Forwards(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

	
def Backwards(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)


def Left(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)


def Right(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)

def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

def Measure():
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
      
        
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance


try:
    
    GPIO.output(pinTrigger, False)

    
    time.sleep(0.1)

    
    while True:
        print("Seeking the car")
        GPIO.output(pinLedA, True)
        GPIO.output(pinLedB, False)

        SeekSize = 0.15 
        SeekCount = 1 
        MaxSeekCount = 8

        
        while SeekCount <= MaxSeekCount:
            DistanceToObject = Measure()
            print(DistanceToObject)
            
            if DistanceToObject <= 65:
                print('Within 50cm')
                GPIO.output(pinLedB, True)
                GPIO.output(pinLedA, False)
                
                if DistanceToObject <= 25:
                    Forwards(-10)
                    time.sleep(1)
                    StopMotors()
                    continue
                
                if DistanceToObject >= 35:
                    Forwards(10)
                    time.sleep(1)
                    StopMotors()
                    continue
					
                Forwards(0)
                time.sleep(1)
                StopMotors()
                continue

            Left(0)
            time.sleep(SeekSize)
            StopMotors()
            
            SeekCount += 1


except KeyboardInterrupt:
    GPIO.cleanup()
