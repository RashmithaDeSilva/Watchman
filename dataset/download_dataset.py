import kagglehub

# Download latest version
path = kagglehub.dataset_download("constantinwerner/human-detection-dataset")

print("Path to dataset files:", path)
