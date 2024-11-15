# Modulo_Agenda_Electronica_Educativa

### Pasos para la instalación de Odoo:

1) *clonar el repositorio de git*
   ```bash
   git clone https://github.com/odoo/odoo.git
   ```

2. **Crear un entorno virtual (opcional pero recomendado):**
   Es una buena práctica crear un entorno virtual para cada proyecto Python. Esto ayuda a mantener las dependencias del proyecto separadas de otros proyectos y del sistema global. Para crear un entorno virtual, abre una terminal y ejecuta los siguientes comandos:

   ```bash
    python -m venv myenv
    ```

   Esto creará un nuevo directorio llamado myenv que contendrá el entorno virtual.

3. **Activar el entorno virtual:**

   ```bash
      .\env\Scripts\activate o
      source env/scripts/activate
    ```

4. **Instalar las librerías requeridas:**

   ```bash
   pip install setuptools Wheel
   pip install -r requirements.txt
    ```

5. **Correr el servidor (opcional):**
  ```bash
  python odoo-bin -r usuario -w contraseña --addons-path=addons -d nombreBase -i base
    ```

en usuario colocar el nombre de usuario de postgresql y en "contraseña" la contraseña de tu base de datos por ultimo cambiar el "nombrebase" al nombre de tu base de datos 

6. **Agregar un nuevo Modulo a odoo (opcional):**
  ```bash
     python odoo-bin scaffold my_module addons/
    ```
Donde "my_module" es el nombre que quieres darle a tu nuevo módulo. Este comando creará una estructura básica para tu módulo en la carpeta "addons/".
Recuerda ejecutar este comando desde el directorio raíz de tu instalación de Odoo.