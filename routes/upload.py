from fastapi import APIRouter, File, UploadFile, Path
from os.path import dirname, abspath, join
from typing import Optional, List
from helper.response import Response as Res
import io
import shutil

router = APIRouter()

dir = dirname(dirname(abspath(__file__)))
upload_path = join(dir, 'uploads/')

# FOR SINGLE FILE UPLOAD...


@router.post('/upload')
async def saveFile(file: UploadFile = File(...)):
    try:
        print('dirname.........', dir)
        print('upload_path.........', upload_path)
        print('file.........', file.filename)
        with open(file.filename, 'wb') as f:
            [f.write(chunk)
             for chunk in iter(lambda: file.file.read(10000), b'')]
        shutil.move(file.filename, upload_path)
        return Res({'fileName': file.filename}).successRes()
    except Exception as error:
        print('POST /upload Error', error)
        return Res(500).errorRes()

# TO UPLOAD MULTIPLE FILES :


@router.post('/multi/uploads')
async def storeFiles(files: List[UploadFile] = File(...)):
    print('POST : /multipleFiles')
    try:
        for file in files:
            with open(file.filename, 'wb') as f:
                [f.write(chunk)
                 for chunk in iter(lambda: file.file.read(10000), b'')]
            shutil.move(file.filename, upload_path)
        return {'filenames': [file.filename for file in files]}
    except Exception as error:
        print('POST /multi/uploads Error', error)
        return Res(500).errorRes()
