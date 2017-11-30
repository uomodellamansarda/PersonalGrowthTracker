import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


va='Python'
tvoi=' Durata'

csvname="logs.csv"
#read the csv	

dfraw=pd.read_csv(csvname,sep=',',header=0,skipfooter=0, index_col=False)


print(dfraw[tvoi].map(lambda x: len(x)).max())

dfraw[tvoi] = dfraw[tvoi].astype('str')
mask = (dfraw[tvoi].str.len() == 6) 
dfraw = dfraw.loc[mask]

dfraw[tvoi]=dfraw[tvoi].str.strip()

dfraw[tvoi]=pd.to_datetime(dfraw[tvoi], format='%M:%S')


pythondf=dfraw[dfraw['Attività'].str.contains("Python",na=False)]
pythondf['Date'] = pythondf.apply(lambda row: datetime(row['Anno'], row[' Mese'], row[' Giorno']), axis=1)

numacti=pythondf.groupby('Date').count()
numacti=numacti['Attività']
numacti=numacti.divide(2)
cumulata=numacti.cumsum()


day=pd.concat([numacti, cumulata], axis=1)
day.columns=['pgiorno','cumulata']
maxh=cumulata.max()
plt.plot(day.index,day['cumulata'])
plt.xticks(rotation=90)
plt.title('Totale ore di studio e lavoro con Python (%d ore)' %(maxh))
plt.tight_layout()
plt.show()
