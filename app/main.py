
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Lire la clé OpenAI de la variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

class WhatsAppMessage(BaseModel):
    Body: str
    From: str

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    user_input = message.Body
    user_number = message.From

    print(f"Message reçu de {user_number}: {user_input}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant de réservation intelligent pour hôtels et restaurants."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message["content"]
        print(f"Réponse générée : {reply}")
        return {"reply": reply}

    except Exception as e:
        print("Erreur OpenAI :", str(e))
        return {"reply": "Désolé, une erreur est survenue. Réessayez plus tard."}
