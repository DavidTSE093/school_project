from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask!"

@app.route('/generate_qrcode')
def generate_qrcode_route():
    return "QR Code generation route!"

if __name__ == '__main__':
    app.run(debug=True)
