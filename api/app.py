from flask import Flask, request, jsonify, render_template, url_for
import os
import cohere
from vercel.wsgi import VercelWSGI

app = Flask(__name__, template_folder='../../templates', static_folder='../../static')

cohere_api_key = os.environ.get("COHERE_API_KEY")
co = cohere.Client(cohere_api_key) if cohere_api_key else None

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    if not co:
        return jsonify({"error": "COHERE_API_KEY tidak dikonfigurasi sebagai environment variable di Vercel."}, 500)

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Payload JSON harus berisi kunci 'message'."}), 400

    message = data["message"]
    try:
        response = co.generate(
            prompt=message,
            max_tokens=50,  # Sesuaikan sesuai kebutuhan
            model="command-r-plus" # Sesuaikan model jika perlu
        )
        reply = response.generations[0].text
        return jsonify({"reply": reply})
    except cohere.error.CohereAPIError as e:
        return jsonify({"error": f"Error dari Cohere API: {str(e)}"}), 500

vercel_app = VercelWSGI(app)

if __name__ == "__main__":
    app.run(debug=True)
