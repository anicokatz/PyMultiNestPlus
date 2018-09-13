import simulation_handler as shandle

# models and their parameters
# structure of a model vector is:
# model_name_string, tolerance_double, n_live_integer, resume_boolean, max_iterations_integer
# typically, tolerance = 0.5, max_iterations = 0 will work to a reasonable degree
# for generating new data each time, set resume to false
# for using old data (provided nothing has changed in that particular model's folder), set resume to true
# setting max_iterations to anything but -1 will ensure a cut-off that may be useful for extremely low-likelihood models

tol = 0.5
n_live = 200
resume = False
max_iter = -1

model1 = ["model_1", 0.2, 300, False, -1]
model2 = ["model_2", 0.4, 200, False, -1]
modelNH = ["normal_hierarchy", tol, n_live, resume, max_iter]
modelIH = ["inverted_hierarchy", tol, n_live, resume, max_iter]
modelNH_nui = ["normal_hierarchy_nui", tol, n_live, resume, max_iter]
modelIH_nui = ["inverted_hierarchy_nui", tol, n_live, resume, max_iter]

model_list = [model1, model2]

# first we make a simulation handler to (surprise surprise) handle our simulation for us
simulation_handler = shandle.SimulationHandler(model_list)

# we then generate our data for all models
simulation_handler.generate_all_data()