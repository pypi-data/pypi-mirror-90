import numpy as np
import datatest as dt

a = np.array([(1, 12.25),
              (2, 33.75),
              (3, 101.5)],
             dtype='int32, object')

dt.validate(a, (np.integer, np.floating))

