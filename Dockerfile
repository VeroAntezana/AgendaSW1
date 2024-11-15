FROM odoo:17

# Copiar los addons personalizados al contenedor
#COPY ./addons /mnt/extra-addons

# Establecer permisos para los addons
#RUN chown -R odoo:odoo /mnt/extra-addons
USER root

# Instalar dependencias adicionales si las necesitas
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python necesarias para tu módulo
RUN pip3 install google-cloud-speech speechrecognition pydub
RUN apt-get update && apt-get install -y ffmpeg
# Copiar los addons personalizados al contenedor
COPY ./addons /mnt/extra-addons

# Establecer permisos correctos
RUN chown -R odoo:odoo /mnt/extra-addons \
    && chown -R odoo:odoo /var/lib/odoo \
    && chown -R odoo:odoo /etc/odoo

USER odoo