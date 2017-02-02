import RPi.GPIO as GPIO # Importeren GPIO
import time     # Importeren Time

# GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO pinnen voor sonar
pinTrigger = 17
pinEcho = 18

# Frequency
Frequency = 34
# Cycle tijd
CycleAperc = 30
CycleBperc = 30
# stoppen met draaien als 0
Stop = 0

# Motor pinnen
pinLinksVooruit = 10
pinLinksAchteruit = 9
pinRechtsVooruit = 8
pinRechtsAchteruit = 7

# Output Pin
GPIO.setup(pinLinksVooruit, GPIO.OUT)
GPIO.setup(pinLinksAchteruit, GPIO.OUT)
GPIO.setup(pinRechtsVooruit, GPIO.OUT)
GPIO.setup(pinRechtsAchteruit, GPIO.OUT)

# Pin output en input
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)       

# Frequency
pwmLinksVooruit = GPIO.PWM(pinLinksVooruit, Frequency)
pwmLinksAchteruit = GPIO.PWM(pinLinksAchteruit, Frequency)
pwmRechtsVooruit = GPIO.PWM(pinRechtsVooruit, Frequency)
pwmRechtsAchteruit = GPIO.PWM(pinRechtsAchteruit, Frequency)

# PWM cycle 0
pwmLinksVooruit.start(Stop)
pwmLinksAchteruit.start(Stop)
pwmRechtsVooruit.start(Stop)
pwmRechtsAchteruit.start(Stop)

# righting vooruit
def Forwards(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# naar achter
def Backwards(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)

# links draaien
def Left(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmRechtsVooruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# rechts draaien
def Right(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)

# Stoppen
def StopMotors():
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# meet de afstand
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

# De code
try:
     # Zet de trigger op False
    GPIO.output(pinTrigger, False)

    # ff stil
    time.sleep(0.1)

    
    while True:

        SeekSize = 0.15 # Draaien
        SeekCount = 1 # zoeken
        MaxSeekCount = 8 # max zoeken

        # Bepalen hoelang we al aan het zoeken zijn
        while SeekCount <= MaxSeekCount:
            DistanceToObject = Measure()
            print(DistanceToObject)
            # Afstandbepalen
            if DistanceToObject <= 60:
                print('Binnen 50cm') # het is binnen 50 cm

                # langzamer gaan rijden als het dichtbij is
                if DistanceToObject <= 24:
                    Forwards(-10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # harder gaan rijden als verweg is
                if DistanceToObject >= 34:
                    Forwards(10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # snelheid
                Forwards(0)
                time.sleep(1)
                StopMotors()
                continue

            Left(0)
            time.sleep(SeekSize)
            StopMotors()
            # Zoek
            SeekCount += 1

# Einde
except KeyboardInterrupt:
    GPIO.cleanup()
