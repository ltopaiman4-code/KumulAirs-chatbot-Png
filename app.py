from flask import Flask, request, jsonify
import os

app = Flask(__name__)

CUSTOMER_SERVICE = "180 3444"

@app.route('/')
def home():
    return "KumulAirs Chatbot PNG - Live! 🇵🇬✈️"

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').lower()
    
    if any(word in user_msg for word in ['gude', 'hello', 'hi']):
        reply = f"Gude! Mi KumulAirs AI Chatbot 🇵🇬✈️ Mi ken helpim yu lo flights na bookings. Ringim {CUSTOMER_SERVICE} sapos yu nidim man."
    elif 'book' in user_msg or 'flight' in user_msg:
        reply = f"Lo bukim flight, ringim KumulAirs Customer Service lo {CUSTOMER_SERVICE} 24/7. Yu redi lo helpim yu!"
    elif 'baggage' in user_msg or 'bag' in user_msg:
        reply = f"Lo baggage questions, ringim {CUSTOMER_SERVICE}. Ol bai helpim yu lo weight na fees."
    else:
        reply = f"Mi no clear tumas. Yu ken ringim KumulAirs Customer Service lo {CUSTOMER_SERVICE} lo help."
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
