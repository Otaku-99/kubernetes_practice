from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("http://backend/hello")

    return f"""
    <html>
        <body>
            <h1>Frontend</h1>
            <p>Response from backend:</p>
            <h2>{response.json()["message"]}</h2>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)