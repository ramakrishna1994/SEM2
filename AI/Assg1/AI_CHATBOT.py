#!/usr/bin/python
import requests
import aiml
import os
import json
import cricbuzz 

kernel = aiml.Kernel()
API_KEY = "a3550474b09bb6611e2f7269c0bb30ac"
WEATHER_API_CALL_FAILED = "weather api call failed"
c = cricbuzz.Cricbuzz()
matches = c.matches()
with open('city.list.json') as json_data:
        cities = json.load(json_data)
        

def getcityid(cityname):
    for city in cities:                                                                                                 
        if cityname.lower() in city['name'].lower():
            #print city['id'] , city['name'].lower()
            return city['id']
        
# Function definition is here
def callweatherapi( query ):
    id = getcityid(query)
    url = 'http://api.openweathermap.org/data/2.5/weather?id='+str(id)+'&appid='+API_KEY+'&units=metric'
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
    
def printcricketscores():
    for match in matches:    
        data = json.loads(json.dumps(c.livescore(match['id'])))
        if data != None :
            print data['matchinfo']['mchdesc'] + ' (' + data['matchinfo']['status'] +')' + ' (' + data['matchinfo']['srs'] +')'  
            print data['batting']['team'] + ' -- ' + data['batting']['score'][0]['runs'] + '/' + data['batting']['score'][0]['wickets'] + ' (' + data['batting']['score'][0]['overs'] + ')'
            print data['bowling']['team'] + ' -- ' + data['bowling']['score'][0]['runs'] + '/' + data['bowling']['score'][0]['wickets'] + ' (' + data['bowling']['score'][0]['overs'] + ')'
        print '--------------------'
    
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
        elif "cricket" in answer:
            print "BOT(ANSWER)     >> Below are the cricket scores!!" 
            printcricketscores()
        elif answer == "":
            continue
        else:
            print "BOT(ANSWER)     >> " + answer
            
            
            
            
            
            
            

