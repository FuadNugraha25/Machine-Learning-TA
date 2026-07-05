import kagglehub

# Download latest version
path = kagglehub.dataset_download("kekavigi/earthquakes-in-indonesia")

print("Path to dataset files:", path)
