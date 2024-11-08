def main_deformation():
    from openpiv import windef  # <---- see windef.py for details
    from openpiv import tools, scaling, validation, filters, preprocess
    import openpiv.pyprocess as process
    from openpiv import pyprocess
    import numpy as np
    import pathlib
    import importlib_resources
    from time import time
    import warnings
    import matplotlib.pyplot as plt

    settings = windef.PIVSettings()

    path = importlib_resources.files('openpiv')

    'Data related settings'
    # Folder with the images to process
    settings.filepath_images = path / r"C:\Users\win10\Documents\sinmec\openpiv" / 'imagens_salvas'  # type: ignore
    # Folder for the outputs
    settings.save_path = path / r"C:\Users\win10\Documents\sinmec\openpiv" / 'output'  # type: ignore
    # Root name of the output Folder for Result Files
    settings.save_folder_suffix = 'output'
    # Format and Image Sequence (see below for more options)
    settings.frame_pattern_a = 'Imagem0_A.PNG'
    settings.frame_pattern_b = 'Imagem0_B.PNG'

    # or if you have a sequence:
    # settings.frame_pattern_a = '000*.tif'
    # settings.frame_pattern_b = '(1+2),(2+3)'
    # settings.frame_pattern_b = '(1+3),(2+4)'
    # settings.frame_pattern_b = '(1+2),(3+4)'

    'Region of interest'
    # (50,300,50,300) #Region of interest: (xmin,xmax,ymin,ymax) or 'full' for full image
    settings.roi = 'full'

    'Image preprocessing'
    # 'None' for no masking, 'edges' for edges masking, 'intensity' for intensity masking
    # WARNING: This part is under development so better not to use MASKS
    settings.dynamic_masking_method = 'None'
    settings.dynamic_masking_threshold = 0.005
    settings.dynamic_masking_filter_size = 7

    settings.deformation_method = 'symmetric'

    'Processing Parameters'
    settings.correlation_method='circular'  # 'circular' or 'linear'
    settings.normalized_correlation=False

    settings.num_iterations = 2  # select the number of PIV passes
    # add the interroagtion window size for each pass.
    # For the moment, it should be a power of 2
    settings.windowsizes = (32, 16, 8) # if longer than n iteration the rest is ignored
    # The overlap of the interroagtion window for each pass.
    settings.overlap = (16, 8, 4) # This is 50% overlap
    # Has to be a value with base two. In general window size/2 is a good choice.
    # methode used for subpixel interpolation: 'gaussian','centroid','parabolic'
    settings.subpixel_method = 'gaussian'
    # order of the image interpolation for the window deformation
    settings.interpolation_order = 3
    settings.scaling_factor = 64  # scaling factor pixel/meter
    settings.dt = 0.1  # time between to frames (in seconds)
    'Signal to noise ratio options (only for the last pass)'
    # It is possible to decide if the S/N should be computed (for the last pass) or not
    # settings.extract_sig2noise = True  # 'True' or 'False' (only for the last pass)
    # method used to calculate the signal to noise ratio 'peak2peak' or 'peak2mean'
    settings.sig2noise_method = 'peak2peak'
    # select the width of the masked to masked out pixels next to the main peak
    settings.sig2noise_mask = 2
    # If extract_sig2noise==False the values in the signal to noise ratio
    # output column are set to NaN
    'vector validation options'
    # choose if you want to do validation of the first pass: True or False
    settings.validation_first_pass = True
    # only effecting the first pass of the interrogation the following passes
    # in the multipass will be validated
    'Validation Parameters'
    # The validation is done at each iteration based on three filters.
    # The first filter is based on the min/max ranges. Observe that these values are defined in
    # terms of minimum and maximum displacement in pixel/frames.
    settings.min_max_u_disp = (-30, 30)
    settings.min_max_v_disp = (-30, 30)
    # The second filter is based on the global STD threshold
    settings.std_threshold = 7  # threshold of the std validation
    # The third filter is the median test (not normalized at the moment)
    settings.median_threshold = 3  # threshold of the median validation
    # On the last iteration, an additional validation can be done based on the S/N.
    settings.median_size=1 #defines the size of the local median
    'Validation based on the signal to noise ratio'
    # Note: only available when extract_sig2noise==True and only for the last
    # pass of the interrogation
    # Enable the signal to noise ratio validation. Options: True or False
    # settings.do_sig2noise_validation = False # This is time consuming
    # minmum signal to noise ratio that is need for a valid vector
    settings.sig2noise_threshold = 1.2
    'Outlier replacement or Smoothing options'
    # Replacment options for vectors which are masked as invalid by the validation
    settings.replace_vectors = True # Enable the replacment. Chosse: True or False
    settings.smoothn=True #Enables smoothing of the displacemenet field
    settings.smoothn_p=0.5 # This is a smoothing parameter
    # select a method to replace the outliers: 'localmean', 'disk', 'distance'
    settings.filter_method = 'localmean'
    # maximum iterations performed to replace the outliers
    settings.max_filter_iteration = 4
    settings.filter_kernel_size = 2  # kernel size for the localmean method
    'Output options'
    # Select if you want to save the plotted vectorfield: True or False
    settings.save_plot = False
    # Choose wether you want to see the vectorfield or not :True or False
    settings.show_plot = True
    settings.scale_plot = 200  # select a value to scale the quiver plot of the vectorfield
    # run the script with the given settings
    windef.piv(settings)
