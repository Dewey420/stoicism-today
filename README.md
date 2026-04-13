# Stoicism Today — Phase 2

This build gives you:
- a GitHub Pages-ready dark site
- `data/briefing.json` as the main source
- `data/playlist.json` for music rotation
- `data/widget_fields.json` for KWGT-ready text fields
- a GitHub Actions workflow that can update the repo daily

## Publish
1. Create a GitHub repo, for example `stoicism-today`
2. Upload all files from this folder
3. In GitHub: **Settings → Pages**
4. Under **Build and deployment**, choose **Deploy from a branch**
5. Select `main` and `/root`
6. Save

## Daily automation
The GitHub Action:
- rotates the playlist
- rewrites `data/briefing.json`
- rewrites `data/widget_fields.json`
- commits changes back to the repo

## What is live vs placeholder
Already working:
- site rendering
- playlist rotation
- widget-sync-ready JSON
- daily GitHub Action shell

Still placeholder until you wire a live source:
- holidays
- moon phase
- tarot draw
- quote rotation
