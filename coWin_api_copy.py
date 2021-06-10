#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print('Hello')


# In[ ]:


import requests
import json
import winsound
import pandas as pd
import datetime
import time
from IPython.display import clear_output



# enter path of any sound in wav format
filename = 'mixkit-doorbell-single-press-333.wav'


# In[ ]:


counter=0
while True:
    clear_output(wait=True)
    print('counter :',counter)
    counter = counter+1
    NextDay_Date = datetime.datetime.today() #+ datetime.timedelta(days=1)
    NextDay_Date_Formatted = NextDay_Date.strftime ('%d-%m-%Y') # format the date to ddmmyyyy
#  enter your picode and date in the endpoint
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=<PINCODE>&date={a}".format(a=NextDay_Date_Formatted))

    print('response status :',response.status_code)
    json_response =response.json()
    df1=pd.DataFrame(columns=['name','pincode','date','vaccine','age','dose','dose2'])

    for i in range(len(json_response['centers'])):
        
#         print(json_response['centers'][i]['name'],json_response['centers'][i]['pincode'])
        for j in range(len(json_response['centers'][i]['sessions'])):
            to_append=[json_response['centers'][i]['name']
                       ,json_response['centers'][i]['pincode']
                       ,json_response['centers'][i]['sessions'][j]['date']
                       ,json_response['centers'][i]['sessions'][j]['vaccine']
                       ,json_response['centers'][i]['sessions'][j]['min_age_limit']
                       ,json_response['centers'][i]['sessions'][j]['available_capacity']
                       ,json_response['centers'][i]['sessions'][j]['available_capacity_dose2']]
            a_series = pd.Series(to_append, index = df1.columns)
            df1 = df1.append(a_series, ignore_index=True)

            if(json_response['centers'][i]['sessions'][j]['vaccine']=='COVAXIN' and 
               json_response['centers'][i]['sessions'][j]['min_age_limit']<45   and
               (json_response['centers'][i]['sessions'][j]['available_capacity_dose2']>0 or 
                json_response['centers'][i]['sessions'][j]['available_capacity']>0)):
                name=json_response['centers'][i]['name']
                pincode=json_response['centers'][i]['pincode']
                date=json_response['centers'][i]['sessions'][j]['date']
                vaccine=json_response['centers'][i]['sessions'][j]['vaccine']
                age=json_response['centers'][i]['sessions'][j]['min_age_limit']
                total_dose=json_response['centers'][i]['sessions'][j]['available_capacity']
                dose_2=json_response['centers'][i]['sessions'][j]['available_capacity_dose2']
#enter your telegram bot token and chat id to get notified on telegram
                response3 = requests.get("https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text={name} {pincode}\n{date} {vaccine} {age}\ntotal_dose : {total_dose}\ndose_2 : {dose_2}\nhttps://www.cowin.gov.in/home".format(name=name,pincode=pincode,date=date,vaccine=vaccine,age=age,total_dose=total_dose,dose_2=dose_2))

                
                winsound.PlaySound(filename, winsound.SND_FILENAME)
                print('=================================================================================================')
                print(json_response['centers'][i]['name'],json_response['centers'][i]['pincode'])
                print(json_response['centers'][i]['sessions'][j]['date']
                      ,json_response['centers'][i]['sessions'][j]['vaccine']
                      ,json_response['centers'][i]['sessions'][j]['min_age_limit']
                      ,json_response['centers'][i]['sessions'][j]['available_capacity']
                      ,json_response['centers'][i]['sessions'][j]['available_capacity_dose2'])
                print('=================================================================================================')
                winsound.PlaySound(filename, winsound.SND_FILENAME)
                winsound.PlaySound(filename, winsound.SND_FILENAME)
                winsound.PlaySound(filename, winsound.SND_FILENAME)
                winsound.PlaySound(filename, winsound.SND_FILENAME)


    display(df1)
    time.sleep(20)


# In[ ]:





# In[ ]:




