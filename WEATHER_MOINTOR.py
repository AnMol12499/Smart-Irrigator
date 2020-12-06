
## THIS CODE NEEDS TO BE USED  TO  CREATE LAMBDA FUNCTION ON AWS LAMBDA SERVICES..
## A TRIGGER USING AWS CLOUDWATCH SERVICE NEEDS TO BE SET TO RUN THIS LAMBDA FUNCTION EVERY HOUR...

import json
import requests as r
import time as t


def call(ncco2):     # NEXMO API is used for Calling to The Farmer Phoneno 
    import nexmo
    client = nexmo.Client(
  application_id='6b6ecXXXf8be014d43',
  private_key='private.key',
)   
    response = client.create_call({
     'to': [{
    'type': 'phone',
    'number': '919XXXXX7293'
     }],
    'from': {
    'type': 'phone',
    'number': '91XXXXX7293'
     },
    'ncco': ncco2
     })
   

def msg():    # Msg91 Api is used for sending SMS to Farmer
    url='https://api.msg91.com/api/sendhttp.php?mobiles={}&authkey=295902AXXXX369&route=4&sender=BOLTIO&message={}&country=91'
    mobiles='98XXXXX7293'
    message="This message is from Smart Irrigator.Please check the Status of weatherForecast using webapp at http://172.XX.4X0.106:XX02 "
    URL=url.format(mobiles,message)
    w=r.get(URL)



def location():          # webscraping the  website(https://mylocation.org/) for getting geolocation coordinate of the place..
    from bs4 import BeautifulSoup as bs
    url='https://mylocation.org/'
    w=r.get(url)
    soup=bs(w.text,'html.parser')
    wa=soup.find_all('div',{'class':'info'})
    q=wa[0].find_all('td')
    return (q[3].get_text(),q[5].get_text())


def weather_predict():    ## here Dark sky api is used for getting the Rainfall prediction data at particular location
    import requests as r
    l=location()
    url='https://api.darksky.net/forecast/0752c5572a60c4831d7e17d3ebb3fd8a/{},{}/'
    url=url.format(l[0],l[1])
    w=r.get(url)
    ans=w.json()
    #weather status
    status=[]
    status.append(ans['currently']['summary'])
    status.append(ans['hourly']['summary'])
    status.append(ans['daily']['summary'])
    #chance of rain 
    p=ans['currently']['precipProbability']
    p=p*100
    return [status,p]

# This Script parses the Rainfall prediction data every hour and sends the alert msg and generate system call to Farmer in case it exceeds Threshold..
Threshold_value=50 
while 1:          
    report=weather_predict()

    if report[1]>Threshold_value:
        data=[
        {
        "action": "talk",
       #"voiceName": "Russell",
        "text": '''Hello this message is from Smart Irrigator .kindly Visit  the webapp to check the rainfall forcast status'''
       }
     ]
        call(data)
        msg()
    t.sleep(3600) # THIS STATEMENT NEEDS TO BE COMMENTED IF THIS CODE IS USED ON AWS LAMBDA


