from flask import Flask, jsonify

app = Flask(__name__)

def add(a, b):
    return a + b

@app.route('/')
def home():
    return jsonify({"message": "Hello from Exercise-2! test ", "status": "ok"})

@app.route('/add/<int:a>/<int:b>')
def add_route(a, b):
    return jsonify({"result": add(a, b)})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)