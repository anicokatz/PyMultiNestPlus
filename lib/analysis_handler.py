import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import importlib.util
import pickle
import os

class AnalysisHandler:
    
    def __init__(self, model_names):
        self.fig, self.ax = plt.subplots()
        self.xmaxes, self.xmins, self.ymaxes, self.ymins = [[],[],[],[]]
        self.title_str=""
        
        self.dir = os.getcwd()
        self.n_models = len(model_names)
        self.model_dict = {}
        self.model_samples = {}
        self.model_observables = {}
        
        self.colour_list = ['red', 'blue', 'green', 'yellow', 'orange', 'black']
        self.n_colours = len(self.colour_list)
        
        # loads model data into a dictionary of models
        for name in model_names:
            with open(self.dir+'/'+name+"/chains/record.dat", 'rb') as handle:
                rec = pickle.loads(handle.read())
            self.model_dict[name] = rec
            
        for name in model_names:
            dat = np.loadtxt(self.dir+'/'+name+"/chains/samples.dat", dtype=str)
            dat = dat.astype(float)
            temp = {}
            n = self.model_dict[name]['n_par']
            pnames = self.model_dict[name]['par_names']
            for i in range(0, n):
                temp[pnames[i]] = dat[:,i]
            self.model_samples[name] = temp
            
         # load file
        for name in model_names:
            mod_spec = importlib.util.spec_from_file_location("model", self.dir+"/"+name+"/model.py")
            mod_file = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod_file)
            samples = []
            # turn samples into array
            for psamples in self.model_samples[name].values():
                samples.append(psamples)
            samples = np.transpose(samples)
            obs = []
            for sample in samples:
                obs.append(mod_file.observables(sample))
            self.model_observables[name] = obs
            
    def clear_figure(self):
        self.fig, self.ax = plt.subplots()
        self.title_str = ""
        
    def show_figure(self):
        plt.show()
    
    def refresh(self):
        self.show_figure()
        self.clear_figure()
    
    def get_record(self, key):
        return self.model_dict[key]
    
    def get_samples(self, key):
        return self.model_samples[key]

    def get_observables(self, key):
        return self.model_observables[key]
        
    def get_kde(self, model_key, parameter_keys):
        return stats.gaussian_kde([self.get_samples(model_key)[parameter_keys[0]],self.get_samples(model_key)[parameter_keys[1]]])
    
    # PLOTTING FUNCTIONS
    def plot_hist_1par(self, model_key, parameter_key, bins=None, density=None, cumulative=False):
        h = self.ax.hist(self.get_samples(model_key)[parameter_key], bins=bins, density=density, cumulative=cumulative)
        self.title_str += model_key+" : "+parameter_key + "\n "
        self.ax.set_title(self.title_str)
        return h
    
    def plot_contour_2par(self, model_key, parameter_keys):
        kernel = self.get_kde(model_key, parameter_keys) # get kernel
        # mins and maxes
        xmin = self.get_samples(model_key)[parameter_keys[0]].min()
        xmax = self.get_samples(model_key)[parameter_keys[0]].max()
        ymin = self.get_samples(model_key)[parameter_keys[1]].min()
        ymax = self.get_samples(model_key)[parameter_keys[1]].max()
        # positions
        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        Z = np.reshape(kernel(positions).T, X.shape)
        # plotting
        self.ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
        self.ax.plot(self.get_samples(model_key)[parameter_keys[0]], self.get_samples(model_key)[parameter_keys[1]], 'k.', markersize=2)
        self.ax.set_xlim([xmin, xmax])
        self.ax.set_ylim([ymin, ymax])
        self.ax.set_aspect(1.0/self.ax.get_data_ratio())
        self.title_str += model_key+" : "+parameter_keys[0]+" vs. "+parameter_keys[1]+"\n "
        self.ax.set_title(self.title_str)
        return kernel
        
    def plot_obs_vs_par(self, model_key, obs_number, parameter_key, invert_order=False, oscale='linear', pscale='linear', orange=None, prange=None, style='k.', marker_size=2, ratio=1.0):
        
        obs = np.transpose(self.get_observables(model_key))[obs_number]
        par = self.get_samples(model_key)[parameter_key]
        
        if orange == None:
            omin = obs.min()
            omax = obs.max()
        else:
            omin = orange[0]
            omax = orange[1]
        if prange == None:
            pmin = par.min()
            pmax = par.max()
        else:
            pmin = prange[0]
            pmax = prange[1]

        if invert_order==True:
            self.xmaxes.append(omax)
            self.xmins.append(omin)
            self.ymaxes.append(pmax)
            self.ymins.append(pmin)
            self.ax.plot(obs, par, style, markersize=marker_size)
            self.ax.set_xlim([min(self.xmins), max(self.xmaxes)])
            self.ax.set_ylim([min(self.ymins), max(self.ymaxes)])
            plt.xscale(oscale)
            plt.yscale(pscale)
            self.ax.set_aspect(1.0/self.ax.get_data_ratio()*ratio)
        else:
            self.xmaxes.append(pmax)
            self.xmins.append(pmin)
            self.ymaxes.append(omax)
            self.ymins.append(omin)
            self.ax.plot(par, obs, style, markersize=marker_size)
            self.ax.set_xlim([min(self.xmins), max(self.xmaxes)])
            self.ax.set_ylim([min(self.ymins), max(self.ymaxes)])
            plt.xscale(pscale)
            plt.yscale(oscale)
            self.ax.set_aspect(1.0/self.ax.get_data_ratio()*ratio)
            self.title_str += model_key+" : Observable "+str(obs_number)+" vs. "+parameter_key+"\n "
        self.ax.set_title(self.title_str)
        return [obs, par]
            
        
        
        