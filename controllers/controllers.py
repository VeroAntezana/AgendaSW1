# -*- coding: utf-8 -*-
# from odoo import http


# class DeSchool(http.Controller):
#     @http.route('/de_school/de_school/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_school/de_school/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_school.listing', {
#             'root': '/de_school/de_school',
#             'objects': http.request.env['de_school.de_school'].search([]),
#         })

#     @http.route('/de_school/de_school/objects/<model("de_school.de_school"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_school.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
# controllers.py
# controllers.py
from odoo import http
from odoo.http import request
import io
import json
from google.cloud import speech
from google.oauth2 import service_account

class AudioController(http.Controller):
    @http.route('/modulo_finalParcialSW/transcribe_audio', type='http', auth='user', csrf=False, methods=['POST'])
    def transcribe_audio(self, **kwargs):
        try:
            audio = kwargs.get('audio')
            if not audio:
                return request.make_response(json.dumps({'error': 'No audio file provided'}), headers={'Content-Type': 'application/json'})

            key_path = 'addons/modulo_finalParcialSW/config/key.json'
            credentials = service_account.Credentials.from_service_account_file(key_path)
            client = speech.SpeechClient(credentials=credentials)

            audio_content = io.BytesIO(audio.read()).read()
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="es-ES",
            )

            response = client.recognize(config=config, audio=audio)
            transcription = "".join(result.alternatives[0].transcript for result in response.results)
            return request.make_response(json.dumps({'transcription': transcription}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'error': str(e)}), headers={'Content-Type': 'application/json'})
