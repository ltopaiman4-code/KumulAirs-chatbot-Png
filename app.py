
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CUSTOMER_SERVICE = "180 3444"

@app.route('/')
def home():
    return "KumulAirs Chatbot PNG - Live! 🇵🇬✈️"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    if 'gude' in user_message or 'hello' in user_message or 'hi' in user_message:
        reply = f"Gude gen CEO! Mi KumulAirs Chatbot. Hau mi ken helpim yu tete? Call {CUSTOMER_SERVICE} sapos emergency."
    elif 'book' in user_message or 'bukim' in user_message or 'flight' in user_message:
        reply = f"Yu laik bukim flight a? Mi ken helpim yu checkim price na taim. Kolim {CUSTOMER_SERVICE} lo toktok wantaim agent nau."
    elif 'cargo' in user_message or 'freight' in user_message or 'kago' in user_message:
        reply = f"PNG Air Cargo ken helpim! Minimum charge K50. Kolim {CUSTOMER_SERVICE} lo quote."
    elif 'bag' in user_message or 'luggage' in user_message:
        reply = f"Economy: 16kg + 7kg hand carry. Business: 30kg + 7kg. Moa info? Kolim {CUSTOMER_SERVICE}"
    else:
        reply = f"Sori CEO, mi no clear gut. Askim lo flight, cargo, bag? O kolim {CUSTOMER_SERVICE} sapos urgent."
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
