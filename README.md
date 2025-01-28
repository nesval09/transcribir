# 🎙️ Transcriptor y analizador de audios con IA

Esta aplicación web permite transcribir archivos de audio y generar resúmenes inteligentes utilizando AssemblyAI para la transcripción y Google Gemini para el análisis del contenido.

## ✨ Características

- Transcripción de audio a texto en español
- Identificación automática de hablantes
- Generación de resúmenes estructurados
- Análisis de sentimientos del contenido
- Soporte para múltiples formatos de audio
- Interfaz web responsiva y fácil de usar

## 🛠️ Tecnologías Utilizadas

- Python 3.x
- Flask
- AssemblyAI API
- Google Gemini AI
- Bootstrap
- HTML/CSS

## 📋 Requisitos Previos

- Python 3.x instalado
- Cuenta en AssemblyAI (para obtener API key)
- Cuenta en Google AI Studio (para obtener API key de Gemini)
- pip (gestor de paquetes de Python)

## 🚀 Instalación Local

1. Clonar el repositorio:
```bash
https://github.com/nesval09/transcribir.git
cd transcribir
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
```
Editar el archivo `.env` y agregar tus API keys:
- ASSEMBLYAI_API_KEY: Tu API key de AssemblyAI
- GEMINI_API_KEY: Tu API key de Google Gemini

5. Ejecutar la aplicación:
```bash
python transcribir.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📦 Deploy en PythonAnywhere

1. Crear una cuenta en [PythonAnywhere](https://www.pythonanywhere.com/)

2. En la consola de PythonAnywhere:
```bash
git clone https://github.com/nesval09/transcribir.git
cd transcribir
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configurar variables de entorno:
- Ir a la pestaña "Web"
- En la sección "Environment variables", agregar:
  - ASSEMBLYAI_API_KEY
  - GEMINI_API_KEY

4. Configurar la aplicación web:
- Source code: /home/tu-usuario/transcribir
- Working directory: /home/tu-usuario/transcribir
- WSGI configuration file: Modificar para importar la aplicación Flask

5. Reiniciar la aplicación web

## 📁 Formatos de Audio Soportados

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- MP4 (.mp4)
- AAC (.aac)
- MPEG (.mpeg)

## ⚠️ Limitaciones

- Tamaño máximo de archivo: 100MB
- El archivo debe tener audio claro y comprensible
- La transcripción funciona mejor con español neutro

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz Fork del proyecto
2. Crea una rama para tu característica
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
