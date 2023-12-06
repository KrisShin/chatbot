from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/test")
async def test():
    return "success"

@router.post("/chat")
async def chat(request: Request):
    chat = request.json()