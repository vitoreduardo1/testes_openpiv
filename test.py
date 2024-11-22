def test ():
    import pandas as pd
    import numpy as np
    from scipy.interpolate import griddata
    from matplotlib.ticker import MultipleLocator


    df = pd.read_csv(r"C:\Users\win10\Documents\sinmec\openpiv\exp1_001.txt", delimiter='\t',skipfooter=0,skiprows=0,header=0, engine='python')

 #   print(df.head())
    X = df['# x'].to_numpy()
    Y = df['y'].to_numpy()
    Y_min = Y.min()
    X_min = X.min()
    X = X - X_min
    Y = Y - Y_min
    U = df['u'].to_numpy()
    V = df['v'].to_numpy()

 #   print(Y.max())
 #   print(X.max())

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
    print(griddata(points, U, (4, 2), method='linear'))
    V_interp_values = griddata(points, V, (xi, yi), method='linear')
 #   V_interp_values[R <= 0.5] = np.nan

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
    plt.title("open")
    mesh = plt.pcolormesh(xi, yi, U_interp_values, shading='auto')
    plt.colorbar(mesh,label='valores')
    plt.savefig('U_values_open.png')
    # Configurando os ticks dos eixos
    ax = plt.gca()  # Obtém o objeto Axes atual
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Ticks principais a cada 1 unidade
    ax.xaxis.set_minor_locator(MultipleLocator(0.2))  # Ticks secundários a cada 0.2 unidades
    ax.yaxis.set_major_locator(MultipleLocator(0.5))  # Ticks principais a cada 0.5 unidades
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))  # Ticks secundários a cada 0.1 unidades

    # Adicionando a grade para ticks principais e secundários
    plt.grid(which='major', color='gray', linestyle='-', linewidth=0.8)  # Grade principal
    plt.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)  # Grade secundária
    plt.show()

    ax = plt.gca()
    ax.axis('equal')
    plt.title("open")
    mesh = plt.pcolormesh(xi, yi, V_interp_values, shading='auto')
    plt.colorbar(mesh,label='valores')
    plt.savefig('V_values_open.png')
    plt.grid(True)
    plt.show()

test()