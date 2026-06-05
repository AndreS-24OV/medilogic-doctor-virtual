from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import subprocess
import json
import os

app = FastAPI(
    title="MediLogic API",
    description="API para doctor virtual general usando Prolog, CLISP y Python.",
    version="1.1.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROLOG_FILE = os.path.join(BASE_DIR, "rules", "diagnostico.pl")
LISP_FILE = os.path.join(BASE_DIR, "lisp", "riesgo.lisp")

SINTOMAS_DISPONIBLES = [
    "fiebre", "fiebre_alta", "tos", "tos_seca", "tos_con_flema",
    "dolor_cabeza", "congestion_nasal", "escurrimiento_nasal", "estornudos",
    "dolor_garganta", "dolor_muscular", "escalofrios", "fatiga", "perdida_olfato",
    "nauseas", "vomito", "diarrea", "dolor_abdominal", "acidez",
    "dolor_pecho", "dificultad_respirar", "mareo", "sensibilidad_luz", "rigidez_cuello",
    "picazon_ojos", "ojos_llorosos", "sarpullido", "dolor_oido",
    "ardor_orinar", "orina_frecuente", "dolor_espalda_baja",
    "sed_excesiva", "hambre_excesiva", "vision_borrosa", "perdida_peso",
    "palpitaciones", "ansiedad", "insomnio", "dolor_articulaciones"
]

NOMBRES_ENFERMEDADES = {
    "gripe": "Gripe",
    "resfriado": "Resfriado común",
    "covid_o_infeccion_respiratoria": "COVID o infección respiratoria",
    "bronquitis": "Bronquitis",
    "sinusitis": "Sinusitis",
    "alergia_respiratoria": "Alergia respiratoria",
    "gastroenteritis": "Gastroenteritis",
    "gastritis_o_reflujo": "Gastritis o reflujo",
    "posible_cuadro_respiratorio_grave": "Posible cuadro respiratorio grave",
    "migrana_o_cefalea": "Migraña o cefalea",
    "otitis": "Otitis",
    "infeccion_urinaria": "Infección urinaria",
    "posible_diabetes": "Posible alteración de glucosa",
    "ansiedad_o_estres": "Ansiedad o estrés",
    "posible_infeccion_sistemica": "Posible infección sistémica"
}

class ConsultaRequest(BaseModel):
    sintomas: List[str] = Field(..., example=["fiebre", "tos", "dolor_cabeza"])


def normalizar_resultados(resultados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for item in resultados:
        clave = item.get("enfermedad", "")
        item["enfermedad"] = NOMBRES_ENFERMEDADES.get(clave, clave.replace("_", " ").title())
        item["coincidencias"] = [s.replace("_", " ") for s in item.get("coincidencias", [])]
    return resultados


def diagnostico_respaldo_python(sintomas: List[str]) -> List[Dict[str, Any]]:
    reglas = {
        "gripe": {"fiebre", "tos", "dolor_cabeza", "fatiga", "dolor_garganta", "dolor_muscular", "escalofrios"},
        "resfriado": {"tos", "estornudos", "congestion_nasal", "escurrimiento_nasal", "dolor_garganta"},
        "covid_o_infeccion_respiratoria": {"fiebre", "tos_seca", "fatiga", "dolor_garganta", "perdida_olfato", "dolor_muscular"},
        "bronquitis": {"tos_con_flema", "tos", "fatiga", "dolor_pecho", "dificultad_respirar"},
        "sinusitis": {"congestion_nasal", "dolor_cabeza", "escurrimiento_nasal", "dolor_garganta", "fatiga"},
        "alergia_respiratoria": {"estornudos", "picazon_ojos", "ojos_llorosos", "congestion_nasal", "escurrimiento_nasal"},
        "gastroenteritis": {"nauseas", "vomito", "diarrea", "dolor_abdominal", "fiebre"},
        "gastritis_o_reflujo": {"dolor_abdominal", "acidez", "nauseas", "vomito"},
        "posible_cuadro_respiratorio_grave": {"dolor_pecho", "dificultad_respirar", "fiebre_alta", "fatiga"},
        "migrana_o_cefalea": {"dolor_cabeza", "mareo", "nauseas", "sensibilidad_luz"},
        "otitis": {"dolor_oido", "fiebre", "mareo", "dolor_cabeza"},
        "infeccion_urinaria": {"ardor_orinar", "orina_frecuente", "dolor_abdominal", "dolor_espalda_baja", "fiebre"},
        "posible_diabetes": {"sed_excesiva", "hambre_excesiva", "orina_frecuente", "vision_borrosa", "perdida_peso", "fatiga"},
        "ansiedad_o_estres": {"ansiedad", "palpitaciones", "insomnio", "mareo", "dolor_pecho"},
        "posible_infeccion_sistemica": {"fiebre_alta", "escalofrios", "dolor_muscular", "dolor_articulaciones", "sarpullido"},
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
    return resultados[:5]


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
        convertidos = convertir_salida_prolog(proceso.stdout.strip())
        return convertidos if convertidos else diagnostico_respaldo_python(sintomas)
    except Exception:
        return diagnostico_respaldo_python(sintomas)


def convertir_salida_prolog(salida: str) -> List[Dict[str, Any]]:
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
                "porcentaje": round(porcentaje, 2)
            })
        return resultados[:5]
    except Exception:
        return []


def riesgo_respaldo_python(sintomas: List[str]) -> Dict[str, str]:
    sintomas_set = set(sintomas)
    if (
        "dolor_pecho" in sintomas_set
        or "dificultad_respirar" in sintomas_set
        or ("fiebre_alta" in sintomas_set and "rigidez_cuello" in sintomas_set)
        or ("fiebre_alta" in sintomas_set and "sarpullido" in sintomas_set)
    ):
        return {
            "nivel": "alto",
            "recomendacion": "Busca atención médica inmediata, especialmente si los síntomas son intensos, aparecen de forma repentina o hay dificultad para respirar."
        }
    if (
        "fiebre_alta" in sintomas_set
        or ("fiebre" in sintomas_set and ("vomito" in sintomas_set or "diarrea" in sintomas_set))
        or ("ardor_orinar" in sintomas_set and "dolor_espalda_baja" in sintomas_set)
        or ("sed_excesiva" in sintomas_set and "vision_borrosa" in sintomas_set)
    ):
        return {
            "nivel": "medio",
            "recomendacion": "Mantente hidratado, descansa y considera consultar a un médico si los síntomas persisten, empeoran o se combinan con fiebre alta."
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
    diagnosticos = normalizar_resultados(consultar_prolog(sintomas_limpios))
    riesgo = consultar_clisp(sintomas_limpios)

    return {
        "sintomas_recibidos": [s.replace("_", " ") for s in sintomas_limpios],
        "diagnosticos_posibles": diagnosticos,
        "riesgo": riesgo,
        "aviso": "Este sistema es educativo y no sustituye la valoración de un médico profesional."
    }
