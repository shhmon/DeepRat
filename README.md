# DeepRat

## How to use

In order to use this package, install an Anaconda distribution, go to `conda-environments` and use one of the `.yaml` files (DLC-GPU or DLC-CPU) to create a conda ennvironment:

`conda env create -f DLC-CPU.yaml`

This will install DeepLabCut along with other dependencies inside the environment. GPU or CPU specifies which version of Tensorflow you want to use. To activate the environment:

`conda activate DLC-CPU`

Any problems related to GUI applications on Mac can be solved using by running `conda install python.app` inside the environment and using `pythonw` instead of `ipython`.

### What has been done so far

I've tried using one of the example videos to train a model without success. The training took a whole day and I had to kill it. This is probably due to too many iterations and the fact that I was using `DLC-CPU` instead of `DLC-GPU`. To run the GPU there is some configuration which needs to be done - haven't gotten around to doing it yet.

To create a model, open `ipython` or `pythonw` (depending on what works for you) and run the following lines:

`import deeplabcut`

`deeplabcut.create_new_project("ProjectName", "Author", ["path/to/video.mp4"])`

This creates a new project directory `ProjectName-Author-Date`  which contains a `config.yaml` file. In this file, details such as body parts can be specified. Edit it to preference and save its path to a new variable:

`config_path = "path/to/project/config.yaml"`

Now, run the following:

`deeplabcut.extract_frames(path_config, 'automatic', 'kmeans')`

`deeplabcut.label_frames(path_config)`

This opens a GUI in which you can mark body parts which are to be tracked. Label all the frames (number of frames can be specified in the config file), click save and run:

`deeplabcut.check_labels(path_config)`

`deeplabcut.create_training_dataset(path_config)`

`deeplabcut.train_network(path_config)`

This should train the network and this is as far as I've gotten.

