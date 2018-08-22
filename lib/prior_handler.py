import importlib.util
import numpy as np
import scipy.special as ssp
import scipy.stats as sst
import matplotlib.pyplot as plt
import random

class PriorHandler: 
    
    #unpack breaks the parameter input into easy-to-handle lists
    def __init__(self, model_dir):
        self.dir = model_dir
        # import parameters from current directory
        spec = importlib.util.spec_from_file_location("model", self.dir+"/parameters.py")
        p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(p)
        
        # get the number of each kind of parameter and generate empty lists
        [n_s, n_n, n_c] = [len(p.scanning), len(p.nuisance), len(p.constant)]
        [s, n, c] = [[],[],[]]
        
        # unpack scanning
        for i in range(0, n_s):
            temp = p.scanning[i]
            if temp[4] == 'gaussian': # unpacks as: identifier, min, max, mu, sd
                if temp[1] == 'real':
                    s.append(['rg', temp[2], temp[3], temp[5], temp[6]])
                elif temp[1] == 'periodic':
                    s.append(['pg', temp[2], temp[3], temp[5], temp[6]])
                else:
                    print("Scanning parameter ",i," missing type identifier.")
            elif temp[4] == 'uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    s.append(['ru', temp[2], temp[3]])
                elif temp[1] == 'periodic':
                    s.append(['pu', temp[2], temp[3]])
                else:
                    print("Scanning parameter ",i," missing type identifier.")
            elif temp[4] == 'log10-uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    s.append(['rl10', temp[2], temp[3]])
                elif temp[1] == 'periodic': # deprecated???
                    s.append(['pl10', temp[2], temp[3]])
                else:
                    print("Scanning parameter ",i," missing type identifier.")
            elif temp[4] == 'ln-uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    s.append(['rln', temp[2], temp[3]])
                elif temp[1] == 'periodic': # deprecated???
                    s.append(['pln', temp[2], temp[3]])
                else:
                    print("Scanning parameter ",i," missing type identifier.")
            else: # unpacks as: identifier, distro
                data = np.genfromtxt(self.dir+"/"+'prior_data/'+temp[4]+'.dat', dtype=float)
                hist = np.histogram(data, bins=temp[5])
                distro = sst.rv_histogram(hist)
                s.append(['dd', distro])
        
        # unpack nuisance
        for i in range(0, n_n):
            temp = p.nuisance[i]
            if temp[4] == 'gaussian': # unpacks as: identifier, min, max, mu, sd
                if temp[1] == 'real':
                    n.append(['rg', temp[2], temp[3], temp[5], temp[6]])
                elif temp[1] == 'periodic':
                    n.append(['pg', temp[2], temp[3], temp[5], temp[6]])
                else:
                    print("Nuisance parameter ",i," missing type identifier.")
            elif temp[4] == 'uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    n.append(['ru', temp[2], temp[3]])
                elif temp[1] == 'periodic':
                    n.append(['pu', temp[2], temp[3]])
                else: 
                    print("Nuisance parameter ",i," missing type identifier.")
            elif temp[4] == 'log10-uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    n.append(['rl10', temp[2], temp[3]])
                elif temp[1] == 'periodic': # deprecated???
                    n.append(['pl10', temp[2], temp[3]])
                else:
                    print("Nuisance parameter ",i," missing type identifier.")
            elif temp[4] == 'ln-uniform': # unpacks as: identifier, min, max
                if temp[1] == 'real':
                    n.append(['rln', temp[2], temp[3]])
                elif temp[1] == 'periodic': # deprecated???
                    n.append(['pln', temp[2], temp[3]])
                else:
                    print("Nuisance parameter ",i," missing type identifier.")
            else: # unpacks as: identifier, distro
                data = np.genfromtxt(self.dir+"/"+'prior_data/'+temp[4]+'.dat', dtype=float)
                hist = np.histogram(data, bins=temp[5])
                distro = sst.rv_histogram(hist)
                n.append(['dd', distro])
            
        #unpack constant
        for i in range(0, n_c):
            c.append(p.constant[i][2])
            
        self.s = s
        self.n = n
        self.c = c
        self.n_pars = n_s
        
    # a set of functions which scale up the priors
    def log10_uniform_scale_real(self, mini, maxi, x):
        return 10**(x*(maxi-mini)+mini)
    
    def log10_uniform_scale_periodic(self, mini, maxi, x):
        return 10**(x*(maxi-mini)+mini)
    
    def ln_uniform_scale_real(self, mini, maxi, x):
        return np.exp(x*(maxi-mini)+mini)
    
    def ln_uniform_scale_periodic(self, mini, maxi, x):
        return np.exp(x*(maxi-mini)+mini)
    
    def uniform_scale_real(self, mini, maxi, x):
        return x*(maxi-mini)+mini
    
    def uniform_scale_periodic(self, mini, maxi, x):
        return x*(maxi-mini)+mini
    
    def gaussian_scale_real(self, mini, maxi, mu, sd, x):
        return min(max([mini, mu + sd*ssp.ndtri(x)]), maxi)
    
    def gaussian_scale_periodic(self, mini, maxi, mu, sd, x):
        var = mu + sd*ssp.ndtri(x)
        while(var < mini):
            var = maxi-mini+var
        while(var > maxi):
            var = mini+var-maxi
        return var
    
    def data_scale_real(self, distro, x):
        return distro.ppf(x)
    
    def scale(self, cube):
#        if len(cube) != self.n_pars:
#            print("Dimensionality of cube doesn't match unpacked parameter number.")
        out = []
        for i in range(0, self.n_pars):
            x = cube[i]
            temp = self.s[i]
            if (temp[0] == 'rg'):
                out.append(self.gaussian_scale_real(temp[1], temp[2], temp[3], temp[4], x))
            elif (temp[0] == 'pg'):
                out.append(self.gaussian_scale_periodic(temp[1], temp[2], temp[3], temp[4], x))
            elif (temp[0] == 'ru'):
                out.append(self.uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pu'):
                out.append(self.uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'rln'):
                out.append(self.ln_uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pln'):
                out.append(self.ln_uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'rl10'):
                out.append(self.log10_uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pl10'):
                out.append(self.log10_uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'dd'):
                out.append(self.data_scale_real(temp[1], x))
        return out
    
    def get_nui(self, pars):
        seed_str = int(("%.16f" % pars[0]).replace(".", ""))
        random.seed(seed_str)
        # finish this
        out = []
        for i in range(0, len(self.n)):
            x = random.random()
            temp = self.n[i]
            if (temp[0] == 'rg'):
                out.append(self.gaussian_scale_real(temp[1], temp[2], temp[3], temp[4], x))
            elif (temp[0] == 'pg'):
                out.append(self.gaussian_scale_periodic(temp[1], temp[2], temp[3], temp[4], x))
            elif (temp[0] == 'ru'):
                out.append(self.uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pu'):
                out.append(self.uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'rln'):
                out.append(self.ln_uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pln'):
                out.append(self.ln_uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'rl10'):
                out.append(self.log10_uniform_scale_real(temp[1], temp[2], x))
            elif (temp[0] == 'pl10'):
                out.append(self.log10_uniform_scale_periodic(temp[1], temp[2], x))
            elif (temp[0] == 'dd'):
                out.append(self.data_scale_real(temp[1], x))
        return out