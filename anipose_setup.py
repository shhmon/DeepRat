import os
import sys
import toml
from dlc_setup import read_config

SESSION_NAME = 'session'

# Create new Anipose project

if __name__ == '__main__':
	dlc_folder = sys.argv[1]
	props = read_config()
	config = props['anipose_config']
	
	folder = config['project'] + "-Anipose"
	folder = os.path.abspath(folder)
	config['model_folder'] = dlc_folder

	os.mkdir(folder)
	os.chdir(folder)

	with open('config.toml', 'w') as f:
		toml.dump(config, f)
		f.close()

	for i in range(1, 2):
		os.chdir(folder)
		os.mkdir(SESSION_NAME + str(i))
		os.chdir(SESSION_NAME + str(i))
		os.mkdir(config['pipeline']['videos_raw'])
	
	