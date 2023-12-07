from fastapi import status
from pydantic import BaseModel, validator


class ResponseModel(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = 'success'
    data: dict | list | str | None = None


class ChatValidator(BaseModel):
    msg: str

    @validator('msg')
    def validate_msg(cls, v):
        if not v:
            raise ValueError('msg is required')
        return v
