import deeplabcut

# Create new project

project_name = "TestProject"
author = "Tester"
files = ['/Users/shabo/Desktop/CSProject/DeepRat/example-videos/1a.mp4']

if __name__ == '__main__':
	config_path = deeplabcut.create_new_project(project_name, author, files)
	print('\nPrject has been created. Please edit config.yaml and press enter to continue with labeling\n')
	input()
	deeplabcut.extract_frames(config_path, 'automatic', 'kmeans')
	deeplabcut.label_frames(config_path)
	deeplabcut.check_labels(config_path)
	deeplabcut.create_training_dataset(config_path)
