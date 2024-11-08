def test_og ():
    import pandas as pd
    import numpy as np
    from scipy.interpolate import griddata


    df = pd.read_csv('vonkarman.csv', delimiter=',', skipinitialspace=True)
    #df = pd.read_csv('exp1_001.txt', delimiter='\t',skipfooter=0,skiprows=0,header=0, engine='python')

    print(df.head())

    X = df['x-coordinate'].to_numpy()
    Y = df['y-coordinate'].to_numpy()
    P = df['total-pressure'].to_numpy()
    U = df['x-velocity'].to_numpy()
    V = df['y-velocity'].to_numpy()

    #X = df['# x'].to_numpy()
    #Y = df['y'].to_numpy()
    #U = df['u'].to_numpy()
    #V = df['v'].to_numpy()

    mascarax = X >= 0
    mascaray = (Y >= -2) & (Y <= 2)
    mascaraf = mascarax & mascaray

    X = X[mascaraf]
    Y = Y[mascaraf]
    U = U[mascaraf]
    V = V[mascaraf]

    #X = X*60
    #Y = Y*60

    y_min1 = Y.min()
    x_min1 = X.min()
    X = X + abs(x_min1)
    Y = Y + abs(y_min1)
    print(Y.max())
    print(X.max())
    AR = (Y.max() - Y.min()) / (X.max() - X.min())

    N_x = 2000
    x_interp = np.linspace(X.min(), X.max(), num=N_x)
    y_interp = np.linspace(Y.min(), Y.max(), num=int(N_x * AR))



    xi, yi = np.meshgrid(x_interp, y_interp, indexing='xy')

    R = np.sqrt(xi**2.0 + yi**2.0)

    points = (X,Y)
    #P_interp_values = griddata(points, P, (xi, yi), method='linear')
    #P_interp_values[R <= 0.5] = np.nan

    U_interp_values = griddata(points, U, (xi, yi), method='linear')
#    U_interp_values[R <= 0.5] = np.nan

    V_interp_values = griddata(points, V, (xi, yi), method='linear')
#    V_interp_values[R <= 0.5] = np.nan

    #np.savetxt("von_karman_cylinder.csv", xi,yi,U_interp_values,V_interp_values,P_interp_values], delimiter=","#)

    #np.savez_compressed("von_karman_cylinder.npz", X=xi, Y=yi, U=U_interp_values, V=V_interp_values, P=P_interp_values)

    import matplotlib.pyplot as plt

    #ax = plt.gca()
    #ax.axis('equal')
    #plt.pcolormesh(xi, yi, P_interp_values)
    #plt.savefig('P_values.png')
    #plt.show()

    ax = plt.gca()
    ax.axis('equal')
    mesh = plt.pcolormesh(xi, yi, U_interp_values, shading='auto')
    plt.colorbar(mesh,label='valores')
    plt.savefig('U_values.png')
    plt.show()

    ax = plt.gca()
    ax.axis('equal')
    mesh = plt.pcolormesh(xi, yi, V_interp_values, shading='auto')
    plt.colorbar(mesh,label='valores')
    plt.savefig('V_values.png')
    plt.show()