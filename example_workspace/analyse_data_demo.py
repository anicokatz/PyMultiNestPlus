import analysis_handler as ahandle
import matplotlib.pyplot as plt

# first set up a list of model names
# (MUST be the same names as the folders in which the models are stored)
model_names = ["model_1", "model_2", "normal_hierarchy", "inverted_hierarchy", "normal_hierarchy_nui", "inverted_hierarchy_nui"]

# declare an analyser
# it will automatically load everything it needs to from the model names alone
# predominantly from the record.dat file (using pickle)
analyser = ahandle.AnalysisHandler(model_names)

# boom, analyse away
analyser.plot_contour_2par("model_1", ["radius", "theta"])
analyser.refresh()

analyser.plot_hist_1par("model_1", "radius")
analyser.refresh()

plt1 = analyser.plot_obs_vs_par("normal_hierarchy", 0, "ml", oscale = 'log', pscale='log', style='r.')
plt2 = analyser.plot_obs_vs_par("inverted_hierarchy", 0, "ml", oscale = 'log', pscale='log', style='b.')
plt3 = analyser.plot_obs_vs_par("normal_hierarchy_nui", 0, "ml", oscale = 'log', pscale='log', style='y.')
plt4 = analyser.plot_obs_vs_par("inverted_hierarchy_nui", 0, "ml", oscale = 'log', pscale='log', style='g.')
analyser.refresh()

analyser.plot_contour_2par("normal_hierarchy", ["phi1", "phi2"])
analyser.refresh()

analyser.plot_contour_2par("inverted_hierarchy", ["phi1", "phi2"])
analyser.refresh()
