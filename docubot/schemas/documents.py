from pydantic import utils, root_validator

from .core import CoreModel, IDModelMixin, DateTimeModelMixin
from .tag import TagResponse
from docubot.services.cloudinary import formatting_document_url


class DocumentBase(CoreModel):
    """
    Leaving salt from base model
    """
    url: str
    description: str
    tags: list[TagResponse]
    user_id: int


    @root_validator(pre=True)
    def update_model(cls, values: utils.GetterDict):
        if 'url' not in values.keys():
            values._obj.url = cls.format_url(values._obj.public_id)  # noqa
        return values

    @staticmethod
    def format_url(public_id: str):
        return formatting_document_url(public_id)['url']


class DocumentPublic(DateTimeModelMixin, DocumentBase, IDModelMixin):
    class Config:
        orm_mode = True


class DocumentCreateResponse(CoreModel):
    document: DocumentPublic
    message: str = "Document successfully uploaded"


class DocumentRemoveResponse(CoreModel):
    message: str = "Document successfully deleted"