from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class WhatsAppMessage(BaseModel):
    Body: str
    From: str

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    user_input = message.Body

    # Appel OpenAI pour analyse de message
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant de réservation intelligent pour hôtels et restaurants."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message["content"]

    print(f"Message de {message.From} : {user_input}")
    print(f"Réponse générée : {reply}")

    return {"reply": reply}
