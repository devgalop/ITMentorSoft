# Proyecto de especialización en desarrollo de software: Tutor inteligente para fundamentos de diseño de software y pensamiento computacional

## Descripción del proyecto

Este proyecto tiene como objetivo principal potenciar el dominio de los fundamentos de desarrollo de software y las habilidades de pensamiento computacional en estudiantes que ingresan a programas de ingeniería de software, mediante el diseño e implementación de un tutor inteligente con capacidades de diagnóstico adaptativo y generación de rutas de aprendizaje personalizadas.

## Stack tecnológico

- Python 3.13
- FastAPI

## Arquitectura del proyecto

Este proyecto a nivel de backend se hará mediante un **monolito modular**, con una **arquitectura de capas verticales basadas en features**. Esto permitirá una mejor organización del código y facilitará el mantenimiento y escalabilidad del proyecto.

La estructura del proyecto se organizará de la siguiente manera:

- `src/`: Contendrá el código principal de la aplicación, organizado en módulos según las features.
  - `features/`: Cada feature tendrá su propio módulo con sus respectivas capas (controladores, servicios, repositorios).
  - `infrastructure/`: Contendrá la implementación de la infraestructura necesaria para la aplicación, como la conexión a bases de datos, servicios externos, etc.
  - `main.py`: Punto de entrada de la aplicación.
- `tests/`: Contendrá los tests unitarios y de integración para asegurar la calidad del código.

```bash
├── src/
│   ├── features/
│   │   ├── user-management/
│   │   │    ├── create_user/
│   │   │    │   ├── create_user_endpoint.py
│   │   │    │   ├── create_user_handler.py
│   │   │    │   ├── create_user_request.py
│   │   │    ├── login/
│   │   │    ├── shared/
│   │   │    │   ├── init.py
│   │   │    │   ├── user_repository.py
│   │   │    │   ├── user.py
│   │   ├── content-management/
│   │   ├── evaluation/
│   │   ├── classification/
│   │   ├── recommendation/
│   │   ├── reporting/
│   ├── infrastructure/
│   ├── main.py
├── tests/
```

Para más detalles sobre la arquitectura del proyecto, puedes consultar el documento [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Configuración del entorno de desarrollo

Para obtener detalles sobre cómo configurar el entorno de desarrollo, puedes consultar el documento [SETUP.md](docs/SETUP.md).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Puedes consultar el archivo [LICENSE](LICENSE) para más detalles sobre los términos de la licencia.
