# Arch in Danger

A recovered and completed browser game based on the original **Architect City Quest v2** prototype from this repository.

## Play the full game

**Live site:** https://andreread-vasconcelos.github.io/Arch-in-danger/

Controls:

- Left / Right arrows — move
- Up arrow — jump
- Space — use jetpack after collecting it
- R — restart

Goal: collect blueprints and money, avoid construction hazards and inspection drones, activate checkpoints, and reach the end of the site.

## What was restored

The original repository history contained an incomplete HTML canvas game called **Arch in danger / architect-city-quest**. The file ended midway through the `update()` function, so it could not run. `index.html` restores that concept as a self-contained playable browser game.

## Deployment

The game is deployed automatically to GitHub Pages from the `main` branch by `.github/workflows/pages.yml`. Every future push to `main` republishes the site.
