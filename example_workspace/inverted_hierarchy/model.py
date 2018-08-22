# INVERTED HIERARCHY
import prior_handler as phandle
import math
import numpy as np
import os
cwd = os.path.dirname(os.path.realpath(__file__))
print(cwd)

prior_handler = phandle.PriorHandler(cwd)
con = prior_handler.c
n_pars = prior_handler.n_pars

def prior(cube, n_dims, n_pars):
    return prior_handler.scale(cube)

def model_value(pars):
    # get the nuisances from the par-based seed
    nui = prior_handler.get_nui(pars)
    
    # get mt value
    c13 = math.cos(pars[4])
    
    a1 = abs(math.cos(pars[3]*c13))**2
    a2 = abs(math.sin(pars[3]*c13))**2
    a3 = abs(math.sin(pars[4]))**2
    
    dm2 = pars[5]
    Dm2 = pars[6]
    
    m3 = pars[0]
    m2 = math.sqrt(max([0, m3**2 + Dm2 + dm2/2]))
    m1 = math.sqrt(max([0, m3**2 + Dm2 - dm2/2]))
    
    # with pars, nui, con, start calculation:
    return abs(a1*m1*np.exp(-1j*pars[1]) + a2*m2*np.exp(-1j*pars[2]) + a3*m3 )

def loglikelihood(pars, n_dims, n_pars):
    mval = model_value(pars)
    loglikelihood = (-((mval-con[0])**2)/(2*(con[1]**2)))
    return loglikelihood