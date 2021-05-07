# DeepRat

## How to use

In order to use this package, install an Anaconda distribution, go to `conda-environments` and use the `DLC-CPU.yaml` file to create a conda ennvironment:

`conda env create -f DLC-CPU.yaml`

This will install DeepLabCut along with other dependencies inside the environment. We're using the CPU environment here as the goal is to train the network though a Google colab environment anyway. Activate the conda environment:

`conda activate DLC-CPU`

To create a project, configure the variables at the top of `local.py` and run:

`python local.py`

This will create the project, pause to let you configure `config.yaml` and then proceed to labeling. When labeling is done, upload the project folder (not the whole repo) to the root folder of your drive and run the `training.ipynb` file in Google Colab. The cells are pretty self explanatory, specify the project name and run it.

Once the model is trained, download the repo with the trained model from drive. Now, the project path in `config.yaml` has to be updated again - do it manually. To evaluate the network, open a python interpreter and run (remember to define `config_path` again):

`deeplabcut.evaluate_network(config_path,Shuffles=[1], plotting=True)`

Then, to analyze a new unseen video run:

`deeplabcut.analyze_videos(config_path, ['/path/to/new/video.avi'])`

and finally, to generate a labeled video from the analysis:

`deeplabcut.create_labeled_video(config_path, ['/path/to/new/video.avi'])`

---

## Indivudial steps of creating a project and training a model

**This section describes in a little more detail the process of creating and training a network (without using the `local.py` script)**

To create a model, open `ipython` or `pythonw` (normally `ipython` is used, but GUI bug on mac can be solved with `conda install python.app` and using `pythonw` instead) and run the following lines:

`import deeplabcut`

`config_path = deeplabcut.create_new_project("ProjectName", "Author", ["path/to/video.mp4"])`

This creates a new project directory `ProjectName-Author-Date`  which contains a `config.yaml` file. In this file, details such as body parts and skeleton configuration should be specified. According to the papers, the identification works better with more general models. In other words, models with many body parts tend to work better than the more specific ones (e.g a single body part). Another important point variable is `numframes2pick`, which specifies the number of labeled frames to use (default = 20). More info about the config file can be found [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/functionDetails.md#b-configure-the-project-). The `config_path` variable now specifies the location of the config file. Run the following:

`deeplabcut.extract_frames(config_path, 'automatic', 'kmeans')`

`deeplabcut.label_frames(config_path)`

This opens a GUI in which you can mark body parts which are to be tracked. Start by clicking "Load Frames" and navigating to `project/path/labeled-data/video-file-name`. Click open and label all the frames (number of frames can be specified in the config file), click save and run:

`deeplabcut.check_labels(config_path)`

At this stage, you should switch to a notebook in Colab if you don't want to do the training locally.

`deeplabcut.create_training_dataset(config_path)`

Now it is time to train the network. The training function takes many optional parameters (more about them [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/functionDetails.md#g-train-the-network)). For our purpose, the most important is probably the `maxiters` parameters which specifies the number of iterations:

`deeplabcut.train_network(config_path, maxiters=500000)`

Here, the iteration number is set to 500 000 as the network theoretically should converge in around 200k-400k iterations.

