from flask import Flask, render_template, request, jsonify
import os
import pygame

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pygame.mixer.init()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.wav'):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template('player.html', filename=filename)
    return render_template('upload.html')

@app.route('/play/<filename>')
def play_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        return jsonify({"status": "playing"})
    return jsonify({"status": "file not found"})

@app.route('/stop')
def stop_file():
    pygame.mixer.music.stop()
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(debug=True)