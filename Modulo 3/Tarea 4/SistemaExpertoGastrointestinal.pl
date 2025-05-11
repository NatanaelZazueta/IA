sistema_experto :-
    writeln("Sistema Experto para el Diagnóstico de Enfermedades Gastrointestinales"),
    hipotesis(Enfermedad),
    write('Tu diagnóstico probable es: '),
    writeln(Enfermedad),
    deshacer, !.

% Hipótesis de diagnóstico
hipotesis(gastroenteritis) :- gastroenteritis.
hipotesis(apendicitis) :- apendicitis.
hipotesis(erge) :- erge.
hipotesis(ulcera_peptica) :- ulcera_peptica.
hipotesis(enfermedad_celiaca) :- enfermedad_celiaca.
hipotesis(sii) :- sii.
hipotesis(colecistitis_aguda) :- colecistitis_aguda.
hipotesis(colitis_ulcerosa) :- colitis_ulcerosa.
hipotesis(crohn) :- crohn.
hipotesis(hemorragia_digestiva_alta) :- hemorragia_digestiva_alta.
hipotesis(diverticulitis) :- diverticulitis.
hipotesis(intolerancia_lactosa) :- intolerancia_lactosa.
hipotesis(cancer_colorrectal) :- cancer_colorrectal.
hipotesis(cirrosis_hepatica) :- cirrosis_hepatica.
hipotesis(desconocido).

% Reglas
gastroenteritis :-
    verificar(diarrea_liquida),
    verificar(dolor_colico),
    verificar(nauseas),
    verificar(vomito),
    verificar(fiebre_leve),
    writeln('').

apendicitis :-
    verificar(dolor_cuadrante_inferior_derecho),
    verificar(fiebre),
    verificar(nauseas),
    verificar(leucocitos_altos),
    writeln('').

erge :-
    verificar(ardor_en_pecho_postcomida),
    verificar(regurgitacion_acida_frecuente),
    verificar(mejora_antiacido),
    writeln('').

ulcera_peptica :-
    (verificar(dolor_mejora_al_comer) ; verificar(dolor_mejora_con_antiacidos)),
    verificar(uso_AINES),
    writeln('').

enfermedad_celiaca :-
    verificar(diarrea_cronica),
    verificar(perdida_peso),
    verificar(distension_abdominal),
    verificar(anemia_ferropenica),
    antiverificar(sangrado_aparente),
    writeln('').

sii :-
    verificar(dolor_recurrente),
    verificar(mejora_post_evacuacion),
    (verificar(diarrea) ; verificar(estrenimiento)),
    writeln('').

colecistitis_aguda :-
    verificar(dolor_hipocondrio_derecho),
    verificar(nauseas),
    verificar(fiebre),
    verificar(murphy_positivo),
    writeln('').

colitis_ulcerosa :-
    verificar(diarrea_con_sangre_y_moco),
    verificar(dolor_abdominal),
    verificar(urgencia_defecatoria),
    verificar(perdida_peso),
    writeln('').

crohn :-
    verificar(dolor_abdominal_cronico),
    verificar(perdida_peso),
    verificar(fiebre),
    (verificar(diarrea_con_sangre) ; verificar(diarrea)),
    writeln('').

hemorragia_digestiva_alta :-
    (verificar(hematemesis) ; verificar(melena)),
    writeln('').

diverticulitis :-
    verificar(dolor_abdominal_cuadrante_inferior_izquierdo),
    verificar(fiebre),
    verificar(estrenimiento_reciente),
    writeln('').

intolerancia_lactosa :-
    verificar(distension_abdominal),
    verificar(flatulencias),
    verificar(diarrea_acuosa),
    verificar(consumo_de_lacteos),
    writeln('').

cancer_colorrectal :-
    verificar(sangrado_rectal_intermitente),
    verificar(perdida_peso),
    verificar(anemia),
    verificar(cambio_habito_intestinal),
    writeln('').

cirrosis_hepatica :-
    verificar(ictericia),
    verificar(ascitis),
    verificar(fatiga_cronica),
    verificar(alcoholismo_prolongado),
    writeln('').

% Interacción

preguntar(Sintoma) :-
    write('¿Presenta el siguiente síntoma: '), write(Sintoma), write('? (si/no): '),
    read(Respuesta),
    nl,
    ((Respuesta == si) -> assert(si(Sintoma)) ; assert(no(Sintoma)), fail).

anti_preguntar(Sintoma) :-
    write('¿Se descarta el siguiente síntoma: '), write(Sintoma), write('? (si/no): '),
    read(Respuesta),
    nl,
    ((Respuesta == no) -> assert(no(Sintoma)) ; assert(si(Sintoma)), fail).

:- dynamic si/1, no/1.

verificar(S) :-
    (si(S) -> true ; (no(S) -> fail ; preguntar(S))).

antiverificar(S) :-
    (no(S) -> true ; (si(S) -> fail ; anti_preguntar(S))).

deshacer :- retract(si(_)), fail.
deshacer :- retract(no(_)), fail.
deshacer.