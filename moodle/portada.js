/* Portada: cada tarjeta .as-sec-N lleva a la primera actividad visible de la sección N. */
/* Las tarjetas del Pase (data-sec="N") llevan a la compra; si la persona ya puede entrar a la sección, llevan a la unidad. */
/* Como la portada oculta las secciones 1+, un enlace #section-N del índice abre la página de esa sección. */
/* D-05: un enlace de campaña portal.edunest.co/?c=<canal> lleva al registro gratis del Pase con su código (el portal no tiene registro propio). */
(function(){var m=location.search.match(/[?&]c=([A-Za-z0-9-]{1,40})(&|$)/);if(m&&/^\/(index\.php)?$/.test(location.pathname)){location.replace("https://pase.edunest.co/?c="+encodeURIComponent(m[1].toLowerCase()));}})();
document.addEventListener("DOMContentLoaded",function(){
  var p=document.querySelector(".course-content .as-portada");
  if(!p){return;}
  document.body.classList.add("as-con-portada");
  var c=document.body.className.match(/\bcourse-(\d+)\b/);
  var seccion=function(n){return M.cfg.wwwroot+"/course/view.php?id="+c[1]+"&section="+n;};
  p.querySelectorAll("a.as-portada__unidad").forEach(function(a){
    var m=a.className.match(/as-sec-(\d+)/)||[null,a.getAttribute("data-sec")];
    if(!m[1]){return;}
    var s=document.getElementById("section-"+m[1]);
    if(a.hasAttribute("data-sec")&&(!s||s.querySelector(".section_availability .availabilityinfo"))){return;}
    a.removeAttribute("target");
    var l=s&&s.querySelector(".activity:not(.dimmed) a.aalink, .activity a.aalink");
    if(l){a.href=l.href;return;}
    if(c){a.href=seccion(m[1]);}
  });
  var ir=function(){
    var h=location.hash.match(/^#section-(\d+)$/);
    if(c&&h&&h[1]!=="0"&&!document.body.classList.contains("editing")){location.href=seccion(h[1]);}
  };
  window.addEventListener("hashchange",ir);
  ir();
});
