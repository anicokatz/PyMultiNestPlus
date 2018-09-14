# NORMAL HIERARCHY
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

def observables(pars):
    # get the nuisances from the par-based seed
    nui = prior_handler.get_nui(pars)
    
    # get mt value
    c13 = math.cos(nui[1])
    
    a1 = abs(math.cos(nui[0]*c13))**2
    a2 = abs(math.sin(nui[0]*c13))**2
    a3 = abs(math.sin(nui[1]))**2
    
    dm2 = max(0, nui[2])
    
    m1 = pars[0]
    m2 = math.sqrt(m1**2 + dm2)
    m3 = math.sqrt(m1**2 + max([0, nui[3]]) + dm2/2)
    
    # with pars, nui, con, start calculation:
    return [abs(a1*m1*np.exp(-1j*pars[1]) + a2*m2*np.exp(-1j*pars[2]) + a3*m3 )]

def loglikelihood(pars, n_dims, n_pars):
    mval = observables(pars)
    mval = mval[0]
    loglikelihood = (-((mval-con[0])**2)/(2*(con[1]**2)))
    return loglikelihood