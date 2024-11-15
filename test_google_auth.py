from google.cloud import speech
from google.oauth2 import service_account

def test_google_credentials():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'C:/Veronica/2-2024/sw1/Parcial2-odoo17/odoo-17.0/odoo-17.0/addons/modulo_finalParcialSW/config/key.json'
        )
        client = speech.SpeechClient(credentials=credentials)
        print("Autenticación exitosa con Google Speech-to-Text.")
    except Exception as e:
        print("Error de autenticación:", e)

test_google_credentials()
