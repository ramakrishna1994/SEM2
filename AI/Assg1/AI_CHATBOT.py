#!/usr/bin/python
import requests
import aiml
import os
import json


kernel = aiml.Kernel()
API_KEY = "a3550474b09bb6611e2f7269c0bb30ac"
WEATHER_API_CALL_FAILED = "weather api call failed"

# Function definition is here
def callweatherapi( query ):
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+query+'&appid='+API_KEY
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
        temp = data['main']['temp']-273
        result = 'Temperature in ' +newquery +' is '+str(temp) +' celsius'
        return result
    else :
        return 'Can you be a bit more specific!!'
    
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
        else:
            print "BOT(ANSWER)     >> " + answer
            
            
            
            
            
            
            

