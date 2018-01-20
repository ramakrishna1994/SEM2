#!/usr/bin/python
import requests
import aiml
import os
import json
from pkg_resources._vendor.pyparsing import empty


kernel = aiml.Kernel()
API_KEY = "a3550474b09bb6611e2f7269c0bb30ac"
WEATHER_API_CALL_FAILED = "weather api call failed"

# Function definition is here
def callweatherapi( query ):
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+query+'&appid='+API_KEY+'&units=metric'
    response = requests.get(url)
    if(response.status_code == 200):
        x = response.content
        data = json.loads(x)
        return data
    else:
        return WEATHER_API_CALL_FAILED

def printtemperature(answer):
    newquery = kernel.respond(answer)
    data = callweatherapi(newquery)
    if data != WEATHER_API_CALL_FAILED:
        temp = data['main']['temp']
        maxtemp = data['main']['temp_max']
        result = 'Temperature in ' +newquery +' is currently '+str(temp) +' celsius and it can reach upto '+ str(maxtemp) +' celsius. Take Care !!'
        return result
    else :
       return 'Can you be a bit more specific!! I am not able to find city name'
    
def printhumidity(answer):
    newquery = kernel.respond(answer)
    data = callweatherapi(newquery)
    if data != WEATHER_API_CALL_FAILED:
        humd = data['main']['humidity']
        result = 'Humidity in ' +newquery +' is currently '+str(humd) +'%'
        return result
    else :
        return 'Can you be a bit more specific!! I am not able to find city name'
    
def printweather(answer):
    newquery = kernel.respond(answer)
    data = callweatherapi(newquery)
    if data != WEATHER_API_CALL_FAILED:
        weath = data['weather'][0]['description']
        humd = data['main']['humidity']
        temp = data['main']['temp']
        result = 'Current Weather in ' +newquery +' : '+ str(weath) + ' with temperature '+str(temp) + ' celsius and humidity ' +str(humd)+'%'
        return result
    else :
        return 'Can you be a bit more specific!! I am not able to find city name'
    
# Create the kernel and learn AIML files
kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "reload")
    kernel.saveBrain("bot_brain.brn")

# Press CTRL-C to break this loop
while True:
    query = raw_input("HUMAN(QUESTION) >> ")
    if query == "quit" :
        exit()
    elif query == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        answer = kernel.respond(query)
        if "temperature" in answer:
            print "BOT(ANSWER)     >> " + printtemperature(answer)
        elif "humidity" in answer:
            print "BOT(ANSWER)     >> " + printhumidity(answer)
        elif "weather" in answer:
            print "BOT(ANSWER)     >> " + printweather(answer)
        elif answer == "":
            continue
        else:
            print "BOT(ANSWER)     >> " + answer
            
            
            
            
            
            
            

