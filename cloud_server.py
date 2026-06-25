import os
import stripe
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

# 🔴 SECURE API KEYS (Use Environment Variables in Production)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_stripe_key_here")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID", "your_twilio_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH", "your_twilio_auth")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ================= 1. AI CORE ENDPOINT =================
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    # Insert LLM/ChromaDB logic here
    reply = f"Pasha Cloud: I processed your command: '{user_message}'"
    return jsonify({"reply": reply})

# ================= 2. 2-WAY WHATSAPP INTEGRATION =================
@app.route('/api/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Receives messages from WhatsApp and replies."""
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    # Process via AI Engine
    ai_reply = f"Pasha AI: You said '{incoming_msg}'. How can I assist further?"

    # Send back to WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(ai_reply)
    return str(resp)

@app.route('/api/whatsapp/send', methods=['POST'])
def send_whatsapp_alert():
    """Allows Pasha to initiate a message to your phone."""
    data = request.json
    message = twilio_client.messages.create(
        body=data.get("message", "Pasha System Alert"),
        from_='whatsapp:+14155238886', # Your Twilio Sandbox number
        to=f'whatsapp:{data.get("target_number")}'
    )
    return jsonify({"status": "sent", "sid": message.sid})

# ================= 3. FINANCIAL TRANSACTIONS =================
@app.route('/api/transaction/stripe', methods=['POST'])
def process_payment():
    """Flawless software transaction processing."""
    data = request.json
    amount = data.get('amount', 1000) # Amount in cents ($10.00)
    
    try:
        # Create a PaymentIntent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={"enabled": True},
        )
        return jsonify({"clientSecret": intent.client_secret, "status": "Awaiting Confirmation"})
    except Exception as e:
        return jsonify({"error": str(e)}), 403

if __name__ == '__main__':
    # Must be hosted on a cloud provider (e.g., Render, Heroku, AWS)
    app.run(host='0.0.0.0', port=5000)