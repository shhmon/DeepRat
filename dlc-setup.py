import deeplabcut
import yaml

# Create new DLC project

def read_config():
	with open(r'config.yaml') as f:
		props = yaml.load(f, Loader=yaml.FullLoader)
		f.close()

	return props

def update_dlc_config(config_path, props):
	with open(config_path) as f:
		content = yaml.load(f, Loader=yaml.FullLoader)
		f.close()
	
	for key, value in props.items():
		content[key] = value
	
	with open(config_path, "w") as f:
		yaml.dump(content, f)
		f.close()

def create_dlc_project(name, author, files, props):
	config_path = deeplabcut.create_new_project(name, author, files)
	update_dlc_config(config_path, props)
	deeplabcut.extract_frames(config_path, 'automatic', 'kmeans')
	deeplabcut.label_frames(config_path)
	deeplabcut.check_labels(config_path)

if __name__ == '__main__':

	props = read_config()

	create_dlc_project(
		props['project_name'],
		props['author'],
		props['train_videos'],
		props['dlc_config']
	)
