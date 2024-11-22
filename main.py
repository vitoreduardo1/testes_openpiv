def main ():
    from openpiv import tools, pyprocess, validation, filters, scaling
    import numpy as np
    import matplotlib.pyplot as plt
#    import imageio
    import pandas as pd
    import cv2
    image_a = cv2.imread(r"C:\Users\win10\Documents\sinmec\openpiv\imagens_salvas\Imagem0_A.png")
    frame_a  = tools.imread( r"C:\Users\win10\Documents\sinmec\openpiv\imagens_salvas\Imagem0_A.png" )
    frame_b  = tools.imread( r"C:\Users\win10\Documents\sinmec\openpiv\imagens_salvas\Imagem0_B.png" )
    tf = pd.read_csv('vonkarman.csv', delimiter=',', skipinitialspace=True)
    X_og = tf['x-coordinate'].to_numpy()
    Y_og = tf['y-coordinate'].to_numpy()
    mascarax = X_og >= 0
    mascaray = (Y_og >= -2) & (Y_og <= 2)
    mascaraf = mascarax & mascaray
    X_og = X_og[mascaraf]
    Y_og = Y_og[mascaraf]
    y_min1 = Y_og.min()
    x_min1 = X_og.min()
    X_og = X_og + abs(x_min1)
    Y_og = Y_og + abs(y_min1)
    x_max_og = X_og.max()
    y_max_og = Y_og.max()
    h,l,er = image_a.shape
    #print(x_max_og)
    #print(l)
    #print(h)
    scaling_factor = l/x_max_og
 #   scaling_factor = 59.5
    seta = h/y_max_og
    feta = (seta+scaling_factor)/2
#   print(seta)
#    print(scaling_factor)
    fig,ax = plt.subplots(1,2,figsize=(12,10))
    ax[0].imshow(frame_a,cmap=plt.cm.gray)
    ax[1].imshow(frame_b,cmap=plt.cm.gray)

    winsize = 32 # pixels, interrogation window size in frame A
    searchsize = 38  # pixels, search in image B
    overlap = 17 # pixels, 50% overlap
    dt = 0.1 # sec, time interval between pulses


    u0, v0, sig2noise = pyprocess.extended_search_area_piv(frame_a.astype(np.int32),
                                                           frame_b.astype(np.int32),
                                                           window_size=winsize,
                                                           overlap=overlap,
                                                           dt=dt,
                                                           search_area_size=searchsize,
                                                           sig2noise_method='peak2peak')

    x, y = pyprocess.get_coordinates( image_size=frame_a.shape,
                                     search_area_size=searchsize,
                                     overlap=overlap )

    flags = validation.sig2noise_val( sig2noise,
                                     threshold = 1.05 )
    # if you need more detailed look, first create a histogram of sig2noise
    # plt.hist(sig2noise.flatten())
    # to see where is a reasonable limit

    # filter out outliers that are very different from the
    # neighbours

    u2, v2 = filters.replace_outliers( u0, v0,
                                       flags,
                                       method='localmean',
                                       max_iter=3,
                                       kernel_size=3)

    # convert x,y to mm
    # convert u,v to mm/sec

    x, y, u3, v3 = scaling.uniform(x, y, u2, v2,
                                   scaling_factor = feta ) # 96.52 microns/pixel diminui o vaalor aumenta o tamanho

    # 0,0 shall be bottom left, positive rotation rate is counterclockwise
    x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)

    #save in the simple ASCII table format
    tools.save('exp1_001.txt', x, y, u3, v3, flags)

    fig, ax = plt.subplots(figsize=(8,8))
    tools.display_vector_field('exp1_001.txt',
                               ax=ax, scaling_factor=feta,
                               scale=50, # scale defines here the arrow length
                               width=0.003, # width is the thickness of the arrow
                               on_img=True, # overlay on the image
                               image_name=r"C:\Users\win10\Documents\sinmec\openpiv\imagens_salvas\Imagem0_A.png");
    plt.close('all')
#main()