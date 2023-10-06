import asyncio
import mimetypes
from typing import Optional, Any, List

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query, Body
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from docubot.database.connect import get_db
from docubot.database.models import User, UserRole
from docubot.repository import documents as repository_documents, tags as repository_tags
from docubot.schemas.documents import DocumentCreateResponse, DocumentPublic, DocumentRemoveResponse
from docubot.services import cloudinary
from docubot.services.auth import get_current_active_user
import uuid
import os
import aiofiles
from fastapi.responses import FileResponse

from docubot.services.pdf_to_vectorstore import pdf_to_vectorstore

router = APIRouter(prefix="/documents", tags=["Documents"])

allowed_content_types_upload = [
    ".pdf",
]


@router.post(
    "/",
    response_model=DocumentCreateResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def upload_document(
        file: UploadFile = File(), 
        description: str = Form(min_length=10, max_length=1200),
        tags: Optional[list[str]] = Form(None),
        # tags = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
) -> Any:  
    """
    The upload_document function is used to upload a document file to the vector DB server.
    The function takes in a file, description and tags as parameters. The file parameter is of type UploadFile which
    is a FastAPI class that represents uploaded files. The description parameter is of type str and has minimum length
    of 10 characters and maximum length of 1200 characters while the tags parameter is optional with each tag having
    minimum length 3 characters and maximum 50 characters.

    :param file: UploadFile: Receive the document file from the client
    :param description: str: Get the description of the document from the request body
    :param tags: Optional[list[str]]: Validate the tag list
    :param db: Session: Get the database session
    :param current_user: User: Get the current user that is logged in
    :param : Get the document id from the url
    :return: A dictionary with the document and detail keys
    """
    # try:
    #     tags = {tag.strip() for tag in tags.split(',')}
    # except:
    #     ...
    
    if mimetypes.guess_extension(file.content_type,) not in allowed_content_types_upload:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Invalid file type. Only allowed {allowed_content_types_upload}.")
    
    tags = repository_tags.get_list_tags(tags)

    if tags and len(tags) > 5:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Maximum five tags can be added")

    if tags:
        print(tags)
        for tag in tags:
            if not 3 <= len(tag) <= 50:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail=f'Invalid length tag: {tag}')

    count_documents = await repository_documents.count_documents_by_user_id(current_user.id, db)
    if count_documents >= 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Maximum five documents can be added")


    # loop = asyncio.get_event_loop()
    # document = await loop.run_in_executor(
    #     None,
    #     cloudinary.upload_document,
    #     file.file
    # )
    #
    # if document is None:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document file")

    documentPublicId = str(uuid.uuid4())

    storageDir = os.path.abspath(os.path.dirname(__file__) + "/../../storage")

    documentFilename = storageDir + "/" + documentPublicId + ".pdf"

    async with aiofiles.open(documentFilename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    await pdf_to_vectorstore(documentFilename)

    document = await repository_documents.create_document(
        current_user.id,
        description.strip(),
        tags,
        documentPublicId,
        db
    )

    return {
        "document": document,
        "message": "Document successfully uploaded"
    }


@router.get(
    "/",
    response_model=list[DocumentPublic],
    description="Get all documents",
)
#dependencies=[Depends(RateLimiter(times=30, seconds=60))]
async def get_documents(
        skip: int = 0,
        limit: int = Query(default=10, ge=1, le=100),
        description: Optional[str] = Query(default=None, min_length=3, max_length=1200),
        tags: Optional[list[str]] = Query(default=None, max_length=50),
        document_id: Optional[int] = Query(default=None, ge=1),
        sort_by: Optional[repository_documents.SortMode] = repository_documents.SortMode.NOT_SORT,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    return await repository_documents.get_documents(
        skip,
        limit,
        description,
        tags,
        document_id,
        current_user.id,
        sort_by,
        db
    )

@router.get("/{document_id}", response_model=DocumentPublic)
async def get_document(
        document_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    document = await repository_documents.get_document_by_id(document_id, db)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    return document

@router.get("/content/{document_id}")
async def get_document(
        document_id: int,
        db: Session = Depends(get_db),
) -> Any:

    document = await repository_documents.get_document_by_id(document_id, db)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    storageDir = os.path.abspath(os.path.dirname(__file__) + "/../../storage")
    documentFilename = storageDir + "/" + document.public_id + ".pdf"

    return FileResponse(documentFilename, filename="document.pdf")

@router.patch("/", response_model=DocumentPublic, )# dependencies=[Depends(RateLimiter(times=10, seconds=60))]
async def update_document_data(
        document_id: int = Body(ge=1),
        description: str = Body(min_length=10, max_length=1200),
        tags: Optional[list[str]] = Body(None, min_length=3, max_length=50),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    if tags and len(tags) > 5:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Maximum five tags can be added")

    document = await repository_documents.get_document_by_id(document_id, db)

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    if not (current_user.role == UserRole.admin or document.user_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    updated_document = await repository_documents.update_description(document_id, description, tags, db)

    return updated_document


@router.delete("/{document_id}", response_model=DocumentRemoveResponse,
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_document(
        document_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    document = await repository_documents.get_document_by_id(document_id, db)

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, cloudinary.remove_document, document.public_id)
    await repository_documents.delete_document(document, db)

    return {"message": "Document successfully deleted"}


@router.get("/search/", response_model=List[DocumentPublic],
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_documents(
        data: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_active_user)
) -> Any:

    documents = await repository_documents.search_documents(data, db)
    if not documents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return documents
