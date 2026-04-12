# Configuración del entorno de desarrollo

## Requisitos previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- virtualenv (opcional pero recomendado)

## Variables de entorno necesarias

Para configurar el entorno de desarrollo, es necesario definir las siguientes variables de entorno en el archivo `.env` en la raíz del proyecto:

```bash
JWT_SECRET_KEY=your_secret_key_here     # Reemplaza con una clave secreta segura para la generación de JWT
JWT_ALGORITHM=HS256                     # Algoritmo de encriptación para JWT (puede ser HS256, RS256, etc.)
JWT_EXPIRATION_DELTA_SECONDS=300        # Tiempo de expiración del token en segundos. Si no se define, el token expirará en 5 minutos (300 segundos).
```

**IMPORTANTE**: Recuerda nunca compartir el archivo `.env` ni las claves secretas que contiene, especialmente en repositorios públicos. Asegúrate de agregar el archivo `.env` al archivo `.gitignore` para evitar que se suba al repositorio.

**NOTA**: Configura estas variables sin espacios alrededor del signo igual (`=`) y sin comillas.

## Configuraciones adicionales

### Configuración del entorno virtual (recomendado)

Los entornos virtuales son una herramienta que permite crear un espacio aislado para cada proyecto, evitando conflictos entre dependencias y versiones de paquetes. Para configurar un entorno virtual en Python, puedes seguir estos pasos:

- Crea la carpeta de tu proyecto y navega hacía ella

```bash
#Crear carpeta del proyecto
mkdir mi_proyecto
#Navegar hacía la carpeta del proyecto
cd mi_proyecto
```

- Para crear el entorno virtual, puedes usar el módulo `venv` que viene incluido con Python. Ejecuta el siguiente comando:

```bash
#Crea un entorno virtual llamado "alias_del_entorno"
#Reemplaza "alias_del_entorno" con el nombre que desees para tu entorno virtual
#Se recomienda usar un nombre descriptivo para el entorno virtual, como ".venv"
python -m venv alias_del_entorno
```

- Una vez creado el entorno virtual, debes activarlo para poder usarlo. El comando para activar el entorno virtual varía según el sistema operativo:

```bash
#Recuerda reemplazar "alias_del_entorno" con el nombre que hayas elegido para tu entorno virtual

#Windows PowerShell
alias_del_entorno\Scripts\Activate.ps1

#Windows bash (WSL o Git Bash)
source alias_del_entorno/Scripts/activate

#Linux/MacOS
source alias_del_entorno/bin/activate
```

- Valida que el entorno virtual esté activo. Deberías ver el nombre del entorno virtual entre paréntesis al inicio de la línea de comandos. Por ejemplo:

```bash
(alias_del_entorno) $
```

- Con el entorno virtual activado, puedes instalar las dependencias necesarias para tu proyecto utilizando `pip`. Por ejemplo:

```bash
#Actualiza pip a la última versión disponible
python -m pip install --upgrade pip
```

- Para desactivar el entorno virtual cuando hayas terminado de trabajar, simplemente ejecuta el siguiente comando:

```bash
deactivate
```

### Instalación de dependencias

Para instalar las dependencias necesarias para el proyecto, puedes usar el archivo `requirements.txt` que se encuentra en la raíz del proyecto. Este archivo contiene una lista de todas las dependencias necesarias para ejecutar la aplicación.
Para instalar las dependencias, ejecuta el siguiente comando:

```bash
#Recuerda activar tu entorno virtual antes de ejecutar este comando para asegurarte de que las dependencias se instalen en el entorno virtual y no globalmente
pip install -r requirements.txt
```
