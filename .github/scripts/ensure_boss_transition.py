from pathlib import Path

p=Path('index.html')
s=p.read_text()

# Trigger the boss slightly before the original level-1 edge so the transition
# cannot be skipped by a fast run, jetpack movement, or a large frame step.
s=s.replace(
    'if(!bossMode && !bossDefeated && player.x>NORMAL_WORLD_END){',
    'if(!bossMode && !bossDefeated && player.x>=NORMAL_WORLD_END-40){'
)

# Shorter, clearer transition and a brief safety window on arrival.
s=s.replace('bossIntroTimer=165;', 'bossIntroTimer=120;')
needle='''    bossMode=true;\n    bossIntroTimer=120;'''
if needle in s and 'playerInvuln=120;' not in s[s.index(needle):s.index(needle)+160]:
    s=s.replace(needle, needle+'\n    playerInvuln=120;', 1)

# Make the transition message explicit so the player knows level 2 has begun.
s=s.replace(
    "ctx.fillText('FINAL PROBLEM: EXCAVATOR',W/2,H/2+12);",
    "ctx.fillText('BOSS LEVEL: EXCAVATOR',W/2,H/2+12);"
)

p.write_text(s)
print('Boss transition hardened')
