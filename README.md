# Proyecto de especialización en desarrollo de software: Tutor inteligente para fundamentos de diseño de software y pensamiento computacional

## Descripción del proyecto

Este proyecto tiene como objetivo principal potenciar el dominio de los fundamentos de desarrollo de software y las habilidades de pensamiento computacional en estudiantes que ingresan a programas de ingeniería de software, mediante el diseño e implementación de un tutor inteligente con capacidades de diagnóstico adaptativo y generación de rutas de aprendizaje personalizadas.

## Stack tecnológico

- Python 3.13
- FastAPI
- SQLite (base de datos)
- JWT (autenticación)
- Brevo (servicio de notificaciones email)

## Arquitectura del proyecto

Este proyecto a nivel de backend se hace mediante un **monolito modular**, con una **arquitectura de capas verticales basadas en features**. Esto permite una mejor organización del código y facilita el mantenimiento y escalabilidad del proyecto.

La estructura del proyecto se organizará de la siguiente manera:

- `src/`: Contiene el código principal de la aplicación, organizado en módulos según las features.
  - `features/`: Cada feature tiene su propio módulo con sus operaciones. Cada operación contiene sus capas (endpoint, handler, request, response). Los recursos compartidos (repositorios, modelos, dependencias) viven en `shared/`.
    - `user_management/`: Gestión de usuarios (crear, login, recuperar contraseña, cambiar contraseña, asignar roles, refresh token)
    - `content_management/`: Gestión de contenidos (listar, registrar, calificar, buscar por título, tema o categoría)
    - `shared/`: Abstracciones compartidas como NotificationService
  - `infrastructure/`: Implementación de infraestructura concreta.
    - `database/sqllite/`: Repositorios y modelos SQLite (user, role, content, ratings, tokens)
    - `notification/`: Implementación del servicio de notificaciones (Brevo)
    - `security/`: Implementación de seguridad (JWT token generator, Bcrypt password hasher)
  - `main.py`: Punto de entrada de la aplicación.
- `tests/`: Tests unitarios y de integración.

```bash
src/
├── features/
│   ├── user_management/
│   │   ├── create_user/
│   │   ├── login/
│   │   ├── get_user/
│   │   ├── recovery_password/
│   │   ├── change_password/
│   │   ├── assign_role/
│   │   ├── get_available_roles/
│   │   ├── refresh_token/
│   │   └── shared/
│   │       ├── user.py
│   │       ├── user_repository.py
│   │       ├── role_repository.py
│   │       ├── refresh_token_repository.py
│   │       ├── user_recovery_token_repository.py
│   │       ├── dependencies.py
│   │       └── init.py
│   ├── content_management/
│   │   ├── get_all_contents/
│   │   ├── get_resource_content/
│   │   ├── register_content/
│   │   ├── rate_content/
│   │   ├── get_contents_by_topic/
│   │   ├── get_contents_by_category/
│   │   ├── get_contents_by_title/
│   │   ├── get_contents_by_category_topic/
│   │   └── shared/
│   │       ├── content.py
│   │       ├── content_repository.py
│   │       ├── dependencies.py
│   │       └── init.py
│   └── shared/
│       └── notification_service.py
├── infrastructure/
│   ├── database/
│   │   └── sqllite/
│   │       ├── models/
│   │       │   ├── sqllite_user.py
│   │       │   ├── sqllite_user_mapper.py
│   │       │   ├── sqllite_role.py
│   │       │   ├── sqllite_role_mapper.py
│   │       │   ├── sqllite_resource_content.py
│   │       │   ├── sqllite_resource_content_mapper.py
│   │       │   ├── sqllite_content_rating.py
│   │       │   ├── sqllite_content_rating_mapper.py
│   │       │   └── sqllite_question.py
│   │       ├── repository/
│   │       │   ├── sqllite_user_repository.py
│   │       │   ├── sqllite_role_repository.py
│   │       │   ├── sqllite_resource_content_repository.py
│   │       │   ├── sqllite_content_rating_repository.py
│   │       │   ├── sqllite_user_refresh_token_repository.py
│   │       │   └── sqllite_user_recovery_token_repository.py
│   │       └── shared/
│   │           ├── sqllite_database_session.py
│   │           └── sqllite_seeder.py
│   ├── notification/
│   │   └── brevo_notification_service.py
│   └── security/
│       ├── jwt_token_generator.py
│       └── bcrypt_password_hasher.py
└── main.py
```

Para más detalles sobre la arquitectura del proyecto, puedes consultar el documento [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## API Endpoints

### User Management (`/users`)

| Método | Endpoint | Descripción |
| -------- | ---------- | ------------- |
| POST | `/users/create` | Crear nuevo usuario |
| POST | `/users/login` | Iniciar sesión |
| GET | `/users/me` | Obtener usuario actual |
| POST | `/users/recovery-password` | Solicitar recuperación de contraseña |
| POST | `/users/change-password` | Cambiar contraseña |
| POST | `/users/assign-role` | Asignar rol a usuario |
| GET | `/users/available-roles` | Obtener roles disponibles |
| POST | `/users/refresh-token` | Refrescar token de acceso |

### Content Management (`/content`)

| Método | Endpoint | Descripción |
| -------- | ---------- | ------------- |
| GET | `/content` | Listar todos los contenidos |
| GET | `/content/{id}` | Obtener contenido por ID |
| POST | `/content/register` | Registrar nuevo contenido |
| POST | `/content/rate` | Calificar contenido |
| GET | `/content/by-topic` | Buscar contenidos por tema |
| GET | `/content/by-category` | Buscar contenidos por categoría |
| GET | `/content/by-title` | Buscar contenidos por título |
| GET | `/content/by-category-topic` | Buscar contenidos por categoría y tema |

## Configuración del entorno de desarrollo

Para obtener detalles sobre cómo configurar el entorno de desarrollo, puedes consultar el documento [SETUP.md](docs/SETUP.md).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Puedes consultar el archivo [LICENSE](LICENSE) para más detalles sobre los términos de la licencia.
