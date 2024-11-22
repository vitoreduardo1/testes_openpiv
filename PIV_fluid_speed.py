def image_generator():
    import numpy as np
    import matplotlib.pyplot as plt

    from fluid_cut import fluid_speedx
    from fluid_cut import fluid_speedy
    import pandas as pd
    import math
    import os
    import sys
    import cv2


    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'synpivimage')))


    import synpivimage


    # Nome da pasta onde as imagens serão salvas
    folder_name = 'imagens_salvas'

    # Cria a pasta se ela não existir
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    df = pd.read_csv('vonkarman.csv', delimiter=',', skipinitialspace=True)

    X = df['x-coordinate'].to_numpy()
    Y = df['y-coordinate'].to_numpy()

    mascarax = X >= 0
    mascaray = (Y >= -2) & (Y <= 2)
    mascaraf = mascarax & mascaray


    X = X[mascaraf]
    Y = Y[mascaraf]

    X = X*100
    Y = Y*100



    # calcula a pocição da particula


    def particle_positionx(x_0, delta_t, u_p, y_0, h, L):
        if y_0 > y_min  and x_0 >= x_min :
         x = float(x_0 + delta_t*u_p)
        if y_0 <= y_min  or x_0 < x_min :
            x = x_0
        return x

    # pocição da particula em y


    def particle_positiony(y_0, delta_t, u_p, h, L, x_0):
        if y_0 > y_min  and x_0 >= x_min :
            y = float(y_0 + delta_t*u_p)
        if y_0 <= y_min or x_0 < x_min :
            y = y_0
        return y

    # calcular valor de módulo


    def modulo(x,y):
        t = float(x**2)
        r = float(y**2)
        p = np.sqrt(t+r)
        return p

    # propriedades do fluido e particula


    mi_l = 1e-3    # viscosidade cinematica
    ro_l = 997     # densidade do liquido
    d_p = 7        # diametro da particula

    # dimenções das placas obs:qualquer mudança aqui tambem deve ser feita no fluido_rotacional.py

    y_min1 = Y.min()
    x_min1 = X.min()
    X = X + abs(x_min1)
    Y = Y + abs(y_min1)
    y_min = Y.min()
    x_min = X.min()
    h = Y.max()         # altura
    L = X.max()        # comprimento
    centro = int(h/2)
    # condições iniciais


    n = 12000         # numero de particulas
    inte = 1         #numero de processos
    delta_t = 0.1    # intervalo de tempo


    for i in range(inte):
        xA = np.random.uniform(x_min, L, n)  # pocisão x inicial das particulas
        yA = np.random.uniform(y_min, h, n)  # pocisão y inicial das particulas
        mascaram = np.power(xA,2) + np.power(yA-(0.5*h),2) > 2500
        xA = xA[mascaram]
        yA = yA[mascaram]
        n = np.sum(mascaram)
        u_p = np.zeros((n, 2), dtype=float)   # iniciando o vetor velocidade das particulas com 0
        u_l = np.zeros((n, 2), dtype=float)   # iniciando o vetor velocidade do fluido com 0
        xB = np.full(n, np.nan)
        yB = np.full(n, np.nan)



        # camera
        cam = synpivimage.Camera(
            nx=math.ceil(L),
            ny=math.ceil(h),
            bit_depth=16,
            qe=1,
            sensitivity=1,
            baseline_noise=50,
            dark_noise=10,
            shot_noise=False,
            fill_ratio_x=1.0,
            fill_ratio_y=1.0,
            particle_image_diameter=d_p,
            seed=10
        )

        # laser
        laser = synpivimage.Laser(
            width=0.25,
            shape_factor=2
        )


        # calcula todos os valores e coloca os pontos no plot




        particlesA = synpivimage.Particles(
                x=xA,
                y=yA,
                z=np.zeros(n),
                size=np.ones(n) * 1
            )
        imgA, partA = synpivimage.take_image(laser,
                                                cam,
                                                particlesA,
                                                particle_peak_count=1000)


        for k in range(n):
            vx = float(u_l[k, 0])
            vy = float(u_l[k, 1])
            u_l[k, 0] = fluid_speedx(xA[k], yA[k], h, vx, L)
            u_l[k,1] = fluid_speedy(xA[k], yA[k], h, vy, L)
            u_p[k, 0] = u_l[k, 0]
            xB[k] = particle_positionx(xA[k], delta_t, u_p[k][0], yA[k], h, L)
            u_p[k, 1] = u_l[k, 1]
            yB[k] = particle_positiony(yA[k], delta_t, u_p[k][1], h, L, xA[k])
       # print("XA = ",xA)
       # print("YA = ",yA)
       # print("XB = ",xB)
       # print("YB = ",yB)
       # print("delta x = ",xB - xA)
       # print("delta y = ",yB - yA)
        particlesB = synpivimage.Particles(
                x=xB,
                y=yB,
                z=np.zeros(n),
                size=np.ones(n) * 1
            )
        imgB, partB = synpivimage.take_image(laser,
                                                 cam,
                                                 particlesB,
                                                 particle_peak_count=1000)
        imgA_normalized = (imgA / 256).astype(np.uint8)
        imgB_normalized = (imgB / 256).astype(np.uint8)


        alturaA, larguraA = imgA_normalized.shape[:2]
        alturaB, larguraB = imgB_normalized.shape[:2]

        scale_percent = 100                 # aumentar a imagem
        widthA = int(imgA_normalized.shape[1] * scale_percent / 100)
        heightA = int(imgA_normalized.shape[0] * scale_percent / 100)
        dimA = (widthA, heightA)

        widthB = int(imgB_normalized.shape[1] * scale_percent / 100)
        heightB = int(imgB_normalized.shape[0] * scale_percent / 100)
        dimB = (widthB, heightB)

        # Redimensionar as imagens
        resizedA = cv2.resize(imgA_normalized, dimA, interpolation=cv2.INTER_AREA)
        resizedB = cv2.resize(imgB_normalized, dimB, interpolation=cv2.INTER_AREA)

        resizedA = cv2.equalizeHist(resizedA)
        resizedB = cv2.equalizeHist(resizedB)



        # Mostrar as imagens
        filenameA = os.path.join(folder_name, f"Imagem{i}_A.png")
        filenameB = os.path.join(folder_name, f"Imagem{i}_B.png")
    #    cv2.circle(resizedA, (0,centro), 50, (255,255,255), -1)
    #    cv2.circle(resizedB, (0,centro), 50, (255,255,255), -1)
    #    cv2.imshow(filenameA, resizedA)
    #    cv2.imshow(filenameB, resizedB)
        cv2.imwrite(filenameA, resizedA)
        cv2.imwrite(filenameB, resizedB)
    #    cv2.waitKey(0)
    #    cv2.destroyAllWindows()



