#!/usr/bin/env python3
"""Descarga convocatorias de la BDNS dirigidas a personas y genera data/convocatorias.json.

Solo usa la biblioteca estándar para que la acción de GitHub no instale nada.

Uso:
    python scripts/actualizar_bdns.py              # incorpora lo publicado en los últimos días
    python scripts/actualizar_bdns.py --dias 60    # ventana de descarga más amplia
    python scripts/actualizar_bdns.py --explorar   # vuelca los catálogos de la API en data/raw/

Parámetros y campos verificados contra la API el 2026-11-02 (ver docs/fuentes.md).
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
PAGE_SIZE = 100
PAUSA_SEGUNDOS = 0.3  # entre peticiones, para no castigar una API pública
USER_AGENT = "ayudas-abiertas/0.1 (+https://github.com/remiun/ayudas-abiertas)"

# Tipo de beneficiario 1 = "PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA".
# El 3 agrupa pymes y autónomos; queda fuera de momento para no inundar la web de ayudas a empresas.
TIPOS_BENEFICIARIO = (1,)

# Una convocatoria sin fecha de fin publicada se muestra durante este número de días desde su publicación.
DIAS_VIGENCIA_SIN_FECHA = 90
# Una convocatoria con fecha de fin se sigue mostrando unos días después, marcada como cerrada.
DIAS_GRACIA_TRAS_CIERRE = 3

RAIZ = Path(__file__).resolve().parent.parent
RUTA_SALIDA = RAIZ / "data" / "convocatorias.json"
RUTA_META = RAIZ / "data" / "meta.json"
RUTA_RAW = RAIZ / "data" / "raw"

CATALOGOS = {
    "beneficiarios": "/beneficiarios",
    "regiones": "/regiones",
    "finalidades": "/finalidades",
    "instrumentos": "/instrumentos",
    "sectores": "/sectores",
    "actividades": "/actividades",
}

# Nombres legibles de las comunidades por código NUTS 2. La API devuelve "ES41 - CASTILLA Y LEON".
COMUNIDADES = {
    "ES11": "Galicia",
    "ES12": "Principado de Asturias",
    "ES13": "Cantabria",
    "ES21": "País Vasco",
    "ES22": "Comunidad Foral de Navarra",
    "ES23": "La Rioja",
    "ES24": "Aragón",
    "ES30": "Comunidad de Madrid",
    "ES41": "Castilla y León",
    "ES42": "Castilla-La Mancha",
    "ES43": "Extremadura",
    "ES51": "Cataluña",
    "ES52": "Comunitat Valenciana",
    "ES53": "Illes Balears",
    "ES61": "Andalucía",
    "ES62": "Región de Murcia",
    "ES63": "Ciudad de Ceuta",
    "ES64": "Ciudad de Melilla",
    "ES70": "Canarias",
}
TODA_ESPANA = "Toda España"

# Provincias por código NUTS 3. En Canarias y Baleares la API usa islas; se agrupan en su provincia.
PROVINCIAS = {
    "ES111": "A Coruña", "ES112": "Lugo", "ES113": "Ourense", "ES114": "Pontevedra",
    "ES120": "Asturias", "ES130": "Cantabria",
    "ES211": "Araba/Álava", "ES212": "Gipuzkoa", "ES213": "Bizkaia",
    "ES220": "Navarra", "ES230": "La Rioja",
    "ES241": "Huesca", "ES242": "Teruel", "ES243": "Zaragoza",
    "ES300": "Madrid",
    "ES411": "Ávila", "ES412": "Burgos", "ES413": "León", "ES414": "Palencia", "ES415": "Salamanca",
    "ES416": "Segovia", "ES417": "Soria", "ES418": "Valladolid", "ES419": "Zamora",
    "ES421": "Albacete", "ES422": "Ciudad Real", "ES423": "Cuenca", "ES424": "Guadalajara", "ES425": "Toledo",
    "ES431": "Badajoz", "ES432": "Cáceres",
    "ES511": "Barcelona", "ES512": "Girona", "ES513": "Lleida", "ES514": "Tarragona",
    "ES521": "Alicante/Alacant", "ES522": "Castellón/Castelló", "ES523": "Valencia/València",
    "ES531": "Illes Balears", "ES532": "Illes Balears", "ES533": "Illes Balears",
    "ES611": "Almería", "ES612": "Cádiz", "ES613": "Córdoba", "ES614": "Granada", "ES615": "Huelva",
    "ES616": "Jaén", "ES617": "Málaga", "ES618": "Sevilla",
    "ES620": "Murcia", "ES630": "Ceuta", "ES640": "Melilla",
    "ES703": "Santa Cruz de Tenerife", "ES704": "Las Palmas", "ES705": "Las Palmas", "ES706": "Santa Cruz de Tenerife",
    "ES707": "Santa Cruz de Tenerife", "ES708": "Las Palmas", "ES709": "Santa Cruz de Tenerife",
    "ES701": "Las Palmas", "ES702": "Santa Cruz de Tenerife",
}

# Códigos NUTS 1 que la API usa a veces en lugar de la comunidad. Se expanden a sus comunidades.
NUTS1 = {
    "ES1": ["Galicia", "Principado de Asturias", "Cantabria"],
    "ES2": ["País Vasco", "Comunidad Foral de Navarra", "La Rioja", "Aragón"],
    "ES3": ["Comunidad de Madrid"],
    "ES4": ["Castilla y León", "Castilla-La Mancha", "Extremadura"],
    "ES5": ["Cataluña", "Comunitat Valenciana", "Illes Balears"],
    "ES6": ["Andalucía", "Región de Murcia", "Ciudad de Ceuta", "Ciudad de Melilla"],
    "ES7": ["Canarias"],
}

AMBITOS = {"ESTATAL": "Estatal", "ESTADO": "Estatal", "AUTONOMICA": "Autonómica", "LOCAL": "Local", "OTROS": "Otros organismos"}

# Palabras que se mantienen en minúscula al capitalizar nombres de órganos.
MINUSCULAS = {"de", "del", "la", "las", "los", "el", "y", "e", "i", "u", "en", "para", "por", "con", "da", "do", "das", "dos", "na", "no", "eta"}
# Siglas y nombres que se mantienen tal cual.
INVARIABLES = {"IRPF", "IVA", "PIE", "FP", "ESO", "UE", "FEDER", "FSE", "MRR", "EBAU", "PAU", "ONG", "ONGD", "IMV", "PIB", "I+D", "I+D+I", "TIC", "DNI", "NIE", "UNED", "RTVE", "SEPE", "INEM", "SAS", "IES", "CEIP", "AMPA", "CIF", "NIF", "UPV", "UPC", "UAB", "UB", "UV", "UA", "UJI", "UMH", "UCM", "UAM", "UPM", "URJC", "UC3M", "UGR", "US", "UMA", "UCA", "UCO", "UJA", "UHU", "UAL", "UPO", "USC", "UDC", "UVIGO", "ULL", "ULPGC", "UZ", "UIB", "UM", "UCLM", "UEX", "UNIZAR", "UPNA", "EHU", "UPV/EHU", "URV", "UDG", "UDL", "UOC", "UVA", "USAL", "UBU", "ULE", "UNIOVI", "UNICAN", "UNIRIOJA", "UNAV", "UMU", "UPCT", "UNIA", "UIMP", "CSIC", "ICO", "IDAE", "ICEX", "CDTI", "ENISA", "INJUVE", "IMSERSO", "INSS", "TGSS", "AEAT", "DGT", "BOE", "BOP", "DOGC", "DOGV", "DOG", "BOJA", "BOCM", "BOCYL", "DOCM", "DOE", "BON", "BOR", "BOA", "BOPV", "BOC", "BOIB", "BORM", "BOPA", "BOCCE", "BOME", "UGT", "CCOO", "SMI", "IPREM", "RGI", "PNC", "SAD", "SAAD"}


def capitalizar(texto: str) -> str:
    """Convierte 'AYUNTAMIENTO DE XOVE' en 'Ayuntamiento de Xove'. Respeta siglas conocidas y textos ya mezclados."""
    if not texto or not texto.isupper():
        return texto
    palabras = []
    for i, palabra in enumerate(texto.split()):
        limpia = palabra.strip("(),.;:")
        if limpia in INVARIABLES or (len(limpia) <= 3 and limpia.isalpha() and i > 0 and limpia.lower() not in MINUSCULAS):
            palabras.append(palabra)
        elif i > 0 and palabra.lower() in MINUSCULAS:
            palabras.append(palabra.lower())
        elif len(palabra) > 2 and palabra[1] == "'" and palabra[0] in "DL":
            # Catalán: D'IGUALTAT -> d'Igualtat
            palabras.append(palabra[0].lower() + "'" + palabra[2:3].upper() + palabra[3:].lower())
        else:
            palabras.append("/".join("-".join(parte[:1].upper() + parte[1:].lower() for parte in trozo.split("-")) for trozo in palabra.split("/")))
    return " ".join(palabras)


def titulo_legible(texto: str) -> str:
    """Los títulos escritos todo en mayúsculas pasan a tipo frase, conservando siglas conocidas."""
    if not texto or not texto.isupper():
        return texto
    palabras = []
    for i, palabra in enumerate(texto.split()):
        limpia = palabra.strip("(),.;:")
        if limpia in INVARIABLES or (len(limpia) <= 3 and limpia.isalpha() and i > 0 and limpia.lower() not in MINUSCULAS):
            palabras.append(palabra)
        elif i == 0:
            palabras.append(palabra[:1].upper() + palabra[1:].lower())
        else:
            palabras.append(palabra.lower())
    return " ".join(palabras)


class ApiError(RuntimeError):
    pass


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
            if exc.code in (400, 404):
                raise ApiError(f"La API rechazó {ruta} ({exc.code})") from exc
            ultimo_error = exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            ultimo_error = exc
        print(f"  aviso: fallo {intento}/{intentos} en {ruta}: {ultimo_error}", file=sys.stderr)
        time.sleep(2 * intento)
    raise ApiError(f"La API no respondió en {ruta}: {ultimo_error}")


def fecha_api(d: date) -> str:
    """La búsqueda exige dd/mm/aaaa; el formato ISO devuelve 400."""
    return d.strftime("%d/%m/%Y")


def fecha_iso(valor: str | None) -> str | None:
    """Las fechas del detalle llegan como AAAA-MM-DD. Devuelve None si no se reconoce."""
    if not valor:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor[:10], formato).date().isoformat()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Exploración
# ---------------------------------------------------------------------------


def explorar() -> None:
    """Vuelca los catálogos y una muestra de búsqueda y detalle para inspeccionar campos reales."""
    RUTA_RAW.mkdir(parents=True, exist_ok=True)
    for nombre, ruta in CATALOGOS.items():
        try:
            datos = peticion(ruta)
        except ApiError as exc:
            print(f"{nombre}: {exc}")
            continue
        destino = RUTA_RAW / f"{nombre}.json"
        destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{nombre}: {len(datos)} elementos -> {destino.relative_to(RAIZ)}")

    hoy = date.today()
    pagina = peticion(
        "/convocatorias/busqueda",
        {
            "page": 0,
            "pageSize": 5,
            "fechaDesde": fecha_api(hoy - timedelta(days=7)),
            "fechaHasta": fecha_api(hoy),
            "tiposBeneficiario": list(TIPOS_BENEFICIARIO),
        },
    )
    (RUTA_RAW / "busqueda_muestra.json").write_text(json.dumps(pagina, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"búsqueda de muestra: {pagina.get('totalElements')} convocatorias en 7 días")
    for item in pagina.get("content", [])[:2]:
        num = item["numeroConvocatoria"]
        detalle = peticion("/convocatorias", {"numConv": num})
        (RUTA_RAW / f"detalle_{num}.json").write_text(json.dumps(detalle, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"detalle de {num} -> data/raw/detalle_{num}.json")


# ---------------------------------------------------------------------------
# Descarga y normalización
# ---------------------------------------------------------------------------


def buscar_convocatorias(desde: date, hasta: date) -> list[dict]:
    """Recorre todas las páginas de la búsqueda filtrada por tipo de beneficiario."""
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
                "tiposBeneficiario": list(TIPOS_BENEFICIARIO),
                "order": "fechaRecepcion",
                "direccion": "desc",
            },
        )
        contenido = datos.get("content", [])
        resultados.extend(contenido)
        total_paginas = datos.get("totalPages") or 1
        print(f"  página {pagina + 1}/{total_paginas}: {len(contenido)} convocatorias")
        pagina += 1
        if pagina >= total_paginas or not contenido:
            break
        time.sleep(PAUSA_SEGUNDOS)
    return resultados


def descripciones(valor) -> list[str]:
    if not valor:
        return []
    if isinstance(valor, dict):
        valor = [valor]
    return [(v.get("descripcion") if isinstance(v, dict) else str(v)) or "" for v in valor]


def separar_region(texto: str) -> tuple[str, str]:
    """'ES522 - Castellón / Castelló' -> ('ES522', 'Castellón / Castelló')."""
    codigo, _, nombre = texto.partition(" - ")
    return codigo.strip(), nombre.strip()


def comunidades_de(regiones: list[str]) -> list[str]:
    """Traduce los códigos NUTS de la API a nombres de comunidad. Sin código de comunidad, Toda España."""
    resultado: list[str] = []
    for texto in regiones:
        codigo, _ = separar_region(texto)
        if len(codigo) >= 4 and codigo[:4] in COMUNIDADES:
            nombres = [COMUNIDADES[codigo[:4]]]
        elif len(codigo) == 3 and codigo in NUTS1:
            nombres = NUTS1[codigo]
        else:
            nombres = [TODA_ESPANA]
        for nombre in nombres:
            if nombre not in resultado:
                resultado.append(nombre)
    return resultado or [TODA_ESPANA]


def provincias_de(regiones: list[str]) -> list[str]:
    """Provincias a partir de los códigos NUTS 3. Vacío si la convocatoria es autonómica, estatal o sin código."""
    resultado: list[str] = []
    for texto in regiones:
        codigo, _ = separar_region(texto)
        nombre = PROVINCIAS.get(codigo)
        if nombre and nombre not in resultado:
            resultado.append(nombre)
    return resultado


def url_valida(valor: str | None) -> str | None:
    """La API mezcla URL con texto libre; se conserva solo lo que parece una dirección web."""
    if not valor:
        return None
    valor = valor.strip()
    if valor.startswith(("http://", "https://")):
        return valor
    if "." in valor and " " not in valor and "/" not in valor.split(".")[0]:
        return "https://" + valor
    return None


def organo_texto(detalle: dict) -> str:
    organo = detalle.get("organo") or {}
    nivel2 = (organo.get("nivel2") or "").strip()
    nivel3 = (organo.get("nivel3") or "").strip()
    if nivel2 and nivel3 and nivel2 != nivel3 and nivel2 not in nivel3:
        return f"{capitalizar(nivel3)} ({capitalizar(nivel2)})"
    return capitalizar(nivel3 or nivel2)


def normalizar(detalle: dict) -> dict:
    """Reduce el detalle de la API a los campos que usa la web."""
    num = str(detalle.get("codigoBDNS") or detalle.get("numeroConvocatoria"))
    organo = detalle.get("organo") or {}
    regiones = descripciones(detalle.get("regiones"))
    return {
        "id": num,
        "titulo": titulo_legible(" ".join((detalle.get("descripcion") or "").split())),
        "organo": organo_texto(detalle),
        "ambito": AMBITOS.get((organo.get("nivel1") or "").upper(), organo.get("nivel1") or ""),
        "comunidades": comunidades_de(regiones),
        "provincias": provincias_de(regiones),
        "regiones": [capitalizar(separar_region(r)[1] or r) for r in regiones],
        "finalidad": (detalle.get("descripcionFinalidad") or "").strip() or None,
        "tipoConvocatoria": detalle.get("tipoConvocatoria"),
        "presupuesto": detalle.get("presupuestoTotal"),
        "fechaPublicacion": fecha_iso(detalle.get("fechaRecepcion")),
        "plazoInicio": fecha_iso(detalle.get("fechaInicioSolicitud")),
        "plazoFin": fecha_iso(detalle.get("fechaFinSolicitud")),
        "plazoTexto": " ".join((detalle.get("textFin") or "").split()) or None,
        "urlBases": url_valida(detalle.get("urlBasesReguladoras")),
        "urlSede": url_valida(detalle.get("sedeElectronica")),
        "urlFicha": f"https://www.infosubvenciones.es/bdnstrans/{PORTAL}/es/convocatorias/{num}",
    }


def cargar_meta() -> dict:
    if not RUTA_META.exists():
        return {}
    return json.loads(RUTA_META.read_text(encoding="utf-8"))


def cargar_existentes() -> dict[str, dict]:
    if not RUTA_SALIDA.exists():
        return {}
    datos = json.loads(RUTA_SALIDA.read_text(encoding="utf-8"))
    return {c["id"]: c for c in datos}


def sigue_vigente(conv: dict, hoy: date) -> bool:
    fin = conv.get("plazoFin")
    if fin:
        return date.fromisoformat(fin) >= hoy - timedelta(days=DIAS_GRACIA_TRAS_CIERRE)
    publicada = conv.get("fechaPublicacion")
    if not publicada:
        return False
    return date.fromisoformat(publicada) >= hoy - timedelta(days=DIAS_VIGENCIA_SIN_FECHA)


def hay_que_refrescar(existente: dict | None) -> bool:
    """Se vuelve a pedir el detalle si no lo tenemos o si aún no tenía fecha de fin (pueden añadirla después)."""
    return existente is None or not existente.get("plazoFin")


def actualizar(dias: int) -> None:
    hoy = date.today()
    desde = hoy - timedelta(days=dias)
    print(f"Buscando convocatorias para personas publicadas entre {desde} y {hoy}...")
    resumen = buscar_convocatorias(desde, hoy)

    existentes = cargar_existentes()
    advertencia = None  # condiciones de reutilización que la API adjunta a cada respuesta; se conservan literales
    nuevas = refrescadas = fallos = 0
    for item in resumen:
        num = str(item.get("numeroConvocatoria") or "")
        if not num or not hay_que_refrescar(existentes.get(num)):
            continue
        time.sleep(PAUSA_SEGUNDOS)
        try:
            detalle = peticion("/convocatorias", {"numConv": num})
        except ApiError as exc:
            fallos += 1
            print(f"  aviso: sin detalle para {num}: {exc}", file=sys.stderr)
            continue
        if num in existentes:
            refrescadas += 1
        else:
            nuevas += 1
        advertencia = advertencia or detalle.get("advertencia")
        existentes[num] = normalizar(detalle)

    vigentes = [c for c in existentes.values() if sigue_vigente(c, hoy)]
    vigentes.sort(key=lambda c: (c.get("fechaPublicacion") or "", c["id"]), reverse=True)

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    # Un objeto por línea: diffs legibles en git y fichero compacto para el navegador.
    RUTA_SALIDA.write_text("[\n" + ",\n".join(json.dumps(c, ensure_ascii=False) for c in vigentes) + "\n]\n", encoding="utf-8")
    RUTA_META.write_text(
        json.dumps(
            {
                "actualizado": datetime.now().isoformat(timespec="minutes"),
                "total": len(vigentes),
                "nuevas": nuevas,
                "refrescadas": refrescadas,
                "fallos": fallos,
                "ventanaDias": dias,
                "fuente": "Origen de los datos: Intervención General de la Administración del Estado",
                "portal": "https://www.infosubvenciones.es/",
                "condicionesReutilizacion": "https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal",
                "advertencia": advertencia or cargar_meta().get("advertencia"),
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Listo: {len(vigentes)} ayudas vigentes para personas ({nuevas} nuevas, {refrescadas} refrescadas, {fallos} fallos).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--explorar", action="store_true", help="volcar catálogos y muestras en data/raw/")
    parser.add_argument("--dias", type=int, default=10, help="días hacia atrás que se consultan (por defecto 10)")
    args = parser.parse_args()
    try:
        if args.explorar:
            explorar()
        else:
            actualizar(args.dias)
    except ApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
