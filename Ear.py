# import RPi.GPIO as GPIO
import csv
import os
import time
import traceback
from subprocess import call

import pygame
import speech_recognition as recognizer

import Actions
import Voice

# Start voice listener
listener = recognizer.Recognizer()

# Sets assistant name
name = "Jarvis"

#Sets admin name
adminName = "Adam"

# Variable setup
wakewordSaid = None
greeting = "Yes?"
phraseTime = 5
ext = False
lastSave = time.time()

#A list of all color codes for the lights
colors = {"red":"R", "orange":"O", "yellow":"Y", "green":"G", "blue":"B", "cyan":"C", "purple":"P", "white":"W", "on":"PWR", "off":"PWR", "pwr":"PWR"}

#Setup for gpio indicator
# indicator = GPIO.LOW
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(20, GPIO.OUT)
# indicatorLight = GPIO.PWM(20, 500)
# indicatorLight.start(100)
# on = 1000
# off = 0
isSleeping = False

#Setup to write commands and command types to a .csv file

#Command type, time, date
headers = ["Command type", "time", "date"]

if os.path.exists("log.csv") == False: 
    #Opens the log file in write mode
    log = open("log.csv", "w")
 
    #Creates the log writer instance
    logWriter = csv.writer(log)
     
    #Writes the headers
    logWriter.writerow(headers)
    print("Headers have been written")
else:
    #Opens the log file in append mode
    log = open("log.csv", "a")
    
    #Creates the log writer instance
    logWriter = csv.writer(log)
    




def idle():
    global isSleeping
    global p
    global ext
    global log, logWriter
    wakewordSaid = False
    logCommand = ""
    
    while wakewordSaid == False:
        
        with recognizer.Microphone() as source:
            #Adjust for the ambient noise
            listener.adjust_for_ambient_noise(source)
            #Or, you could do
            #listener.energy_threshold=300
            # Wait for the user to say something
            print("Say something!")
            # if isSleeping == False:
                # indicatorLight.ChangeDutyCycle(0.5)
            
            audio = listener.listen(source, phrase_time_limit = phraseTime)
            print('Said something')
            
        
        # Try to recognize the audio captured
        try:
            # indicatorLight.ChangeDutyCycle(0)
            stuffSaid = listener.recognize_google(audio)
            stuffSaid = stuffSaid.lower() + " "
            
            print(stuffSaid)
            
            # Check if the assistant has been called
            if name.lower() in stuffSaid:
                pygame.mixer.music.stop()
                if "light" in stuffSaid:
                        for c, v in colors.items():
                            if c in stuffSaid:
                                Actions.lights(v)
                        logCommand = "lights"

                elif "define" in stuffSaid:
                    index = stuffSaid.find("define")
                    index += 6 + 1
                    c = ""
                    term = ""
                    while c != " ":
                        print("looping 1")
                        c = stuffSaid[index]
                        term = term + c
                        index += 1
                    print("Getting definition")
                    words = Actions.define(term)
                    print("Got definition")
                    Voice.say(words)
                    logCommand = "define"
                    
                elif "what" in stuffSaid and "is it" in stuffSaid:
                    if "time" in stuffSaid:
                        Voice.say(Actions.what___IsIt("time"))
                        logCommand = "what time"    
                    elif "day" in stuffSaid or "date" in stuffSaid:
                        Voice.say(Actions.what___IsIt("date"))
                        logCommand = "what date"
                
                elif "weather" in stuffSaid and "tomorrow" in stuffSaid or "temperature" in stuffSaid and "tomorrow" in stuffSaid:
                    s = stuffSaid
                    nextOne = False
                    if "in" in stuffSaid:
                        i = stuffSaid.find(" in ")
                        location = s[i:i+3]
                        d = Actions.what___IsIt("day_only")
                        weather = Actions.forecast(d, location = location)
                        Voice.say("It will be {} degrees out in {}.".format(weather, location))
                        logCommand = "forecast in location"
                    else:
                        d = Actions.what___IsIt("day_only")
                        weather = Actions.forecast(d)
                        Voice.say("It will be {} degrees outside and {} tomorrow.".format(weather[0], weather[1]))
                        logCommand = "forecast at present location"
                
                elif "weather" in stuffSaid:
                    s = stuffSaid
                    if "in" in stuffSaid:
                        i = stuffSaid.find(" in ")
                        s = s[i+4:]
                        weather = Actions.getWeather()
                        Voice.say("It is currently {} degrees outside and {} in {}.".format(weather[0], weather[1], s))
                        logCommand = "weather at location"
                    else:
                        weather = Actions.getWeather()
                        Voice.say("It is currently {} degrees outside and {}".format(weather[1], weather[0]))
                        logCommand = "weather at present location"
                
                elif "temperature" in stuffSaid:
                    s = stuffSaid
                    if "in" in stuffSaid:
                        i = stuffSaid.find(" in ")
                        s = s[i+4:]
                        weather = Actions.getWeather(t = "temperature", location = s)
                        Voice.say("It is currently {} degrees out in {}.".format(weather, s))
                        logCommand = "temperature in location"
                    else:
                        weather = Actions.getWeather()
                        Voice.say("It is currently {} degrees outside.".format(weather[1], weather[0]))
                        logCommand = "temperature at present location"
                
                elif "dance to my music" in stuffSaid or "dance" in stuffSaid:
                    Actions.lightDance()
                    logCommand = "music dance"
                
                elif "are you on" in stuffSaid:
                    Voice.say("Yes")
                    logCommand = "are you on"
                    
                elif "good night" in stuffSaid or "goodnight" in stuffSaid:
                    isSleeping = True
                    Voice.say("Good night " + adminName)
                    Actions.lights("PWR")
                    logCommand = "good night"
                
                elif "good morning" in stuffSaid or "goodmorning" in stuffSaid:
                    isSleeping = False
                    Voice.say("Good morning " + adminName)
                    Actions.lights("PWR")
                    Voice.say("It is currently {}, and it is {} and {} degrees outside. The high today will be {}".format(Actions.what___IsIt("time"), Actions.getWeather()[0], Actions.getWeather()[1], Actions.forecast(Actions.what___IsIt("day_only"))))
                    logCommand = "good morning"
                    
                elif "trigger shutdown" in stuffSaid:
                    Voice.say("Shutting down systems")
                    while Voice.words.get_busy():
                        p = 1
                    call("sudo shutdown -h ", shell=True)
                    logCommand = "trigger shutdown"
                    
                elif "do you like men" in stuffSaid:
                    Voice.say("Only if that man is you winky emoji")
    
                elif "when are you listening" in stuffSaid:
                    Voice.say("Always")
                    
                elif "open the pod bay doors" in stuffSaid:
                    Voice.say("I can not do that dave")
                    
                elif "i am your father" in stuffSaid or "i'm your father" in stuffSaid:
                    Voice.say("no o o o")
                    
                elif "love me" in stuffSaid:
                    Voice.say("Not to be rude or anything, but nobody could ever love you")
                

                elif "stop" in stuffSaid:
                    pygame.mixer.music.stop()
                    logCommand = "stop audio"
                
                elif "trigger process end" in stuffSaid:
                    logCommand = "shutdown jarvis"
                    ext = True
                    
                elif "save log" in stuffSaid or "say vlog" in stuffSaid:
                    log.close()
                    
                    #Opens the log file in append mode
                    log = open("log.csv", "a")
                    
                    #Creates the log writer instance
                    logWriter = csv.writer(log)
                    
                    Voice.say("Saved logs")
                
                else:
                    Voice.say("I was unable to understand what you said.")
                    logCommand = "summoned but no valid command"
                    
                
                date = Actions.what___IsIt("raw_date")
                tim = Actions.what___IsIt("time")
                
                logWriter.writerow([logCommand, tim, "{}/{}/{}".format(date[0], date[1], date[2])])
                
                if time.time()-lastSave > 90:
                    log.close()
                    
                    #Opens the log file in append mode
                    log = open("log.csv", "a")
                    
                    #Creates the log writer instance
                    logWriter = csv.writer(log)
                
                
                
            else:
                print(stuffSaid)
                
        
        #Error handling
        except recognizer.UnknownValueError:
            print("Could not understand audio.")
        except recognizer.RequestError as e:
            print("Request from Google Speech Recognition failed; {0}".format(e))
        except Exception as e:
            print("Exception at {}, :{}".format(time.time(), traceback.print_exc()))
        
        if ext == True:
            log.close()
            raise SystemExit("Exiting system because 'trigger process end' was said")
    

