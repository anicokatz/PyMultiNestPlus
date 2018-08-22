import numpy as np
# priors.py has three sections:

# scanning parameters over which the simulation is run
# nuisance parameters which act as noise
# constant parameters

# all parameters are first defined as individual lists, then manually loaded 
# into the different parameter arrays.

# Parameter lists have between three and seven elements.

# The first two elements are always strings: the parameter name and type
# There are three currently implemented types: 'real', 'periodic', 'const'
# only parameters in the constant parameter list can have 'const' type
posterior_mean = ['mu','const',0]
posterior_sd = ['sd','const',1]

# For the other two types, the next three elements are the minimum value,
# maximum value, and distribution type (two doubles and a string respectively)
# There are currently two distribution types: 'uniform', 'gaussian'

# if the distribution string is 'uniform' then it uses the scanning range:
theta = ['theta','periodic',0,2*np.pi,'uniform']

# if the distribution string is 'gaussian' then two more parameters are needed:
# mean_double, standard-deviation_double:
rad = ['radius','real',0,100,'gaussian',1,0.01]

# if the distribution string is something else then it is interpreted as the
# name of a .dat file containing a 1-D array of data points that produce the 
# desired distribution when plotted as a normalised histogram.
# the final value (after the distribution string) is the number of bins to use
# when generating the data histogram.
phi = ['phi','periodic',0,2*np.pi,'phidata',10]

# Finally we load the parameters into their respective arrays:
scanning = [rad, theta] # we are scanning over rad and theta
nuisance = [phi] # phi is treated as a nuisance parameter
constant = [posterior_mean, posterior_sd]