from pathlib import Path

p=Path('index.html')
s=p.read_text()

old="""    if(player.jetpack && keys[' ']) player.vy -= 0.9;\n\n    player.vy += gravity;"""
new="""    // Jetpack: stronger initial lift, but capped so the architect never rockets off-screen.\n    if(player.jetpack && keys[' ']){\n      player.vy -= 1.05;\n      if(player.vy < -5.4) player.vy = -5.4;\n    }\n\n    player.vy += gravity;"""
if old not in s:
    raise RuntimeError('Jetpack thrust block not found')
s=s.replace(old,new,1)

old2="""    player.x = clamp(player.x,0,WORLD_W-player.w);\n    player.onGround=false;"""
new2="""    player.x = clamp(player.x,0,WORLD_W-player.w);\n\n    // Keep the architect visible while flying. The game has a fixed vertical camera,\n    // so the jetpack gets a soft ceiling instead of allowing the player above the canvas.\n    if(player.jetpack && player.y < 38){\n      player.y = 38;\n      if(player.vy < 0) player.vy = 0;\n    }\n    player.onGround=false;"""
if old2 not in s:
    raise RuntimeError('Player clamp block not found')
s=s.replace(old2,new2,1)

# Make the mobile hint clearer.
s=s.replace('hold JET after pickup','hold JET to fly · release to descend')

p.write_text(s)
print('Jetpack tuned for controlled, on-screen flight')
