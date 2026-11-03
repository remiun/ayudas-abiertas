# Aviso legal de la BDNS y cómo lo cumplimos

**Principio número uno del proyecto: no infringir en ningún caso las condiciones de uso de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas (SNPSAP).** Ante la duda, se consulta este documento y, si sigue habiendo duda, no se hace.

- Fuente: https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal
- Copia tomada el 2026-11-03 con el flujo `Volcar aviso legal de la BDNS`. El portal indicaba "Última actualización: 02/11/2026" y versión 1.2.4.
- Se vuelve a volcar y comparar al menos una vez al trimestre o cuando cambie la versión del portal.

## Qué nos permite

La reutilización de los documentos del SNPSAP está autorizada para fines comerciales y no comerciales, e incluye expresamente copia, difusión, modificación, adaptación, extracción, reordenación y combinación de la información, con cesión gratuita y no exclusiva de los derechos de propiedad intelectual. Ayudas Abiertas hace extracción, reordenación y difusión de convocatorias, que entra de lleno en lo autorizado.

## Las condiciones y nuestra medida para cada una

| Condición del aviso legal | Medida en Ayudas Abiertas | Dónde |
| --- | --- | --- |
| Prohibido desnaturalizar el sentido de la información. | Se muestran los campos oficiales sin alterar su contenido. Solo se cambia la capitalización de títulos y órganos escritos en mayúsculas. Cualquier resumen o explicación propia futura irá marcado como tal, separado del texto oficial y con enlace a la ficha. | `scripts/actualizar_bdns.py`, `assets/app.js` |
| Citar la fuente con la fórmula "Origen de los datos: Intervención General de la Administración del Estado". | Esa frase literal aparece en el pie de la web y en el README. | `index.html`, `README.md` |
| Mencionar la fecha de la última actualización de los documentos. | Cada tarjeta muestra la fecha de publicación en la BDNS. El pie muestra la fecha de la última extracción. | `assets/app.js`, `data/meta.json` |
| En caso de disociación de datos personales, citarlo. | No aplica: no se tratan datos personales. Solo se usan convocatorias, nunca concesiones ni beneficiarios. | `docs/aviso-legal.md` |
| No indicar ni insinuar que la IGAE participa, patrocina o apoya la reutilización. | Aviso de independencia en el pie y en el README. No se usan logotipos ni la identidad visual del portal. | `index.html`, `README.md` |
| Conservar, sin alterar ni suprimir, los metadatos de fecha de actualización y condiciones de reutilización incluidos en el documento. | El campo `advertencia` que devuelve la API se guarda literal en `data/meta.json`, junto con la URL del aviso legal y la fecha de extracción. | `scripts/actualizar_bdns.py` |

## Otras obligaciones y cómo las respetamos

- **Datos personales.** El aviso solo permite reutilizar datos personales para controlar la actuación pública o con fines históricos, estadísticos o científicos previa disociación. Ayudas Abiertas no descarga concesiones ni ningún dato de beneficiarios. Está prohibido añadir esa funcionalidad.
- **Uso del API.** La Administración puede restringir el acceso ante "manifiesto abuso del servicio". Medidas: una ejecución diaria, descarga incremental solo de lo publicado en los últimos días, pausa entre peticiones, un solo hilo, `User-Agent` identificable con enlace al repositorio, y respeto a las [buenas prácticas de consulta de API de datos.gob.es](https://datos.gob.es/es/blog/limitaciones-la-consulta-de-una-api). Nunca se descarga el histórico completo.
- **Carácter informativo.** La información del portal es meramente informativa y no puede alegarse frente a la Administración. La web lo dice en el pie y enlaza siempre a la ficha oficial para que la persona compruebe requisitos y plazos.
- **Responsabilidad del reutilizador.** El agente reutilizador responde frente a terceros y queda sujeto al régimen sancionador de la Ley 37/2007. Es una razón más para no inventar nada: lo que no esté en la fuente, no se afirma.

## Lista de comprobación antes de cada cambio

- [ ] ¿Sigue apareciendo la cita literal de origen de los datos?
- [ ] ¿Sigue visible la fecha de actualización en tarjetas y pie?
- [ ] ¿Sigue intacto el campo `advertencia` en `data/meta.json`?
- [ ] ¿Algún texto nuevo podría sugerir apoyo o participación de la IGAE?
- [ ] ¿El cambio toca concesiones o datos de personas? Si es así, no se hace.
- [ ] ¿El cambio aumenta el número de peticiones al API? Si es así, justificarlo y mantener la pausa.

## Texto íntegro de las condiciones de uso (copia literal del 2026-11-03)

Condiciones de uso de los datos del SNPSAP

### Obligatoriedad de las condiciones generales
Las presentes condiciones generales, disponibles con carácter permanente bajo https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal , vincularán a cualquier agente reutilizador por el mero hecho de hacer uso de los documentos sometidos a ellas. A estos efectos se entiende por agente reutilizador toda persona, física o jurídica que reutilice información del sector público, ya sea para fines comerciales o no comerciales.

### Contenido del SNPSAP

Según el artículo 7 del Real Decreto 130/2019, de 8 de marzo, por el que se regula la Base de Datos Nacional de Subvenciones y la publicidad de las subvenciones y demás ayudas públicas el SNPSAP proporciona información sobre subvenciones y ayudas públicas según lo establecido en la Ley 38/2003, de 17 de noviembre, General de Subvenciones (LGS); en la Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno; en la normativa emanada de la Unión Europea sobre transparencia de ayudas públicas y ayudas de mínimis; y en cuantas otras normas resulten de aplicación.

El SNPSAP proporciona información sobre convocatorias y concesiones de ayudas públicas.

Los datos personales de los beneficiarios personas físicas, se publican de acuerdo con los principios y la normativa de protección de datos. No se publican las subvenciones o ayudas públicas concedidas a personas físicas cuando:

La información contenida en la BDNS o el propio objeto de la convocatoria proporciona información o datos especialmente protegidos de los beneficiarios o relativos a las categorías especiales de datos relacionados en los artículos 9 y 10 del Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales y a la libre circulación de estos datos y por el que se deroga la Directiva 95/46/CE (Reglamento general de protección de datos).
La persona física se encuentra en una situación de protección especial que pueda verse agravada con la cesión o publicación de sus datos personales, en particular, cuando sea víctima de violencia de género o de otras formas de violencia contra la mujer.

En el primer caso, el órgano convocante es responsable de señalarlo expresamente en la convocatoria si así se ha previsto en las bases reguladoras.

En el segundo caso, el órgano convocante procederá a anonimizar la información que consta en la BDNS, de oficio o a instancia del interesado. Cuando la persona física sea víctima de violencia de género, se aplicará lo previsto en el protocolo de colaboración que se elabore de conformidad con la Disposición adicional séptima de la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y Garantía de los Derechos Digitales.

Tampoco se publicarán las subvenciones concedidas cuando a juicio del órgano convocante su publicidad suponga un perjuicio de los previstos en el apartado 1 del artículo 14 de la Ley 19/2013, de 9 de diciembre, y resulte procedente limitar la publicidad de las subvenciones concedidas según lo establecido en su apartado 2.

La información sobre concesiones permanecerá publicada durante los cuatro años naturales siguientes al año en que se concedió la subvención, siendo retirada automáticamente por el propio SNPSAP transcurrido dicho plazo. En el caso de concesiones a favor de personas físicas, la publicidad se reduce al año de concesión y al año siguiente. No obstante, estos plazos se sustituirán por los establecidos en la normativa europea, en caso de que ésta señale plazos superiores.

El SNPSAP también publica información de las sanciones firmes impuestas por infracciones muy graves en los términos recogidos en el artículo 20.9 de la LGS, cuando así se haya acordado por la autoridad competente, que deberá resolver igualmente acerca del tiempo durante el cual la sanción deberá permanecer publicada en el SNPSAP.


### Autorización de reutilización y cesión no exclusiva de derechos de propiedad intelectual

Las presentes condiciones generales permiten la reutilización de los documentos sometidos a ellas para fines comerciales y no comerciales. Se entiende por reutilización el uso de documentos que obran en poder de los órganos de la Administración General del Estado y los demás organismos y entidades del sector público estatal referidos en el artículo 1.2 del Real Decreto 1495/2011, de 24 de octubre, por el que se desarrolla la Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público estatal, por personas físicas o jurídicas, con fines comerciales o no comerciales, siempre que dicho uso no constituya una actividad administrativa pública. La reutilización autorizada incluye, a modo ilustrativo, actividades como la copia, difusión, modificación, adaptación, extracción, reordenación y combinación de la información.

No obstante, cuando los documentos respecto de los que se pretenda llevar a cabo la reutilización contengan datos de carácter personal, dicha reutilización sólo será posible si tiene por fin el control de la actuación de los gestores públicos (art. 5.1 Ley 19/2013); también se podrá reutilizar esta información con fines históricos, estadísticos o científicos, en cuyo caso los reutilizadores deberán proceder previamente a la disociación de los datos personales.

El concepto de documento es el establecido en el apartado 2 del artículo 3 de la Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público, por lo que comprende toda información cualquiera que sea su soporte material o electrónico así como su forma de expresión gráfica, sonora o en imagen utilizada, incluyendo, en consecuencia, también los datos en sus niveles más desagregados o "en bruto".

Esta autorización conlleva, asimismo, la cesión gratuita y no exclusiva de los derechos de propiedad intelectual, en su caso, correspondientes a tales documentos, autorizándose la realización de actividades de reproducción, distribución, comunicación pública o transformación, necesarias para desarrollar la actividad de reutilización autorizada, en cualquier modalidad y bajo cualquier formato, para todo el mundo y por el plazo máximo permitido por la Ley.


### Condiciones generales para la reutilización

Son de aplicación las siguientes condiciones generales para la reutilización de los documentos sometidos a ellas:

Está prohibido desnaturalizar el sentido de la información.
Debe citarse la fuente de los documentos objeto de la reutilización. Esta cita podrá realizarse de la siguiente manera: "Origen de los datos: Intervención General de la Administración del Estado".
Debe mencionarse la fecha de la última actualización de los documentos objeto de la reutilización, siempre cuando estuviera incluida en el documento original.
En caso de disociación de datos personales deberá citarse su realización y quién la efectúa.
No se podrá indicar, insinuar o sugerir que la Intervención General de la Administración del Estado participa, patrocina o apoya la reutilización que se lleve a cabo con ella.
Deben conservarse, no alterarse ni suprimirse los metadatos sobre la fecha de actualización y las condiciones de reutilización aplicables incluidos, en su caso, en el documento puesto a disposición para su reutilización.

### Exclusión de responsabilidad

El SNPSAP es un portal integrado por la información aportada por diferentes Administraciones y órganos; cada uno de ellos mantiene la propiedad y responsabilidad del contenido suministrado a la BDNS (art. 9.1 del RD 130/2019).

La utilización de los conjuntos de datos se realizará por parte de los usuarios o agentes de la reutilización bajo su propia cuenta y riesgo, correspondiéndoles en exclusiva a ellos responder frente a terceros por daños que pudieran derivarse de ella.

La Intervención General de la Administración del Estado no será responsable del uso que de su información hagan los agentes reutilizadores ni tampoco de los daños sufridos o pérdidas económicas que, de forma directa o indirecta, produzcan o puedan producir perjuicios económicos, materiales o sobre datos, provocados por el uso de la información reutilizada.

La Intervención General de la Administración del Estado no garantiza la continuidad en la puesta a disposición de los documentos reutilizables, ni en contenido ni en forma, ni asume responsabilidades por cualquier error u omisión contenido en ellos.

De acuerdo con lo previsto en el apartado 3 del artículo 9 del Real Decreto 130/2019, la Intervención General de la Administración del Estado es el órgano ante el que se ejercitará el derecho de acceso. Los derechos de oposición, rectificación y cancelación se ejercitarán ante el órgano responsable del suministro de la información.

La información contenida en esta Web procede de fuentes públicas. La Administración presupuestaria no se hace responsable de los daños y perjuicios que pudiera ocasionar la utilización de las herramientas e informaciones contenidas en la web en relación con la adopción de decisiones sobre el inicio, desarrollo o resultado de procedimientos administrativos. Tales decisiones deben ser contrastadas en los centros, organismos o dependencias competentes.

En cualquier caso, la información y contenidos de esta Web no podrán ser alegados en procesos contradictorios con la Administración Pública, no asumiendo responsabilidad alguna por las discrepancias que pudiesen existir entre los documentos impresos de la Administración competente y la publicación electrónica en estas páginas.

La Administración presupuestaria no se responsabiliza de las contestaciones que se realicen a través de las distintas direcciones de correo electrónico que aparecen en estas páginas. La información obtenida a través de los buzones contenidos en estas páginas tiene carácter meramente informativo, sin que en ningún caso pueda derivarse de ella efecto jurídico vinculante alguno (Real Decreto 208/1996, art 4 b).

La Administración presupuestaria se reserva el derecho a realizar cambios en el Portal sin previo aviso, con el objeto de actualizar, corregir, modificar, añadir o eliminar los contenidos del Portal o de su diseño. Asimismo, no se responsabiliza de los contenidos que terceras partes hayan incluido en los hipervínculos a los que se hace referencia en esta página.

Los textos, normativa y en general cualquier información contenida en las páginas de este Portal tienen carácter meramente informativo, por lo que sugerimos compruebe la vigencia y exactitud de los datos en las fuentes administrativas oficiales correspondientes.

La Administración presupuestaria no se responsabiliza de los daños y perjuicios derivados del no borrado de los metadatos en los documentos aportados por otras Administraciones u órganos, salvo aquellos que sean estrictamente necesario para su correcta indexación.


### Responsabilidad del agente reutilizador

El agente reutilizador se halla sometido a la normativa aplicable en materia de reutilización de la información del sector público, incluyendo el régimen sancionador previsto en el artículo 11 de la Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público.


### Accesos al API del sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas

La Administración Presupuestaria, para salvaguardar la protección del acceso libre e irrestricto de los ciudadanos a este Portal y a su información, podrá adoptar medidas restrictivas de acceso al API ante situaciones de manifiesto abuso del servicio, riesgos de seguridad, o uso fraudulento de la información descargada, de acuerdo con las buenas prácticas de gestión de datos abiertos establecidas por el Ministerio para la Transformación Digital y de la Función Pública.

