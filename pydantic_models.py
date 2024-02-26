from pydantic import BaseModel
from typing import Union, Optional

class AddAfterModel(BaseModel):
    after_message_id: str
    content: str

class AddBeforeModel(BaseModel):
    before_message_id: str
    content: str

class ModifyModel(BaseModel):
    message_id: str
    content: str

class JsonResponseModel(BaseModel):
    delete: Optional[list[str]] = None
    modify: Optional[list[ModifyModel]] = None
    add: Optional[Union[AddAfterModel, AddBeforeModel]] = None
    anonymize: list[str]
    formatting: dict[str, str]

