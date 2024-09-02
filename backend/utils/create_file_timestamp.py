import os
from datetime import datetime
from fastapi import UploadFile


def create_file_timestamp(upload_file: UploadFile):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    directory = "./temp"
    file_path = os.path.join(
        directory, f"arquivo_{timestamp}")

    os.makedirs(directory, exist_ok=True)

    with open(file_path, 'wb') as file:
        content = upload_file.file.read()
        file.write(content)

    return file_path
