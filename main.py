
from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body")
    user_number = form.get("From")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es Askley, un assistant moderne, élégant et intelligent. Tu aides à réserver hôtels, restaurants et trouver les meilleurs deals."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = "Je rencontre une difficulté technique. Merci de réessayer plus tard."

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)
