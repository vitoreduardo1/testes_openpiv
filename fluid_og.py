import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import RegularGridInterpolator
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import Rbf
from scipy.ndimage import zoom

df = pd.read_csv(r"C:\Users\win10\Documents\sinmec\PIV sintetico\Particle_Tracking\PIV vitor\vonkarman.csv", delimiter=',', skipinitialspace=True)
#print(df.columns)
#print(df.head())

X = df['x-coordinate'].to_numpy()
Y = df['y-coordinate'].to_numpy()
U = df['x-velocity'].to_numpy()
V = df['y-velocity'].to_numpy()



mascarax = X >= 0
mascaray = (Y >= -2) & (Y <= 2)
mascaraf = mascarax & mascaray

#X = X[mascaraf]
#Y = Y[mascaraf]
#U = U[mascaraf]
#V = V[mascaraf]

#factor = 60

#X = X*factor
#Y = Y*factor
#U = U*factor
#V = V*factor

y_min = Y.min()
x_min = X.min()

X = X + abs(x_min)
Y = Y + abs(y_min)

y_min = Y.min()
x_min = X.min()


points = (X,Y)

interpolatoru = LinearNDInterpolator(points, U)
#interpolatorU = NearestNDInterpolator(points, U)
interpolatorv = LinearNDInterpolator(points, V)
#interpolatorV = NearestNDInterpolator(points, V)
#print(interpolatoru([0,0]))
#print(interpolatorv([0,0]))

# calcular a velocidade usando o interpolador
def fluid_speedx(x, y, h, u_0, L):
    if y > y_min  and x >= x_min :
     u_f = interpolatoru([x, y])
    if y <= y_min  or x < x_min  :
        u_f = u_0
    return u_f

def fluid_speedy(x, y, h, u_0, L):
    if y > y_min  and x >= x_min :
     u_f = interpolatorv([x, y])
    if y <= y_min or x < x_min :
        u_f = u_0
    return u_f