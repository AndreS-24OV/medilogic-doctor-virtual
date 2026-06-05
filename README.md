# MediLogic - Doctor Virtual General

Aplicación web educativa que integra:

- **Django**: interfaz web.
- **FastAPI**: API intermedia.
- **Prolog**: motor de reglas para posibles enfermedades.
- **CLISP**: evaluación de nivel de riesgo.

> Importante: este sistema no sustituye a un médico. Solo ofrece orientación general con fines educativos.

---

## 1. Requisitos

Instala Python 3.10 o superior.

Opcionalmente instala:

- SWI-Prolog para ejecutar las reglas Prolog reales.
- CLISP para ejecutar el módulo Lisp real.

Si no tienes Prolog o CLISP instalados, la API usa una lógica de respaldo en Python para que el proyecto funcione.

---

## 2. Instalar dependencias

Desde la carpeta principal del proyecto:

```bash
pip install -r requirements.txt
```

---

## 3. Ejecutar FastAPI

En una terminal:

```bash
cd api_service
uvicorn main:app --reload --port 8001
```

La API estará en:

```text
http://127.0.0.1:8001
```

Puedes probarla en:

```text
http://127.0.0.1:8001/docs
```

---

## 4. Ejecutar Django

En otra terminal:

```bash
cd django_web
python manage.py migrate
python manage.py runserver 8000
```

Abre la página en:

```text
http://127.0.0.1:8000
```

---

## 5. Funcionamiento

1. El usuario selecciona síntomas en la página web.
2. Django envía los síntomas a FastAPI.
3. FastAPI consulta reglas en Prolog para posibles enfermedades.
4. FastAPI consulta CLISP para calcular nivel de riesgo.
5. Django muestra el resultado al usuario.

---

## 6. Síntomas incluidos

- fiebre
- tos
- dolor_cabeza
- congestion_nasal
- estornudos
- dolor_garganta
- nauseas
- vomito
- diarrea
- dolor_abdominal
- dolor_pecho
- dificultad_respirar
- mareo
- fatiga

---

## 7. Advertencia médica

Este proyecto es una demostración académica de integración entre lenguajes y frameworks. No debe usarse para tomar decisiones médicas reales.
