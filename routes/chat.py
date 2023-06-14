from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

router = APIRouter(prefix="/api", tags=["chat"])


@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    chain = ConversationChain(llm=ChatOpenAI(temperature=0))
    while True:
        try:
            msg = await websocket.receive_text()
            ans = chain.run(input=msg)
            await websocket.send(ans)
        except WebSocketDisconnect:
            break
