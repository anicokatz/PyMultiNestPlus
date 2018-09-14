# The model file must be named model.py

# It must contain a loglikelihood function which take a single
# input: the list of scanning parameter values (all doubles).
#
# It must contain a prior function which takes a single input: a random
# point in the N-hypercube. This prior function must return a parameter
# list which has been scaled from the N-hypercube to the scanning parameter
# priors.
#
# It is useful to include a model function which computes
# A model parameter from the scanning parameters. This model function can be
# called inside the loglikelihood function for the sake of readability.
#
# This is an example model file

# --------------------------------------
#   Things the user shouldn't change
# --------------------------------------
import prior_handler as phandle
import numpy as np
import os
cwd = os.path.dirname(os.path.realpath(__file__))
print(cwd) #for verbosity

prior_handler = phandle.PriorHandler(cwd)
con = prior_handler.c #manually load constant parameters
n_pars = prior_handler.n_pars

def prior(cube, n_dims, n_pars):
    return prior_handler.scale(cube)

# --------------------------------------
#   Things the user should change
# --------------------------------------

def observables(pars): #must return a list of observables
    # get the nuisances from the par-based seed
    # note that this must be done on a per-parameter basis, and so cannot
    # be loaded once at the start
    nui = prior_handler.get_nui(pars)
    
    # with pars, nui, con, start calculation:
    return [pars[0]*np.cos(pars[1])*np.sin(nui[0])]

def loglikelihood(pars, n_dims, n_pars):
    obs = observables(pars)
    loglikelihood = (-((obs[0]-con[0])**2)/(2*(con[1]**2)))
    return loglikelihood
