odoo.define('modulo_finalParcialSW.audio_recorder', [], function (require) {
    "use strict";
    const core = require('web.core');
    const rpc = require('web.rpc');

    document.addEventListener('DOMContentLoaded', function() {
        const waitForMicrophoneButton = setInterval(() => {
            const microphoneButton = document.getElementById('start-recording');
            if (microphoneButton) {
                clearInterval(waitForMicrophoneButton); // Detenemos el intervalo una vez que encontramos el botón

                let mediaRecorder;
                let audioChunks = [];

                // Crear un elemento de texto para mostrar "Grabando..."
                const recordingStatus = document.createElement('span');
                recordingStatus.id = 'recording-status';
                recordingStatus.textContent = 'Grabando...';
                recordingStatus.style.color = 'red';
                recordingStatus.style.marginLeft = '10px';
                recordingStatus.style.display = 'none'; // Oculto por defecto
                microphoneButton.parentElement.appendChild(recordingStatus); // Añadimos junto al botón

                microphoneButton.addEventListener('click', async () => {
                    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
                        console.log("Iniciando grabación...");

                        try {
                            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                            mediaRecorder = new MediaRecorder(stream);

                            mediaRecorder.ondataavailable = event => {
                                audioChunks.push(event.data);
                                console.log("Datos de audio disponibles:", event.data);
                            };

                            mediaRecorder.onstart = () => {
                                console.log("Grabación iniciada");
                                recordingStatus.style.display = 'inline'; // Mostrar "Grabando..."
                            };

                            mediaRecorder.onstop = async () => {
                                console.log("Grabación detenida");
                                recordingStatus.style.display = 'none'; // Ocultar "Grabando..."
                                
                                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                                audioChunks = [];
                                console.log("Blob de audio creado:", audioBlob);

                                // Enviar audio al servidor para la transcripción
                                const formData = new FormData();
                                formData.append('audio', audioBlob);

                                try {
                                    const response = await fetch('/modulo_finalParcialSW/transcribe_audio', {
                                        method: 'POST',
                                        body: formData,
                                    });

                                    if (!response.ok) {
                                        console.error("Error en la respuesta del servidor:", response.statusText);
                                        return;
                                    }

                                    const data = await response.json();
                                    console.log("Respuesta de transcripción recibida:", data);

                                    if (data.transcription) {
                                        // Colocar el texto transcrito directamente en el campo de descripción
                                        const descripcionField = document.querySelector('textarea[name="descripcion"]');
                                        if (descripcionField) {
                                            descripcionField.value = data.transcription;
                                            console.log("Texto transcrito colocado en la descripción.");
                                        } else {
                                            console.warn('El campo de descripción no se encontró en el DOM');
                                        }
                                    }
                                } catch (error) {
                                    console.error('Error al transcribir el audio:', error);
                                }
                            };

                            mediaRecorder.start();
                        } catch (error) {
                            console.error("Error al acceder al micrófono:", error);
                        }

                    } else if (mediaRecorder.state === 'recording') {
                        console.log("Deteniendo la grabación...");
                        mediaRecorder.stop();
                    }
                });
            }
        }, 500); // Verificamos cada 500ms hasta que el botón esté disponible
    });
});
