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

'''OP WELKE PINS ZIT DE LICHTSENSOR'''
pinCheckLijn = 25


'''OP WELKE PINS ZITTEN DE LEDJES'''
pinLED1 = 22
pinLED2 = 23
#----------------------------------------------------------

'''FREQUENTIE VAN DE WIELEN, HOEVAAK AAN/UIT PER SECONDE'''
frequentie = 25
#---------------------------------------------------------

'''PROCENTEN DAT DE WIELEN AAN MOETEN STAAN'''
rondjesLinks = 40
rondjesRechts = 45
#---------------------------------------------------------

'''VARIABELE VOOR HET STOPPEN VAN DE AUTO'''
stop = 0
#---------------------------------------------------------

'''ZIJN DE PINNEN IN/OUT-PUT'''
GPIO.setup(pinLinksVooruit, GPIO.OUT)
GPIO.setup(pinLinksAchteruit, GPIO.OUT)
GPIO.setup(pinRechtsVooruit, GPIO.OUT)
GPIO.setup(pinRechtsAchteruit, GPIO.OUT)

GPIO.setup(pinStuurSignaal, GPIO.OUT)
GPIO.setup(pinOntvangSignaal, GPIO.IN)

GPIO.setup(pinCheckLijn, GPIO.IN)

GPIO.setup(pinLED1, GPIO.OUT)
GPIO.setup(pinLED2, GPIO.OUT)
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

'''FUNCTIE VOOR HALFLINKS'''
def HalfLinks():
    pwmMotorLinksVooruit.ChangeDutyCycle(stop)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(rondjesRechts)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)
#---------------------------------------------------------

'''FUNCTIE VOOR RECHTS'''
def Rechts():
    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(rondjesRechts)
	
'''FUNCTIE VOOR HALFRECHTS'''
def HalfRechts():
    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)
    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)
    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)
    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)
#---------------------------------------------------------

'''DETECTEREN VAN LIJN'''
try:
	while True:
		#Als de sensor geen licht oppikt is het oppervlak zwart, gaat het autootje naar rechts en het rechterlampje aan
		if GPIO.input(pinCheckLijn)==0:
			GPIO.output(pinLED1, 1)
			GPIO.output(pinLED2, 0)
			Rechts()
		#Als de sensor wel iets oppikt gaat het autootje naar links en het linker lampje aan
		else:
			GPIO.output(pinLED2, 1)
			GPIO.output(pinLED1, 0)
			HalfLinks()
		
#Stop het script met CTRL + C 
except KeyboardInterrupt:
	GPIO.cleanup()


