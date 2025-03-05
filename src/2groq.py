from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv('API_KEY')
client = Groq(api_key=GROQ_API_KEY)

@app.route('/generate', methods=['POST'])
def generate_greeting_metadata():
    user_input = request.json.get('user_input')
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that generates structured greeting card metadata based on a given festival greeting. Your response should include:\n"
                           "- Language of the greeting\n"
                           "- A suitable title for the greeting card\n"
                           "- Sender's name (if available, else 'Unknown')\n"
                           "- Recipient's name (if available, else 'Friends & Family')\n"
                           "- A suitable text color (hex code)\n"
                           "- An image theme for the background\n"
                           "- A suitable background color (hex code)"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=False,
    )

    response = chat_completion.choices[0].message.content
    metadata = {}
    for line in response.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            key = key.strip().lower().replace(' ', '_')
            metadata[key] = value.strip()

    return jsonify(metadata)

if __name__ == '__main__':
    app.run(debug=True)
