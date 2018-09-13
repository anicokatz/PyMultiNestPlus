import numpy as np
import pickle
import os

class AnalysisHandler:
    
    def __init__(self, model_names):
        self.dir = os.getcwd()
        self.n_models = len(model_names)
        self.model_dict = {}
        
        self.colour_list = ['red', 'blue', 'green', 'yellow', 'orange', 'black']
        self.n_colours = len(self.colour_list)
        
        # loads model data into a dictionary of models
        for name in model_names:
            with open(self.dir+'/'+name+"/chains/record.dat", 'rb') as handle:
                rec = pickle.loads(handle.read())
            self.model_dict[name] = rec
            
    def get_samples(self, key):
        dat = np.loadtxt(self.dir+'/'+self.model_dict[key]+"/chains/samples.dat", dtype=str)
        dat = dat.astype(float)
        return dat
            
    def get_record(self, key):
        return self.model_dict[key]