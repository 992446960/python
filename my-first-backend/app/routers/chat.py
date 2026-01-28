from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.services.chat import chat_stream

router = APIRouter(prefix="/chat", tags=["聊天"])


@router.post(
    "",
    summary="聊天接口（SSE流式）",
    description="POST /chat SSE流式响应，支持多种事件类型"
)
async def chat(request: ChatRequest):
    """
    聊天接口，使用 Server-Sent Events (SSE) 进行流式响应
    
    :param request: 聊天请求参数
    :return: SSE 流式响应
    """
    return StreamingResponse(
        chat_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )