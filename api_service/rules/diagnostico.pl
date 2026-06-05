% Base de conocimiento para orientación médica general.
% Proyecto educativo: no sustituye consulta médica.

sintoma(gripe, fiebre).
sintoma(gripe, tos).
sintoma(gripe, dolor_cabeza).
sintoma(gripe, fatiga).
sintoma(gripe, dolor_garganta).

sintoma(resfriado, tos).
sintoma(resfriado, estornudos).
sintoma(resfriado, congestion_nasal).
sintoma(resfriado, dolor_garganta).

sintoma(gastroenteritis, nauseas).
sintoma(gastroenteritis, vomito).
sintoma(gastroenteritis, diarrea).
sintoma(gastroenteritis, dolor_abdominal).

sintoma(posible_cuadro_respiratorio_grave, dolor_pecho).
sintoma(posible_cuadro_respiratorio_grave, dificultad_respirar).
sintoma(posible_cuadro_respiratorio_grave, fiebre).

sintoma(migrana_o_cefalea, dolor_cabeza).
sintoma(migrana_o_cefalea, mareo).
sintoma(migrana_o_cefalea, nauseas).

enfermedad(E) :- sintoma(E, _).

coincide(SintomasUsuario, Enfermedad, Sintoma) :-
    sintoma(Enfermedad, Sintoma),
    member(Sintoma, SintomasUsuario).

contar_sintomas_enfermedad(Enfermedad, Total) :-
    findall(S, sintoma(Enfermedad, S), Lista),
    length(Lista, Total).

resultado_enfermedad(SintomasUsuario, resultado(Enfermedad, Coincidencias, Porcentaje)) :-
    enfermedad(Enfermedad),
    findall(S, coincide(SintomasUsuario, Enfermedad, S), Coincidencias),
    length(Coincidencias, Cantidad),
    Cantidad > 0,
    contar_sintomas_enfermedad(Enfermedad, Total),
    Porcentaje is (Cantidad / Total) * 100.

diagnosticar(SintomasUsuario, ResultadoOrdenado) :-
    findall(R, resultado_enfermedad(SintomasUsuario, R), Resultados),
    predsort(comparar_resultados, Resultados, ResultadoOrdenado).

comparar_resultados(Orden, resultado(_, _, P1), resultado(_, _, P2)) :-
    compare(OrdenTemporal, P2, P1),
    (OrdenTemporal = (=) -> Orden = (<) ; Orden = OrdenTemporal).
