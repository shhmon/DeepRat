# DeepRat

## How to use

In order to use this package, install an Anaconda distribution, go to `conda-environments` and use one of the `.yaml` files (DLC-GPU or DLC-CPU) to create a conda ennvironment:

`conda env create -f DLC-CPU.yaml`

This will install DeepLabCut along with other dependencies inside the environment. GPU or CPU specifies which version of Tensorflow you want to use. To activate the environment:

`conda activate DLC-CPU`

Any problems related to GUI applications on Mac can be solved using by running `conda install python.app` inside the environment and using `pythonw` instead of `ipython`.

### What has been done so far

I've tried using one of the example videos to train a model without success. The training took a whole day and I had to kill it. This is probably due to too many iterations and the fact that I was using `DLC-CPU` instead of `DLC-GPU`. To run the GPU version of Tensorflow, the `cudnn` package is required by the conda configuration file - this package only exists for Nvidia GPU:s.

To create a model, open `ipython` or `pythonw` (depending on what works for you) and run the following lines:

`import deeplabcut`

`deeplabcut.create_new_project("ProjectName", "Author", ["path/to/video.mp4"])`

This creates a new project directory `ProjectName-Author-Date`  which contains a `config.yaml` file. In this file, details such as body parts and skeleton configuration should be specified. According to the papers, the identification works better with more general models. In other words, models with many body parts tend to work better than the more specific ones (e.g a single body part). Another important point variable is `numframes2pick`, which specifies the number of labeled frames to use (default = 20). More info about the config file can be found [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/functionDetails.md#b-configure-the-project-). Edit it to preference and save its path to a new variable:

`config_path = "path/to/project/config.yaml"`

Now, run the following:

`deeplabcut.extract_frames(config_path, 'automatic', 'kmeans')`

`deeplabcut.label_frames(config_path)`

This opens a GUI in which you can mark body parts which are to be tracked. Start by clicking "Load Frames" and navigating to `project/path/labeled-data/video-file-name`. Click open and label all the frames (number of frames can be specified in the config file), click save and run:

`deeplabcut.check_labels(config_path)`

`deeplabcut.create_training_dataset(config_path)`

At this point, it is time to train the network. The training function takes many optional parameters (more about them [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/functionDetails.md#g-train-the-network)). For our purpose, the most important is probably the `maxiters` parameters which specifies the number of iterations:

`deeplabcut.train_network(config_path, maxiters=500000)`

Here, the iteration number is set to 500 000 as the network theoretically should converge in around 200k-400k iterations. The problem right now is that 500 000 iterations would take a couple of days to run on my Mac, and it has no Nvidia GPU so using cudnn with Tensorflow is out of the question. Also, labeling the frames is quite hard as the resolution is poor.

