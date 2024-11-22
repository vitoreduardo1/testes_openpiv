import numpy as np

from PIV_fluid_speed import image_generator
from main import main
from error import total_error

n = 1
t = 58

for i in range(n):


    image_generator()
    main()
    total_error()

