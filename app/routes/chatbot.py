from fastapi import APIRouter
from app.services.chatbot_service import ChatbotService

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

chatbot_service = ChatbotService()

@router.post("/chat")
def get_chatbot_response(message: dict):
    return chatbot_service.handle_message(message.get("message", ""))
