// Ayudas Abiertas: carga el JSON generado y filtra en el navegador.
// Sin dependencias, sin peticiones a terceros, sin almacenamiento de datos personales.

(function () {
  "use strict";

  const RUTA_DATOS = "data/convocatorias.json";
  const RUTA_META = "data/meta.json";
  const DIAS_URGENTE = 7;

  const $ = (sel) => document.querySelector(sel);
  const form = $("#filtros");
  const estado = $("#estado");
  const contenedor = $("#resultados");
  const plantilla = $("#plantilla-ayuda");
  const selRegion = $("#region");
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
      if (ayuda.abierto === false) return { texto: "Plazo cerrado", clase: "cerrado" };
      return { texto: ayuda.plazoTexto ? "Plazo: " + ayuda.plazoTexto : "Plazo sin fecha de fin publicada", clase: "sin-fecha" };
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
    if (dias === null) return ayuda.abierto !== false;
    return dias >= 0;
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

  function prepararFiltros() {
    const regiones = new Set();
    const ambitos = new Set();
    const finalidades = new Set();
    for (const a of ayudas) {
      (a.regiones || []).forEach((r) => regiones.add(r));
      if (a.ambito) ambitos.add(a.ambito);
      if (a.finalidad) finalidades.add(a.finalidad);
    }
    rellenarSelect(selRegion, regiones);
    rellenarSelect(selAmbito, ambitos);
    rellenarSelect(selFinalidad, finalidades);
  }

  function filtrar() {
    const datos = new FormData(form);
    const texto = normalizar(datos.get("texto"));
    const region = datos.get("region");
    const ambito = datos.get("ambito");
    const finalidad = datos.get("finalidad");
    const soloAbiertas = datos.get("abiertas") === "on";

    return ayudas.filter((a) => {
      if (soloAbiertas && !estaAbierta(a)) return false;
      if (region && !(a.regiones || []).includes(region)) return false;
      if (ambito && a.ambito !== ambito) return false;
      if (finalidad && a.finalidad !== finalidad) return false;
      if (texto) {
        const pajar = normalizar([a.titulo, a.organo, a.finalidad, (a.beneficiarios || []).join(" ")].join(" "));
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
    for (const a of lista) {
      const nodo = plantilla.content.cloneNode(true);
      const plazo = textoPlazo(a);
      const pPlazo = nodo.querySelector(".plazo");
      pPlazo.textContent = plazo.texto;
      if (plazo.clase) pPlazo.classList.add(plazo.clase);

      const enlaceTitulo = nodo.querySelector(".titulo a");
      enlaceTitulo.textContent = a.titulo || "Convocatoria " + a.id;
      enlaceTitulo.href = a.urlFicha;

      nodo.querySelector(".organo").textContent = a.organo || "";

      const ul = nodo.querySelector(".etiquetas");
      const etiquetas = [].concat(a.regiones || [], a.finalidad ? [a.finalidad] : [], a.ambito ? [a.ambito] : []);
      for (const e of etiquetas.slice(0, 5)) {
        const li = document.createElement("li");
        li.textContent = e;
        ul.appendChild(li);
      }

      nodo.querySelector(".enlace-ficha").href = a.urlFicha;
      const sede = nodo.querySelector(".enlace-sede");
      if (a.urlSede) { sede.href = a.urlSede; sede.hidden = false; }
      const bases = nodo.querySelector(".enlace-bases");
      if (a.urlBases) { bases.href = a.urlBases; bases.hidden = false; }

      frag.appendChild(nodo);
    }
    contenedor.appendChild(frag);
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
          $("#actualizado").textContent = "Última actualización: " + f[2] + "/" + f[1] + "/" + f[0] + ".";
        }
      }
    } catch (err) { /* el pie queda sin fecha */ }
  }

  form.addEventListener("input", actualizar);
  form.addEventListener("submit", (e) => { e.preventDefault(); actualizar(); });
  cargar();
})();
