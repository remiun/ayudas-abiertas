#!/usr/bin/env python3
"""Prueba nombres de parámetros de la búsqueda de la BDNS y vuelca el aviso legal.

Herramienta de desarrollo. Se ejecuta desde el flujo "Explorar API" porque el
entorno de desarrollo no tiene acceso al dominio.
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

API = "https://www.infosubvenciones.es/bdnstrans/api"
UA = "ayudas-abiertas/0.1 (+https://github.com/remiun/ayudas-abiertas)"


def get(ruta: str, params: dict) -> dict:
    url = f"{API}{ruta}?{urllib.parse.urlencode({'vpd': 'GE', **params}, doseq=True)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def total(params: dict) -> str:
    try:
        datos = get("/convocatorias/busqueda", {"page": 0, "pageSize": 1, **params})
        return str(datos.get("totalElements"))
    except Exception as exc:  # noqa: BLE001
        return f"ERROR {exc}"


def main() -> int:
    hoy = date.today()
    base = {"fechaDesde": (hoy - timedelta(days=7)).strftime("%d/%m/%Y"), "fechaHasta": hoy.strftime("%d/%m/%Y")}
    print("== Total últimos 7 días sin filtro:", total(base))
    print("== Sin fechas (todo el histórico):", total({}))
    print("== Formato ISO de fechas:", total({"fechaDesde": (hoy - timedelta(days=7)).isoformat(), "fechaHasta": hoy.isoformat()}))

    print("\n== Candidatos para filtrar por tipo de beneficiario (id 1 = personas físicas):")
    for nombre in ("tiposBeneficiario", "tipoBeneficiario", "tiposBeneficiarios", "beneficiarios", "beneficiario", "idTipoBeneficiario"):
        print(f"  {nombre}=1 ->", total({**base, nombre: 1}), "|", f"{nombre}=3 ->", total({**base, nombre: 3}))

    print("\n== Candidatos para filtrar por región (id 29 = Castilla y León):")
    for nombre in ("regiones", "region", "idRegion", "regionesImpacto"):
        print(f"  {nombre}=29 ->", total({**base, nombre: 29}))

    print("\n== Candidatos para finalidad (id 8 = vivienda):")
    for nombre in ("finalidad", "finalidades", "idFinalidad"):
        print(f"  {nombre}=8 ->", total({**base, nombre: 8}))

    print("\n== Candidatos para tipo de administración:")
    for nombre, valor in (("tipoAdministracion", "C"), ("tipoAdministracion", "A"), ("tipoAdministracion", "L"), ("tiposAdministracion", "C"), ("administracion", "C")):
        print(f"  {nombre}={valor} ->", total({**base, nombre: valor}))

    print("\n== Solo abiertas:")
    for nombre in ("abierto", "abiertas", "soloAbiertas", "estado"):
        print(f"  {nombre}=true ->", total({**base, nombre: "true"}))

    print("\n== Orden:")
    for order in ("fechaRecepcion", "numeroConvocatoria", "fechaFinSolicitud"):
        print(f"  order={order} ->", total({**base, "order": order, "direccion": "desc"}))

    print("\n== Muestra de 3 convocatorias con tiposBeneficiario=1 (si el parámetro existe):")
    try:
        datos = get("/convocatorias/busqueda", {"page": 0, "pageSize": 3, **base, "tiposBeneficiario": 1})
        for item in datos.get("content", []):
            det = get("/convocatorias", {"numConv": item["numeroConvocatoria"]})
            resumen = {k: det.get(k) for k in ("codigoBDNS", "descripcion", "tiposBeneficiarios", "regiones", "descripcionFinalidad", "abierto", "fechaInicioSolicitud", "fechaFinSolicitud", "textFin", "sedeElectronica", "urlBasesReguladoras", "tipoConvocatoria", "documentos")}
            print(json.dumps(resumen, ensure_ascii=False)[:1500])
    except Exception as exc:  # noqa: BLE001
        print("  no disponible:", exc)

    print("\n== Aviso legal (texto plano, recortado):")
    try:
        req = urllib.request.Request("https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            pagina = resp.read().decode("utf-8", errors="replace")
        texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", pagina, flags=re.S | re.I)
        texto = re.sub(r"<[^>]+>", " ", texto)
        texto = html.unescape(re.sub(r"\s+", " ", texto))
        print(texto[:6000])
    except Exception as exc:  # noqa: BLE001
        print("  no disponible:", exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
