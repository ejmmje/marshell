#Elliot Marshallsay
#3238 5316


import aiml
import os
import requests
import json
import time
import datetime



# kernel is responsible for responding to users
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
dirname = 'aiml_data'
filenames = [os.path.join(dirname, f) for f in os.listdir(dirname)]
aiml_filenames = [f for f in filenames if os.path.splitext(f)[1]=='.aiml']

kernel = aiml.Kernel()
for filename in aiml_filenames:
    kernel.learn(filename)

DarkSkyApiKey = '3464f55c1654b4b097e868aef603ebbc'
DarkSkyURL = 'https://api.darksky.net/forecast'
GoogleAPIKey = 'AIzaSyBPinPBorvHVa3OxTNkbCod0Hnyh2hqE4U'



CACHE_FNAME = 'cache.json'


try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


def getWithCaching(baseURL, params={}):

    req = requests.Request(method = 'GET', url = baseURL, params = sorted(params.items()))
    prepped = req.prepare()
    fullURL = prepped.url

    # if we haven't seen this URL before
    if fullURL not in CACHE_DICTION:
    # make the request and store the response
        response = requests.Session().send(prepped)
        CACHE_DICTION[fullURL] = response.text

    # write the updated cache file
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    elif fullURL in CACHE_DICTION and 'darksky' in fullURL:
        if time.time() > (json.loads(CACHE_DICTION[fullURL])['currently']['time'] + (5*60)):
            print ("Getting New Data...")
            response = requests.Session().send(prepped)
            CACHE_DICTION[fullURL] = response.text
            cache_file = open(CACHE_FNAME, 'w')
            cache_file.write(json.dumps(CACHE_DICTION))
            cache_file.close()
            return CACHE_DICTION[fullURL]


    return CACHE_DICTION[fullURL]


def getPosition(x):
    try:
        google_result = getWithCaching('https://maps.googleapis.com/maps/api/geocode/json', params={
        'key': GoogleAPIKey,
        'address': x
        })
        result = json.loads(google_result)
        lng = result['results'][0]['geometry']['location']['lng']
        lat = result['results'][0]['geometry']['location']['lat']
        return lat,lng
    except:
        return 'Is {} a city?'.format(x)


def getWeather(x):
    try:
        lat,lng = getPosition(x)
        target_url = '{}/{}/{},{}'.format(DarkSkyURL,DarkSkyApiKey,lat,lng)
        request_data = getWithCaching(target_url)
        data_weather = json.loads(request_data)

        return data_weather
    except:
        return "Sorry, I don't know."



def getDailyWeather(x):
    try:
        response = getWeather(x)
        temp = response['currently']['temperature']
        summ = response['currently']['summary']
        return 'In {}, it is {} degrees and {}'.format(x,temp,summ)
    except:
        return 'There was an issue with retrieving the daily weather for {}. Is {} a city?'.format(x,x)

def getDailyRain(x):
    try:
        response = getWeather(x)
        chance = response['daily']['data'][0]['precipProbability']
        temp = []
        total_temp = 0
        avg_temp = 0
        for nice in response['hourly']['data']:
            if len(temp) < 24:
                temp.append(nice['temperature'])
        for zz in temp:
            total_temp += zz
        avg_temp = total_temp / 24
        if avg_temp > 32.00:
            if chance > 0.9:
                return 'It will almost definitely rain in {}'.format(x)
            elif chance > 0.5:
                return 'It probably will rain in {}'.format(x)
            elif chance > 0.1:
                return 'It probably will not rain in {}'.format(x)
            else:
                return 'It almost definitely will not rain in {}'.format(x)
        else:
            print('...The average hourly temperature is below 32.00 degrees Fahrenheit!')
            if chance > 0.9:
                return 'It will almost definitely snow in {}'.format(x)
            elif chance > 0.5:
                return 'It probably will snow in {}'.format(x)
            elif chance > 0.1:
                return 'It probably will not snow in {}'.format(x)
            else:
                return 'It almost definitely will not snow in {}'.format(x)
    except:
        return 'There was an issue with retrieving the daily precipitation for {}. Is {} a city?'.format(x,x)

def getDailyHot(x):
    try:
        response = getWeather(x)
        hots = []
        final_hot = 0
        for tt in response['hourly']['data']:
            hots.append(tt['temperature'])
        for hh in hots:
            if hh > final_hot:
                final_hot = hh
        return 'In {}, it will reach {} degrees'.format(x,final_hot)
    except:
        return 'There was an issue with retrieving the daily high temperature for {}. Is {} a city?'.format(x,x)

def getDailyCold(x):
    try:
        response = getWeather(x)
        colds = []
        final = 99999
        for y in response['hourly']['data']:
            colds.append(y['temperature'])
        for z in colds:
            if z < final:
                final = z
        return 'In {}, the low is {} degrees'.format(x,final)
    except:
        return 'There was an issue with retrieving the daily low temperature for {}. Is {} a city?'.format(x,x)

def getWeeklyHot(x):
    try:
        response = getWeather(x)
        week_temps = []
        for a in response['daily']['data']:
            week_temps.append(a['temperatureHigh'])
        current_high = 0
        for b in week_temps:
            if b > current_high:
                current_high = b
        return 'In {}, the high is {} degrees'.format(x,current_high)
    except:
        return 'There was an issue with retrieving the weekly high temperature for {}. Is {} a city?'.format(x,x)

def getWeeklyCold(x):
    try:
        response = getWeather(x)
        week_colds = []
        for y in response['daily']['data']:
            week_colds.append(y['temperatureLow'])
        current_low = 999999
        for z in week_colds:
            if z < current_low:
                current_low = z
        return 'In {}, the coldest it will reach this week is {} degrees'.format(x,current_low)
    except:
        return 'There was an issue with retrieving the weekly low tempurature for {}. Is {} a city?'.format(x,x)

def getWeeklyRain(x):
    try:
        response = getWeather(x)
        weekly_chances = []
        total = 1
        final = 0
        temp = []
        total_temp = 0
        avg_temp = 0
        for snw in response['daily']['data']:
            temp.append(snw['temperatureHigh'])
        for avg in temp:
            total_temp += avg
        avg_temp = total_temp / 7
        for y in response['daily']['data']:
            weekly_chances.append(1 - (y['precipProbability']))
        for z in weekly_chances:
            total = total * z
        final = 1 - total
        if avg_temp > 32.00:
            if final > 0.9:
                return 'It will almost definitely rain in {}'.format(x)
            elif final > 0.5:
                return 'It probably will rain in {}'.format(x)
            elif final > 0.1:
                return 'It probably will not rain in {}'.format(x)
            else:
                return 'It almost definitely will not rain in {}'.format(x)
        else:
            print('...This week, the average daily high tempurature is below 32.00 degrees Fahrenheit!')
            if final > 0.9:
                return 'It will almost definitely snow in {}'.format(x)
            elif final > 0.5:
                return 'It probably will snow in {}'.format(x)
            elif final > 0.1:
                return 'It probably will not snow in {}'.format(x)
            else:
                return 'It almost definitely will not snow in {}'.format(x)
    except:
        return 'There was an issue with retrieving the weekly precipitation probability for {}. Is {} a city?'.format(x,x)


kernel.addPattern("What's the weather like in {x}?", getDailyWeather)
kernel.addPattern('Is it going to rain in {x} today?', getDailyRain)
kernel.addPattern('How hot will it get in {x} today?', getDailyHot)
kernel.addPattern('How cold will it get in {x} today?', getDailyCold)
kernel.addPattern('Is it going to rain in {x} this week?', getWeeklyRain)
kernel.addPattern('How hot will it get in {x} this week?', getWeeklyHot)
kernel.addPattern('How cold will it get in {x} this week?', getWeeklyCold)



print('\n')
print('-'*40)
print("Hello. I am your leader. You may call me Weather Bot.\n")
print('Please, say Hello.')
queries = ''
while queries != 'exit':
    print('...{}\n'.format(kernel.respond(queries)))
    queries = input('> ')

print('\n')
print("Goodbye, thank you for using Elliot's Weather Bot.")
print('-'*40)
