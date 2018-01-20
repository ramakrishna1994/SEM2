import cricbuzz 
import json

c = cricbuzz.Cricbuzz()
matches = c.matches()
for match in matches:    
    data = json.loads(json.dumps(c.livescore(match['id'])))
    if data != None :
        print data['matchinfo']['mchdesc'] + ' (' + data['matchinfo']['status'] +')'
        print data['batting']['team'] + ' -- ' + data['batting']['score'][0]['runs'] + '/' + data['batting']['score'][0]['wickets'] + ' (' + data['batting']['score'][0]['overs'] + ')'
        print data['bowling']['team'] + ' -- ' + data['bowling']['score'][0]['runs'] + '/' + data['bowling']['score'][0]['wickets'] + ' (' + data['bowling']['score'][0]['overs'] + ')'
    print '--------------------'

with open('city.list.json') as json_data:
    cities = json.load(json_data)
    for city in cities:
        print city['id']
        break
    