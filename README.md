# PyMultiNestPlus

PyMultiNestPlus is a small library of python files that provides additional functionality to PyMultiNest in an effort to shore up some of its shortcomings. It namely includes:
- Functionality for generating and analysing data for multiple different models at once.
- The ability to implement nuisance and constant parameters alongside scanning parameters.
- Additional data sanitisation.
- Automatic generation and handling of non-standard prior distributions from a list of data points.
- Automatic scaling from the unit hypercube to the prior space.

In essence, PyMultiNestPlus streamlines a lot of the tedious or time-consuming and pedantic parts of using PyMultiNest, while keeping as much of the original flexibility as possible.

## Getting Started

### Prerequisites

PyMultiNestPlus requires a working python 3.6+ installation, MultiNest, and PyMultiNest to function properly. Instructions for the installation of both MultiNest and PyMultiNest are provided at https://johannesbuchner.github.io/PyMultiNest/install 

### Installing

PyMultiNestPlus doesn't need to be installed. The library and workspace can be cloned directly from github:
```
git clone https://github.com/anicokatz/PyMultiNestPlus
```
And the appropriate path must be exported:
```
export PYTHONPATH="${PYTHONPATH}:<directory-to-PyMultiNestPlus>/PyMultiNestPlus/lib"
```
Consider adding the previous line to your /.bashrc so that you don't have to export the path for every new working shell.

## Running the tests

To test PyMultiNestPlus, first navigate to the example workspace:
```
cd <directory-to-PyMultiNestPlus>/PyMultiNestPlus/example_workspace
```
And run `generate_data_demo.py`:
```
python demo.py
```
You should see a long list of values, and two lines at the end that read:
```
Sampling finished. Exiting MultiNest
<directory-to-PyMultiNestPlus>/PyMultiNestPlus/example_workspace/inverted_hierarchy_nui
```
Then run `analyse_data_demo.py`:
```
python analyse_data_demo.py
```
You should see a dictionary of important variables regarding `model_1`:
```
{'workspace_dir': '<directory-to-PyMultiNestPlus>/PyMultiNestPlus/example_workspace', 'model_name': 'model_1', 'par_names': ['radius', 'theta'], 'nui_names': ['phi'], 'con_names': ['mu', 'sd'], 'n_par': 2, 'n_nui': 1, 'n_con': 2, 'tolerance': 0.2, 'n_live': 300, 'resume': False, 'max_iterations': -1, 'n_samples': 697, 'logZ': nan}
```
(Note that the value of `'n_samples'` may differ; but should land within the 500-1000 range. A value of zero, a value outside of this range, or a value of exactly 718 may indicate that PyMultiNestPlus/PyMultiNest/MultiNest is not working. Rerun the `generate_data_demo.py` file; and if the result doesn't change, do a clean reinstallation.

## Tutorial

A brief overview of the workspace structure is given below. More information can be found in the files in the  `model_1` folder in the example workspace. Workspaces are independent of each other.

### Workspace Structure

Each workspace consists of a single file which manages the program, and a single folder for each model that you want to simulate over. Each model contains a folder for the output data called `chains`, a folder for the non-standard (gaussian, uniform) prior data called `prior_data`, a parameters/priors file called `parameters.py`, and a model file called `model.py`.

The program reads from `parameters.py` once at runtime, and loads from it all model parameters: scanning parameters which the simulation is run over, nuisance or noisy parameters, and constants. These parameters should include the parameters which define the posterior distribution. In the case that a non-standard parameter type is used, it will load sample data (a single string of space-separated values in a `.dat` file) of the same type from `prior_data` and generate a distribution from that. For example:
```
mass = ['mass', 'real', 1, 10, 'uniform']
phi1 = ['phi1', 'periodic', 0, 2*np.pi, 'phi1-data']
phi2 = ['phi2', 'periodic', 0, 2*np.pi, 'gaussian', np.pi, 0.1]
scanning = [mass, phi1]
nuisance = [phi2]
constant = []
```
Creates a uniformly distributed mass parameter between 1 and 10, a periodic phi1 parameter distributed between 0 and 2pi according to the file `phi1-data.dat` in `prior_data`, and a periodic phi2 parameter which follows a gaussian distribution of mean pi and standard deviation 0.1. It then loads mass and phi1 into the scanning parameters, and phi2 into the nuisance parameters.

The model file `model.py` contains two functions which can be edited by the user: `model_value` and `loglikelihood`. `model_value` should return an object `mval` which is then directly passed to `loglikelihood` which in turn should return a single value: the logarithm of the likelihood of `mval` when compared to the target distribution. Parameters are zero-indexed in the same order that they are loaded in `parameters.py`.

The rest of `model.py` should not be edited, as it automatically handles prior scaling and nuisance parameter extraction.

### Functions

Each model can `run()`, `sanitise()`, and  `generate_samples_file()` by itself, for itself. However, a `simulation_handler` object will automatically deal with every loaded model. An example of how to do this is detailed in `demo.py`.

### Output

Model sample chains are outputted as `samples.dat` in the model's `chains` folder. It contains a sanitised and correctly scaled-from-unit-hypercube version of the data in `post_equal_weights.dat`, and should be immediately readable using standard library file reading functions.

The final column in the file is the logarithm of the likelihood of the sample.

The logarithm of the global model evidence can be found in `stats.dat`.

## Authors

* **Alex Nico-Katz** - *Initial work* - [Alex Nico-Katz](https://github.com/alexnicokatz)

## License

No clue. Open source? What even is a license.

## Acknowledgments

* J. Buchner for creating the PyMultiNest wrapper on which this is built - [Johannes Buchner](https://github.com/johannesbuchner)

* F. Feroz et al. for creating MultiNest.

