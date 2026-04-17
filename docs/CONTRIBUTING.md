# Guía de Contribución

Gracias por tu interés en contribuir a este proyecto. Para mantener la calidad del código y un flujo de trabajo consistente, sigue las siguientes pautas.

---

## Flujo de trabajo: Git Flow

Este proyecto utiliza **Git Flow** como modelo de ramas.

### Ramas principales

* `main`: contiene código listo para producción.
* `develop`: contiene el desarrollo en curso.

### Ramas de soporte

* `feature/*`: nuevas funcionalidades
* `bugfix/*`: corrección de errores
* `hotfix/*`: correcciones urgentes sobre `main`

### Proceso básico

1. Crear una rama desde `develop`:

   ```bash
   git checkout develop
   git pull
   git checkout -b feature/nombre-descriptivo
   ```

2. Realizar los cambios necesarios.

3. Asegurarte de que el código cumple con los estándares [ver sección siguiente](#validaciones-antes-de-hacer-commit).

---

## Validaciones antes de hacer commit

Antes de realizar cualquier commit, debes ejecutar los siguientes comandos:

```bash
# Formato
black .

# Linting
ruff check .

# Seguridad
bandit -r src/
```

### Importante

* Corrige todos los problemas reportados por estas herramientas.
* No se deben hacer commits con errores de formato, linting o seguridad.

---

## Commits

* Usa mensajes claros y descriptivos.
* Ejemplo:

  ```bash
  feat: agrega validación de usuario
  fix: corrige error en autenticación
  ```

---

## Pull Requests (PR)

Todos los cambios deben ser enviados mediante un **Pull Request (PR)**.

### Reglas para PR

* Nunca hacer push directo a `main`.
* El PR debe apuntar a la rama `develop` (salvo hotfix).
* Debe incluir una descripción clara de los cambios.
* Si aplica, adjuntar contexto, pruebas o capturas.

### Revisión

* El PR debe ser revisado y aprobado antes de hacer merge.
* Se pueden solicitar cambios antes de aprobar.

---

## Buenas prácticas

* Mantén las ramas actualizadas con `develop`.
* Realiza cambios pequeños y enfocados.
* Escribe código limpio y legible.
* Añade pruebas cuando sea necesario.

---

## Automatización (recomendado)

Se recomienda configurar hooks de git o herramientas como `pre-commit` para automatizar las validaciones antes del commit.

Para configurar `pre-commit`, sigue estos pasos:

1. Instala `pre-commit`:

   ```bash
   pip install pre-commit
   ```

2. Crea un archivo `.pre-commit-config.yaml` en la raíz del proyecto con el siguiente contenido:

   ```yaml
    repos:
    - repo: https://github.com/psf/black
        rev: 24.4.2
        hooks:
    - id: black

    - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.4.4
        hooks:
    - id: ruff

    - repo: https://github.com/PyCQA/bandit
        rev: 1.7.8
        hooks:
    - id: bandit
        args: ["-r", "src/"]
        exclude: ^tests/
   ```

3. Instala los hooks:

   ```bash
    pre-commit install
    ```

4. Ahora, cada vez que intentes hacer un commit, se ejecutarán automáticamente las validaciones configuradas. Si alguna de las validaciones falla, el commit será rechazado y deberás corregir los problemas antes de intentar hacer commit nuevamente.

---

Gracias por contribuir 🚀
