import os
from flask import Flask, request, jsonify, render_template, render_template_string
import whisper

app = Flask(__name__)
model = whisper.load_model("small")#base
#base	~74 MB	🟡 Decente	🟢 Rápida	1-2 GB
#small	~244 MB	🟢 Buena	🟡 Rápida	2-3 GB


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''

<!doctype html>
<title>Transcriptor de voz de Discord</title>
<h1>Sube un mensaje de voz (.ogg, .mp3, .wav)</h1>

<form method=post enctype=multipart/form-data>
    <input type=file name=audio>
    <br><br>
    <label for=language>Selecciona el idioma:</label>
    <select name=language>
        <option value="es">Español</option>
        <option value="en">Inglés</option>
        <option value="fr">Francés</option>
        <option value="pt">Portugués</option>
        <option value="auto">Detectar automáticamente</option>
    </select>
    <br><br>
    <input type=submit value=Transcribir>
</form>

{% if transcription %}
    <h2>Transcripción:</h2>
    <pre>{{transcription}}</pre>
{% endif %}

'''

@app.route("/", methods=["GET", "POST"])
def transcribe():
    transcription = None
    if request.method == "POST":
        file = request.files["audio"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        #conversion para los archivos .ogg (como pro ejemplo los audios al descargarlos de whatsapp)
        if filepath.endswith(".ogg"):
            wav_path = filepath.replace(".ogg", ".wav")
            os.system(f"ffmpeg -y -i {filepath} {wav_path}")
            filepath = wav_path
            
        #result = model.transcribe(filepath) 
        # ESTO PARA QUE TRANSCRIBA EL ARHCIVO DE LA RUTA SELECCIONADA - pero como vamos a añadirle idioma a la transcripcion, habra q hacerlo mas abajo selgun la eleccion del usuario
        
        #leer el idioma seleccionado por el usuario en el select :)
        selected_lang = request.form.get("language", "auto")
        if selected_lang == "auto":
            result = model.transcribe(filepath)
        else:
            result = model.transcribe(filepath, language=selected_lang) # <-- esta es la linea con lo del idioma añadido
        
        transcription = result["text"]
    
    return render_template_string(HTML, transcription=transcription)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")