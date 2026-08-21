from pathlib import Path

p = Path('index.html')
s = p.read_text()

if 'id="mobileControls"' in s:
    print('Mobile controls already present')
    raise SystemExit(0)

css = r'''

  /* Phone / touch controls */
  .mobile-controls{
    display:none;
    padding:12px;
    background:#0e1318;
    border-top:1px solid #272c33;
    user-select:none;
    -webkit-user-select:none;
    -webkit-touch-callout:none;
    touch-action:none;
  }
  .mobile-row{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .mobile-group{display:flex;align-items:center;gap:9px}
  .mobile-btn{
    appearance:none;
    -webkit-appearance:none;
    min-width:64px;
    height:62px;
    padding:0 13px;
    border:1px solid #48515b;
    border-bottom-width:3px;
    border-radius:17px;
    background:#202833;
    color:#fff;
    font:700 22px/1 system-ui,-apple-system,sans-serif;
    box-shadow:0 4px 12px rgba(0,0,0,.28);
    touch-action:none;
  }
  .mobile-btn span{display:block;font-size:10px;font-weight:600;opacity:.72;margin-top:5px;letter-spacing:.04em}
  .mobile-btn.attack{background:#734029;border-color:#a56647}
  .mobile-btn.jump{background:#22577a;border-color:#3c7ca5}
  .mobile-btn.jet{background:#6a4b20;border-color:#9d7133}
  .mobile-btn.utility{height:40px;min-width:auto;padding:0 14px;font-size:13px;border-radius:12px;background:#171d24}
  .mobile-btn.active,.mobile-btn:active{transform:translateY(2px);border-bottom-width:1px;filter:brightness(1.25)}
  .mobile-utility-row{display:flex;justify-content:center;gap:10px;margin-top:10px}
  .mobile-hint{text-align:center;font-size:11px;opacity:.55;margin-top:8px}

  @media (hover:none) and (pointer:coarse), (max-width:820px){
    body{padding:0;gap:0}
    .top{padding:10px 12px;align-items:center}
    .top .pill{display:none}
    .game-shell{width:100%;border-left:0;border-right:0;border-radius:0}
    .hud{padding:8px 10px}
    .controls{display:none}
    .mobile-controls{display:block}
    .footer{padding:8px 12px}
    canvas{touch-action:none}
  }

  @media (max-width:520px){
    h1{font-size:21px}
    .sub{font-size:12px}
    .mobile-btn{min-width:58px;height:58px;padding:0 10px;font-size:20px}
    .mobile-group{gap:7px}
    .mobile-row{gap:8px}
  }
'''

s = s.replace('</style>', css + '\n</style>', 1)

controls = r'''
    <div class="mobile-controls" id="mobileControls" aria-label="Touch game controls">
      <div class="mobile-row">
        <div class="mobile-group" aria-label="Walking controls">
          <button class="mobile-btn" id="mobileLeft" type="button" aria-label="Walk left">◀<span>LEFT</span></button>
          <button class="mobile-btn" id="mobileRight" type="button" aria-label="Walk right">▶<span>RIGHT</span></button>
        </div>
        <div class="mobile-group" aria-label="Action controls">
          <button class="mobile-btn jump" id="mobileJump" type="button" aria-label="Jump or double jump">↑<span>JUMP</span></button>
          <button class="mobile-btn attack" id="mobileAttack" type="button" aria-label="Swing blueprint tube">✕<span>HIT</span></button>
          <button class="mobile-btn jet" id="mobileJet" type="button" aria-label="Use jetpack">▲<span>JET</span></button>
        </div>
      </div>
      <div class="mobile-utility-row">
        <button class="mobile-btn utility" id="mobileRestart" type="button">↻ Restart</button>
        <button class="mobile-btn utility" id="mobileFullscreen" type="button">⛶ Full screen</button>
      </div>
      <div class="mobile-hint">Hold ◀ / ▶ to walk · tap JUMP twice for double jump · hold JET after pickup</div>
    </div>
'''

needle = '    </div>\n  </div>\n  <div class="footer">'
if needle not in s:
    raise RuntimeError('Could not find game-shell insertion point')
s = s.replace(needle, '    </div>\n' + controls + '  </div>\n  <div class="footer">', 1)

js = r'''

  // Touch controls use the same game state as the keyboard, so phone and desktop
  // remain behaviorally identical.
  function setMobileActive(el,on){
    if(!el) return;
    el.classList.toggle('active',!!on);
  }

  function bindMobileHold(id,key){
    const el=document.getElementById(id);
    if(!el) return;
    const down=e=>{
      e.preventDefault();
      unlockAudio();
      keys[key]=true;
      setMobileActive(el,true);
      try{ if(e.pointerId!==undefined) el.setPointerCapture(e.pointerId); }catch(_){}
    };
    const up=e=>{
      if(e) e.preventDefault();
      keys[key]=false;
      setMobileActive(el,false);
    };
    el.addEventListener('pointerdown',down);
    el.addEventListener('pointerup',up);
    el.addEventListener('pointercancel',up);
    el.addEventListener('lostpointercapture',up);
    el.addEventListener('contextmenu',e=>e.preventDefault());
  }

  function bindMobileTap(id,fn){
    const el=document.getElementById(id);
    if(!el) return;
    el.addEventListener('pointerdown',e=>{
      e.preventDefault();
      unlockAudio();
      setMobileActive(el,true);
      fn();
      try{ if(e.pointerId!==undefined) el.setPointerCapture(e.pointerId); }catch(_){}
    });
    const up=e=>{
      if(e) e.preventDefault();
      setMobileActive(el,false);
    };
    el.addEventListener('pointerup',up);
    el.addEventListener('pointercancel',up);
    el.addEventListener('lostpointercapture',up);
    el.addEventListener('contextmenu',e=>e.preventDefault());
  }

  bindMobileHold('mobileLeft','ArrowLeft');
  bindMobileHold('mobileRight','ArrowRight');
  bindMobileHold('mobileJet',' ');
  bindMobileTap('mobileJump',()=>{ jumpPressed=true; });
  bindMobileTap('mobileAttack',()=>{ attackPressed=true; });
  bindMobileTap('mobileRestart',()=>{ resetGame(); });
  bindMobileTap('mobileFullscreen',()=>{
    const shell=document.querySelector('.game-shell');
    try{
      if(document.fullscreenElement){
        document.exitFullscreen();
      }else if(shell && shell.requestFullscreen){
        shell.requestFullscreen();
      }
    }catch(_){}
  });

  // Prevent a stuck movement button if the browser loses focus or the finger
  // leaves the page unexpectedly.
  addEventListener('blur',()=>{
    keys.ArrowLeft=false;
    keys.ArrowRight=false;
    keys[' ']=false;
    document.querySelectorAll('.mobile-btn.active').forEach(el=>el.classList.remove('active'));
  });
'''

marker = "\n  function seededNoise(n){"
if marker not in s:
    raise RuntimeError('Could not find JavaScript insertion point')
s = s.replace(marker, js + marker, 1)

p.write_text(s)
print('Added touch/mobile controls')
