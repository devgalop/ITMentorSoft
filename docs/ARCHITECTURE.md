# Arquitectura del proyecto

Este proyecto a nivel de backend se hace mediante un **monolito modular**, con una **arquitectura de capas verticales basadas en features**. Esto permite una mejor organización del código y facilita el mantenimiento y escalabilidad del proyecto.

## Estructura general

```bash
src/
├── features/          # Features con sus operaciones (capas verticales)
├── infrastructure/    # Implementaciones concretas de infraestructura
└── main.py            # Punto de entrada FastAPI
```

## Arquitectura de features (capas verticales)

Cada feature vive en su propio módulo y contiene todas sus capas:

```bash
features/
└── {feature_name}/
    ├── {operation_a}/          # Una operación = una unidad de negocio
    │   ├── {operation}_endpoint.py   # Capa de presentación (FastAPI)
    │   ├── {operation}_handler.py    # Capa de lógica de negocio
    │   ├── {operation}_request.py    # Esquema de request
    │   └── {operation}_response.py   # Esquema de response
    ├── {operation_b}/
    └── shared/                        # Recursos compartidos del feature
        ├── {domain_model}.py         # Modelo de dominio
        ├── {repository}.py           # Interfaz/abstracción del repositorio
        ├── dependencies.py           # Inyección de dependencias
        └── init.py                   # Agrega todos los routers
```

**Beneficios de esta estructura:**

- Cada feature es autocontenida (endpoint, handler, request, response)
- Los recursos compartidos (repositorios, modelos) viven en `shared/`
- Agregar una nueva operación no requiere modificar código existente
- Cada feature tiene su propio `__init__.py` que exporta su router principal

## Features implementados

### User Management (`/users`)

Gestión completa de usuarios y autenticación:

| Operación | Descripción |
| ----------- | ------------- |
| `create_user` | Registro de nuevos usuarios |
| `login` | Autenticación con JWT |
| `get_user` | Obtener perfil del usuario actual |
| `recovery_password` | Solicitar recuperación de contraseña (envía email) |
| `change_password` | Cambiar contraseña con token de recuperación |
| `assign_role` | Asignar roles a usuarios |
| `get_available_roles` | Listar roles disponibles |
| `refresh_token` | Refrescar token de acceso |

**Recursos compartidos:**

- `User` - Modelo de dominio
- `UserRepository` - Abstracción del repositorio de usuarios
- `RoleRepository` - Abstracción del repositorio de roles
- `RefreshTokenRepository` - Abstracción para tokens de refresh
- `UserRecoveryTokenRepository` - Abstracción para tokens de recuperación
- `PasswordHasher` - Abstracción para hashing de contraseñas
- `TokenGenerator` - Abstracción para generación de JWT

### Content Management (`/content`)

Gestión de contenidos educativos:

| Operación | Descripción |
| ----------- | ------------- |
| `get_all_contents` | Listar todos los contenidos |
| `get_resource_content` | Obtener contenido específico por ID |
| `register_content` | Registrar nuevo contenido educativo |
| `rate_content` | Calificar un contenido |
| `get_contents_by_topic` | Filtrar contenidos por tema |
| `get_contents_by_category` | Filtrar contenidos por categoría |
| `get_contents_by_title` | Buscar contenidos por título |
| `get_contents_by_category_topic` | Filtrar por categoría y tema |

**Recursos compartidos:**

- `Content` - Modelo de dominio
- `ContentRepository` - Abstracción del repositorio de contenidos

## Infrastructure

Capa de implementación concreta que sustenta a las features:

```bash
infrastructure/
├── database/
│   └── sqllite/           # Implementación SQLite
│       ├── models/        # Modelos de base de datos + mappers
│       ├── repository/    # Implementaciones concretas de repositorios
│       └── shared/        # Sesión de BD y seeder
├── notification/
│   └── brevo_notification_service.py  # Implementación con Brevo API
└── security/
    ├── jwt_token_generator.py         # Implementación JWT
    └── bcrypt_password_hasher.py      # Implementación bcrypt
```

### SQLite Models

| Modelo | Descripción |
| ----------- | ------------- |
| `SqlliteUser` | Modelo de usuario en BD |
| `SqlliteRole` | Modelo de rol en BD |
| `SqlliteResourceContent` | Modelo de contenido educativo |
| `SqlliteContentRating` | Modelo de calificaciones |
| `SqlliteQuestion` | Modelo de preguntas |

### Repositorios SQLite

| Repositorio | Descripción |
| ----------- | ------------- |
| `SqlliteUserRepository` | Persistencia de usuarios |
| `SqlliteRoleRepository` | Persistencia de roles |
| `SqlliteResourceContentRepository` | Persistencia de contenidos |
| `SqlliteContentRatingRepository` | Persistencia de calificaciones |
| `SqlliteUserRefreshTokenRepository` | Tokens de refresh |
| `SqlliteUserRecoveryTokenRepository` | Tokens de recuperación |

## Flujo de dependencias

```bash
┌─────────────────────────────────────────────────────────┐
│                    main.py                              │
│              (FastAPI app + lifespan)                   │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
    ┌─────▼─────┐                 ┌─────▼─────┐
    │  users    │                 │  content  │
    │  router   │                 │  router   │
    └─────┬─────┘                 └─────┬─────┘
          │                             │
    ┌─────▼─────┐                 ┌─────▼─────┐
    │  handler  │                 │  handler  │
    │  (lógica) │                 │  (lógica) │
    └─────┬─────┘                 └─────┬─────┘
          │                             │
    ┌─────▼─────┐                 ┌─────▼─────┐
    │  reposit. │                 │  reposit. │
    │  (interfaz)│                │  (interfaz)│
    └─────┬─────┘                 └─────┬─────┘
          │                             │
    ┌─────▼─────────────────────────────▼─────┐
    │         infrastructure                  │
    │   (implementaciones concretas)          │
    │  ┌──────────┐  ┌────────────┐  ┌───────┐│
    │  │ SQLite   │  │ Brevo      │  │ JWT   ││
    │  │          │  │ Notification│ │ Bcrypt││
    │  └──────────┘  └────────────┘  └───────┘│
    └──────────────────────────────────────────┘
```

## Diagramas de arquitectura

A continuación se presentan los diagramas de arquitectura del proyecto:

### Diagrama de contexto

![diagrama_contexto](./resources/c4_context_tutor.drawio.png)

### Diagrama de contenedores

![diagrama_contenedores](./resources/c4_containers_tutor.drawio.png)
