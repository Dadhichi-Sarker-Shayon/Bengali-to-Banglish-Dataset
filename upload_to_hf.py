import os
from huggingface_hub import HfApi

api = HfApi()

repo_id = "ShayonSarker/Bengali-to-Banglish-Dataset"
repo_type = "dataset"

print("Uploading main dataset...")
api.upload_file(
    path_or_fileobj="D:/BN-BE-EN/Bengali-to-Banglish-Dataset.csv",
    path_in_repo="Bengali-to-Banglish-Dataset.csv",
    repo_id=repo_id,
    repo_type=repo_type
)

print("Uploading backup dataset...")
api.upload_file(
    path_or_fileobj="D:/BN-BE-EN/Bengali-to-Banglish-Dataset-backup.csv",
    path_in_repo="Bengali-to-Banglish-Dataset-backup.csv",
    repo_id=repo_id,
    repo_type=repo_type
)

print("Uploading Dataset Card (README.md)...")
api.upload_file(
    path_or_fileobj="D:/BN-BE-EN/HF_Dataset_Card.md",
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type=repo_type
)

print("All files uploaded successfully!")
