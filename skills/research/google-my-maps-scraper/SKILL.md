---
name: google-my-maps-scraper
description: "Extract all features from a public Google My Maps into GeoJSON using Playwright. Use when user wants to download, archive, or convert a Google My Maps (maps.google.com/maps/d/) to offline format. Handles KML 403 blocks, CORS restrictions, and multi-format geometry."
version: 1.0.0
author: Doremon
license: MIT
metadata:
  hermes:
    tags: [google-my-maps, geojson, scraping, maps, offline, kml, geo-data, playwright, vietnam, quy-hoach]
    category: research
    requires_toolsets: [terminal]
---

# Google My Maps Scraper

Extract all features (points, lines, polygons) from any **public** Google My Maps and convert to GeoJSON offline format, using Playwright to parse the `_pageData` blob embedded in the page HTML.

## When to Use

- User shares a `maps.google.com/maps/d/` URL and wants data offline
- User wants to build a competing product using similar map data as a reference
- User wants to convert My Maps features to GeoJSON / QGIS / Kepler.gl format
- User wants to archive a map before it disappears

## Why Not KML Export?

Google's KML export endpoints (`/maps/d/kml?mid=...`) return **HTTP 403** even for public maps unless the map owner has explicitly enabled download **and** the request comes from a logged-in session. This scraper bypasses that entirely.

## How It Works

Google My Maps embeds **all feature data** in a `_pageData` variable in the page HTML (25–30MB). No XHR is needed — all geometry + names are inline. The scraper:

1. Loads the viewer URL with Playwright (headless Chromium)
2. Grabs `document.documentElement.outerHTML` (25–30 MB)
3. Finds `_pageData` and JSON-unescapes + parses it
4. `parsed[1][6]` = array of layers, each `layer[4]` = features
5. Each feature: `f[4]` = geometry, `f[5]` = attributes (name, description)
6. Handles **two geometry formats**:
   - **Format A** (Point/LineString): `[[null, [lat, lng]], [null, [lat, lng]], ...]`  
     → iterate geomArray, extract `g[1]` = `[lat, lng]`, emit as `[lng, lat]` GeoJSON
   - **Format B** (Polygon bbox): `[[[lng1, lat1, lng2, lat2]], ...]`  
     → expand to 5-point closed Polygon ring

## Prerequisites

```bash
pip install playwright
python3 -m playwright install chromium
```

## Script

See `scripts/scrape_my_maps.py` — pass `MID` (the `mid=` param from the URL) and `OUT` path.

## Quick Usage

```bash
MID="1tXE01OUdI6ACJoi3XJpmFzKS4fO6DXg"  # from URL mid=...
python3 ~/.hermes/skills/research/google-my-maps-scraper/scripts/scrape_my_maps.py \
  "$MID" /tmp/output.geojson
```

## Output: GeoJSON FeatureCollection

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": { "layer": "LAYER NAME", "name": "Feature name", "description": "..." },
      "geometry": { "type": "Point", "coordinates": [105.88, 20.70] }
    }
  ]
}
```

Properties preserved: `layer` (My Maps layer name), `name`, `description`.

## Offline HTML Viewer

After extracting GeoJSON, create a self-contained Leaflet viewer:

```html
<!-- Requires datmaps.geojson in same directory -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

- Use `L.circleMarker` for Points, `L.polyline` for LineStrings, `L.polygon` for Polygons
- Layer toggles via `L.layerGroup()` + click handler
- Dark background (`#1a1a2e`) with colored layers by name

See `templates/offline_viewer.html` for the full ready-to-use template.

## Pitfalls

- **KML 403**: `forcekml=1` and `/kml?mid=...` both return 403 for protected maps — use this Playwright approach instead
- **CORS blocks localhost**: Don't try to `fetch('http://localhost:PORT')` from browser console while on google.com — it will fail with "TypeError: Failed to fetch" due to CORS. Use Playwright server-side instead
- **`window._variable` lost between console calls**: Browser console variables don't survive page navigation or long pauses. Do extract + save in a single script execution
- **sessionStorage/indexedDB**: Also unreliable across browser_console calls in Hermes. Commit to server-side (Playwright) approach from the start
- **Geometry format varies by layer type**: Icon/Point layers use Format A; Polygon/KCN layers use Format B. The script must handle both
- **GeoJSON coordinate order**: My Maps stores `[lat, lng]` but GeoJSON requires `[lng, lat]` — always swap
- **Private maps**: This only works on publicly shared maps (viewer URL accessible without login). Private maps will return no `_pageData` feature data

## Verification

```bash
python3 -c "
import json
with open('/tmp/output.geojson') as f: gj = json.load(f)
from collections import Counter
print(f'Features: {len(gj[\"features\"])}')
print(Counter(f[\"properties\"][\"layer\"] for f in gj[\"features\"]))
"
```

## Related Skills

- `maps` — OSM geocoding/routing (different use case)
- `vietnam-planning-map-research` — research quy hoạch routes from news/infographics
