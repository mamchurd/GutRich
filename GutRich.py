import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from dateutil import relativedelta
from scipy.optimize import curve_fit

def dateTranslator(dateStr):
    return dt.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

def dateDelta(datesStr):
    datesMap = map(dateTranslator, datesStr)
    dates = list(datesMap)
    return max(dates).year - min(dates).year

def lineFunc(x, k, b):
    return  - k*x + b;

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

popt, pcov = curve_fit(lineFunc, hist, lg_cumsum)
lineY = [lineFunc(x, popt[0], popt[1]) for x in linspace]

plt.plot(linspace, lg_cumsum, "o")
plt.plot(linspace, lineY)

plt.show()
print(hist)
print(lg_cumsum)
