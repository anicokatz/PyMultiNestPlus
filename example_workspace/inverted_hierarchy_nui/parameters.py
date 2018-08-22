import numpy as np
# priors.py has three sections:

# scanning parameters over which the simulation is run
ml = ['ml', 'real', -4, 0, 'log10-uniform']
phi1 = ['phi1', 'periodic', 0, 2*np.pi, 'uniform']
phi2 = ['phi2', 'periodic', 0, 2*np.pi, 'uniform']

# nuisance parameters which act as noise
t12 = ['t12', 'periodic', 0, 2*np.pi, 'gaussian', 0.588, 0.013]
t13 = ['t13', 'periodic', 0, 2*np.pi, 'gaussian', 0.148, 0.003]
dm2 = ['dm2', 'real', -1000, 1000, 'gaussian', 7.56*(10**(-5)), 0.24*(10**(-5))]
Dm2 = ['Dm2', 'real', -1000, 1000, 'gaussian', 2.40*(10**(-3)), 0.07*(10**(-3))]

# constant parameters
posterior_mu = ['mu','const',10**(-2)]
posterior_sd = ['sd','const',1]

# Finally we load the parameters into their respective arrays:
scanning = [ml, phi1, phi2] # we are scanning over rad and theta
nuisance = [t12, t13, dm2, Dm2] # phi is treated as a nuisance parameter
constant = [posterior_mu, posterior_sd]