import pandas as pd
import numpy as np
import math as math
import matplotlib.pyplot as plt
import datetime as dt
import geopy as gp
from scipy.optimize import curve_fit

def dateTranslator(dateStr):
    return dt.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

def ArrayDates(dateStr):
    datesMap = map(dateTranslator, datesStr)
    return list(datesMap)

def dateDelta(datesStr):
    dates = ArrayDates(datesStr)
    return max(dates).year - min(dates).year

def lineFunc(x, k, b):
    return  - k*x + b;

def lyambda(m, popt):
    return 10**lineFunc(m, popt[0], popt[1])

def probability(s, m, t, popt):
    return (lyambda(m, popt)*t)**s * math.exp(-lyambda(m, popt)*t) / math.factorial(s)
    
file = "reports_list_12-25-20012021.xlsx"
xl = pd.ExcelFile(file)
df = xl.parse('Reports list')
magArray = df.mag.values
maxMag = max(magArray)
minMag = min(magArray)
steps = int((maxMag - minMag) * 10 + 1)

linspace = np.linspace(minMag, maxMag, steps)
hist = np.histogram(magArray, steps)[0]

datesStr = df.event_datetime.values
  
hist = hist[::-1]
linspace = linspace[::-1]

cumsum = np.cumsum(hist)/dateDelta(datesStr)
lg_cumsum = np.log10(cumsum)

popt, pcov = curve_fit(lineFunc, linspace, lg_cumsum)
lineY = [lineFunc(x, popt[0], popt[1]) for x in linspace]

plt.plot(linspace, lg_cumsum, "o")
plt.plot(linspace, lineY)

plt.show()
P = probability(1, 8, 400, popt)
print("probability = " + str(P))
#Посчитать кол-во сценариев при опр магинтуде опр кол-во раз при опр расстоянии 
#geopy - distance, point

magnitudes = df.mag.values
dates = ArrayDates(datesStr)
latitude = df.mag.latitude
longitude = df.mag.longitude
points = [gp.Point(x,y) for (x,y) in (latitude, longitude)]
