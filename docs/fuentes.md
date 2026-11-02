# Fuentes de datos

## Base de Datos Nacional de Subvenciones (BDNS)

- Portal: https://www.infosubvenciones.es/
- Documentación de la API (Swagger): https://www.infosubvenciones.es/bdnstrans/doc/swagger
- Base de la API: `https://www.infosubvenciones.es/bdnstrans/api`
- Formato: JSON. Acceso público sin clave. Referencias: [catálogo de datos.gob.es](https://datos.gob.es/es/catalogo/e05250001-base-de-datos-nacional-de-subvenciones) y [manual del Sistema Nacional de Publicidad de Subvenciones, versión 2023](https://www.pap.hacienda.gob.es/bdnstrans/estaticos/ayuda/AYUDA%20-%20Sistema%20Nacional%20de%20Publicidad%20de%20Subvenciones%20y%20Ayudas%20P%C3%BAblicas%20v2023.pdf).
- Marco legal: artículo 20 de la Ley 38/2003 General de Subvenciones y Real Decreto 130/2019. Toda administración pública española está obligada a publicar aquí sus convocatorias.

### Condiciones de reutilización

Cada respuesta de la API incluye un campo `advertencia` que remite al [aviso legal](https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal) y recuerda que los datos son dinámicos y pueden corregirse después de extraerlos. El manual de 2023 pide citar la fuente, con la Intervención General de la Administración del Estado (IGAE) como origen de los datos, y restringe la reutilización de datos personales. Esta web:

- cita la fuente y la IGAE en el pie de cada página y enlaza a la ficha oficial de cada convocatoria;
- no trata datos personales: solo convocatorias, nunca concesiones a personas;
- muestra la fecha de la última extracción;
- limita el ritmo de peticiones (una pausa entre cada una) y descarga solo lo publicado en los últimos días.

Pendiente: leer el texto íntegro del aviso legal, que se sirve como aplicación web y no se pudo extraer de forma automática.

### Verificado el 2026-11-02

Resultado de sondear la API desde GitHub Actions con `scripts/explorar_parametros.py`.

**Búsqueda** `GET /convocatorias/busqueda`

| Parámetro | Valores | Nota |
| --- | --- | --- |
| `vpd` | `GE` | Portal general. Obligatorio. |
| `page`, `pageSize` | enteros | Paginación. La respuesta trae `content`, `totalElements`, `totalPages`. |
| `fechaDesde`, `fechaHasta` | `dd/mm/aaaa` | Fecha de publicación. El formato ISO devuelve 400. |
| `tiposBeneficiario` | id del catálogo | Filtra en servidor. `1` dejó 267 de 1572 convocatorias en una semana. |
| `regiones` | id del catálogo | Filtra en servidor. |
| `finalidad` | id del catálogo | Filtra en servidor. |
| `tipoAdministracion` | `C`, `A`, `L` | Estatal, autonómica, local. |
| `order`, `direccion` | `fechaRecepcion`, `desc` | `fechaFinSolicitud` no se admite como orden. |

Campos de cada elemento: `id`, `numeroConvocatoria`, `descripcion`, `descripcionLeng`, `fechaRecepcion` (ISO), `nivel1` (`ESTATAL`, `AUTONOMICA`, `LOCAL`), `nivel2`, `nivel3`, `mrr`.

No existe parámetro para pedir solo convocatorias abiertas; el filtrado por plazo se hace en el cliente.

**Detalle** `GET /convocatorias?numConv=NNN`

Campos relevantes: `codigoBDNS`, `descripcion`, `organo` (`nivel1`, `nivel2`, `nivel3`), `tiposBeneficiarios[].descripcion`, `regiones[].descripcion` (con código NUTS, por ejemplo `ES522 - Castellón / Castelló`), `descripcionFinalidad`, `instrumentos[].descripcion`, `tipoConvocatoria`, `presupuestoTotal`, `fechaRecepcion`, `fechaInicioSolicitud`, `fechaFinSolicitud` (ISO o `null`), `textInicio`, `textFin`, `abierto`, `sedeElectronica`, `urlBasesReguladoras`, `documentos[]`.

Observaciones de calidad de datos:

- Muchas convocatorias no publican `fechaFinSolicitud`; el plazo va en `textFin` como texto libre ("15 días hábiles desde la publicación en el BOP").
- `abierto` sale `false` incluso en convocatorias recién publicadas, así que no se usa.
- `urlBasesReguladoras` y `sedeElectronica` mezclan direcciones web con texto libre o dominios sin esquema. Se validan antes de enlazar.

**Catálogos** (todos con `?vpd=GE`): `/beneficiarios`, `/regiones` (árbol NUTS), `/finalidades`, `/instrumentos`, `/sectores`, `/actividades`. No existen `/tiposbeneficiario` ni `/tiposadministracion`; `/organos` exige parámetros.

Tipos de beneficiario: `1` personas físicas sin actividad económica, `2` personas jurídicas sin actividad económica, `3` pymes y personas físicas con actividad económica, `4` gran empresa, `5` sin información específica.

### Qué consideramos "ayuda para personas"

1. Tipo de beneficiario `1`, filtrado en servidor. El tipo `3` (autónomos y pymes) queda para una segunda fase, como filtro opcional.
2. Se muestra mientras el plazo no haya cerrado. Sin fecha de fin publicada, durante 90 días desde la publicación.
3. Cada noche se vuelve a pedir el detalle de las convocatorias sin fecha de fin, por si la añaden.

## Otras fuentes a valorar más adelante

- Boletines oficiales autonómicos para convocatorias que lleguen tarde a la BDNS.
- Sede electrónica de cada órgano para el enlace directo de solicitud.
