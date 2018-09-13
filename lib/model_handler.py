import pymultinest
import numpy as np
import importlib.util
import pickle, json

class ModelHandler: 
    
    #initialises the simulation handler
    def __init__(self, wsd, ml, tol, nl, resume, maxiter):
        self.workspace_dir = wsd
        self.model_name = ml
        self.tolerance = tol
        self.n_live = nl
        self.resume = resume
        self.max_iterations = maxiter
        self.n_samples = 0
        self.logZ = np.NaN #get evidence WRITE THIS
        
        # load and execute parameters.py and model.py from model folder
        self.par_spec = importlib.util.spec_from_file_location("model", self.workspace_dir+"/"+self.model_name+"/parameters.py")
        self.par_file = importlib.util.module_from_spec(self.par_spec)
        self.par_spec.loader.exec_module(self.par_file)
        
        self.mod_spec = importlib.util.spec_from_file_location("model", self.workspace_dir+"/"+self.model_name+"/model.py")
        self.mod_file = importlib.util.module_from_spec(self.mod_spec)
        self.mod_spec.loader.exec_module(self.mod_file)
        
        self.par_names = [i[0] for i in self.par_file.scanning]
        self.n_par = len(self.par_names)
        
        self.nui_names = [i[0] for i in self.par_file.nuisance]
        self.n_nui = len(self.nui_names)
        
        self.con_names = [i[0] for i in self.par_file.constant]
        self.n_con = len(self.con_names)
        
    def run(self):

        pymultinest.run(self.mod_file.loglikelihood, self.mod_file.prior, self.mod_file.n_pars,
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
        
        dat = np.loadtxt(self.model_name+"/chains/post_equal_weights.dat", dtype=str)
        dat = dat.astype(float)
        # scale up cube to samples
        for i in range(0, self.n_samples):
            temp = self.mod_file.prior(dat[i][0:-1], self.n_par, self.n_par)
            temp.append(dat[i][-1])
            dat[i] = temp
        np.savetxt(self.model_name+"/chains/samples.dat", dat, delimiter='    ')
        return self.n_live
    
    def generate_record_file(self):
        d = {
                'workspace_dir':self.workspace_dir,
                'model_name':self.model_name,
                'par_names':self.par_names,
                'nui_names':self.nui_names,
                'con_names':self.con_names,
                'n_par':self.n_par,
                'n_nui':self.n_nui,
                'n_con':self.n_con,
                'tolerance':self.tolerance,
                'n_live':self.n_live,
                'resume':self.resume,
                'max_iterations':self.max_iterations,
                'n_samples':self.n_samples,
                'logZ':self.logZ
            }
        with open(self.model_name+"/chains/record.dat", 'wb') as handle:
            pickle.dump(d, handle)
        
        # create a utf-8 human-readable version with json
        with open(self.model_name+"/chains/record_READABLE.txt", 'w', encoding="utf-8") as handle:
            json.dump(d, handle)