def total_error ():
    import numpy as np
    from fluid_og import fluid_speedx, fluid_speedy
    import pandas as pd
    from scipy.interpolate import LinearNDInterpolator
    from scipy.interpolate import griddata
    from fluid_og import XK,YK
    import math
    df = pd.read_csv('exp1_001.txt', delimiter='\t',skipfooter=0,skiprows=0,header=0, engine='python')



    X = df['# x'].to_numpy()
    Y = df['y'].to_numpy()
    Y_min = Y.min()
    X_min = X.min()
    X = X - X_min
    Y = Y - Y_min
    U = df['u'].to_numpy()
    V = df['v'].to_numpy()

    points = (X,Y)

    interpolatoru = LinearNDInterpolator(points, U)
    interpolatorv = LinearNDInterpolator(points, V)

    def fluid_speedxn(x, y):
        u_f = interpolatoru([x, y])
        if math.isnan(u_f):
            u_f = griddata(points, U, (x, y), method='linear')
        return u_f

    def fluid_speedyn(x, y):
        u_f = interpolatorv([x, y])
        if math.isnan(u_f):
            u_f = griddata(points, V, (x, y), method='linear')
        return u_f

    def error(x,y):
        error = np.sqrt(abs((np.power(x,2))-(np.power(y,2))))
        return error
    n=1000
    x = np.linspace(0.1,XK.max()-0.9,n)
    y = np.linspace(0.1,YK.max()-0.9,n)

 #   x = np.linspace(XK.max()/2, XK.max() - 0.9, n)
 #   y = np.linspace(YK.max()/2, YK.max() - 0.9, n)


 #   x = np.linspace(0.1, XK.max()/2, n)
 #   y = np.linspace(0.1, YK.max()/2, n)



    errou = 0
    errov = 0
    for i in range(n):
        ufxn = fluid_speedxn(x[i], y[i])
        ufyn = fluid_speedyn(x[i], y[i])
        ufx = fluid_speedx(x[i], y[i])
        ufy = fluid_speedy(x[i], y[i])
        errou = error(ufxn,ufx) + errou
        errov = error(ufy,ufyn) + errov
 #       print(i)
    errou = (errou/n)*100
    errov = (errov/n)*100


    print("errou = ", errou,"%")
    print("errov = ",errov,"%")
