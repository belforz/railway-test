from app.models.interaction import InteractionModel
from datetime import datetime, UTC

class ChatbotService:
    def handle_message(self, message: str) -> InteractionModel:
        return InteractionModel(
            message=message,
            response="Mock de sucesso: " + message,
            timestamp=datetime.now(UTC)
        )
