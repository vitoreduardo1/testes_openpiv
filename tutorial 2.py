from openpiv import tools, scaling, pyprocess, validation, filters
import pathlib
import numpy as np
def func( args ):
    """A function to process each image pair."""

    # this line is REQUIRED for multiprocessing to work
    # always use it in your custom function

    file_a, file_b, counter = args


    #####################
    # Here goes you code
    #####################

    # read images into numpy arrays
    frame_a  = tools.imread( path / file_a )
    frame_b  = tools.imread( path.joinpath(file_b) )

    frame_a = (frame_a*1024).astype(np.int32)
    frame_b = (frame_b*1024).astype(np.int32)


    # process image pair with extended search area piv algorithm.
    u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=32, overlap=12, dt=0.02, search_area_size=38, sig2noise_method='peak2peak')
    mask = validation.sig2noise_val( sig2noise, threshold = 1.05 )
    u, v = filters.replace_outliers( u, v, mask, method='localmean', max_iter=3, kernel_size=3)
    # get window centers coordinates
    x, y = pyprocess.get_coordinates( image_size=frame_a.shape, search_area_size=38, overlap=12 )
    x, y, u, v = scaling.uniform(x, y, u, v,
                                   scaling_factor=96.52)  # 96.52 microns/pixel
    # 0,0 shall be bottom left, positive rotation rate is counterclockwise
    x, y, u, v = tools.transform_coordinates(x, y, u, v)
    # save to a file
    tools.save('test2_%03d.txt' % counter, x, y, u, v, mask)
    tools.display_vector_field('test2_%03d.txt' % counter)
path = pathlib.Path(r"C:\Users\win10\Documents\sinmec\PIV sintetico\Particle_Tracking\PIV vitor\imagens_salvas")
task = tools.Multiprocesser( data_dir = path, pattern_a='Imagem*_A.png', pattern_b='Imagem*_A.png' )
task.run( func = func, n_cpus=1 )
