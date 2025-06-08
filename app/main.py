from fastapi import FastAPI
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant de réservation intelligent pour hôtels et restaurants."},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message["content"]
    return {"reply": reply}
