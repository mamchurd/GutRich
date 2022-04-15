import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cwd = os.getcwd();
file = "reports_list_12-25-20012021.xlsx"
xl = pd.ExcelFile(file)
df = xl.parse('Reports list')
magArray = df.mag.values
вф
maxMag = max(magArray)
minMag = min(magArray)
steps = int((maxMag - minMag) * 10 + 1)
linspace = np.linspace(minMag, maxMag, steps)
hist = np.histogram(magArray, steps)[0]
linspace = linspace[::-1]
hist = hist[::-1]
cumsum = np.cumsum(hist)
