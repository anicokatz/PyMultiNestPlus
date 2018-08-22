import pymultinest
import matplotlib.pyplot as plt
import numpy as np
import importlib.util

class ModelHandler: 
    
    #initialises the simulation handler
    def __init__(self, wsd, ml, tol, nl, resume, maxiter):
        self.workspace_dir = wsd
        self.model_name = ml
        self.tolerance = tol
        self.n_live = nl
        self.resume = resume
        self.max_iterations = maxiter
        
    def run(self):
        # import modules from model path
        spec = importlib.util.spec_from_file_location("model", self.workspace_dir+"/"+self.model_name+"/model.py")
        model_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_file)
        
        pymultinest.run(model_file.loglikelihood, model_file.prior, model_file.n_pars,
                        n_clustering_params=None, wrapped_params=None, 
                        importance_nested_sampling=True, multimodal=True, 
                        const_efficiency_mode=False, n_live_points=self.n_live, 
                        evidence_tolerance=self.tolerance, sampling_efficiency=0.8, 
                        n_iter_before_update=100, null_log_evidence=-1e+90, 
                        max_modes=100, mode_tolerance=-1e+90, 
                        outputfiles_basename=self.model_name+"/chains/", seed=-1, 
                        verbose=True, resume=self.resume, context=0, 
                        write_output=True, log_zero=-1e+100, max_iter=self.max_iterations, 
                        init_MPI=False, dump_callback=None)
        
    def sanitise(self):
        dat = np.loadtxt(self.model_name+"/chains/post_equal_weights.dat", dtype=str)
        self.n_pars = len(dat[0])-1
        self.n_samples = 0
        
        # first we sanitise the data
        for index, item in enumerate(dat):
            self.n_samples += 1
            for jndex, jtem in enumerate(item):
                try:
                    dat[index][jndex] = float(jtem)
                except ValueError:
                    dat[index][jndex] = 0.0
        np.savetxt(self.model_name+"/chains/post_equal_weights.dat", dat.astype(float), delimiter='    ')
        return self.n_samples
        
    def generate_samples_file(self):
        spec = importlib.util.spec_from_file_location("model", self.workspace_dir+"/"+self.model_name+"/model.py")
        model_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_file)
        
        dat = np.loadtxt(self.model_name+"/chains/post_equal_weights.dat", dtype=str)
        dat = dat.astype(float)
        # scale up cube to samples
        for i in range(0, self.n_samples):
            temp = model_file.prior(dat[i][0:-1], self.n_pars, self.n_pars)
            temp.append(dat[i][-1])
            dat[i] = temp
        np.savetxt(self.model_name+"/chains/samples.dat", dat, delimiter='    ')
        return self.n_live