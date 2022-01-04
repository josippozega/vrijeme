#Moduli
import streamlit as st
import requests
from datetime import datetime , timedelta
import pandas as pd
import matplotlib.pyplot as plt
import time



#API ključ - pohranjen u -STREAMLIT mapi
api_key = st.secrets["api_key"]


#API poziv sa OPEN WEATHER MAP web-aplikacije
url = 'api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}'

#funkcija za dohvaćanje vremena
def getweather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        #st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

#funkcija za dohvaćanje povijesnih podataka o vremenu
def get_hist_data(lat,lon,start):
 res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data , temp

#pišemo aplikaciju
st.header('Vremenska prognoza')
st.markdown('Aplikacija by prof. Josip Požega, mag.inf.')

im1,im2 = st.beta_columns(2)
with im2:
    image0 = 'vrijeme.jpg'
    st.image(image0,use_column_width=True,caption = 'Negdje u Hrvatskoj: ')
with im1:
    image1 = 'vrijeme2.jpg'
    st.image(image1, caption='Koristit ćemo Open Weather Map API kao naš izvor podataka. ',use_column_width=True)

col1, col2 = st.beta_columns(2)

with col1:
    city_name = st.text_input("Unesite grad za koji želite vidjeti prognozu vremena: ")
    #show_hist = st.checkbox('Show me history')
with col2:
		if city_name:
		        res , json = getweather(city_name)
		        #st.write(res)
		        st.success('Trenutna temperatura: ' + str(round(res[1],2)))
		        st.info('Osjećaj: ' + str(round(res[2],2)))
		        #st.info('Humidity: ' + str(round(res[3],2)))
		        st.subheader('Status: ' + res[7])
		        web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[6])+"@2x.png)"
		        st.markdown(web_str)

if city_name:
    show_hist = st.beta_expander(label = 'Vremenska prognoza zadnjih 5 dana')
    with show_hist:
            start_date_string = st.date_input('Datum: ')
            #start_date_string = str('2021-06-26')
            date_df = []
            max_temp_df = []
            for i in range(5):
                        date_Str = start_date_string - timedelta(i)
                        start_date = datetime.strptime(str(date_Str),"%Y-%m-%d")
                        timestamp_1 = datetime.timestamp(start_date)
                        #res , json = getweather(city_name)
                        his , temp = get_hist_data(res[5],res[4],int(timestamp_1))
                        date_df.append(date_Str)
                        max_temp_df.append(max(temp) - 273.5)

            df = pd.DataFrame()
            df['Datum'] = date_df
            df['Max temp'] = max_temp_df
            st.table(df)

	st.map(pd.DataFrame({'lat' : [res[5]] , 'lon' : [res[4]]},columns = ['lat','lon']))
