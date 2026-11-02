# Fuentes de datos

## Base de Datos Nacional de Subvenciones (BDNS)

- Portal: https://www.infosubvenciones.es/
- Documentación de la API (Swagger): https://www.infosubvenciones.es/bdnstrans/doc/swagger
- Base de la API: `https://www.infosubvenciones.es/bdnstrans/api`
- Formato: JSON. Acceso público sin clave según el manual de la BDNS de diciembre de 2023 y el [catálogo de datos.gob.es](https://datos.gob.es/es/catalogo/e05250001-base-de-datos-nacional-de-subvenciones).
- Marco legal: artículo 20 de la Ley 38/2003 General de Subvenciones y Real Decreto 130/2019. Toda administración pública española está obligada a publicar aquí sus convocatorias.

### Endpoints que usa el script

> Pendiente de verificar contra el Swagger real. Los nombres de parámetros y campos de abajo se han escrito de memoria y deben confirmarse en la primera ejecución con `--explorar`.

| Uso | Endpoint | Notas |
| --- | --- | --- |
| Búsqueda paginada de convocatorias | `GET /convocatorias/busqueda` | Parámetros: `vpd=GE`, `page`, `pageSize`, `fechaDesde`, `fechaHasta` (dd/mm/aaaa), `tiposBeneficiario`, `regiones`, `tipoAdministracion`, `order`, `direccion`. |
| Detalle de una convocatoria | `GET /convocatorias?numConv=...&vpd=GE` | Trae plazos, beneficiarios, finalidad, regiones, sede electrónica y bases reguladoras. |
| Catálogo de tipos de beneficiario | `GET /tiposbeneficiario?vpd=GE` | Para localizar los códigos de "personas físicas". |
| Catálogo de regiones | `GET /regiones?vpd=GE` | Comunidades y provincias. |
| Catálogo de finalidades | `GET /finalidades?vpd=GE` | Política de gasto. |

### Qué consideramos "ayuda para personas"

Primera aproximación, a revisar con datos reales:

1. El tipo de beneficiario incluye personas físicas, con o sin actividad económica.
2. La convocatoria tiene plazo de solicitud abierto o sin fecha de fin.
3. Se excluyen premios y concursos salvo que estén claramente dirigidos a ciudadanía general.

## Otras fuentes a valorar más adelante

- Boletines oficiales autonómicos para convocatorias que lleguen tarde a la BDNS.
- Sede electrónica de cada órgano para el enlace directo de solicitud.
