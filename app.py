from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# KumulAirs / PNG Air Customer Service
CUSTOMER_SERVICE = "180 3444"  # PNG Air Call Centre

# 22 Province blo PNG
PROVINCES = [
    "Western", "Gulf", "Central", "NCD", "Milne Bay", "Oro", "Southern Highlands",
    "Hela", "Enga", "Western Highlands", "Jiwaka", "Chimbu", "Eastern Highlands", 
    "Morobe", "Madang", "East Sepik", "West Sepik", "Manus", "New Ireland", 
    "East New Britain", "West New Britain", "Bougainville"
]

# PX Main Routes
PX_ROUTES = ["POM-LAE", "POM-MDG", "POM-RAB", "POM-HGU", "POM-BUA", "POM-KVG", 
             "LAE-POM", "MDG-POM", "RAB-POM", "HGU-POM"]

# Detect language: Tok Pisin or English
def detect_tokpisin(text):
    tokpisin_words = ['yu', 'mi', 'ol', 'blo', 'wantaim', 'laik', 'ken', 'inap', 
                      'plis', 'sori', 'gutpela', 'nogut', 'wanem', 'we', 'haus', 
                      'bukim', 'praiss', 'apinun', 'monin', 'na']
    text_lower = text.lower()
    return any(word in text_lower.split() for word in tokpisin_words)

# Main Q&A Logic
def get_reply(msg):
    msg_lower = msg.lower()
    is_tokpisin = detect_tokpisin(msg)
    
    # 1. Angry customer handling
    angry_words = ['stupid', 'useless', 'nogut', 'kros', 'angry', 'bagarap', 'fuck', 'shit']
    if any(word in msg_lower for word in angry_words):
        if is_tokpisin:
            return f"Sori tru CEO. Mi AI assistant tasol. Plis kolim PNG Air Customer Service lo {CUSTOMER_SERVICE} na ol bai helpim yu kwiktaim."
        else:
            return f"I am sorry. I am an AI assistant only. Please call PNG Air Customer Service on {CUSTOMER_SERVICE} for immediate help."
    
    # 2. Greeting
    if any(word in msg_lower for word in ['hello', 'hi', 'apinun', 'monin', 'gude']):
        if is_tokpisin:
            return "Mi, PNG Air, traveling assistant blo yu. Inap me helpim yu? Yu laik bukim flight, checkim praiss, o save lo rule blo baggage?"
        else:
            return "I am PNG Air, your travel assistant. How can I help you? Do you want to book a flight, check prices, or know baggage rules?"
    
    # 3. Booking
    if any(word in msg_lower for word in ['bukim', 'book', 'flight', 'ticket']):
        if is_tokpisin:
            return "Gutpela! Yu laik go we? Yumi flai go lo olgeta 22 province: POM, LAE, RAB, MDG, HGU na planti moa. Tokim mi province yu laik go lo em."
        else:
            return "Great! Where would you like to go? We fly to all 22 provinces: POM, LAE, RAB, MDG, HGU and more. Tell me your destination province."
    
    # 4. Price
    if any(word in msg_lower for word in ['price', 'praiss', 'hau mas', 'how much', 'cost']):
        if is_tokpisin:
            return f"Praiss em depend lo we yu go na wanem taim. Kolim {CUSTOMER_SERVICE} blo stret praiss nau. Tasol yumi gat flight POM-LAE, POM-RAB, POM-MDG everyday."
        else:
            return f"Prices depend on destination and date. Call {CUSTOMER_SERVICE} for exact prices now. But we have flights POM-LAE, POM-RAB, POM-MDG daily."
    
    # 5. Baggage Rules
    if any(word in msg_lower for word in ['baggage', 'bag', 'kago', 'kg', 'weight', 'rule']):
        if is_tokpisin:
            return "Rule blo kago: Economy 16kg free, Business 30kg free. Hand carry 7kg tasol. Sapos i winim, yu baim extra. Kolim {CUSTOMER_SERVICE} sapos yu no klia."
        else:
            return "Baggage rule: Economy 16kg free, Business 30kg free. Hand carry 7kg only. Excess baggage charges apply. Call {CUSTOMER_SERVICE} if unclear."
    
    # 6. Province check
    for prov in PROVINCES:
        if prov.lower() in msg_lower:
            if is_tokpisin:
                return f"Yes, yumi flai go lo {prov}. Yu laik bukim flight nau o yu laik save lo praiss pastaim? Kolim {CUSTOMER_SERVICE} blo bukim kwiktaim."
            else:
                return f"Yes, we fly to {prov}. Do you want to book a flight now or check the price first? Call {CUSTOMER_SERVICE} to book quickly."
    
    # 7. Route check
    for route in PX_ROUTES:
        if route.lower() in msg_lower or route.replace("-", " ").lower() in msg_lower:
            if is_tokpisin:
                return f"Yes, yumi gat flight {route} everyday. Yu laik bukim? Kolim {CUSTOMER_SERVICE} nau."
            else:
                return f"Yes, we have {route} flights daily. Do you want to book? Call {CUSTOMER_SERVICE} now."
    
    # 8. Default - PNG Air only
    if is_tokpisin:
        return f"Mi save helpim yu lo PNG Air flight tasol. Yu laik bukim flight, checkim praiss, o save lo rule? Sapos yu gat wari, kolim {CUSTOMER_SERVICE}."
    else:
        return f"I can only help you with PNG Air flights. Do you want to book a flight, check prices, or know rules? If you have concerns, call {CUSTOMER_SERVICE}."

@app.route('/')
def home():
    return "PNG Air Chatbot API - Tok Pisin + English | By Liam Topaiman CEO"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_msg = data.get('message', '')
    reply = get_reply(user_msg)
    
    return jsonify({
        "reply": reply,
        "language": "tokpisin" if detect_tokpisin(user_msg) else "english",
        "airline": "PNG Air"
    })

if __name__ == '__main__':
    app.run(debug=True)
