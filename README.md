# Ayudas Abiertas

Buscador gratuito de ayudas públicas abiertas en España para personas: filtra por comunidad, situación y plazo. Usa los datos abiertos de la Base de Datos Nacional de Subvenciones (BDNS). Sin cuentas, sin anuncios y sin rastreo.

> Estado: en construcción. Primera versión en desarrollo (noviembre de 2026).

## Qué hace

- Muestra las convocatorias de ayudas, becas y subvenciones **abiertas ahora** y dirigidas a **personas físicas**.
- Permite filtrar por comunidad autónoma, tipo de administración, finalidad y texto libre.
- Destaca el **plazo que queda** para solicitar cada ayuda.
- Enlaza siempre a la ficha oficial en la BDNS y a la sede electrónica donde se solicita. Esta web orienta, no tramita.

## Cómo funciona

1. Una acción de GitHub se ejecuta cada noche y descarga de la API pública de la BDNS las convocatorias nuevas o modificadas.
2. Un script filtra las dirigidas a personas y genera un fichero JSON estático en `data/`.
3. La web es estática y se sirve con GitHub Pages. Todo el filtrado ocurre en el navegador.

No hay servidor propio, ni base de datos, ni coste de operación.

## Fuente de datos

Los datos proceden del [Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas](https://www.infosubvenciones.es/), de acceso público según el artículo 20 de la Ley 38/2003 General de Subvenciones. Más detalle en [`docs/fuentes.md`](docs/fuentes.md).

## Desarrollo

Requisitos: Python 3.12 o superior. El script no usa dependencias externas.

```bash
# Explorar los catálogos de la API (regiones, tipos de beneficiario, finalidades)
python scripts/actualizar_bdns.py --explorar

# Descargar y generar data/convocatorias.json
python scripts/actualizar_bdns.py

# Servir la web en local
python -m http.server 8000
```

## Licencia

Código bajo licencia MIT. Los datos conservan las condiciones de la fuente original.
