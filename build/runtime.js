class DCLogic{constructor(p){this.props=p||{};this.state={}}setState(p){Object.assign(this.state,typeof p==='function'?p(this.state):p);this._r&&this._r()}}
function boot(C){
  const fixImg=(s)=>s.replace(/\/_blob\/([0-9a-f]{32})/g,(m,i)=>IMG[i]||m);
  document.getElementById('app-css').textContent=fixImg(document.getElementById('css-src').textContent);
  const tpl=document.createElement('template');tpl.innerHTML=document.getElementById('tpl').textContent;
  const inst=new C({});let handlers=[];
  const get=(p,sc)=>{const parts=p.trim().split('.');let v=sc[parts[0]];for(let i=1;i<parts.length&&v!=null;i++)v=v[parts[i]];return v};
  const HOLE=/\{\{\s*([^}]*?)\s*\}\}/g;
  const interp=(s,sc)=>s.replace(HOLE,(m,p)=>{const v=get(p,sc);return v==null||v===false?'':String(v)});
  function build(n,sc,par){
    if(n.nodeType===3){par.appendChild(document.createTextNode(HOLE.test(n.nodeValue)?(HOLE.lastIndex=0,interp(n.nodeValue,sc)):n.nodeValue));HOLE.lastIndex=0;return}
    if(n.nodeType!==1)return;
    const tag=n.localName;
    if(tag==='sc-for'){const as=n.getAttribute('as');const list=get(n.getAttribute('list').replace(/[{}]/g,''),sc)||[];list.forEach((it,i)=>{const s2=Object.create(sc);s2[as]=it;s2.index=i;n.childNodes.forEach(c=>build(c,s2,par))});return}
    if(tag==='sc-if'){if(get(n.getAttribute('value').replace(/[{}]/g,''),sc))n.childNodes.forEach(c=>build(c,sc,par));return}
    const el=document.createElementNS(n.namespaceURI,tag);
    for(const a of n.attributes){
      const nm=a.name;if(nm.startsWith('hint-'))continue;
      if(/^on[a-z]+$/.test(nm)){const fn=get(a.value.replace(/[{}]/g,''),sc);if(typeof fn==='function'){handlers.push(fn);el.setAttribute('data-ev-'+nm.slice(2),handlers.length-1)}continue}
      el.setAttribute(nm,fixImg(interp(a.value,sc)));
    }
    n.childNodes.forEach(c=>build(c,sc,el));par.appendChild(el);
  }
  function morph(o,n){
    if(o.nodeType!==n.nodeType||o.nodeName!==n.nodeName){o.replaceWith(n);return}
    if(o.nodeType===3){if(o.nodeValue!==n.nodeValue)o.nodeValue=n.nodeValue;return}
    for(const a of [...o.attributes])if(!n.hasAttribute(a.name))o.removeAttribute(a.name);
    for(const a of n.attributes)if(o.getAttribute(a.name)!==a.value)o.setAttribute(a.name,a.value);
    if(o.localName==='input'||o.localName==='textarea'||o.localName==='select'){if(n.hasAttribute('value')&&o.value!==n.getAttribute('value')&&o.type!=='file')o.value=n.getAttribute('value')}
    const oc=[...o.childNodes],nc=[...n.childNodes];
    nc.forEach((c,i)=>{if(oc[i])morph(oc[i],c);else o.appendChild(c)});
    for(let i=nc.length;i<oc.length;i++)oc[i].remove();
  }
  const app=document.getElementById('app');
  function render(){
    handlers=[];const sc=Object.assign({},inst.renderVals());const box=document.createElement('div');
    tpl.content.childNodes.forEach(c=>build(c,sc,box));
    if(!app.firstChild){while(box.firstChild)app.appendChild(box.firstChild)}
    else{const oc=[...app.childNodes],nc=[...box.childNodes];nc.forEach((c,i)=>{if(oc[i])morph(oc[i],c);else app.appendChild(c)});for(let i=nc.length;i<oc.length;i++)oc[i].remove()}
  }
  let queued=false;inst._r=()=>{if(queued)return;queued=true;Promise.resolve().then(()=>{queued=false;render()})};
  ['click','input','change','submit'].forEach(t=>document.addEventListener(t,e=>{const el=e.target.closest&&e.target.closest('[data-ev-'+t+']');if(!el)return;const h=handlers[+el.getAttribute('data-ev-'+t)];if(h)h(e)}));
  render();
  if(inst.componentDidMount)inst.componentDidMount();
}
