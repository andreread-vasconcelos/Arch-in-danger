from pathlib import Path

p = Path('index.html')
s = p.read_text()

start = s.index('  function ensureAudio(){')
end = s.index("\n\n  addEventListener('keydown'", start)

new = r'''  function ensureAudio(){
    try{
      if(!audioCtx){
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if(!AudioContextClass) return null;
        audioCtx = new AudioContextClass();
      }
      return audioCtx;
    }catch(e){
      return null;
    }
  }

  function unlockAudio(){
    const ac=ensureAudio();
    if(!ac) return;
    try{
      if(ac.state !== 'running'){
        const resumeResult=ac.resume();
        if(resumeResult && typeof resumeResult.catch === 'function') resumeResult.catch(()=>{});
      }
      const osc=ac.createOscillator();
      const gain=ac.createGain();
      const now=ac.currentTime;
      gain.gain.setValueAtTime(0.00001,now);
      osc.connect(gain); gain.connect(ac.destination);
      osc.start(now); osc.stop(now+0.012);
    }catch(e){}
  }

  function runWithAudio(buildSound){
    const ac=ensureAudio();
    if(!ac) return;
    const play=()=>{
      try{ buildSound(ac); }catch(e){}
    };
    if(ac.state === 'running'){
      play();
      return;
    }
    try{
      const resumeResult=ac.resume();
      if(resumeResult && typeof resumeResult.then === 'function'){
        resumeResult.then(()=>play()).catch(()=>{});
      }else{
        setTimeout(play,0);
      }
    }catch(e){}
  }

  function playJumpSound(isDouble){
    runWithAudio(ac=>{
      const now=ac.currentTime;
      const osc=ac.createOscillator();
      const gain=ac.createGain();
      const shimmer=ac.createOscillator();
      const shimmerGain=ac.createGain();

      osc.type='square';
      osc.frequency.setValueAtTime(isDouble ? 520 : 390,now);
      osc.frequency.exponentialRampToValueAtTime(isDouble ? 800 : 620,now+0.09);
      gain.gain.setValueAtTime(0.0001,now);
      gain.gain.exponentialRampToValueAtTime(0.085,now+0.008);
      gain.gain.exponentialRampToValueAtTime(0.0001,now+0.14);

      shimmer.type='sine';
      shimmer.frequency.setValueAtTime(isDouble ? 1040 : 780,now);
      shimmer.frequency.exponentialRampToValueAtTime(isDouble ? 1320 : 980,now+0.08);
      shimmerGain.gain.setValueAtTime(0.0001,now);
      shimmerGain.gain.exponentialRampToValueAtTime(isDouble ? 0.03 : 0.020,now+0.01);
      shimmerGain.gain.exponentialRampToValueAtTime(0.0001,now+0.11);

      osc.connect(gain); gain.connect(ac.destination);
      shimmer.connect(shimmerGain); shimmerGain.connect(ac.destination);
      osc.start(now); shimmer.start(now);
      osc.stop(now+0.15); shimmer.stop(now+0.12);
    });
  }

  function playBlueprintSwing(){
    runWithAudio(ac=>{
      const now=ac.currentTime;
      const osc=ac.createOscillator();
      const gain=ac.createGain();
      osc.type='triangle';
      osc.frequency.setValueAtTime(300,now);
      osc.frequency.exponentialRampToValueAtTime(115,now+0.09);
      gain.gain.setValueAtTime(0.0001,now);
      gain.gain.exponentialRampToValueAtTime(0.065,now+0.006);
      gain.gain.exponentialRampToValueAtTime(0.0001,now+0.11);
      osc.connect(gain); gain.connect(ac.destination);
      osc.start(now); osc.stop(now+0.12);
    });
  }

  function playBlueprintImpact(){
    runWithAudio(ac=>{
      const now=ac.currentTime;
      const osc=ac.createOscillator();
      const gain=ac.createGain();
      osc.type='square';
      osc.frequency.setValueAtTime(170,now);
      osc.frequency.exponentialRampToValueAtTime(70,now+0.10);
      gain.gain.setValueAtTime(0.0001,now);
      gain.gain.exponentialRampToValueAtTime(0.09,now+0.004);
      gain.gain.exponentialRampToValueAtTime(0.0001,now+0.13);
      osc.connect(gain); gain.connect(ac.destination);
      osc.start(now); osc.stop(now+0.14);
    });
  }'''

s = s[:start] + new + s[end:]
s = s.replace("      ensureAudio();\n      jumpPressed = true;", "      unlockAudio();\n      jumpPressed = true;")
s = s.replace("      ensureAudio();\n      attackPressed = true;", "      unlockAudio();\n      attackPressed = true;")

needle = "  addEventListener('keyup', e => keys[e.key] = false);"
replacement = "  addEventListener('keyup', e => keys[e.key] = false);\n  addEventListener('pointerdown', unlockAudio, {passive:true});\n  addEventListener('touchstart', unlockAudio, {passive:true});"
if needle in s and 'pointerdown' not in s:
    s = s.replace(needle, replacement, 1)

p.write_text(s)
