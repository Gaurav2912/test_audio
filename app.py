import os

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    file = request.files['music-file']
    file_path = os.path.join('static', file.filename)
    file.save(file_path)
    return {'filename': file.filename}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)