import analysis_handler as ahandle
import matplotlib.pyplot as plt

# first set up a list of model names
# (MUST be the same names as the folders in which the models are stored)
model_names = ["model_1", "model_2"]

# declare an analyser
# it will automatically load everything it needs to from the model names alone
# predominantly from the record.dat file (using pickle)
analyser = ahandle.AnalysisHandler(model_names)

# boom, analyse away
print(analyser.get_record("model_1"))