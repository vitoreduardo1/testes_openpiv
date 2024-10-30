import numpy as np
from fluid_og import fluid_speedx, fluid_speedy
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

df = pd.read_csv('exp1_001.txt', delimiter='\t',skipfooter=0,skiprows=0,header=0, engine='python')

print(df.columns)
X = df['# x'].to_numpy()
Y = df['y'].to_numpy()
U = df['u'].to_numpy()
V = df['v'].to_numpy()

points = (X,Y)

interpolatoru = LinearNDInterpolator(points, U)
interpolatorv = LinearNDInterpolator(points, V)

def fluid_speedxn(x, y, h, u_0, L):
    if y > 0  and x >= 0 :
     u_f = interpolatoru([x, y])
    if y <= 0  or x < 0  :
        u_f = u_0
    return u_f

def fluid_speedyn(x, y, h, u_0, L):
    if y > 0  and x >= 0 :
     u_f = interpolatorv([x, y])
    if y <= 0 or x < 0 :
        u_f = u_0
    return u_f

def error(x,y,n):
    error = np.sqrt((np.power(x,2))-(np.power(y,2)))
    return error
