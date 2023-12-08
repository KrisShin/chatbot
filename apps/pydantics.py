from fastapi import status
from pydantic import BaseModel, validator


class ResponseModel(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = 'success'
    data: dict | list | str | None = None


class ChatValidator(BaseModel):
    messages: list

    @validator('messages')
    def validate_msg(cls, msg_list):
        if not msg_list:
            raise ValueError('messages is required')
        return msg_list
