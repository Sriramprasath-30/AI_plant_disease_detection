# download_dataset.py
import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Set Kaggle credentials
os.environ['KAGGLE_USERNAME'] = "sriramprasathkumar"
os.environ['KAGGLE_KEY'] = "1061d87c08c1102b844938ec40a44d30"

# Initialize API
api = KaggleApi()
api.authenticate()

# Replace with your dataset path from Kaggle URL
dataset_name = "shuvobasak4004/rose-leaf-disease-dataset"

# Download and unzip
api.dataset_download_files(dataset_name, path="dataset", unzip=True)
print("Dataset downloaded and extracted to 'dataset/' folder")
