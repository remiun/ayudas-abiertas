# Hoja de ruta

Dedicación prevista: 1-2 horas al día. Cada paso deja la web publicable. Fechas absolutas; se actualiza al cerrar cada paso.

## Hecho

- 2026-11-02. Repositorio, web estática con filtros, script de descarga con la biblioteca estándar, acción nocturna, primera carga real (1.863 ayudas vigentes para personas, 60 días).
- 2026-11-03. Aviso legal de la BDNS volcado íntegro y convertido en principio número uno (`docs/aviso-legal.md`): cita literal de origen, fecha en cada tarjeta, aviso de independencia, campo `advertencia` conservado, enlace correcto a la ficha oficial. GitHub Pages activado.

## Fase 1. Que sea útil de verdad (noviembre de 2026)

1. **Comprobar la actualización nocturna** durante una semana: que corre, que no falla y cuántas nuevas trae al día.
2. **Filtro por provincia.** El grueso de las ayudas es local; la comunidad se queda corta. Los datos ya traen el código NUTS 3.
3. **Plazo estimado a partir del texto.** Más de la mitad de las convocatorias solo dicen "15 días hábiles desde la publicación en el BOP". Calcular una fecha estimada, marcarla claramente como estimación propia y nunca sustituir el texto oficial.
4. **Portada con sentido:** las que cierran esta semana, las nuevas de hoy, y accesos por tema (vivienda, estudios, familia, mayores, empleo, dependencia).
5. **Página "Cómo funciona"** en lenguaje claro: de dónde salen los datos, qué no es esta web, cómo comprobar una ayuda en la fuente oficial.

## Fase 2. Llegar a más gente (diciembre de 2026)

6. **Enlaces compartibles**: cada filtro y cada ayuda con su URL, para pasarlas por WhatsApp.
7. **Suscripción sin cuenta**: canal RSS por comunidad o tema, generado como ficheros estáticos.
8. **Autónomos** como filtro opcional, tipo de beneficiario 3, separado por defecto para no mezclar con empresas.
9. **Accesibilidad revisada**: lector de pantalla, contraste, tamaños, navegación con teclado.
10. **Rendimiento**: partir el JSON por comunidad si pasa de 2 MB.

## Fase 3. Explicar, no solo listar (2027)

11. **Resumen en lenguaje claro** de cada convocatoria, generado en local con un modelo abierto, revisado por muestreo y siempre etiquetado como "resumen no oficial" con enlace a la ficha. Hay que medir antes la calidad con una muestra de 50.
12. **Otras fuentes oficiales** que lleguen antes que la BDNS: boletines autonómicos. Solo si la calidad lo justifica y con las mismas garantías legales.

## Fuera de alcance, salvo decisión expresa

- Concesiones, beneficiarios o cualquier dato personal: lo veta el aviso legal.
- Cuentas de usuario, anuncios, analítica de terceros.
- Tramitar o rellenar solicitudes en nombre de nadie.
