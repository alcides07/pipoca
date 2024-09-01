import tempfile
import shutil
from fastapi import UploadFile


async def create_temporary_file(upload_file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)
        return temp_file.name
