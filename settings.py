;;; Evaluador de riesgo en CLISP.
;;; Proyecto educativo: no sustituye consulta médica.

(defun contiene (elemento lista)
  (not (null (member elemento lista))))

(defun evaluar-riesgo (sintomas)
  (cond
    ((or (contiene 'dolor_pecho sintomas)
         (contiene 'dificultad_respirar sintomas)
         (and (contiene 'fiebre_alta sintomas)
              (contiene 'rigidez_cuello sintomas))
         (and (contiene 'fiebre_alta sintomas)
              (contiene 'sarpullido sintomas)))
     'alto)
    ((or (contiene 'fiebre_alta sintomas)
         (and (contiene 'fiebre sintomas)
              (or (contiene 'vomito sintomas)
                  (contiene 'diarrea sintomas)))
         (and (contiene 'ardor_orinar sintomas)
              (contiene 'dolor_espalda_baja sintomas))
         (and (contiene 'sed_excesiva sintomas)
              (contiene 'vision_borrosa sintomas)))
     'medio)
    ((contiene 'fiebre sintomas)
     'medio)
    (t 'bajo)))

(defun recomendacion (nivel)
  (cond
    ((eq nivel 'alto)
     "Busca atención médica inmediata, especialmente si hay dolor en el pecho, dificultad para respirar, fiebre alta con rigidez de cuello o sarpullido.")
    ((eq nivel 'medio)
     "Mantente hidratado, descansa y considera consultar a un médico si los síntomas persisten, empeoran o se combinan con fiebre alta.")
    (t
     "Observa la evolución de los síntomas, descansa y acude a consulta si aparecen señales de alarma.")))

(defun imprimir-riesgo (sintomas)
  (let ((nivel (evaluar-riesgo sintomas)))
    (format t "{\"nivel\":\"~(~A~)\",\"recomendacion\":\"~A\"}~%" nivel (recomendacion nivel))))
