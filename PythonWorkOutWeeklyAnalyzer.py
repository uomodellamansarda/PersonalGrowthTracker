import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


va='Python'
tvoi='Length'

csvname="logs.csv"
#read the csv	
columns_name=['Year', 'Month', 'Day', 'Time', 'Length', 'Start', 'End', 'Activity']
dfraw=pd.read_csv(csvname,names=columns_name,sep=',',skiprows=1,skipfooter=0, index_col=False)


dfraw[tvoi] = dfraw[tvoi].astype('str')
mask = (dfraw[tvoi].str.len() == 6) 
dfraw = dfraw.loc[mask]

dfraw[tvoi]=dfraw[tvoi].str.strip()

dfraw[tvoi]=pd.to_datetime(dfraw[tvoi], format='%M:%S')
dfraw['Date'] = dfraw.apply(lambda row: datetime(row['Year'], row['Month'], row['Day']), axis=1)

#Python activity filter 
pythondf=dfraw[(dfraw['Activity'].str.contains("Python",na=False)) | (dfraw['Activity'].str.contains("python",na=False))] 
numacti=pythondf.groupby('Date').count()
numacti=numacti['Activity']
numacti=numacti.divide(2)
cumulata=numacti.cumsum()


day=pd.concat([numacti, cumulata], axis=1)
day.columns=['pgiorno','cumulata']
maxh=cumulata.max()
plt.plot(day.index,day['cumulata'])
plt.xticks(rotation=90)
plt.title('Total Hours Studying and Working With Python (%d H)' %(maxh))
plt.tight_layout()
plt.show()

#Questa parte è per l'analisi della settimana 
python_work=10
python_study=6
sutdy='study'
marketing='marketing'

python_marketing=4
total=python_work+python_study+python_marketing

#Selezioniamo solo gli ultimi giorni oggetto di analisi 
days=7
cutoff_date= dfraw['Date'].iloc[-1]- pd.Timedelta(days=days)
print("Last day recorded", pythondf['Date'].iloc[-1])
print("Last day dfraw recorded",dfraw['Date'].iloc[-1])
print("Cut-off Date", cutoff_date)
last_7days= pythondf[pythondf['Date'] > cutoff_date] 
#Qualsiasi attivita' che non abbia come label "marketing" o "study" "datacamp" "ripasso" "libro" é considerata "work"
#Per del codice migliore cercherò nei prossimi log di avere solo tre label study work marketing come metag
work_mask=(last_7days['Activity'].str.contains("ripasso",na=False) | last_7days['Activity'].str.contains("datacamp",na=False)) | (last_7days['Activity'].str.contains("Libro",na=False)) | (last_7days['Activity'].str.contains("marketing",na=False))
study_mask=(last_7days['Activity'].str.contains("ripasso",na=False) | last_7days['Activity'].str.contains("datacamp",na=False)| last_7days['Activity'].str.contains("Libro",na=False))
pythondf_study=last_7days[study_mask]

pythondf_marketing=last_7days[last_7days['Activity'].str.contains("marketing",na=False)]


pythondf_work=last_7days[~work_mask]

#Ricordando che i pomodori sono slot da 30 min 
#dobbiamo contare per categoria il numero di pomodori e dividere per 2
#Qui sotto si poteva realizzare un ciclo for, scusate la pigrizia, suggerimenti ben accetti 

print('Total hours in the last 7 days',last_7days.count()/2)
print("Weekly % of Python Working",round(pythondf_work['Activity'].count()/2/python_work*100,2))
print("Weekly % of Python Study", round(pythondf_study['Activity'].count()/2/python_study*100,2))
print("Weekly % of Python Marketng",round(pythondf_marketing['Activity'].count()/2/python_marketing*100,2))


