import deeplabcut
import webbrowser
import shutil
import yaml
import toml
import os

NESTING = 1
VIDEOS_RAW = "videos_raw"
TRAINING_URL = "https://colab.research.google.com/github/shhmon/DeepRat/blob/master/training.ipynb"

# Flatten and remove duplicates
flatuniq = lambda li: list(set([i for s in li for i in s]))

# Read the config.yaml file
def read_config():
	with open(r'config.yaml') as f:
		conf = yaml.load(f, Loader=yaml.FullLoader)
		f.close()

	return conf

# Injects the DLC config with values from config.yaml
def update_dlc_config(config_path, props):
	with open(config_path) as f:
		content = yaml.load(f, Loader=yaml.FullLoader)
		f.close()
	
	for key, value in props.items():
		content[key] = value
	
	with open(config_path, "w") as f:
		yaml.dump(content, f)
		f.close()

# Creates a DLC project
def create_dlc_project(name, author, files, props):
	config_path = deeplabcut.create_new_project(name, author, files)
	update_dlc_config(config_path, props)
	deeplabcut.extract_frames(config_path, 'automatic', 'kmeans', userfeedback=False)
	deeplabcut.label_frames(config_path)
	deeplabcut.check_labels(config_path)
	
	return config_path.replace('/config.yaml', '')

# Creates a folder structure for the Anipose project
def create_anipose_project(dlc_folder, name, train_files, cailb_files, props):
	props['project'] = name
	folder = os.path.abspath(name)
	props['model_folder'] = dlc_folder

	os.mkdir(folder)
	os.chdir(folder)

	# Create config file in root
	with open('config.toml', 'w') as f:
		toml.dump(props, f)
		f.close()
	
	# Create the structure
	os.chdir(folder)
	os.mkdir('calibration')
	os.chdir('calibration')

	for file in cailb_files:
		fname = file.split('/')[-1]
		shutil.copy2(file, f'{os.getcwd()}/{fname}')
	
	os.chdir(folder)
	os.mkdir('session0')
	os.chdir('session0')
	os.mkdir(props['pipeline']['videos_raw'])
	os.chdir(props['pipeline']['videos_raw'])

	for file in train_files:
		fname = file.split('/')[-1]
		shutil.copy2(file, f'{os.getcwd()}/{fname}')

if __name__ == '__main__':

	conf = read_config()

	# Create the conf to be injected to DLC
	dlc_conf = {
		'bodyparts': flatuniq(conf['scheme']),
		'numframes2pick': conf['frames'],
		'skeleton': conf['scheme'],
	}

	# Modify the supplied Anipose config
	anp_conf = {
		**conf['anipose_config'],
		'nesting': NESTING,
		'labeling': {
			'scheme': conf['scheme']
		},
		'pipeline': {
			'videos_raw': VIDEOS_RAW
		}
	}

	# Create the DLC project
	dlc_folder = create_dlc_project(
		conf['project_name'],
		conf['author'],
		conf['training_videos'],
		dlc_conf
	)

	# Create the Anipose project
	create_anipose_project(
		dlc_folder,
		conf['project_name'],
		conf['training_videos'],
		conf['calibration_videos'],
		anp_conf
	)

	webbrowser.open(TRAINING_URL, new=2)
