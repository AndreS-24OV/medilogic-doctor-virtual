import json
import os
import requests
from django.shortcuts import render
from .models import Consulta

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8001/consulta")

SINTOMAS = [
    ("fiebre", "Fiebre"),
    ("tos", "Tos"),
    ("dolor_cabeza", "Dolor de cabeza"),
    ("congestion_nasal", "Congestión nasal"),
    ("estornudos", "Estornudos"),
    ("dolor_garganta", "Dolor de garganta"),
    ("nauseas", "Náuseas"),
    ("vomito", "Vómito"),
    ("diarrea", "Diarrea"),
    ("dolor_abdominal", "Dolor abdominal"),
    ("dolor_pecho", "Dolor de pecho"),
    ("dificultad_respirar", "Dificultad para respirar"),
    ("mareo", "Mareo"),
    ("fatiga", "Fatiga"),
]


def inicio(request):
    resultado = None
    error = None
    seleccionados = []

    if request.method == "POST":
        seleccionados = request.POST.getlist("sintomas")
        if not seleccionados:
            error = "Selecciona al menos un síntoma."
        else:
            try:
                respuesta = requests.post(API_URL, json={"sintomas": seleccionados}, timeout=8)
                respuesta.raise_for_status()
                resultado = respuesta.json()

                Consulta.objects.create(
                    sintomas=", ".join(seleccionados),
                    resultado=json.dumps(resultado, ensure_ascii=False, indent=2)
                )
            except requests.exceptions.ConnectionError:
                error = "No se pudo conectar con FastAPI. Revisa que esté corriendo en el puerto 8001."
            except Exception as exc:
                error = f"Ocurrió un error al procesar la consulta: {exc}"

    return render(request, "consultas/inicio.html", {
        "sintomas": SINTOMAS,
        "resultado": resultado,
        "error": error,
        "seleccionados": seleccionados,
    })


def historial(request):
    consultas = Consulta.objects.order_by("-fecha")[:20]
    return render(request, "consultas/historial.html", {"consultas": consultas})
