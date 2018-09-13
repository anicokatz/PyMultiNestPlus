import model_handler as mhandle
import matplotlib.pyplot as plt
import os

class SimulationHandler:
    
    #initialises the simulation handler
    def __init__(self, models_info):
        self.dir = os.getcwd()
        self.n_models = 0
        self.model_dict = {}
        # generates a list of modelhandlers with the initialisation parameters for each model
        for item in models_info:
            self.model_dict[item[0]] = mhandle.ModelHandler(self.dir, item[0], item[1], item[2], item[3], item[4])
            self.n_models += 1
        
    def generate_all_data(self):
        for key, model in self.model_dict.items():
            model.run()
            model.sanitise()
            model.generate_samples_file()
            model.generate_record_file()