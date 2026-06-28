
from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

CUSTOMER_SERVICE = "180 3444"
WHATSAPP_NUMBER = "+675 7850 0000"

PROVINCES = [
    "Western", "Gulf", "Central", "NCD", "Milne Bay", "Oro", 
    "Southern Highlands", "Hela", "Enga", "Western Highlands", "Jiwaka", 
    "Chimbu", "Eastern Highlands", "Morobe", "Madang", "East Sepik", "West Sepik", 
    "Manus", "New Ireland", "East New Britain", "West New Britain", "Bougainville"
]

PX_ROUTES = ["POM-LAE", "POM-MDG", "POM-RAB", "POM-HKN", "POM-KVG", "POM-MAS", 
             "LAE-POM", "MDG-POM", "RAB-POM", "HKN-POM", "KVG-POM", "MAS-POM"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kumul Air - PNG Air AI Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #CE1126 0%, #000000 50%, #FFD100 100%);
            margin: 0; padding: 20px; min-height: 100vh;
        }
      .chat-container { 
            max-width: 600px; margin: 0 auto; background: white; 
            border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
      .header { 
            background: #CE1126; color: white; padding: 20px; 
            border-radius: 15px 15px 0 0; text-align: center;
        }
      .header h1 { margin: 0; font-size: 24px; }
      .header p { margin: 5px 0 0 0; opacity: 0.9; }
      .chat-box { height: 400px; overflow-y: auto; padding: 20px; }
      .message { margin: 10px 0; padding: 12px; border-radius: 10px; max-width: 80%; }
      .user { background: #FFD100; margin-left: auto; text-align: right; }
      .bot { background: #f0f0f0; }
      .input-area { padding: 20px; border-top: 2px solid #CE1126; display: flex; }
        input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 25px; }
        button { 
            background: #CE1126; color: white; border: none; 
            padding: 12px 25px; border-radius: 25px; margin-left: 10px; cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>✈️ KUMUL AIR 🇵🇬</h1>
            <p>PNG Air AI Assistant | Customer Service: 180 3444</p>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">
                Gude! Mi Kumul Air AI Assistant blo PNG Air ✈️🇵🇬<br><br>
                Mi ken helpim yu lo:<br>
                - Bookim flight blo PNG Air<br>
                - Checkim flight schedule POM-LAE, POM-MDG, etc<br>
                - Cargo & Freight lo 22 Province<br>
                - Customer service 180 3444<br><br>
                Yu laik go we?
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Askim mi lo Tok Pisin or English..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const message = input.value.trim();
            if (!message) return;
            
            chatBox.innerHTML += `<div class="message user">${message}</div>`;
            input.value = '';
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
          .then(res => res.json())
          .then(data => {
                chatBox.innerHTML += `<div class="message bot">${data.response}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').lower()
    
    if any(word in user_msg for word in ['gude', 'hello', 'hi', 'apinun']):
        return jsonify({"response": f"Gude! Mi Kumul Air AI Assistant 🇵🇬✈️<br><br>Mi ken helpim yu lo PNG Air flights, cargo, na customer service 180 3444.<br><br>Yu laik go we lo PNG?"})
    
    if 'book' in user_msg or 'flight' in user_msg or 'balus' in user_msg:
        return jsonify({"response": f"Yes! Mi ken helpim yu bookim PNG Air flight ✈️<br><br><b>PNG Air Routes:</b><br>• POM to LAE, MDG, RAB, HKN<br>• LAE to POM, MDG<br>• MDG to POM, LAE<br><br><b>Bookim nau:</b><br>📞 Call: {CUSTOMER_SERVICE}<br>📱 WhatsApp: {WHATSAPP_NUMBER}<br><br>Yu laik go lo wanem province?"})
    
    if any(route in user_msg.upper() for route in ['POM', 'LAE', 'MDG', 'RAB']) or 'schedule' in user_msg:
        return jsonify({"response": f"PNG Air Schedule ✈️<br><br><b>Popular Routes:</b><br>• POM ↔ LAE - Daily flights<br>• POM ↔ MDG - Mon/Wed/Fri<br>• POM ↔ RAB - Tue/Thu/Sat<br>• POM ↔ HKN - Daily<br><br><b>Checkim availability:</b><br>📞 Call: {CUSTOMER_SERVICE}<br><br>Yu laik checkim wanem route?"})
    
    if 'cargo' in user_msg or 'freight' in user_msg or 'kago' in user_msg:
        return jsonify({"response": f"PNG Air Cargo Service 📦<br><br>Mi ken helpim yu sendim kago lo ol 22 Province:<br><br>• Highlands: Hagen, Goroka, Mendi<br>• Momase: Lae, Madang, Wewak<br>• Islands: Rabaul, Kavieng, Manus<br>• Southern: POM, Daru, Kerema<br><br><b>Cargo Hotline:</b> {CUSTOMER_SERVICE}<br><br>Yu laik sendim kago go we?"})
    
    if 'help' in user_msg or 'service' in user_msg or 'contact' in user_msg or '180' in user_msg:
        return jsonify({"response": f"PNG Air Customer Service 📞<br><br><b>24/7 Hotline:</b> {CUSTOMER_SERVICE}<br><b>WhatsApp:</b> {WHATSAPP_NUMBER}<br><b>Email:</b> info@pngair.com.pg<br><br><b>Head Office:</b><br>Jacksons International Airport<br>Port Moresby, NCD<br><br>Mi stap here 24/7 lo helpim yu! 🇵🇬"})
    
    return jsonify({"response": f"Mi Kumul Air AI blo PNG Air ✈️🇵🇬<br><br>Mi ken helpim yu lo:<br>• Flight booking<br>• Schedule blo balus<br>• Cargo lo 22 Province<br>• Customer service<br><br>Ringim {CUSTOMER_SERVICE} lo help o askim mi gen!<br><br>Yu laik save lo wanem?"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    @app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    if 'gude' in user_message or 'hello' in user_message:
        reply = f"Gude gen! Mi Kumul Air AI. Yu laik bookim flight go we? Ringim {CUSTOMER_SERVICE} o tokim mi route."
    elif 'book' in user_message or 'flight' in user_message:
        reply = f"OK! Lo bookim PNG Air flight, ringim Customer Service {CUSTOMER_SERVICE} nau. Ol i save lo olgeta PX routes: POM-LAE, POM-MDG, POM-HGU. Yu laik go we?"
    elif 'cargo' in user_message or 'freight' in user_message:
        reply = f"Mi ken helpim lo cargo! PNG Air i karim freight go lo 22 Province. Ringim {CUSTOMER_SERVICE} lo quote. Yu laik salim cargo go we?"
    elif 'help' in user_message or 'customer' in user_message:
        reply = f"PNG Air Customer Service: {CUSTOMER_SERVICE} 📞 Ol i op 24/7. Ol i ken helpim yu lo booking, schedule, cargo. Wanem problem blo yu?"
    else:
        reply = f"Sori, mi no klia tumas. Askim mi lo: book flight, cargo, schedule. O ringim {CUSTOMER_SERVICE} lo helpim yu nau."
    
    return jsonify({"reply": reply})
    Add /chat route - fix repeat bug
