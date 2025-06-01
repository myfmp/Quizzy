import os
import uuid
from django.core.files.storage import default_storage
from .converter import *

def upload_file(file, quizz_id):
    # Valid extensions and maximum file size in bytes
    valid_extensions = ['doc', 'docx', 'pdf', 'png', 'jpg']
    max_file_size = 10 * 1024 * 1024  # 10 MB

    if not file:
        return {'error': 'No file provided.'}

    # Validate file extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in valid_extensions:
        return {'error': 'Invalid file extension.'}

    # Validate file size
    if file.size > max_file_size:
        return {'error': 'File size exceeds the maximum limit of 10 MB.'}

    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    folder_path = 'tmp'
    file_path = default_storage.save(os.path.join(folder_path, unique_filename), file)

    download_link = default_storage.url(file_path)

    return OCR(download_link)
