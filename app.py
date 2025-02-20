from flask import Flask
from app.routes.embedding_route import pdf_blueprint
from app.routes.ask_route import ask_blueprint

app = Flask(__name__)
app.config['DEBUG'] = True # Deployment에서는 False로 변경!

@app.route("/")
def hello():
    return "Hello, Flask!"

app.register_blueprint(pdf_blueprint, url_prefix='/ai/pdf')
app.register_blueprint(ask_blueprint, url_prefix='/ai/ask')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)