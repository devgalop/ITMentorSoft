# Configuración del entorno de desarrollo

## Requisitos previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- virtualenv (opcional pero recomendado)
- Docker y Docker Compose (para servicios de infraestructura local)

## Servicios de infraestructura con Docker

El proyecto utiliza Docker Compose para levantar PostgreSQL y LocalStack (SQS) en el entorno de desarrollo y pruebas.

### Iniciar los servicios

```bash
# Desde la raíz del proyecto
docker compose up -d
```

Esto levanta:
- **PostgreSQL 18.6-alpine3.24** en `localhost:5432`
- **Floci** (emulador SQS) en `localhost:4566`

### Verificar que los servicios están activos

```bash
# Ver estado de los contenedores
docker compose ps

```

### Detener los servicios

```bash
docker compose down
```

Para eliminar también los datos persistidos:

```bash
docker compose down -v
```

## Variables de entorno necesarias

Para configurar el entorno de desarrollo, es necesario definir las siguientes variables de entorno en el archivo `.env` en la raíz del proyecto:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA_SECONDS=1800
RANDOM_TOKEN_EXPIRATION_DELTA_SECONDS=1800
REFRESH_TOKEN_EXPIRATION_DELTA_SECONDS=604800

# Database — PostgreSQL (Docker local)
DATABASE_URL=postgresql+asyncpg://mentor:mentor123@localhost:5432/mentorsoft
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Database Seeder
DATABASE_ADMIN_USERNAME=admin
DATABASE_ADMIN_PASSWORD=your-admin-password
DATABASE_ADMIN_EMAIL=admin@example.com
DEFAULT_STUDENT_PASSWORD=your-student-password
DEFAULT_TEACHER_PASSWORD=your-teacher-password
DEFAULT_USER_PASSWORD=your-user-password

# Email (Brevo)
BREVO_API_KEY=your-brevo-api-key
BREVO_BASE_API_URL=https://api.brevo.com/v3
EMAIL_DEFAULT_SENDER=noreply@example.com

# URLs
RECOVERY_URL_BASE=http://localhost:8000/reset-password
REVIEW_URL_BASE=http://localhost:8000/assessments/pending-approval-questions
LOGIN_URL_BASE=http://localhost:8000/login

# AI Services
GROQ_API_KEY=your-groq-api-key
OPENCODE_API_KEY=your-opencode-api-key
OPENCODE_API_URL=https://opencode.ai/zen/go/v1

# Application
ASSESSMENT_QUALIFICATION_CHUNK_SIZE=5

# AWS/SQS (LocalStack)
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_REGION=us-east-1
AWS_ENDPOINT_URL=http://localhost:4566
AWS_SQS_QUALIFICATION_QUEUE_URL=http://localhost:4566/000000000000/mq-itmentorsoft-qualify-001
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

## Probar SQS con Floci

Floci emula AWS SQS localmente. Para verificar que los mensajes fluyen correctamente:

### 2. Listar las colas disponibles

```bash
# Usando AWS CLI con LocalStack
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

### 3. Crear una cola de prueba

```bash
aws --endpoint-url=http://localhost:4566 sqs create-queue \
  --queue-name test-queue \
  --attributes '{"VisibilityTimeout": "60"}'
```

### 4. Enviar un mensaje a la cola

```bash
aws --endpoint-url=http://localhost:4566 sqs send-message \
  --queue-url http://localhost:4566/000000000000/test-queue \
  --message-body '{"test": "hello from localstack"}'
```

### 5. Recibir mensajes

```bash
aws --endpoint-url=http://localhost:4566 sqs receive-message \
  --queue-url http://localhost:4566/000000000000/test-queue
```

### 6. Limpiar mensajes de una cola

```bash
# Purge (elimina todos los mensajes)
aws --endpoint-url=http://localhost:4566 sqs purge-queue \
  --queue-url http://localhost:4566/000000000000/test-queue
```

### 7. Notas sobre las colas del proyecto

El proyecto crea automáticamente dos colas al iniciar:

- `mq-itmentorsoft-qualify-001` — Cola de cualificación

Estas se configuran mediante las variables de entorno `AWS_SQS_QUALIFICATION_QUEUE_URL`
