import json
import os
import requests
from django.shortcuts import render
from .models import Consulta

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8001/consulta")

SINTOMAS = [
    {"valor": "fiebre", "texto": "Fiebre", "descripcion": "Temperatura elevada, sensación de calor, sudoración o escalofríos leves."},
    {"valor": "fiebre_alta", "texto": "Fiebre alta", "descripcion": "Temperatura muy elevada, malestar intenso, escalofríos fuertes o decaimiento."},
    {"valor": "tos", "texto": "Tos", "descripcion": "Expulsión repetida de aire por irritación en garganta o vías respiratorias."},
    {"valor": "tos_seca", "texto": "Tos seca", "descripcion": "Tos sin flemas, irritante, con sensación de garganta raspada."},
    {"valor": "tos_con_flema", "texto": "Tos con flema", "descripcion": "Tos acompañada de moco o secreción en el pecho o garganta."},
    {"valor": "dolor_cabeza", "texto": "Dolor de cabeza", "descripcion": "Presión, punzada o molestia en frente, sienes, nuca o toda la cabeza."},
    {"valor": "congestion_nasal", "texto": "Congestión nasal", "descripcion": "Nariz tapada, dificultad para respirar por la nariz o exceso de mucosidad."},
    {"valor": "escurrimiento_nasal", "texto": "Escurrimiento nasal", "descripcion": "Salida constante de moco claro o espeso por la nariz."},
    {"valor": "estornudos", "texto": "Estornudos", "descripcion": "Expulsiones repentinas de aire por la nariz y boca, usualmente repetidas."},
    {"valor": "dolor_garganta", "texto": "Dolor de garganta", "descripcion": "Ardor, irritación o dolor al tragar saliva, alimentos o bebidas."},
    {"valor": "dolor_muscular", "texto": "Dolor muscular", "descripcion": "Cuerpo cortado, pesadez o dolor en músculos sin esfuerzo físico claro."},
    {"valor": "escalofrios", "texto": "Escalofríos", "descripcion": "Sensación de frío interno, temblores o piel erizada aunque el ambiente no esté frío."},
    {"valor": "fatiga", "texto": "Fatiga", "descripcion": "Cansancio intenso, falta de energía o dificultad para realizar actividades normales."},
    {"valor": "perdida_olfato", "texto": "Pérdida de olfato", "descripcion": "Dificultad para percibir olores o sabores de forma normal."},
    {"valor": "nauseas", "texto": "Náuseas", "descripcion": "Sensación de querer vomitar, asco o malestar en el estómago."},
    {"valor": "vomito", "texto": "Vómito", "descripcion": "Expulsión del contenido del estómago por la boca."},
    {"valor": "diarrea", "texto": "Diarrea", "descripcion": "Evacuaciones líquidas o muy frecuentes, con urgencia para ir al baño."},
    {"valor": "dolor_abdominal", "texto": "Dolor abdominal", "descripcion": "Cólico, presión, ardor o dolor en la zona del estómago o vientre."},
    {"valor": "acidez", "texto": "Acidez", "descripcion": "Ardor en la boca del estómago o sensación de quemazón que sube al pecho."},
    {"valor": "dolor_pecho", "texto": "Dolor de pecho", "descripcion": "Presión, opresión, ardor o dolor en el pecho. Puede ser señal de alarma."},
    {"valor": "dificultad_respirar", "texto": "Dificultad para respirar", "descripcion": "Falta de aire, respiración agitada o sensación de no poder llenar los pulmones."},
    {"valor": "mareo", "texto": "Mareo", "descripcion": "Sensación de inestabilidad, giro, debilidad o que podrías desmayarte."},
    {"valor": "sensibilidad_luz", "texto": "Sensibilidad a la luz", "descripcion": "La luz molesta o empeora el dolor de cabeza o la incomodidad visual."},
    {"valor": "rigidez_cuello", "texto": "Rigidez de cuello", "descripcion": "Dificultad para mover el cuello o dolor fuerte al inclinar la cabeza."},
    {"valor": "picazon_ojos", "texto": "Picazón en ojos", "descripcion": "Comezón, irritación o necesidad de tallarse los ojos."},
    {"valor": "ojos_llorosos", "texto": "Ojos llorosos", "descripcion": "Lagrimeo constante, ojos húmedos o irritados."},
    {"valor": "sarpullido", "texto": "Sarpullido", "descripcion": "Manchas, ronchas, puntos rojos o irritación visible en la piel."},
    {"valor": "dolor_oido", "texto": "Dolor de oído", "descripcion": "Molestia, punzada, presión o sensación de oído tapado."},
    {"valor": "ardor_orinar", "texto": "Ardor al orinar", "descripcion": "Dolor, ardor o molestia al hacer pipí."},
    {"valor": "orina_frecuente", "texto": "Orina frecuente", "descripcion": "Necesidad de orinar muchas veces, incluso con poca cantidad."},
    {"valor": "dolor_espalda_baja", "texto": "Dolor de espalda baja", "descripcion": "Dolor en la parte baja de la espalda, cerca de cintura o riñones."},
    {"valor": "sed_excesiva", "texto": "Sed excesiva", "descripcion": "Necesidad constante de tomar agua, más de lo normal."},
    {"valor": "hambre_excesiva", "texto": "Hambre excesiva", "descripcion": "Apetito muy aumentado aunque ya hayas comido."},
    {"valor": "vision_borrosa", "texto": "Visión borrosa", "descripcion": "Dificultad para enfocar, ver nublado o pérdida momentánea de claridad visual."},
    {"valor": "perdida_peso", "texto": "Pérdida de peso", "descripcion": "Bajar de peso sin intentarlo o sin cambio claro en dieta y actividad."},
    {"valor": "palpitaciones", "texto": "Palpitaciones", "descripcion": "Latidos rápidos, fuertes o irregulares que se sienten en pecho o garganta."},
    {"valor": "ansiedad", "texto": "Ansiedad", "descripcion": "Nerviosismo, preocupación intensa, tensión o sensación de alerta constante."},
    {"valor": "insomnio", "texto": "Insomnio", "descripcion": "Dificultad para dormir, despertar muchas veces o no descansar bien."},
    {"valor": "dolor_articulaciones", "texto": "Dolor de articulaciones", "descripcion": "Dolor en rodillas, muñecas, codos, tobillos u otras articulaciones."},
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
