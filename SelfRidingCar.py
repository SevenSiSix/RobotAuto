'''IMPORTEREN VAN ALLE LIBRARY'S'''
import RPi.GPIO as GPIO
import time
import random
#---------------------------------------------------------

'''PINMODES AANGEVEN'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#---------------------------------------------------------

'''OP WELKE PINS ZITTEN DE MOTOREN'''
pinLinksVooruit = 10
pinLinksAchteruit = 9
pinRechtsVooruit = 8
pinRechtsAchteruit = 7
#---------------------------------------------------------

'''OP WELKE PINS ZITTEN DE 'OGEN' '''
pinStuurSignaal = 17
pinOntvangSignaal = 18
#---------------------------------------------------------

'''OP WELKE PINS ZITTEN DE LEDS'''
pinLedEen = 22
pinLedTwee = 23
#---------------------------------------------------------

'''FREQUENTIE VAN DE WIELEN, HOEVAAK AAN/UIT PER SECONDE'''
frequentie = 10
#---------------------------------------------------------

'''PROCENTEN DAT DE WIELEN AAN MOETEN STAAN'''
rondjesLinks = 30
rondjesRechts = 30
stop = 0
#---------------------------------------------------------

'''ZIJN DE PINNEN IN/OUT-PUT'''
GPIO.setup(pinLinksVooruit, GPIO.OUT)
GPIO.setup(pinLinksAchteruit, GPIO.OUT)
GPIO.setup(pinRechtsVooruit, GPIO.OUT)
GPIO.setup(pinRechtsAchteruit, GPIO.OUT)

GPIO.setup(pinStuurSignaal, GPIO.OUT)
GPIO.setup(pinOntvangSignaal, GPIO.IN)
#---------------------------------------------------------

'''VARIABELE VOOR AFSTANDSMETING'''
hoeDichtBij = 20.0
#---------------------------------------------------------

'''VARIABELE VOOR RANDOMIZER'''
naarRechtsOfLinks = 0
#---------------------------------------------------------

'''ZET PWM OP 'FREQUENTIE' '''
pwmMotorLinksVooruit = GPIO.PWM(pinLinksVooruit, frequentie)
pwmMotorLinksAchteruit = GPIO.PWM(pinLinksAchteruit, frequentie)
pwmMotorRechtsVooruit = GPIO.PWM(pinRechtsVooruit, frequentie)
pwmMotorRechtsAchteruit = GPIO.PWM(pinRechtsAchteruit, frequentie)
#---------------------------------------------------------

'''ZET ALLES UIT'''
pwmMotorLinksVooruit.start(stop)
pwmMotorLinksAchteruit.start(stop)
pwmMotorRechtsVooruit.start(stop)
pwmMotorRechtsAchteruit.start(stop)
#---------------------------------------------------------

'''FUNCTIE VOOR ALLE MOTORS UIT'''
def motorsUit():
    pwmMotorLinksVooruit.ChangeDutyCycle(stop)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)
#---------------------------------------------------------

'''FUNCTIE VOOR VOORUIT'''
def rijVooruit():
    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(rondjesRechts)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)
#---------------------------------------------------------

'''FUNCTIE VOOR ACHTERUIT'''
def rijAchteruit():
    pwmMotorLinksVooruit.ChangeDutyCycle(stop)
    pwmMotorLinksAchteruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(rondjesRechts)

'''FUNCTIE VOOR LINKS'''
def Links():
    pwmMotorLinksVooruit.ChangeDutyCycle(stop)
    pwmMotorLinksAchteruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorRechtsVooruit.ChangeDutyCycle(rondjesRechts)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)
#---------------------------------------------------------

'''FUNCTIE VOOR RECHTS'''
def Rechts():
    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(rondjesRechts)
#---------------------------------------------------------

'''FUNCITE VOOR AFSTAND METEN'''
def meetAfstand():
    GPIO.output(pinStuurSignaal, True)
    time.sleep(0.00001)
    GPIO.output(pinStuurSignaal, False)
    StartTime = time.time()
    StopTime = StartTime
    while GPIO.input(pinOntvangSignaal) == 0:
        StartTime = time.time()
        StopTime = StartTime
    while GPIO.input(pinOntvangSignaal) == 1:
        StopTime = time.time()
    return ((StopTime-StartTime)*34326)/2
#---------------------------------------------------------

'''DETECTEREN VAN OBSTAKEL'''
def isObstakel(lokaleHoeDichtBij):
    return meetAfstand() < lokaleHoeDichtBij
#---------------------------------------------------------

'''VERMIJD OBSTAKEL DOOR NAAR LINKS TE DRAAIEN'''
def vermijdObstakelLinks():
    motorsUit()
    Links()
#---------------------------------------------------------

'''VERMIJD OBSTAKEL DOOR NAAR RECHTS TE DRAAIEN'''
def vermijdObstakelRechts():
    motorsUit()
    Rechts()
#---------------------------------------------------------

'''HOOFDPROGRAMMA'''
try:
    GPIO.output(pinStuurSignaal, False)
    time.sleep(0.1)
    while True:
            '''ZOLANG ER GEEN OBSTAKEL IS, RIJ VOORUIT'''
            rijVooruit()
            time.sleep(0.1)
            naarRechtsOfLinks = random.randrange(2)
            GPIO.output(pinLedEen, 1)
            GPIO.output(pinLedTwee, 1)
            print naarRechtsOfLinks
            '''ZOLANG ER EEN OBSTAKEL IS, EN naarRechtsOfLinks IS 0, DRAAI DAN NAAR LINKS (EN BLIJF DRAAIEN VOOR EEN HALVE SECONDE)'''
            while(isObstakel(hoeDichtBij) and naarRechtsOfLinks == 0):
                GPIO.output(pinLedTwee, 0)
                print 'IK GA NAAR LINKS'
                vermijdObstakelLinks()
                time.sleep(0.5)
                motorsUit()
            '''ZOLANG ER EEN OBSTAKEL IS, EN naarRechtsOfLinks IS 1, DRAAI DAN NAAR RECHTS (EN BLIJF DRAAIEN VOOR EEN HALVE SECONDE)'''
            while(isObstakel(hoeDichtBij) and naarRechtsOfLinks == 1):
                GPIO.output(pinLedEen, 0)
                print 'IK GA NAAR RECHTS'
                vermijdObstakelRechts()
                time.sleep(0.5)
                motorsUit()
except KeyboardInterrupt:
    GPIO.cleanup()
