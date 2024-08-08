from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
import os
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        # Load the WAV file
        audio = AudioSegment.from_wav(filepath)
        
        # You can perform operations on the audio here if needed
        # For example, let's trim the first 5 seconds:
        # audio = audio[:5000]
        
        # Convert to WAV format
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        buffer.seek(0)
        
        return send_file(buffer, mimetype="audio/wav", as_attachment=True, download_name=filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)