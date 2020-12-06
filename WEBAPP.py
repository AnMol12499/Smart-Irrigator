
##### This code can be  hosted on AWS EC2 to access it world wide######## 
import streamlit as st
import time as t
import json
import requests as r
import datetime as d

def statusdevice(): # show the status of bolt device
    urlstatus='https://cloud.boltiot.com/remote/ca609XXX-178fcae8b0f2/isOnline?&deviceName=BOLTXXXX'
    w=r.get(urlstatus)
    if w.status_code==200:
        status=json.loads(w.text)
        if status['value']=='online':
        	st.success('DEVICE IS ONLINE')
        else:
        	st.info("device is offline")       
    else:
    	status=json.loads(w.text)
    	if 'You have been rate limited' in status['value']:
    		st.warning('Sorry!!'+status['value'])
    	else:
    		st.warning("INTERNET PROBLEM OR DEVICE NOT ACCESSED")


def restart(): # to restart bolt device
    urlrestart='https://cloud.boltiot.com/remote/ca6097XXXXfcae8b0f2/restart?&deviceName=BOLTXXXX'
    response=r.get(urlrestart)
    if response.status_code==200:
        resp=json.loads(response.text)
        if resp['value']=='Restarted':
            st.success('RESTARTED SUCCESSFULLY!!!!!..')
    else:
    	resp=json.loads(response.text)
    	if 'You have been rate limited' in resp['value']:
    		st.warning('Sorry!!'+status['value'])
    	else:
    		st.warning('Internet connection problem')

def on(): # to turn ON the water pump connected to pin no 1 of BOLT device
    urlon='https://cloud.boltiot.com/remote/ca609XXXX-ad7e-178XXX8b0f2/digitalWrite?pin=1&state=HIGH&deviceName=BOLTXXXX'
    on=r.get(urlon)
    if on.status_code==200:
        on=json.loads(on.text)
        if on['value']=='1':
             st.success('WATER PUMP turns on')
        elif 'Device is offline' in on['value'] :
    	     st.warning('Sorry!!! '+on['value'])
    else:
        st.info('internet problem')

def ont(): # to turn water pump for given period of time
    urlon='https://cloud.boltiot.com/remote/ca6097c8-XXXXXXX78fcae8b0f2/digitalWrite?pin=1&state=HIGH&deviceName=BOLTXXXX'
    on=r.get(urlon)
    if on.status_code==200:
        on=json.loads(on.text)
        if on['value']=='1':
             print('onnn')
             #st.success('WATER PUMP turns on')
        elif 'Device is offline' in on['value'] :
             st.warning('Sorry!!! '+on['value'])
    else:
        st.info('internet problem')

    
def off(): # to turn OFF  water pump connected to pin no 1 of BOLT device
    urloff='https://cloud.boltiot.com/remote/ca6097XXXXXX7e-178fcae8b0f2/digitalWrite?pin=1&state=LOW&deviceName=BOLTXXXXX'
    off=r.get(urloff)
    if off.status_code==200:
    	off=json.loads(off.text)
    	if off['value']=='1':
    		st.info('WATER PUMP turns off')
    	elif 'Device is offline' in off['value']:
    		st.warning('Sorry!!! '+off['value'])
        
    else:
        print('internet problem')
        st.info('internet problem')


def readanalog(): # to read analog pin AO attached with Temperature sensor
    urlA0='https://cloud.boltiot.com/remote/ca6097c8XXXXX-178fcae8b0f2/analogRead?pin=A0&deviceName=BOLTXXXX'
    analogRead=r.get(urlA0)
    if analogRead.status_code==200:
        ar=json.loads(analogRead.text)
        if ('Command timed out' not in ar['value']) or ('Device is offline' not in ar['value']):
            print(ar['value'])
            return ar['value']

def mylocation(): # to extract the location of place 
    import requests as r
    from bs4 import BeautifulSoup as bs
    url='https://mylocation.org/'
    w=r.get(url)
    soup=bs(w.text,'html.parser')
    wa=soup.find_all('div',{'class':'info'})
    q=wa[0].find_all('td')
    return (q[3].get_text(),q[5].get_text())


def weather_predict():# to get weather report of extracted location
    l=mylocation()
    url='https://api.darksky.net/forecast/0752cXXXXXXXebb3fd8a/{},{}/'
    url=url.format(l[0],l[1])
    w=r.get(url)
    ans=w.json()
    #weather status
    status=[]
    status.append(ans['currently']['summary'])
    status.append(ans['hourly']['summary'])
    status.append(ans['daily']['summary'])
    #summary='|'.join(status)
    #chance of rain 
    p=ans['currently']['precipProbability']
    p=p*100
    return [status,p]
    
st.title('SMART IRRIGATOR')
st.subheader( 'Bolt IOT')
from PIL import Image
img=Image.open('weather.jpeg')
st.image(img,width=450)
status= st.button('Bolt Status')
if status:
   statusdevice()
W=st.button('RESTART')
if W:
	with st.spinner('Restarting......'):
		t.sleep(1)
	restart()


st.header('||Irrigation Timing||')
temp=st.button('<<<<||Surrounding Temparture||>>>>')
if temp:
    anal=readanalog()
    ana=int(anal)*0.0488
    ana=round(ana,1)
    st.info('THE CURRENT TEMPERATURE: '+str(ana)+'Celsuis')
    if ana>=5 and ana<=10:
        ot=10
    elif ana>10 and ana<=15:
        ot=15
    elif ana>15 and ana<=20:
        ot=20
    else:
        ot=''
    st.info('Optimum Operating Time:'+str(ot)+'min.')

st.header('||RAINFALL PREDICTION||')
wr=st.button('<<<<||RAINFALL_PREDICTION__REPORT||>>>>')
if wr:
    report=weather_predict()
    st.markdown('RAINFALL STATUS')
    st.info(report[0][0])
    st.info(report[0][1])
    st.info(report[0][2])
    st.markdown('PRECIP_PROBABILITY')
    st.info('The Chance of RAINFALL -'+str(report[1])+' %')
    if report[1]>50:
        st.warning('No Need to Operate Water Pump in order To conserve Water')
    else:
        st.success('Water Pump can be Operate for Optimal Timing Based on Surrounding Temperture ')

timer=st.time_input("ENTER TIME FOR PUMP TO OPERATE",d.time())
settime=timer.hour+timer.minute/60
w=st.radio('PUMP CONTROL',('ON','OFF'))
s=st.button('DONE')

if w=='ON' and s and settime!=0:
    ont()
    with st.spinner('Pump turns on for {} seconds....'.format(settime)):
        t.sleep(settime)
    off()
    
elif w=="OFF" and s:
         off()


