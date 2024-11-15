from odoo import api, fields, models
import base64
import tempfile
import logging
import os
from google.cloud import speech
from pydub import AudioSegment
import wave

_logger = logging.getLogger(__name__)

class CalendarEventCustom(models.Model):
    _inherit = 'calendar.event'  # Heredamos de 'calendar.event' para extenderlo
    
    # Campos adicionales que necesitas en el formulario de reunión
    m4a_file = fields.Binary("Archivo M4A")
    m4a_filename = fields.Char("Nombre del Archivo M4A")
    transcription_file = fields.Binary("Archivo de Transcripción", readonly=True)
    transcription_filename = fields.Char("Nombre del Archivo de Transcripción", readonly=True)

    def action_transcribe_audio(self):
        if not self.m4a_file:
            raise ValueError("No se ha cargado ningún archivo M4A.")
    
        try:
            # Decodificar el archivo M4A
            m4a_data = base64.b64decode(self.m4a_file)
            _logger.info("Archivo M4A decodificado correctamente.")

            # Crear un archivo temporal para el M4A
            with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as temp_m4a:
                temp_m4a.write(m4a_data)
                temp_m4a.flush()

                # Convertir M4A a WAV y asegurarse de que sea mono
                audio = AudioSegment.from_file(temp_m4a.name, format="m4a")
                audio = audio.set_channels(1)  # Convertir a un solo canal (mono)
                wav_file_path = temp_m4a.name.replace(".m4a", ".wav")
                audio.export(wav_file_path, format="wav")
                _logger.info(f"Archivo convertido a WAV (mono) y almacenado en: {wav_file_path}")

            # Configurar el cliente de Google Speech
            client = speech.SpeechClient.from_service_account_file('key.json')  # Cambia la ruta si es necesario

            # Verificar la tasa de muestreo del archivo WAV
            with wave.open(wav_file_path, 'rb') as wav:
                sample_rate = wav.getframerate()
                channels = wav.getnchannels()
                _logger.info(f"Tasa de muestreo del audio: {sample_rate} Hz, Canales: {channels}")
                if channels != 1:
                    raise ValueError("El archivo WAV no es mono. Verifica el archivo de entrada.")

            # Leer el contenido del archivo WAV
            with open(wav_file_path, 'rb') as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    enable_automatic_punctuation=True,
                    sample_rate_hertz=sample_rate,
                    language_code='es-ES'
                )

                # Realizar la transcripción
                response = client.recognize(config=config, audio=audio)
                transcription = " ".join([result.alternatives[0].transcript for result in response.results]) if response.results else "No se obtuvo ninguna transcripción."
                _logger.info("Transcripción completada exitosamente.")

            # Guardar la transcripción como archivo y asignarlo a `transcription_file`
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_txt:
                temp_txt.write(transcription.encode("utf-8"))
                temp_txt.flush()

            with open(temp_txt.name, "rb") as txt_file:
                self.transcription_file = base64.b64encode(txt_file.read())
                self.transcription_filename = "transcripcion.txt"

        except Exception as e:
            _logger.error(f"Error durante la transcripción: {e}")
            raise ValueError("Ocurrió un error al procesar el archivo de audio. Verifica el formato y vuelve a intentarlo.")
    
        finally:
            # Eliminar archivos temporales
            if os.path.exists(temp_m4a.name):
                os.remove(temp_m4a.name)
                _logger.info(f"Archivo temporal {temp_m4a.name} eliminado.")
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
                _logger.info(f"Archivo temporal {wav_file_path} eliminado.")

