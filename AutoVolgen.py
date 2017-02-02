import RPi.GPIO as GPIO # Imports
import time

# modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# De pinnen
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# Pinnen van sonar
pinTrigger = 17
pinEcho = 18

# pinnen voor de LEDs
pinLedA = 24
pinLedB = 23

# Pinnen frequency
Frequency = 35

# Pin cycle, als precentage
DutyCycleA = 30
DutyCycleB = 30

# cycle 0, motor stoppen.
Stop = 0

# Pin Output
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

# pin output input
GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
GPIO.setup(pinEcho, GPIO.IN)      # Echo

# Zet pinnen als output
GPIO.setup(pinLedA, GPIO.OUT)   # Rood
GPIO.setup(pinLedB, GPIO.OUT)   # Blauw

# PWM Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

# Start PWM Cycle 0
pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)

# motoren uit
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Naar voren
def Forwards(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Naar Achter
def Backwards(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)

# Naar Links
def Left(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Naar Rechts
def Right(AdditionalSpeed):
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA + AdditionalSpeed)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB + AdditionalSpeed)

# Afstand meting
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
        # Als de senor te dichtbij is bij een ander object, dan kan
        # de PI de echo niet snel genoeg opvangen, dus hebben we een probleem
        # en melding in de console wat er is gebeurt.
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance

# De code
try:
    # Zet de trigger op False (Laag)
    GPIO.output(pinTrigger, False)

    # ff niks
    time.sleep(0.1)

    # Forever!
    while True:
        print("Seeking the car")
        GPIO.output(pinLedA, True)
        GPIO.output(pinLedB, False)

        SeekSize = 0.15 # Draai 0.25s
        SeekCount = 1 # Het aantal keer zoeken voor de andere auto
        MaxSeekCount = 8 # Het maximaal aantal keer dat de auto de andere auto zoekt

        # Of we al te lang aan het zoeken zijn
        while SeekCount <= MaxSeekCount:
            DistanceToObject = Measure()
            print(DistanceToObject)
            # Kijkt of de auto binnen bereik is
            if DistanceToObject <= 65:
                print('Within 50cm')
                GPIO.output(pinLedB, True)
                GPIO.output(pinLedA, False)
                # Als de auto te dichtbij is, moet ie langzamer gaan rijden
                if DistanceToObject <= 25:
                    Forwards(-10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # Als de auto aan de verwegge kant is, moet ie harder gaan rijden
                if DistanceToObject >= 35:
                    Forwards(10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # De standaard snelheid van de auto
                Forwards(0)
                time.sleep(1)
                StopMotors()
                continue

            Left(0)
            time.sleep(SeekSize)
            StopMotors()
            # Zoek teller toename met 1
            SeekCount += 1

# Als je op CTRL+C toetst, cleanup en stop
except KeyboardInterrupt:
    GPIO.cleanup()
