from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import subprocess
import json
import os

app = FastAPI(
    title="MediLogic API",
    description="API para doctor virtual general usando Prolog, CLISP y Python.",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROLOG_FILE = os.path.join(BASE_DIR, "rules", "diagnostico.pl")
LISP_FILE = os.path.join(BASE_DIR, "lisp", "riesgo.lisp")

SINTOMAS_DISPONIBLES = [
    "fiebre", "tos", "dolor_cabeza", "congestion_nasal", "estornudos",
    "dolor_garganta", "nauseas", "vomito", "diarrea", "dolor_abdominal",
    "dolor_pecho", "dificultad_respirar", "mareo", "fatiga"
]

class ConsultaRequest(BaseModel):
    sintomas: List[str] = Field(..., example=["fiebre", "tos", "dolor_cabeza"])


def diagnostico_respaldo_python(sintomas: List[str]) -> List[Dict[str, Any]]:
    reglas = {
        "gripe": {"fiebre", "tos", "dolor_cabeza", "fatiga", "dolor_garganta"},
        "resfriado": {"tos", "estornudos", "congestion_nasal", "dolor_garganta"},
        "gastroenteritis": {"nauseas", "vomito", "diarrea", "dolor_abdominal"},
        "posible_cuadro_respiratorio_grave": {"dolor_pecho", "dificultad_respirar", "fiebre"},
        "migraña_o_cefalea": {"dolor_cabeza", "mareo", "nauseas"},
    }
    sintomas_set = set(sintomas)
    resultados = []
    for enfermedad, requeridos in reglas.items():
        coincidencias = sorted(list(sintomas_set.intersection(requeridos)))
        if coincidencias:
            porcentaje = round((len(coincidencias) / len(requeridos)) * 100, 2)
            resultados.append({
                "enfermedad": enfermedad,
                "coincidencias": coincidencias,
                "porcentaje": porcentaje
            })
    resultados.sort(key=lambda x: x["porcentaje"], reverse=True)
    return resultados[:3]


def consultar_prolog(sintomas: List[str]) -> List[Dict[str, Any]]:
    sintomas_prolog = "[" + ",".join(sintomas) + "]"
    query = f"consult('{PROLOG_FILE}'), diagnosticar({sintomas_prolog}, Resultado), write_canonical(Resultado), halt."
    try:
        proceso = subprocess.run(
            ["swipl", "-q", "-g", query],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proceso.returncode != 0 or not proceso.stdout.strip():
            return diagnostico_respaldo_python(sintomas)
        return convertir_salida_prolog(proceso.stdout.strip())
    except Exception:
        return diagnostico_respaldo_python(sintomas)


def convertir_salida_prolog(salida: str) -> List[Dict[str, Any]]:
    # Salida esperada: [resultado(gripe,[dolor_cabeza,fiebre,tos],60.0),...]
    # Para mantenerlo simple y robusto en la práctica escolar, si no se puede convertir, usamos respaldo.
    try:
        salida = salida.strip()
        if salida == "[]":
            return []
        resultados = []
        partes = salida.replace("[resultado(", "resultado(").rstrip("]").split(",resultado(")
        for parte in partes:
            parte = parte.replace("resultado(", "")
            enfermedad = parte.split(",[", 1)[0]
            resto = parte.split(",[", 1)[1]
            coincidencias_txt, porcentaje_txt = resto.rsplit("],", 1)
            coincidencias = [s for s in coincidencias_txt.split(",") if s]
            porcentaje = float(porcentaje_txt.rstrip(")"))
            resultados.append({
                "enfermedad": enfermedad,
                "coincidencias": coincidencias,
                "porcentaje": porcentaje
            })
        return resultados
    except Exception:
        return []


def riesgo_respaldo_python(sintomas: List[str]) -> Dict[str, str]:
    sintomas_set = set(sintomas)
    if "dolor_pecho" in sintomas_set or "dificultad_respirar" in sintomas_set:
        return {
            "nivel": "alto",
            "recomendacion": "Busca atención médica inmediata, especialmente si los síntomas son intensos o aparecen de forma repentina."
        }
    if "fiebre" in sintomas_set and ("vomito" in sintomas_set or "diarrea" in sintomas_set):
        return {
            "nivel": "medio",
            "recomendacion": "Mantente hidratado y considera consultar a un médico si los síntomas persisten o empeoran."
        }
    if "fiebre" in sintomas_set:
        return {
            "nivel": "medio",
            "recomendacion": "Descansa, toma líquidos y monitorea la temperatura. Consulta a un médico si la fiebre dura más de 48 horas."
        }
    return {
        "nivel": "bajo",
        "recomendacion": "Observa la evolución de los síntomas, descansa y acude a consulta si aparecen señales de alarma."
    }


def consultar_clisp(sintomas: List[str]) -> Dict[str, str]:
    sintomas_lisp = "(" + " ".join(sintomas) + ")"
    expresion = f'(load "{LISP_FILE}") (imprimir-riesgo \'{sintomas_lisp})'
    try:
        proceso = subprocess.run(
            ["clisp", "-q", "-x", expresion],
            capture_output=True,
            text=True,
            timeout=5
        )
        salida = proceso.stdout.strip().splitlines()[-1]
        if not salida:
            return riesgo_respaldo_python(sintomas)
        return json.loads(salida)
    except Exception:
        return riesgo_respaldo_python(sintomas)


@app.get("/")
def inicio():
    return {"mensaje": "MediLogic API funcionando"}


@app.get("/sintomas")
def sintomas():
    return {"sintomas": SINTOMAS_DISPONIBLES}


@app.post("/consulta")
def consulta(datos: ConsultaRequest):
    sintomas_limpios = [s.strip().lower() for s in datos.sintomas if s.strip()]
    diagnosticos = consultar_prolog(sintomas_limpios)
    riesgo = consultar_clisp(sintomas_limpios)

    return {
        "sintomas_recibidos": sintomas_limpios,
        "diagnosticos_posibles": diagnosticos,
        "riesgo": riesgo,
        "aviso": "Este sistema es educativo y no sustituye la valoración de un médico profesional."
    }
