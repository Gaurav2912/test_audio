from flask import Flask, render_template, request
import os

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
    app.run(debug=True)