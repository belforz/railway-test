from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chatbot import router as chatbot_router

app = FastAPI(title="MiniBot API - Teste Limpo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)

@app.get("/")
def root():
    return {"message": "API funcionando perfeitamente!"}
