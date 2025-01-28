import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import assemblyai as aai
import google.generativeai as genai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
Bootstrap(app)

# Configuración de directorios y archivos permitidos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'mp4', 'aac', 'mpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB límite

# Configuración de Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno")

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-exp-1206",
    generation_config=generation_config
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_summary(text):
    try:
        prompt = """Como experto en análisis de contenido, analiza el siguiente texto transcrito y genera un resumen estructurado siguiendo estas instrucciones:

[INSTRUCCIONES]
1. Identifica y lista 5-10 temas principales discutidos en el texto
2. Para cada tema, incluye:
   - Breve explicación del tema
   - Citas textuales relevantes con identificación del hablante
   - Puntos clave y conclusiones

[FORMATO DE SALIDA]
# Síntesis 📑

## Temas principales 🎯
1. [Tema 1
2. [Tema 2]
...

## Análisis detallado 📋

### 1. [Tema 1]
- **Contexto**: [breve explicación]
- **Citas destacadas**:
  > "[cita textual]" - [Hablante]
- **Puntos clave**:
  - [punto 1]
  - [punto 2]

[continuar con el resto de temas]

Texto a analizar:
{text}
"""
        response = model.generate_content(prompt.format(text=text))
        return response.text
    except Exception as e:
        print(f"Error al generar el resumen: {str(e)}")
        return None

def generate_sentiment_analysis(text):
    try:
        prompt = """Como experto en análisis de sentimientos, examina el siguiente texto transcrito y proporciona un análisis detallado siguiendo estas instrucciones:

[INSTRUCCIONES]
1. Identifica el tono general y la atmósfera de la conversación
2. Detecta las emociones predominantes y sus variaciones
3. Analiza el lenguaje utilizado y su impacto emocional
4. Identifica momentos clave que revelan sentimientos significativos

[FORMATO DE SALIDA]
# Foco emocional del audio 🥰

## Tono 🌟
[Descripción del tono predominante y cómo evoluciona]

## Emociones Detectadas 💫
- Emoción 1: [descripción y ejemplos]
- Emoción 2: [descripción y ejemplos]
...

## Lenguaje y expresiones 🗣️
- Patrones de lenguaje observados
- Palabras y frases clave
- Impacto emocional del lenguaje usado

## Momentos clave 🔑
1. [Momento/frase específica y su significado emocional]
2. [Otro momento significativo]
...

## Conclusión 📊
[Resumen del análisis emocional general]

Texto a analizar:
{text}
"""
        response = model.generate_content(prompt.format(text=text))
        return response.text
    except Exception as e:
        print(f"Error al generar el análisis de sentimiento: {str(e)}")
        return None

@app.route('/generate_summary', methods=['POST'])
def summary_endpoint():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No se proporcionó texto para resumir'}), 400

        summary = generate_summary(text)
        if summary:
            return jsonify({'summary': summary})
        else:
            return jsonify({'error': 'Error al generar el resumen'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_sentiment', methods=['POST'])
def sentiment_endpoint():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No se proporcionó texto para analizar'}), 400

        sentiment = generate_sentiment_analysis(text)
        if sentiment:
            return jsonify({'sentiment': sentiment})
        else:
            return jsonify({'error': 'Error al generar el análisis de sentimiento'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = None
    error = None
    summary = None
    sentiment = None

    if request.method == 'POST':
        if 'audio_file' not in request.files:
            error = 'No se seleccionó ningún archivo'
            return render_template('index.html', error=error)

        file = request.files['audio_file']
        if file.filename == '':
            error = 'No se seleccionó ningún archivo'
            return render_template('index.html', error=error)

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Configurar API key de AssemblyAI
                aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

                # Transcribir el audio
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(
                    filepath,
                    config=aai.TranscriptionConfig(
                        language_code="es",
                        punctuate=True,
                        format_text=True,
                        speaker_labels=True
                    )
                )

                if transcript.status == aai.TranscriptStatus.error:
                    error = f"Error en la transcripción: {transcript.error}"
                    transcript = None
                elif transcript.status == aai.TranscriptStatus.completed:
                    formatted_text = []
                    current_speaker = None

                    for utterance in transcript.utterances:
                        if utterance.speaker != current_speaker:
                            current_speaker = utterance.speaker
                            formatted_text.append(f"Hablante {current_speaker}")
                        formatted_text.append(utterance.text)

                    raw_transcript = "\n".join(formatted_text)

                    if not raw_transcript or len(raw_transcript.strip()) == 0:
                        error = "La transcripción está vacía"
                        transcript = None
                    else:
                        # Optimizar la transcripción con Gemini
                        try:
                            prompt = """Como experto en procesamiento de texto, optimiza la siguiente transcripción:
1. Mantén EXACTAMENTE las mismas palabras y su orden
2. Corrige y optimiza los signos de puntuación
3. Asegúrate que los nombres propios estén correctamente capitalizados
4. Asegúrate que las siglas estén en mayúsculas (ej: CGT, OEA, ONU, AFIP, ARCA, etc.)
5. Usa formato numérico en español, separando cifras de miles con punto y no con coma (ej: 1.000.000: un millón; 1.000: mil, 100.000 cien mil; etc.)

Texto a optimizar:
{text}

Formato de respuesta:
[Texto transcripto]"""

                            response = model.generate_content(prompt.format(text=raw_transcript))
                            transcript = response.text if response.text else raw_transcript
                            summary = generate_summary(transcript)
                        except Exception as e:
                            print(f"Error al optimizar la transcripción: {str(e)}")
                            transcript = raw_transcript
                            summary = generate_summary(transcript)
                else:
                    error = f"Estado inesperado de la transcripción: {transcript.status}"
                    transcript = None

                # Limpiar el archivo después de la transcripción
                os.remove(filepath)

            except Exception as e:
                error = f"Error inesperado: {str(e)}"
                print(f"Error detallado: {error}")
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            error = 'Formato de archivo no permitido'

    return render_template('index.html', transcript=transcript, error=error, summary=summary, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=False)
