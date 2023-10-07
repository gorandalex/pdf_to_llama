import os
from pathlib import Path
from typing import List

from fastapi import Request, APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query, Body

from docubot.schemas.vectorstore_schema import VectorstoreResponse

from sqlalchemy.orm import Session
from docubot.database.connect import get_db
from docubot.services import cloudinary
from docubot.services.auth import get_current_active_user
from docubot.database.models import User
from docubot.repository import vectorstores as repo_vectorstores

import cloudinary
import cloudinary.uploader

from docubot.services.pdf_to_vectorstore import pdf_to_vectorstore

router = APIRouter(prefix="/vectorstore", tags=["Vectorstore"])


@router.get('/', response_model=List[VectorstoreResponse])
async def get_vectorstores(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    vector_stores = await repo_vectorstores.get_all_vectorstores(db, current_user)
    if not vector_stores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing was found'
        )
    return vector_stores


@router.get('/{name}', response_model=VectorstoreResponse)
async def get_vectorstore_by_name(name: str,
                                  db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_active_user)):
    vector_store = await repo_vectorstores.get_vectorstore_by_name(name, db, current_user)
    if not vector_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing was found'
        )
    return vector_store


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    # try:
    file_name, extension = file.filename.split('.')
    if extension != 'pdf':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="підтримує тільки PDF")

    save_path = Path("uploaded_files") / file.filename

    save_path.parent.mkdir(parents=True, exist_ok=True)

    with save_path.open("wb") as buffer:
        buffer.write(await file.read())

    # Зберігаємо шлях до файлу у сесії
    request.session["current_path_document"] = str(save_path.absolute())
    return {"success": True, 'filename': file_name, 'path': str(save_path.absolute())}
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Помилка при завантаженні файлу: {e}")

@router.post('/')
async def upload_vectorstore(file: UploadFile = File()):
    # cloudinary.config(
    #     cloud_name=os.environ.get('CLOUDINARY_NAME'),
    #     api_key=os.environ.get('CLOUDINARY_API_KEY'),
    #     api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    #     secure=True
    # )
    # with open(file.file, 'rb') as f:
    #     print(f.read())
    print(f'file - {file}')
    print(f'file.file - {file.file._file}')
    print(f'file.read - {await file.file}')
    with open('D:\Programming\Projects_Go_It\DataScience_Command_Project\pdf_to_llama\pic.txt', 'wb') as f:
        f.write(await file.read())
        print(f.read())
    # vector_store = await pdf_to_vectorstore(file.__dict__)
    # print(vector_store)
    # public_name = file.filename.split(".")[0]
    # # cloudinary.
    # # file_name = public_name + "_" + str(current_user.username)
    # r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{public_name}', overwrite=True)
    # src_url = cloudinary.CloudinaryImage(f'PhotoShare/{public_name}') \
    #     .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    #
    # image, details = await images.add_image(db, body, correct_tags, src_url, correct_public_name, current_user)