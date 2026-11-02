# Ayudas Abiertas

Buscador web gratuito de ayudas públicas abiertas en España para personas físicas, con datos abiertos de la BDNS.

## Restricciones que mandan
- Coste de operación cero: web estática en GitHub Pages, datos generados por una acción de GitHub. Sin servidor, sin base de datos, sin API de pago.
- Sin cuentas, sin anuncios, sin cookies de rastreo ni analítica de terceros.
- Solo datos de fuentes públicas y oficiales. Cada ayuda enlaza a su ficha oficial. La web orienta, no tramita ni promete derechos.
- Accesible y usable en móvil primero: la mayoría de la gente llegará desde el teléfono.
- Dedicación prevista: 1-2 horas al día. Cambios pequeños, que dejen la web siempre en un estado publicable.

## Idioma
- Español de España en interfaz, documentación, comentarios y commits.
- Identificadores de código en inglés.

## Estructura
- `index.html`, `assets/`: la web. HTML, CSS y JavaScript sin frameworks ni paso de compilación.
- `data/convocatorias.json`: datos generados. No se edita a mano.
- `scripts/actualizar_bdns.py`: descarga y filtrado. Solo biblioteca estándar de Python.
- `.github/workflows/`: actualización nocturna.
- `docs/`: fuentes, decisiones y notas.

## Comandos
- `python scripts/actualizar_bdns.py --explorar`: volcar catálogos de la API.
- `python scripts/actualizar_bdns.py`: regenerar los datos.
- `python -m http.server 8000`: probar la web en local.

## Git
- Commits en español con prefijo (`feat`, `fix`, `docs`, `chore`, `refactor`).
- Trabajo directo en `main` mientras el proyecto sea de una persona. Nunca force-push.
