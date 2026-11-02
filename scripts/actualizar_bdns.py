#!/usr/bin/env python3
"""Descarga convocatorias de la BDNS y genera data/convocatorias.json.

Solo usa la biblioteca estándar para que la acción de GitHub no instale nada.

Uso:
    python scripts/actualizar_bdns.py              # regenera los datos
    python scripts/actualizar_bdns.py --explorar   # vuelca los catálogos de la API
    python scripts/actualizar_bdns.py --dias 30    # ventana de descarga en días

Los nombres de endpoints, parámetros y campos están pendientes de verificar
contra el Swagger oficial (ver docs/fuentes.md). Se han aislado en las
constantes de arriba para que ajustarlos sea un cambio pequeño.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

API_BASE = "https://www.infosubvenciones.es/bdnstrans/api"
PORTAL = "GE"  # portal general de la BDNS
PAGE_SIZE = 200
PAUSA_SEGUNDOS = 0.3  # entre peticiones, para no castigar la API pública
USER_AGENT = "ayudas-abiertas/0.1 (+https://github.com/remiun/ayudas-abiertas)"

RAIZ = Path(__file__).resolve().parent.parent
RUTA_SALIDA = RAIZ / "data" / "convocatorias.json"
RUTA_META = RAIZ / "data" / "meta.json"
RUTA_RAW = RAIZ / "data" / "raw"

# Catálogos de la API que conviene volcar antes de fijar los filtros.
CATALOGOS = {
    "regiones": "/regiones",
    "finalidades": "/finalidades",
    "instrumentos": "/instrumentos",
    # Nombres por confirmar: la API devuelve 404 en /tiposbeneficiario y /tiposadministracion.
    "beneficiarios": "/beneficiarios",
    "tiposbeneficiarios": "/tiposbeneficiarios",
    "organos": "/organos",
    "sectores": "/sectores",
    "actividades": "/actividades",
}

# Palabras que identifican a personas físicas en la descripción del tipo
# de beneficiario. Se usa texto y no códigos hasta confirmar los códigos reales.
MARCAS_PERSONA_FISICA = ("PERSONAS FÍSICAS", "PERSONAS FISICAS")


def peticion(ruta: str, params: dict | None = None, intentos: int = 3) -> dict | list:
    """GET a la API con reintentos sencillos. Devuelve el JSON decodificado."""
    params = {"vpd": PORTAL, **(params or {})}
    url = f"{API_BASE}{ruta}?{urllib.parse.urlencode(params, doseq=True)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    ultimo_error: Exception | None = None
    for intento in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise RuntimeError(f"La API no tiene {ruta} (404)") from exc
            ultimo_error = exc
            print(f"  aviso: fallo {intento}/{intentos} en {ruta}: {exc}", file=sys.stderr)
            time.sleep(2 * intento)
            continue
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            ultimo_error = exc
            print(f"  aviso: fallo {intento}/{intentos} en {ruta}: {exc}", file=sys.stderr)
            time.sleep(2 * intento)
    raise RuntimeError(f"La API no respondió en {ruta}: {ultimo_error}")


def fecha_api(d: date) -> str:
    """La BDNS usa dd/mm/aaaa en los parámetros de fecha."""
    return d.strftime("%d/%m/%Y")


def fecha_iso(valor: str | None) -> str | None:
    """Normaliza fechas de la API a AAAA-MM-DD. Devuelve None si no se reconoce."""
    if not valor:
        return None
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(valor[:26], formato).date().isoformat()
        except ValueError:
            continue
    return None


def explorar() -> None:
    """Vuelca los catálogos y una página de búsqueda para inspeccionar campos reales."""
    RUTA_RAW.mkdir(parents=True, exist_ok=True)
    for nombre, ruta in CATALOGOS.items():
        try:
            datos = peticion(ruta)
        except RuntimeError as exc:
            print(f"{nombre}: {exc}")
            continue
        destino = RUTA_RAW / f"{nombre}.json"
        destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        tamano = len(datos) if isinstance(datos, list) else len(datos.get("content", datos))
        print(f"{nombre}: {tamano} elementos -> {destino.relative_to(RAIZ)}")

    hoy = date.today()
    pagina = peticion(
        "/convocatorias/busqueda",
        {"page": 0, "pageSize": 5, "fechaDesde": fecha_api(hoy - timedelta(days=7)), "fechaHasta": fecha_api(hoy)},
    )
    destino = RUTA_RAW / "busqueda_muestra.json"
    destino.write_text(json.dumps(pagina, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"búsqueda de muestra -> {destino.relative_to(RAIZ)}")

    elementos = pagina.get("content", []) if isinstance(pagina, dict) else pagina
    if elementos:
        num = elementos[0].get("numeroConvocatoria")
        detalle = peticion("/convocatorias", {"numConv": num})
        destino = RUTA_RAW / "detalle_muestra.json"
        destino.write_text(json.dumps(detalle, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"detalle de {num} -> {destino.relative_to(RAIZ)}")


def buscar_convocatorias(desde: date, hasta: date) -> list[dict]:
    """Recorre todas las páginas de la búsqueda entre dos fechas de publicación."""
    resultados: list[dict] = []
    pagina = 0
    while True:
        datos = peticion(
            "/convocatorias/busqueda",
            {
                "page": pagina,
                "pageSize": PAGE_SIZE,
                "fechaDesde": fecha_api(desde),
                "fechaHasta": fecha_api(hasta),
                "order": "fechaRecepcion",
                "direccion": "desc",
            },
        )
        contenido = datos.get("content", []) if isinstance(datos, dict) else datos
        resultados.extend(contenido)
        total_paginas = datos.get("totalPages", 1) if isinstance(datos, dict) else 1
        print(f"  página {pagina + 1}/{total_paginas}: {len(contenido)} convocatorias")
        pagina += 1
        if pagina >= total_paginas or not contenido:
            break
        time.sleep(PAUSA_SEGUNDOS)
    return resultados


def es_para_personas(detalle: dict) -> bool:
    tipos = detalle.get("tiposBeneficiarios") or detalle.get("tipoBeneficiario") or []
    if isinstance(tipos, dict):
        tipos = [tipos]
    for tipo in tipos:
        texto = tipo.get("descripcion", "") if isinstance(tipo, dict) else str(tipo)
        if any(marca in texto.upper() for marca in MARCAS_PERSONA_FISICA):
            return True
    return False


def organo_texto(detalle: dict) -> str:
    organo = detalle.get("organo") or {}
    if isinstance(organo, dict):
        partes = [organo.get("nivel1"), organo.get("nivel2"), organo.get("nivel3")]
        return " · ".join(p for p in partes if p)
    return str(organo)


def lista_descripciones(valor) -> list[str]:
    if not valor:
        return []
    if isinstance(valor, dict):
        valor = [valor]
    return [v.get("descripcion", str(v)) if isinstance(v, dict) else str(v) for v in valor]


def normalizar(detalle: dict) -> dict:
    """Reduce el detalle de la API a los campos que usa la web."""
    num = detalle.get("numeroConvocatoria") or detalle.get("codigoBDNS")
    return {
        "id": str(num),
        "titulo": (detalle.get("descripcion") or "").strip(),
        "organo": organo_texto(detalle),
        "ambito": (detalle.get("tipoAdministracion") or detalle.get("nivel1") or "").strip(),
        "regiones": lista_descripciones(detalle.get("regiones")),
        "beneficiarios": lista_descripciones(detalle.get("tiposBeneficiarios")),
        "finalidad": (detalle.get("finalidad") or {}).get("descripcion") if isinstance(detalle.get("finalidad"), dict) else detalle.get("finalidad"),
        "instrumentos": lista_descripciones(detalle.get("instrumentos")),
        "presupuesto": detalle.get("presupuestoTotal"),
        "fechaPublicacion": fecha_iso(detalle.get("fechaRecepcion")),
        "plazoInicio": fecha_iso(detalle.get("fechaInicioSolicitud")),
        "plazoFin": fecha_iso(detalle.get("fechaFinSolicitud")),
        "plazoTexto": (detalle.get("textInicio") or detalle.get("textFin") or "").strip() or None,
        "abierto": detalle.get("abierto"),
        "urlBases": detalle.get("urlBasesReguladoras"),
        "urlSede": detalle.get("sedeElectronica"),
        "urlFicha": f"https://www.infosubvenciones.es/bdnstrans/{PORTAL}/es/convocatoria/{num}",
    }


def cargar_existentes() -> dict[str, dict]:
    if not RUTA_SALIDA.exists():
        return {}
    datos = json.loads(RUTA_SALIDA.read_text(encoding="utf-8"))
    return {c["id"]: c for c in datos}


def sigue_vigente(conv: dict, hoy: date) -> bool:
    """Una ayuda deja de mostrarse cuando su plazo cerró hace más de 7 días."""
    fin = conv.get("plazoFin")
    if not fin:
        return conv.get("abierto") is not False
    return date.fromisoformat(fin) >= hoy - timedelta(days=7)


def actualizar(dias: int) -> None:
    hoy = date.today()
    desde = hoy - timedelta(days=dias)
    print(f"Descargando convocatorias publicadas entre {desde} y {hoy}...")
    resumen = buscar_convocatorias(desde, hoy)

    existentes = cargar_existentes()
    nuevas = 0
    for item in resumen:
        num = item.get("numeroConvocatoria")
        if not num or str(num) in existentes:
            continue
        time.sleep(PAUSA_SEGUNDOS)
        try:
            detalle = peticion("/convocatorias", {"numConv": num})
        except RuntimeError as exc:
            print(f"  aviso: sin detalle para {num}: {exc}", file=sys.stderr)
            continue
        if not es_para_personas(detalle):
            continue
        existentes[str(num)] = normalizar(detalle)
        nuevas += 1

    vigentes = [c for c in existentes.values() if sigue_vigente(c, hoy)]
    vigentes.sort(key=lambda c: (c.get("plazoFin") or "9999-12-31", c.get("fechaPublicacion") or ""))

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_SALIDA.write_text(json.dumps(vigentes, ensure_ascii=False, indent=1), encoding="utf-8")
    RUTA_META.write_text(
        json.dumps(
            {
                "actualizado": datetime.now().isoformat(timespec="minutes"),
                "total": len(vigentes),
                "nuevasEnEstaEjecucion": nuevas,
                "ventanaDias": dias,
                "fuente": "Base de Datos Nacional de Subvenciones",
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"Listo: {len(vigentes)} ayudas vigentes para personas ({nuevas} nuevas).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--explorar", action="store_true", help="volcar catálogos y muestras en data/raw/")
    parser.add_argument("--dias", type=int, default=45, help="días hacia atrás que se consultan (por defecto 45)")
    args = parser.parse_args()
    if args.explorar:
        explorar()
    else:
        actualizar(args.dias)
    return 0


if __name__ == "__main__":
    sys.exit(main())
