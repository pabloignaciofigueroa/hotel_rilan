// Capturas estáticas de cada sección del sitio para el dossier (escritorio y celular).
const {chromium}=require('playwright');
const OUT=__dirname+'/shots/';
const U='http://localhost:8765/index.html';
const S=[ // [clave, selector, modo, extra]
 ['hero','.hero','top'],
 ['portal-a','.portal','frac',0.16],
 ['portal-b','.portal','frac',0.97],
 ['welcome','.welcome','center'],
 ['territory','#territory','top'],
 ['chapter','.chapter','center'],
 ['hscroll','.hscroll','offset',0.22],
 ['mysticism','#mysticism','top'],
 ['silence','.silence','center'],
 ['listen','.listen','top'],
 ['refuge','#refuge','top'],
 ['refuge-text','.refuge','offset',0.08],
 ['rooms','.rooms','offset',0.05],
 ['fire','.fire','top'],
 ['kitchen','.kitchen','offset',0.12],
 ['cocktail','.cocktail','center'],
 ['cava','.cava','top'],
 ['table','.table','center'],
 ['heritage','#heritage','top'],
 ['heritage-text','.heritage','offset',0.16],
 ['arch','.arch','center'],
 ['hosts','.hosts','center'],
 ['arrive','#llegar','top'],
 ['book','.book','top'],
 ['foot','.foot','bottom'],
];
async function shoot(p,vh,prefix,list){
  for(const [k,sel,mode,x] of list){
    const y=await p.evaluate(([sel,mode,x,vh])=>{const e=document.querySelector(sel);const top=e.getBoundingClientRect().top+scrollY;const h=e.offsetHeight;
      if(mode==='top')return top; if(mode==='frac')return top+(h-vh)*x; if(mode==='offset')return top+h*x; if(mode==='bottom')return top+h-vh; return top+(h-vh)/2;},[sel,mode,x,vh]);
    await p.evaluate(y=>window.scrollTo(0,y),Math.max(0,y));
    await p.waitForTimeout(400);await p.evaluate(y=>window.scrollTo(0,y),Math.max(0,y)+1);
    await p.waitForTimeout(2600);
    await p.evaluate(()=>{const n=document.querySelector('[data-nav]');n&&n.classList.remove('is-hidden')});
    await p.waitForTimeout(500);
    await p.screenshot({path:`${OUT}${prefix}-${k}.jpg`,type:'jpeg',quality:84});
  }
}
(async()=>{const b=await chromium.launch();
 // escritorio
 const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});const p=await c.newPage();
 await p.goto(U);await p.waitForTimeout(1050);await p.screenshot({path:OUT+'d-loader.jpg',type:'jpeg',quality:84});
 await p.waitForFunction(()=>!document.querySelector('.loader'),null,{timeout:20000});await p.waitForTimeout(800);
 await shoot(p,900,'d',S);
 // menú abierto
 await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);await p.setViewportSize({width:1000,height:900});await p.waitForTimeout(800);
 await p.click('[data-menu-open]');await p.waitForTimeout(1500);await p.hover('[data-menu-key="refuge"]');await p.waitForTimeout(1200);await p.screenshot({path:OUT+'d-menu.jpg',type:'jpeg',quality:84});
 await c.close();
 // celular
 const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2.5,isMobile:true,hasTouch:true,locale:'es-CL'});const q=await m.newPage();
 await q.goto(U);await q.waitForFunction(()=>!document.querySelector('.loader'),null,{timeout:20000});await q.waitForTimeout(800);
 await shoot(q,844,'m',S.filter(s=>!['portal-a','hscroll'].includes(s[0])));
 await m.close();await b.close();console.log('listo');
})();
