# DeepRat

## How to use

All configuration for this pipeline should be done through `config.yaml`. The upper part consists of configuration values for DLC whereas the lower part concerns Anipose. The current values for Anipose are the default values gathered from a number of sources and will not work properly without further reading and adaptation.

### DLC Training

In order to use this pipeline, install an Anaconda distribution and use the `DLC-CPU.yaml` file to create a conda ennvironment:

* `conda env create -f DLC-CPU.yaml`

This will install DeepLabCut and Anipose along with other dependencies inside the environment. We're using the CPU environment here as the goal is to train the network though a Google colab environment anyway. Activate the conda environment:

* `conda activate DLC-CPU`

To create a DLC project and a linked Anipose project, configure the variables in `config.yaml` and run:

* `python main.py`

This will create a DLC project, extract frames and then proceed to manual labeling. When labeling is done, an Anipose project structure will be created and linked to the DLC project. The folder with the longer name (with a date) will be the DLC project and the shorter will be Anipose.

The `training.ipynb` notebook should automatically open in Google Colab. Proceed with uploading the DLC project folder (NOT the whole repo) to the root folder of your drive and run the notebook. The cells are pretty self explanatory, specify the folder and you're good to go.

Once the model is trained, download the trained DLC folder from drive. Put it back in the same place as before. That's it for the DLC network, the section below describes how to proceed with Anipose.

### Anipose usage

The Anipose project should be created and linked to the DLC project if everything worked correctly. There are three short commands which will suffice for this description. They are composed of multiple commands described in more detail in a section below:

* `anipose run-data` (composed of `analyze, filer, calibrate, triangulate, angles`)
* `anipose run-viz` (composed of `label-2d, label-3d, label-combined`)
* `anipose run-all`(composed of `run-data, run-viz`)


---

## Indivudial steps of creating a project and training a model

*Read with caution, this section might be outdated*

**This section describes in a little more detail the process of creating and training a network (without using the `dlc_setup.py` script)**

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

Here, the iteration number is set to 500 000 as the network theoretically should converge in around 200k-400k iterations. The network can be evaluated post-training by running:

`deeplabcut.evaluate_network(config_path,Shuffles=[1], plotting=True)`

And used to analyse an unseen video with:

`deeplabcut.analyze_videos(config_path, ['/path/to/new/video.avi'])`

and finally, to generate a labeled video from the analysis:

`deeplabcut.create_labeled_video(config_path, ['/path/to/new/video.avi'])`

## Anipose command details

To analyzes the project and make sure everything is in order:

* `anipose analyze`

If there are errors, there is probably some problems with config paths. If not, the filter command gets rid of any predicted labels that do not come within the threshold:

* `anipose filter`

To generate a labeled video from the data:

* `anipose label-2d-filter`

To calibrate the cameras:

* `anipose calibrate`

To triangulate the points:

* `anipose triangulate`

Now we can label or get raw angle data with:

* `anipose label-3d`
* `anipose angles`

For viewing, combine the videos to one with:

* `anipose label-combined`