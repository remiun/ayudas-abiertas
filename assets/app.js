// Ayudas Abiertas: carga el JSON generado y filtra en el navegador.
// Sin dependencias, sin peticiones a terceros, sin almacenamiento de datos personales.

(function () {
  "use strict";

  const RUTA_DATOS = "data/convocatorias.json";
  const RUTA_META = "data/meta.json";
  const DIAS_URGENTE = 7;
  const DIAS_CIERRAN_PRONTO = 14;

  const $ = (sel) => document.querySelector(sel);
  const form = $("#filtros");
  const estado = $("#estado");
  const contenedor = $("#resultados");
  const plantilla = $("#plantilla-ayuda");
  const selRegion = $("#region");
  const selProvincia = $("#provincia");
  const selPerfil = $("#perfil");

  // Orden fijo de los perfiles, el mismo que en el script de descarga.
  const PERFILES = ["Estudiantes", "Jóvenes", "Familias e infancia", "Personas mayores", "Mujeres", "Discapacidad y dependencia",
    "Desempleo y empleo", "Vivienda", "Pocos ingresos y emergencia social", "Salud", "Deportistas", "Cultura y creación", "Investigación",
    "Transporte y movilidad", "Energía y hogar", "Campo, mar y medio rural", "Autónomos y emprendedores", "Migración y retorno",
    "Víctimas y catástrofes", "Nacimiento, bodas y defunciones", "Asociaciones y voluntariado", "Concursos y premios", "Otros"];

  // Comunidad de cada provincia, para que el selector de provincia siga al de comunidad
  // y para que una ayuda autonómica cuente también al filtrar por una provincia de esa comunidad.
  const PROVINCIAS = {
    "A Coruña": "Galicia", "Lugo": "Galicia", "Ourense": "Galicia", "Pontevedra": "Galicia",
    "Asturias": "Principado de Asturias", "Cantabria": "Cantabria",
    "Araba/Álava": "País Vasco", "Gipuzkoa": "País Vasco", "Bizkaia": "País Vasco",
    "Navarra": "Comunidad Foral de Navarra", "La Rioja": "La Rioja",
    "Huesca": "Aragón", "Teruel": "Aragón", "Zaragoza": "Aragón",
    "Madrid": "Comunidad de Madrid",
    "Ávila": "Castilla y León", "Burgos": "Castilla y León", "León": "Castilla y León", "Palencia": "Castilla y León",
    "Salamanca": "Castilla y León", "Segovia": "Castilla y León", "Soria": "Castilla y León", "Valladolid": "Castilla y León", "Zamora": "Castilla y León",
    "Albacete": "Castilla-La Mancha", "Ciudad Real": "Castilla-La Mancha", "Cuenca": "Castilla-La Mancha", "Guadalajara": "Castilla-La Mancha", "Toledo": "Castilla-La Mancha",
    "Badajoz": "Extremadura", "Cáceres": "Extremadura",
    "Barcelona": "Cataluña", "Girona": "Cataluña", "Lleida": "Cataluña", "Tarragona": "Cataluña",
    "Alicante/Alacant": "Comunitat Valenciana", "Castellón/Castelló": "Comunitat Valenciana", "Valencia/València": "Comunitat Valenciana",
    "Illes Balears": "Illes Balears",
    "Almería": "Andalucía", "Cádiz": "Andalucía", "Córdoba": "Andalucía", "Granada": "Andalucía", "Huelva": "Andalucía", "Jaén": "Andalucía", "Málaga": "Andalucía", "Sevilla": "Andalucía",
    "Murcia": "Región de Murcia", "Ceuta": "Ciudad de Ceuta", "Melilla": "Ciudad de Melilla",
    "Las Palmas": "Canarias", "Santa Cruz de Tenerife": "Canarias"
  };
  const selAmbito = $("#ambito");
  const selFinalidad = $("#finalidad");

  let ayudas = [];

  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  function diasHasta(fechaIso) {
    if (!fechaIso) return null;
    const fin = new Date(fechaIso + "T00:00:00");
    return Math.round((fin - hoy) / 86400000);
  }

  function textoPlazo(ayuda) {
    const dias = diasHasta(ayuda.plazoFin);
    if (dias === null) {
      if (ayuda.plazoTexto) {
        const t = ayuda.plazoTexto.length > 90 ? ayuda.plazoTexto.slice(0, 87) + "..." : ayuda.plazoTexto;
        return { texto: "Plazo: " + t, clase: "sin-fecha" };
      }
      return { texto: "Plazo no publicado todavía", clase: "sin-fecha" };
    }
    if (dias < 0) return { texto: "Plazo cerrado el " + formatearFecha(ayuda.plazoFin), clase: "cerrado" };
    if (dias === 0) return { texto: "Último día para solicitar", clase: "urgente" };
    if (dias === 1) return { texto: "Queda 1 día", clase: "urgente" };
    if (dias <= DIAS_URGENTE) return { texto: "Quedan " + dias + " días", clase: "urgente" };
    return { texto: "Hasta el " + formatearFecha(ayuda.plazoFin), clase: "" };
  }

  function formatearFecha(iso) {
    const [a, m, d] = iso.split("-");
    return d + "/" + m + "/" + a;
  }

  function estaAbierta(ayuda) {
    const dias = diasHasta(ayuda.plazoFin);
    if (dias === null) return true; // sin fecha publicada: se da por posible
    return dias >= 0;
  }

  function cierraPronto(ayuda) {
    const dias = diasHasta(ayuda.plazoFin);
    return dias !== null && dias >= 0 && dias <= DIAS_CIERRAN_PRONTO;
  }

  function normalizar(texto) {
    return (texto || "").toString().normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function rellenarSelect(select, valores) {
    const ordenados = Array.from(valores).filter(Boolean).sort((a, b) => a.localeCompare(b, "es"));
    for (const v of ordenados) {
      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      select.appendChild(opt);
    }
  }

  function rellenarProvincias() {
    const comunidad = selRegion.value;
    const actual = selProvincia.value;
    selProvincia.textContent = "";
    const todas = document.createElement("option");
    todas.value = "";
    todas.textContent = "Todas";
    selProvincia.appendChild(todas);
    const lista = Object.keys(PROVINCIAS).filter((p) => !comunidad || PROVINCIAS[p] === comunidad);
    rellenarSelect(selProvincia, lista);
    if (lista.includes(actual)) selProvincia.value = actual;
  }

  function prepararFiltros() {
    const regiones = new Set();
    const ambitos = new Set();
    const finalidades = new Set();
    for (const a of ayudas) {
      (a.comunidades || []).forEach((r) => regiones.add(r));
      if (a.ambito) ambitos.add(a.ambito);
      if (a.finalidad) finalidades.add(a.finalidad);
    }
    const presentes = new Set(ayudas.flatMap((a) => a.perfiles || []));
    for (const nombre of PERFILES.filter((n) => presentes.has(n))) {
      const opt = document.createElement("option");
      opt.value = nombre;
      opt.textContent = nombre;
      selPerfil.appendChild(opt);
    }
    rellenarSelect(selRegion, regiones);
    rellenarProvincias();
    rellenarSelect(selAmbito, ambitos);
    rellenarSelect(selFinalidad, finalidades);
  }

  function filtrar() {
    const datos = new FormData(form);
    const texto = normalizar(datos.get("texto"));
    const perfil = datos.get("perfil");
    const region = datos.get("region");
    const provincia = datos.get("provincia");
    const ambito = datos.get("ambito");
    const finalidad = datos.get("finalidad");
    const soloAbiertas = datos.get("abiertas") === "on";

    return ayudas.filter((a) => {
      if (soloAbiertas && !estaAbierta(a)) return false;
      if (perfil && !(a.perfiles || []).includes(perfil)) return false;
      if (region && !(a.comunidades || []).includes(region) && !(a.comunidades || []).includes("Toda España")) return false;
      if (provincia) {
        const provs = a.provincias || [];
        const coms = a.comunidades || [];
        const cubrePorAmbito = provs.length === 0 && (coms.includes(PROVINCIAS[provincia]) || coms.includes("Toda España"));
        if (!provs.includes(provincia) && !cubrePorAmbito) return false;
      }
      if (ambito && a.ambito !== ambito) return false;
      if (finalidad && a.finalidad !== finalidad) return false;
      if (texto) {
        const pajar = normalizar([a.titulo, a.organo, a.finalidad, (a.regiones || []).join(" "), (a.provincias || []).join(" "), (a.comunidades || []).join(" ")].join(" "));
        if (!texto.split(/\s+/).every((palabra) => pajar.includes(palabra))) return false;
      }
      return true;
    });
  }

  function pintar(lista) {
    contenedor.textContent = "";
    if (lista.length === 0) {
      const vacio = document.createElement("p");
      vacio.className = "vacio";
      vacio.textContent = ayudas.length === 0
        ? "Todavía no hay datos publicados. La primera actualización automática los traerá."
        : "Ninguna ayuda coincide con esos filtros. Prueba a quitar alguno.";
      contenedor.appendChild(vacio);
      return;
    }
    const frag = document.createDocumentFragment();
    const pronto = lista.filter(cierraPronto);
    const resto = lista.filter((a) => !cierraPronto(a));
    pronto.sort((x, y) => (x.plazoFin || "").localeCompare(y.plazoFin || ""));
    if (pronto.length) {
      frag.appendChild(encabezadoGrupo("Cierran pronto", pronto.length));
      for (const a of pronto) frag.appendChild(tarjeta(a));
    }
    if (resto.length) {
      if (pronto.length) frag.appendChild(encabezadoGrupo("Publicadas recientemente", resto.length));
      for (const a of resto) frag.appendChild(tarjeta(a));
    }
    contenedor.appendChild(frag);
  }

  function encabezadoGrupo(titulo, n) {
    const h = document.createElement("h2");
    h.className = "grupo";
    h.textContent = titulo + " (" + n + ")";
    return h;
  }

  function tarjeta(a) {
    {
      const nodo = plantilla.content.cloneNode(true);
      const plazo = textoPlazo(a);
      const pPlazo = nodo.querySelector(".plazo");
      pPlazo.textContent = plazo.texto;
      if (plazo.clase) pPlazo.classList.add(plazo.clase);

      const enlaceTitulo = nodo.querySelector(".titulo a");
      enlaceTitulo.textContent = a.titulo || "Convocatoria " + a.id;
      enlaceTitulo.href = a.urlFicha;

      nodo.querySelector(".organo").textContent = a.organo || "";
      nodo.querySelector(".publicada").textContent = a.fechaPublicacion ? "Publicada en la BDNS el " + formatearFecha(a.fechaPublicacion) : "";

      const ul = nodo.querySelector(".etiquetas");
      const lugar = (a.provincias && a.provincias.length) ? a.provincias : (a.comunidades || []);
      const perfiles = (a.perfiles || []).filter((p) => p !== "Otros").slice(0, 2);
      const etiquetas = [].concat(perfiles, lugar, a.finalidad ? [a.finalidad] : [], a.ambito ? [a.ambito] : []);
      for (const e of etiquetas.slice(0, 6)) {
        const li = document.createElement("li");
        li.textContent = e;
        ul.appendChild(li);
      }

      nodo.querySelector(".enlace-ficha").href = a.urlFicha;
      const sede = nodo.querySelector(".enlace-sede");
      if (a.urlSede) { sede.href = a.urlSede; sede.hidden = false; }
      const bases = nodo.querySelector(".enlace-bases");
      if (a.urlBases) { bases.href = a.urlBases; bases.hidden = false; }

      return nodo;
    }
  }

  function actualizar() {
    const lista = filtrar();
    pintar(lista);
    estado.textContent = ayudas.length === 0
      ? ""
      : lista.length === 1 ? "1 ayuda encontrada" : lista.length + " ayudas encontradas";
  }

  async function cargar() {
    try {
      const resp = await fetch(RUTA_DATOS, { cache: "no-cache" });
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      ayudas = await resp.json();
    } catch (err) {
      ayudas = [];
      estado.textContent = "";
    }
    prepararFiltros();
    actualizar();

    try {
      const resp = await fetch(RUTA_META, { cache: "no-cache" });
      if (resp.ok) {
        const meta = await resp.json();
        if (meta.actualizado) {
          const f = meta.actualizado.slice(0, 10).split("-");
          $("#actualizado").textContent = "Última extracción de datos: " + f[2] + "/" + f[1] + "/" + f[0] + ".";
        }
      }
    } catch (err) { /* el pie queda sin fecha */ }
  }

  selRegion.addEventListener("change", rellenarProvincias);
  form.addEventListener("input", actualizar);
  form.addEventListener("submit", (e) => { e.preventDefault(); actualizar(); });
  cargar();
})();
