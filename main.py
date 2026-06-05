% Base de conocimiento para orientación médica general.
% Proyecto educativo: no sustituye consulta médica.

sintoma(gripe, fiebre).
sintoma(gripe, tos).
sintoma(gripe, dolor_cabeza).
sintoma(gripe, fatiga).
sintoma(gripe, dolor_garganta).
sintoma(gripe, dolor_muscular).
sintoma(gripe, escalofrios).

sintoma(resfriado, tos).
sintoma(resfriado, estornudos).
sintoma(resfriado, congestion_nasal).
sintoma(resfriado, escurrimiento_nasal).
sintoma(resfriado, dolor_garganta).

sintoma(covid_o_infeccion_respiratoria, fiebre).
sintoma(covid_o_infeccion_respiratoria, tos_seca).
sintoma(covid_o_infeccion_respiratoria, fatiga).
sintoma(covid_o_infeccion_respiratoria, dolor_garganta).
sintoma(covid_o_infeccion_respiratoria, perdida_olfato).
sintoma(covid_o_infeccion_respiratoria, dolor_muscular).

sintoma(bronquitis, tos).
sintoma(bronquitis, tos_con_flema).
sintoma(bronquitis, fatiga).
sintoma(bronquitis, dolor_pecho).
sintoma(bronquitis, dificultad_respirar).

sintoma(sinusitis, congestion_nasal).
sintoma(sinusitis, dolor_cabeza).
sintoma(sinusitis, escurrimiento_nasal).
sintoma(sinusitis, dolor_garganta).
sintoma(sinusitis, fatiga).

sintoma(alergia_respiratoria, estornudos).
sintoma(alergia_respiratoria, picazon_ojos).
sintoma(alergia_respiratoria, ojos_llorosos).
sintoma(alergia_respiratoria, congestion_nasal).
sintoma(alergia_respiratoria, escurrimiento_nasal).

sintoma(gastroenteritis, nauseas).
sintoma(gastroenteritis, vomito).
sintoma(gastroenteritis, diarrea).
sintoma(gastroenteritis, dolor_abdominal).
sintoma(gastroenteritis, fiebre).

sintoma(gastritis_o_reflujo, dolor_abdominal).
sintoma(gastritis_o_reflujo, acidez).
sintoma(gastritis_o_reflujo, nauseas).
sintoma(gastritis_o_reflujo, vomito).

sintoma(posible_cuadro_respiratorio_grave, dolor_pecho).
sintoma(posible_cuadro_respiratorio_grave, dificultad_respirar).
sintoma(posible_cuadro_respiratorio_grave, fiebre_alta).
sintoma(posible_cuadro_respiratorio_grave, fatiga).

sintoma(migrana_o_cefalea, dolor_cabeza).
sintoma(migrana_o_cefalea, mareo).
sintoma(migrana_o_cefalea, nauseas).
sintoma(migrana_o_cefalea, sensibilidad_luz).

sintoma(otitis, dolor_oido).
sintoma(otitis, fiebre).
sintoma(otitis, mareo).
sintoma(otitis, dolor_cabeza).

sintoma(infeccion_urinaria, ardor_orinar).
sintoma(infeccion_urinaria, orina_frecuente).
sintoma(infeccion_urinaria, dolor_abdominal).
sintoma(infeccion_urinaria, dolor_espalda_baja).
sintoma(infeccion_urinaria, fiebre).

sintoma(posible_diabetes, sed_excesiva).
sintoma(posible_diabetes, hambre_excesiva).
sintoma(posible_diabetes, orina_frecuente).
sintoma(posible_diabetes, vision_borrosa).
sintoma(posible_diabetes, perdida_peso).
sintoma(posible_diabetes, fatiga).

sintoma(ansiedad_o_estres, ansiedad).
sintoma(ansiedad_o_estres, palpitaciones).
sintoma(ansiedad_o_estres, insomnio).
sintoma(ansiedad_o_estres, mareo).
sintoma(ansiedad_o_estres, dolor_pecho).

sintoma(posible_infeccion_sistemica, fiebre_alta).
sintoma(posible_infeccion_sistemica, escalofrios).
sintoma(posible_infeccion_sistemica, dolor_muscular).
sintoma(posible_infeccion_sistemica, dolor_articulaciones).
sintoma(posible_infeccion_sistemica, sarpullido).

% Devuelve enfermedades sin repetir para evitar que una enfermedad aparezca varias veces.
enfermedades_unicas(Lista) :-
    setof(E, S^sintoma(E, S), Lista).

coincide(SintomasUsuario, Enfermedad, Sintoma) :-
    sintoma(Enfermedad, Sintoma),
    member(Sintoma, SintomasUsuario).

contar_sintomas_enfermedad(Enfermedad, Total) :-
    findall(S, sintoma(Enfermedad, S), Lista),
    length(Lista, Total).

resultado_enfermedad(SintomasUsuario, Enfermedad, resultado(Enfermedad, Coincidencias, Porcentaje)) :-
    findall(S, coincide(SintomasUsuario, Enfermedad, S), Coincidencias),
    length(Coincidencias, Cantidad),
    Cantidad > 0,
    contar_sintomas_enfermedad(Enfermedad, Total),
    Porcentaje is (Cantidad / Total) * 100.

diagnosticar(SintomasUsuario, ResultadoOrdenado) :-
    enfermedades_unicas(Enfermedades),
    findall(R, (member(E, Enfermedades), resultado_enfermedad(SintomasUsuario, E, R)), Resultados),
    predsort(comparar_resultados, Resultados, ResultadoOrdenado).

comparar_resultados(Orden, resultado(_, _, P1), resultado(_, _, P2)) :-
    compare(OrdenTemporal, P2, P1),
    (OrdenTemporal = (=) -> Orden = (<) ; Orden = OrdenTemporal).
