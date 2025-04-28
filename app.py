from flask import Flask, request, jsonify, render_template
import cohere
import os

app = Flask(__name__)
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Pesan tidak ditemukan'}), 400

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=user_message,
            max_tokens=150,
            temperature=0.7,
            num_generations=1
        )
        bot_response = response.generations[0].text.strip()
        return jsonify({'response': bot_response})
    except cohere.error.CohereAPIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)