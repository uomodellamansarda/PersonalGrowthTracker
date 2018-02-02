#Script for weekly KPI Analysis
#name the activity with the correct name of your workout activity
#example activity_1= "study_math" 
#activity_2="reading"
#acitivity_3="call_a_friend"
#tu vuoi che lo script il mercoledì ti indichi dove rispetto agli obiettivi che ti sei dato identifichi dove dedicare più ore e ridefinire le priorità rispetto ad un disegno di lungo termine evitando che tu ti possa focalizzare troppo in una direzione piuttosto che in un'altra
# Legge le attività
# Vede quanto durano (conta i pomodori di ogni attività)
# Legge le proporzioni
#Calcola la proporzione 
# il codice andrà ulteriormente migliorato attraverso un caricamento più pulito dell'hader del csv
# anche se brutto il codice potresti creare una nuova colonna di forma temporale 
# che tenga considerazione di quello che è stato fatto 
# crea un dictonary or tupla dove iterare
activity_1="CV" 
activity_2="Python"
activity_3="englishstudy"
time_variable=' Durata'	
#define the proportion between each main acitivity 
act_1=0.40
act_2=0.20
act_3=0.10

#Import all the necessary library
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


#Insert the name of the csv where your pomodoro slots are logged
csvname="logs.csv"

tot_activity=[activity_1, activity_2, activity_3]
#read the csv	

dataframe_raw=pd.read_csv(csvname,sep=',',header=0,skipfooter=0, index_col=False)
print(dataframe_raw.head())

#remove anomalies clearing the time column with more than 25'for slot
print(dataframe_raw[time_variable].map(lambda x: len(x)).max())
dataframe_raw.tail()
dataframe_raw[time_variable] = dataframe_raw[time_variable].astype('str')
mask = (dataframe_raw[time_variable].str.len() == 6) 
dataframe_raw = dataframe_raw.loc[mask]

dataframe_raw[time_variable]=dataframe_raw[time_variable].str.strip()

dataframe_raw[time_variable]=pd.to_datetime(dataframe_raw[time_variable], format='%M:%S')
dataframe_raw.sort_values(by=' Tempo',ascending=False)

dataframe_raw.info()
dataframe_raw.tail()
dataframe_raw["Date"]= dataframe_raw.apply(lambda x: datetime.strptime("{0} {1} {2}".format(x["Anno"],x[" Mese"], x[" Giorno"]), "%Y %m %d"), axis=1)

print(dataframe_raw.tail())
#identifing the "last week column" 

#based on how the clockwork work is better to merge year-month-day columns


#The dataframe column with containing the day will be the "Date" 
#Later you need to modify "Date" and delete this comment
print(dataframe_raw["Date"].tail(5))
time= np.sort(dataframe_raw["Date"].unique())
print(time[-1])


print(dataframe_raw.dtypes)
#defing the last 7 days to analyze
w1=time[-8:]
print(w1)
#last seven days data 
lw= dataframe_raw[dataframe_raw["Date"].isin(w1)]
#Now we have only the data about the 7 days 
#We can start identyfing if we are working well

print(lw.tail(5))

#Now we have only the data about the 7 days 
#We can start identyfing if we are working well

#extract all the row contains all the dictonary tot_activity
print(tot_activity)
activity_1df= lw['Attività'].str.contains("CV",na=False)
activity_2df= lw['Attività'].str.contains("Python",na=False)
activity_3df= lw['Attività'].str.contains("englishstudy",na=False)

sum=activity_1df|activity_2df|activity_3df



lw_filter=lw[sum]
print(lw_filter.head())

total_activity= lw_filter['Attività'].count()
lw_filter['totale']=total_activity

print(lw_filter.head())
#in questo modo sei riuscito a capire come il tempo è allocato ma la strada
# è ancora lunga perchè serve capire come aggregare tutte le attività legate a 
#python e alla lettura 
prova= lw_filter.groupby('Attività').count().apply(lambda x : 100*x/float(total_activity))
print(prova) 

