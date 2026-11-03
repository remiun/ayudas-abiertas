# Perfiles de destinatario ("Para quién")

## Qué es y qué no es

El filtro "Para quién" clasifica cada convocatoria según **a quién parece dirigida por su título**. Es una clasificación propia de Ayudas Abiertas, orientativa, hecha con expresiones regulares en `scripts/actualizar_bdns.py` (lista `PERFILES`). No modifica ningún dato oficial: se guarda en un campo aparte, `perfiles`, y la web lo anuncia como orientativo.

**La BDNS no publica requisitos personales.** No hay campos de edad, sexo, renta, patrimonio, situación familiar ni nacionalidad. Esos requisitos están en las bases y en la convocatoria, normalmente en PDF, y solo allí se puede comprobar si una persona concreta puede pedir la ayuda. Por eso:

- No existe filtro por renta ni patrimonio. Un umbral como "no superar 3 veces el IPREM" solo aparece dentro del documento. Si en el futuro se extrae, será con la misma regla: etiquetado como lectura nuestra y con enlace al original.
- No existe filtro por religión. Las administraciones públicas españolas no conceden ayudas a personas por su religión, y la BDNS no recoge ese dato.
- "Mujeres", "Jóvenes" o "Personas mayores" significan que el título lo menciona, no que la convocatoria excluya a los demás ni que incluya a todas.

## Perfiles

En este orden en la web. Una convocatoria puede tener varios. Si no encaja en ninguno, queda como "Otros".

| Perfil | Pistas en el título (castellano y lenguas cooficiales) |
| --- | --- |
| Estudiantes | beca, estudio, alumnado, universitario, máster, material escolar, comedor escolar, grado, TFG; beques, bolsas, ikasle |
| Jóvenes | joven, juventud, carné joven, menores de 30 o 35, emancipación; joves, mocidade, gazte |
| Familias e infancia | familia, natalidad, nacimiento, hijos, infancia, guardería, conciliación, monoparental, numerosa; infants, nenos |
| Personas mayores | mayores, tercera edad, jubilados, pensionistas, teleasistencia; gent gran, maiores, adineko |
| Mujeres | mujer, violencia de género, igualdad, maternidad; dona, muller, emakume |
| Discapacidad y dependencia | discapacidad, dependencia, movilidad reducida, cuidadores, accesibilidad |
| Desempleo y empleo | desempleo, paro, inserción laboral, contratación, prácticas; atur, ocupació, emprego, enplegu |
| Vivienda | vivienda, alquiler, hipoteca, rehabilitación, IBI; habitatge, lloguer, vivenda, etxebizitza |
| Pocos ingresos y emergencia social | emergencia social, vulnerabilidad, renta mínima, suministros, alimentos, ayudas económicas, servicios sociales |
| Salud | salud, tratamiento, medicamentos, gafas, ortodoncia, celiaquía, terapia |
| Deportistas | deportista, deporte, atleta, federado; esport, kirol |
| Cultura y creación | artistas, creación, música, teatro, danza, cine, literatura, residencias |
| Investigación | investigación, predoctoral, posdoctoral, tesis, doctorado |
| Transporte y movilidad | transporte, bono bus, taxi, vehículo, carné de conducir, bicicleta |
| Energía y hogar | eficiencia energética, autoconsumo, placas solares, calderas, electrodomésticos |
| Campo, mar y medio rural | agricultura, ganadería, pesca, apicultura, rural, forestal, caza |
| Autónomos y emprendedores | autónomos, emprendimiento, negocio, comercio, hostelería |
| Migración y retorno | inmigración, refugiados, asilo, retorno, emigrantes, acogida |
| Víctimas y catástrofes | víctimas, terrorismo, catástrofe, DANA, inundaciones, incendio, damnificados |
| Nacimiento, bodas y defunciones | sepelio, entierro, defunción, matrimonio |
| Asociaciones y voluntariado | voluntariado, participación ciudadana, vecinal |
| Concursos y premios | concurso, certamen, premio, himno; concurs, premi, lehiaketa |

## Cobertura con los datos del 2026-11-03

De 1.863 convocatorias. 1.416 reciben al menos un perfil y el resto queda en "Otros". Las que quedan sin clasificar suelen ser convenios con entidades concretas o títulos sin información útil. Cualquier mejora se hace añadiendo pistas a la lista y volviendo a clasificar; la clasificación se recalcula entera en cada actualización nocturna solo para las convocatorias nuevas o refrescadas, así que un cambio de reglas obliga a reclasificar los datos existentes con un script de una línea.
