
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Configuration sécurisée
openai.api_key = os.getenv("OPENAI_API_KEY")

class WhatsAppMessage(BaseModel):
    Body: str
    From: str

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    user_input = message.Body
    user_number = message.From

    print(f"Message reçu de {user_number}: {user_input}")

    # Si la clé API est absente
    if not openai.api_key:
        print("Erreur : Clé OpenAI manquante.")
        return {"reply": "Clé API OpenAI absente. Vérifiez la configuration du serveur."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant intelligent qui aide à réserver hôtels et restaurants au Maroc."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message["content"]
        print(f"Réponse IA : {reply}")
        return {"reply": reply}

    except Exception as e:
        print("Erreur OpenAI :", str(e))
        return {"reply": "Désolé, une erreur est survenue avec le service d'IA. Réessayez plus tard."}
