const {chromium}=require('playwright');const OUT=__dirname+'/shots/';const U='http://localhost:8765/index.html';
const pos=(p,sel,dy)=>p.evaluate(([sel,dy])=>{const e=document.querySelector(sel);return Math.max(0,e.getBoundingClientRect().top+scrollY+dy)},[sel,dy]);
async function run(p,prefix,list){for(const [k,sel,dy] of list){const y=await pos(p,sel,dy);await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(400);await p.evaluate(y=>scrollTo(0,y+1),y);await p.waitForTimeout(2600);
 await p.evaluate(()=>{const n=document.querySelector('[data-nav]');n&&n.classList.remove('is-hidden')});await p.waitForTimeout(400);await p.screenshot({path:`${OUT}${prefix}-${k}.jpg`,type:'jpeg',quality:84});}}
(async()=>{const b=await chromium.launch();
 const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});const p=await c.newPage();await p.goto(U);await p.waitForFunction(()=>!document.querySelector('.loader'),null,{timeout:20000});await p.waitForTimeout(600);
 await run(p,'d',[['refuge-text','.refuge',40],['heritage-text','.heritage',60],['arch','.arch',-200]]);await c.close();
 const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2.5,isMobile:true,hasTouch:true,locale:'es-CL'});const q=await m.newPage();await q.goto(U);await q.waitForFunction(()=>!document.querySelector('.loader'),null,{timeout:20000});await q.waitForTimeout(600);
 await run(q,'m',[['chapter','.chapter',40],['refuge-text','.refuge',40],['rooms','.rooms',30],['kitchen','.kitchen',30],['table','.table',30],['heritage-text','.heritage',40],['hosts','.hosts',30],['arrive','#llegar',0],['arch','.arch',-120],['book','.book',0]]);
 await m.close();await b.close();console.log('ok')})();
