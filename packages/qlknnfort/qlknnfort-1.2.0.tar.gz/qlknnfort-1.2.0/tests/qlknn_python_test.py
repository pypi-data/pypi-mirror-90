# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
import time

import numpy as np
import f90nml
from IPython import embed

import _QLKNNFORT

nml = f90nml.read('./test.nml')
inp = np.array(nml['test']['input']).T
outp = np.asfortranarray(np.empty((inp.shape[1], 10)))

# Run once to load networks in memory
_QLKNNFORT.f90wrap_evaluate_qlknn_10d_direct('../lib', inp, outp)

tests = 100
starttime = time.time()
for ii in range(tests):
    _QLKNNFORT.f90wrap_evaluate_qlknn_10d_direct('../lib', inp, outp, verbosityin=0)
endtime = time.time()
print('Took {!s} ms'.format((endtime - starttime)/tests*1000))
