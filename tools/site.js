(function(){
var d=document,w=window,cfg=w.XANDRA||{};
var mb=d.querySelector(".menu-btn"),nav=d.getElementById("nav");
if(mb&&nav)mb.addEventListener("click",function(){var o=nav.classList.toggle("open");mb.setAttribute("aria-expanded",o)});

/* Google tag + Hotjar: loaded after first interaction or 4s after load */
var started=false;
function add(src){var s=d.createElement("script");s.async=true;s.src=src;d.head.appendChild(s)}
function track(){
  if(started)return;started=true;
  w.dataLayer=w.dataLayer||[];w.gtag=function(){w.dataLayer.push(arguments)};
  w.gtag("js",new Date());w.gtag("set","linker",{domains:["www.xandrallc.com"]});w.gtag("config",cfg.gtag);
  add("https://www.googletagmanager.com/gtag/js?id="+cfg.gtag);
  w.hj=w.hj||function(){(w.hj.q=w.hj.q||[]).push(arguments)};w._hjSettings={hjid:cfg.hj,hjsv:6};
  add("https://static.hotjar.com/c/hotjar-"+cfg.hj+".js?sv=6");
}
["pointerdown","keydown","touchstart","scroll"].forEach(function(e){w.addEventListener(e,track,{once:true,passive:true})});
w.addEventListener("load",function(){setTimeout(track,4000)});
})();
