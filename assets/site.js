document.querySelector('.menu-btn')?.addEventListener('click',e=>{const n=document.querySelector('nav.main');n.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',n.classList.contains('open'))});
document.querySelectorAll('form[data-signup]').forEach(f=>{
  const sp=f.querySelector('[name=source_page]');if(sp)sp.value=location.pathname;
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    const n=f.querySelector('.notice'),b=f.querySelector('button[type=submit],button');
    const key=(f.querySelector('[name=access_key]')||{}).value||'';
    const honey=f.querySelector('[name=botcheck]');
    if(honey&&honey.checked)return;
    if(!key||key==='YOUR_WEB3FORMS_ACCESS_KEY'||f.getAttribute('data-connected')==='false'){
      n.textContent='Signup is not connected yet. The free Agent ID Badge is still available on the thanks page once email is live — or email traciandersonart@gmail.com to enlist.';
      return;
    }
    b.disabled=true;n.textContent='Transmitting on a secure channel…';
    const ac=('AbortController' in window)?new AbortController():null;let timedOut=false;
    const t=setTimeout(()=>{timedOut=true;if(ac)ac.abort()},12000);
    try{
      const r=await fetch(f.action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f),signal:ac?ac.signal:undefined});
      clearTimeout(t);
      const j=await r.json().catch(()=>({}));
      if(r.ok&&(j.success===true||j.success==='true')){
        const next=(f.querySelector('[name=redirect]')||{}).value||'/thanks.html';
        location.href=next;return;
      }
      throw 0;
    }catch(_){
      clearTimeout(t);
      n.textContent=timedOut
        ?'Channel is slow. Please try again in a minute, or email traciandersonart@gmail.com to enlist.'
        :'Signal jammed. Please try again in a minute, or email traciandersonart@gmail.com to enlist.';
    }
    b.disabled=false;
  });
});
if(/[?&]enlisted=1/.test(location.search))document.querySelectorAll('form[data-signup] .notice').forEach(n=>n.textContent='You’re in, agent. Watch your inbox (and your back).');
