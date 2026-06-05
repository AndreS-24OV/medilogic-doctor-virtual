# Despliegue en la nube - MediLogic

Esta versión está preparada para ejecutarse en un servidor cloud usando Docker.
El contenedor levanta dos servicios internos:

- Django público en el puerto que dé la nube (`$PORT`).
- FastAPI interno en `127.0.0.1:8001`.

Así los usuarios solo entran al enlace público de Django y no necesitan recibir ningún archivo.

---

## Opción recomendada: Render

Render permite desplegar servicios desde GitHub o desde una imagen Docker. Su documentación indica que puedes crear un **Web Service** conectado a un repositorio o imagen, y también soporta despliegues basados en `Dockerfile`.

Pasos:

1. Crea un repositorio en GitHub.
2. Sube esta carpeta completa al repositorio.
3. Entra a Render.
4. Selecciona **New > Web Service**.
5. Conecta tu repositorio.
6. Render detectará el `Dockerfile`.
7. En variables de entorno usa:

```text
DEBUG=False
ALLOWED_HOSTS=*
API_URL=http://127.0.0.1:8001/consulta
SECRET_KEY=una_clave_larga_segura
```

8. Despliega el servicio.
9. Cuando termine, Render te dará una URL pública.

---

## Opción alternativa: Railway

Railway también puede desplegar desde GitHub usando un `Dockerfile`. La documentación de Railway indica que, si existe un archivo llamado exactamente `Dockerfile` en la raíz, Railway lo detecta para construir el servicio.

Pasos generales:

1. Sube esta carpeta a GitHub.
2. En Railway crea un nuevo proyecto desde GitHub.
3. Selecciona el repositorio.
4. Agrega variables de entorno:

```text
DEBUG=False
ALLOWED_HOSTS=*
API_URL=http://127.0.0.1:8001/consulta
SECRET_KEY=una_clave_larga_segura
```

5. Railway construirá el contenedor y te dará un dominio público.

---

## Probar localmente con Docker

Desde la carpeta raíz:

```bash
docker compose up --build
```

Luego abre:

```text
http://127.0.0.1:8000
```

---

## Notas importantes

- El `Dockerfile` instala SWI-Prolog y CLISP dentro del servidor.
- Django usa WhiteNoise para servir archivos estáticos en producción.
- SQLite funciona para una práctica escolar, pero para producción real conviene PostgreSQL.
- Este sistema es educativo y no sustituye una consulta médica profesional.


## Cambios de esta versión

- Se restauró el panel derecho con descripción de síntomas seleccionados.
- Se corrigieron nombres con guion bajo en síntomas y enfermedades.
- Se evita que una enfermedad salga repetida varias veces.
