/* =====================================================================
   Aula Virtual Empresarial Soacha · motor común de componentes
   - Conexión SCORM 1.2 con Moodle (nota, estado y punto de regreso).
   - Funciona igual fuera de Moodle (vista previa): solo no envía datos.
   - Ayudas para pintar la cabecera, el pie y los espacios por llenar.
   Cada componente define window.CONTENIDO en contenido.js y llama
   Aula.iniciar(CONTENIDO) desde su index.html.
   ===================================================================== */
(function () {
  "use strict";

  /* ---------- SCORM 1.2 ---------- */
  function buscarAPI(w) {
    for (var i = 0; w && i < 10; i++) {
      if (w.API) return w.API;
      if (w.parent === w) break;
      w = w.parent;
    }
    try { if (window.opener && window.opener.API) return window.opener.API; } catch (e) {}
    return null;
  }
  var api = null, activo = false, terminado = false;
  var scorm = {
    conectar: function () {
      try { api = buscarAPI(window); } catch (e) { api = null; }
      if (!api) return false;
      activo = String(api.LMSInitialize("")) === "true";
      if (activo) {
        var est = scorm.leer("cmi.core.lesson_status");
        if (!est || est === "not attempted") scorm.escribir("cmi.core.lesson_status", "incomplete");
        scorm.guardar();
      }
      return activo;
    },
    activo: function () { return activo; },
    leer: function (k) { return activo ? api.LMSGetValue(k) : ""; },
    escribir: function (k, v) { if (activo) api.LMSSetValue(k, String(v)); },
    guardar: function () { if (activo) api.LMSCommit(""); },
    /* Punto de regreso: cualquier objeto pequeño (máx. 4096 caracteres en SCORM 1.2) */
    recordar: function (obj) {
      if (!activo) return;
      try { scorm.escribir("cmi.suspend_data", JSON.stringify(obj).slice(0, 4000)); scorm.guardar(); } catch (e) {}
    },
    recuperar: function () {
      try { var s = scorm.leer("cmi.suspend_data"); return s ? JSON.parse(s) : null; } catch (e) { return null; }
    },
    /* nota de 0 a 100; aprobado según contenido.notaMinima (por defecto 60) */
    terminar: function (nota, notaMinima) {
      if (!activo) return;
      if (typeof nota === "number") {
        scorm.escribir("cmi.core.score.min", 0);
        scorm.escribir("cmi.core.score.max", 100);
        scorm.escribir("cmi.core.score.raw", Math.round(nota));
        scorm.escribir("cmi.core.lesson_status", nota >= (notaMinima || 60) ? "passed" : "failed");
      } else {
        scorm.escribir("cmi.core.lesson_status", "completed");
      }
      scorm.guardar();
    },
    cerrar: function () {
      if (activo && !terminado) { terminado = true; scorm.escribir("cmi.core.exit", "suspend"); scorm.guardar(); api.LMSFinish(""); }
    }
  };
  window.addEventListener("pagehide", scorm.cerrar);
  window.addEventListener("beforeunload", scorm.cerrar);

  /* ---------- Utilidades ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  /* Texto con marcas simples:
     **negrita**, [ESPACIO POR LLENAR] resaltado, {{dato}} desde contenido.datos */
  function texto(s, datos) {
    var t = esc(s);
    t = t.replace(/\{\{(\w+)\}\}/g, function (m, k) { return datos && k in datos ? esc(datos[k]) : m; });
    t = t.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    t = t.replace(/\[([^\]]+)\]/g, '<em class="as-ph">[$1]</em>');
    return t.replace(/\n/g, "<br>");
  }
  var NOMBRES = { video: "Video", vertical: "Video vertical", imagen: "Imagen", audio: "Audio", texto: "Texto" };
  /* Espacio por llenar: tipo = video | vertical | imagen | audio | texto */
  function hueco(tipo, nota) {
    return '<div class="as-hueco as-hueco--' + tipo + '" role="img" aria-label="Espacio para ' + (NOMBRES[tipo] || tipo) + '">' +
      "<b>" + (NOMBRES[tipo] || tipo) + "</b><span>" + esc(nota || "") + "</span></div>";
  }
  /* Medio: si no hay archivo (src vacío) pinta el espacio por llenar */
  function medio(m) {
    if (!m) return "";
    if (!m.src) return hueco(m.tipo, m.nota);
    if (m.tipo === "imagen") return '<img src="' + esc(m.src) + '" alt="' + esc(m.alt || "") + '" loading="lazy">';
    if (m.tipo === "audio") return '<audio controls preload="none" src="' + esc(m.src) + '" style="width:100%"></audio>' +
      (m.transcripcion ? '<details><summary>Leer transcripción</summary><p class="as-sec">' + texto(m.transcripcion) + "</p></details>" : "");
    return '<video controls playsinline preload="metadata" src="' + esc(m.src) + '"' + (m.poster ? ' poster="' + esc(m.poster) + '"' : "") +
      ' style="width:100%;border-radius:12px;background:#000">' +
      (m.subtitulos ? '<track kind="captions" srclang="es" label="Español" src="' + esc(m.subtitulos) + '" default>' : "") + "</video>";
  }
  function mezclar(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function pesos(n) { return "$" + Math.round(n).toLocaleString("es-CO"); }

  /* ---------- Esqueleto de pantalla ---------- */
  function marco(c) {
    document.title = c.titulo || document.title;
    document.body.className = "as";
    document.body.innerHTML =
      '<div class="as-app">' +
      '<header class="as-top"><div class="as-top__fila"><div><div class="as-eti">' + esc(c.paso || "") + " · " + esc(c.unidad || "") +
      '</div><h1>' + esc(c.titulo || "") + '</h1></div><span class="as-chip as-chip--rojo" id="as-cuenta"></span></div>' +
      '<div class="as-barra" aria-hidden="true"><i id="as-progreso" style="width:0"></i></div></header>' +
      '<main class="as-cuerpo" id="as-cuerpo" aria-live="polite"></main>' +
      '<footer class="as-pie" id="as-pie"></footer></div>';
    return {
      cuerpo: document.getElementById("as-cuerpo"),
      pie: document.getElementById("as-pie"),
      progreso: function (actual, total, etiqueta) {
        document.getElementById("as-progreso").style.width = Math.round((actual / total) * 100) + "%";
        document.getElementById("as-cuenta").textContent = etiqueta || actual + " de " + total;
      },
      arriba: function () { window.scrollTo(0, 0); }
    };
  }
  /* Pantalla final común */
  function final(ui, c, nota, detalle) {
    ui.progreso(1, 1, "Listo");
    ui.cuerpo.innerHTML = '<div class="as-tarjeta as-pila as-final">' +
      (typeof nota === "number" ? '<div class="as-final__nota as-num">' + Math.round(nota) + "</div><div class=\"as-eti\">de 100</div>" : "") +
      "<h2>" + texto(c.final && c.final.titulo || "¡Terminaste!") + "</h2>" +
      '<p class="as-sec">' + texto(detalle || (c.final && c.final.texto) || "") + "</p>" +
      '<span class="as-chip ' + (scorm.activo() ? "as-chip--ok\">Resultado enviado a Moodle" : "as-chip--gris\">Vista previa: sin conexión a Moodle") + "</span></div>";
    ui.pie.innerHTML = '<button class="as-btn as-btn--sec" id="as-otra">Volver a intentar</button>';
    document.getElementById("as-otra").onclick = function () { location.reload(); };
    scorm.terminar(nota, c.notaMinima);
  }

  window.Aula = { scorm: scorm, esc: esc, texto: texto, hueco: hueco, medio: medio, mezclar: mezclar, pesos: pesos, marco: marco, final: final };
  scorm.conectar();
})();
