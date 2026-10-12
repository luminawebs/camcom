/* Portada: cada tarjeta .as-sec-N lleva a la primera actividad visible de la sección N. */
document.addEventListener("DOMContentLoaded",function(){
  var p=document.querySelector(".course-content .as-portada");
  if(!p){return;}
  document.body.classList.add("as-con-portada");
  p.querySelectorAll("a.as-portada__unidad").forEach(function(a){
    var m=a.className.match(/as-sec-(\d+)/);
    if(!m){return;}
    var s=document.getElementById("section-"+m[1]);
    var l=s&&s.querySelector(".activity:not(.dimmed) a.aalink, .activity a.aalink");
    if(l){a.href=l.href;return;}
    var c=document.body.className.match(/\bcourse-(\d+)\b/);
    if(c){a.href=M.cfg.wwwroot+"/course/view.php?id="+c[1]+"&section="+m[1];}
  });
});
