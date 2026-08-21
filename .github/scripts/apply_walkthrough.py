from pathlib import Path

p = Path('index.html')
s = p.read_text()

s = s.replace(
    'let player, platforms, blueprints, hazards, enemies, coins, checkpoints, debris, jetpacks;',
    'let player, platforms, blueprints, hazards, enemies, coins, checkpoints, debris, jetpacks, walkthroughBuildings;'
)

s = s.replace(
    'platforms=[]; blueprints=[]; hazards=[]; enemies=[]; coins=[]; checkpoints=[]; debris=[]; jetpacks=[];',
    """platforms=[]; blueprints=[]; hazards=[]; enemies=[]; coins=[]; checkpoints=[]; debris=[]; jetpacks=[];\n\n    walkthroughBuildings=[\n      {x:1180,w:430,h:235,label:'STUDIO',tone:0},\n      {x:4050,w:520,h:285,label:'CIVIC HALL',tone:1},\n      {x:7650,w:470,h:255,label:'DESIGN LAB',tone:2}\n    ];"""
)

if 'function playerInsideWalkthroughBuilding' not in s:
    insert = r'''  function playerInsideWalkthroughBuilding(b){
    const cx=player.x+player.w/2;
    return cx>b.x+18 && cx<b.x+b.w-18 && player.y+player.h>groundY-b.h+24;
  }

  function drawWalkthroughBuildings(){
    if(!walkthroughBuildings) return;
    for(const b of walkthroughBuildings){
      if(!visible(b.x,b.w,180)) continue;
      const x=sx(b.x);
      const top=groundY-b.h;
      const inside=playerInsideWalkthroughBuilding(b);

      ctx.fillStyle=inside?'rgba(232,228,214,.96)':'rgba(214,218,216,.96)';
      ctx.fillRect(x,top,b.w,b.h);

      ctx.fillStyle='rgba(112,145,158,.42)';
      for(let wx=x+28;wx<x+b.w-24;wx+=58) ctx.fillRect(wx,top+28,34,b.h-86);

      ctx.strokeStyle='rgba(61,70,74,.55)';
      ctx.lineWidth=4;
      const levels=Math.max(2,Math.floor(b.h/82));
      for(let i=1;i<levels;i++){
        const yy=top+i*(b.h/levels);
        ctx.beginPath();ctx.moveTo(x+18,yy);ctx.lineTo(x+b.w-18,yy);ctx.stroke();
      }
      for(let cx=x+52;cx<x+b.w-28;cx+=96){
        ctx.beginPath();ctx.moveTo(cx,top+18);ctx.lineTo(cx,groundY);ctx.stroke();
      }

      const doorW=116;
      const doorX=x+b.w/2-doorW/2;
      ctx.fillStyle='rgba(33,43,48,.25)';
      ctx.fillRect(doorX,groundY-96,doorW,96);
      ctx.strokeStyle='rgba(235,245,248,.75)';
      ctx.lineWidth=2;
      ctx.strokeRect(doorX+8,groundY-88,doorW-16,80);

      ctx.globalAlpha=inside?0.18:0.72;
      ctx.fillStyle=b.tone===0?'#66757c':(b.tone===1?'#7d7467':'#65736a');
      ctx.fillRect(x,top,b.w,b.h);

      ctx.globalAlpha=inside?0.08:0.30;
      ctx.fillStyle='#b9d6df';
      ctx.fillRect(doorX,groundY-96,doorW,96);
      ctx.globalAlpha=1;

      ctx.fillStyle='#f4f0df';
      ctx.font='700 13px system-ui';
      ctx.fillText(b.label,x+20,top+22);

      ctx.fillStyle=inside?'#66ef89':'#f2b94b';
      ctx.fillRect(doorX+22,groundY-118,doorW-44,18);
      ctx.fillStyle='#182026';
      ctx.font='10px system-ui';
      ctx.fillText(inside?'INSIDE':'WALK THROUGH',doorX+28,groundY-105);
    }
  }

  function drawWalkthroughForeground(){
    if(!walkthroughBuildings) return;
    for(const b of walkthroughBuildings){
      if(!visible(b.x,b.w,120)) continue;
      const x=sx(b.x);
      const top=groundY-b.h;
      const inside=playerInsideWalkthroughBuilding(b);
      const doorW=116;
      const doorX=x+b.w/2-doorW/2;

      ctx.globalAlpha=inside?0.42:0.88;
      ctx.fillStyle='#3f494e';
      ctx.fillRect(x,top,14,b.h);
      ctx.fillRect(x+b.w-14,top,14,b.h);
      ctx.fillRect(x,top,b.w,10);
      ctx.fillRect(doorX-8,groundY-104,8,104);
      ctx.fillRect(doorX+doorW,groundY-104,8,104);
      ctx.fillRect(doorX-8,groundY-104,doorW+16,8);
      ctx.globalAlpha=1;
    }
  }

'''
    s = s.replace('  function drawPlayer(){', insert + '  function drawPlayer(){', 1)

if 'drawWalkthroughBuildings();' not in s:
    s = s.replace('    drawSkyline();', '    drawSkyline();\n    drawWalkthroughBuildings();', 1)

if 'drawWalkthroughForeground();' not in s:
    s = s.replace('    drawPlayer();', '    drawPlayer();\n    drawWalkthroughForeground();', 1)

s = s.replace(
    '<span>🗞️ X = blueprint tube</span>',
    '<span>🗞️ X = blueprint tube</span><span>🏢 some buildings are walk-through</span>'
)

p.write_text(s)
