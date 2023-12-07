from uuid import uuid4
from fastapi import APIRouter, Request

from apps.pydantics import ChatValidator, ResponseModel
from common.chat_utils import ChatUtil
from common.global_variables import CHAT_MAPPING

router = APIRouter()


@router.get('/test')
async def test():
    return 'success'


@router.post('/chat')
async def chat():
    chat_id = uuid4().hex
    chat = ChatUtil.create_chat()
    CHAT_MAPPING[chat_id] = chat
    return ResponseModel(data={'chat_id': chat_id})


@router.post('/chat/{chat_id}')
async def chat(chat_id: str, message: ChatValidator):
    chat = CHAT_MAPPING.get(chat_id)
    if not chat:
        return ResponseModel(code=404, message='chat not found')
    stream = chat.chat(message.msg)
    answer = 'bot: '
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            msg = chunk.choices[0].delta.content or ''
            answer += msg
            print(msg, end='')
    chat.messages.append({'role': 'assistant', 'content': answer})
    return ResponseModel(data=answer)
