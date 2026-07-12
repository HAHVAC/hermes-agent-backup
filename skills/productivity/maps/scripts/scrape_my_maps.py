#!/usr/bin/env python3
"""
Scrape any public Google My Maps and extract all features as GeoJSON.

Usage:
    python3 scrape_my_maps.py <MID> <output.geojson>

    MID  — the map ID from the URL: maps.google.com/maps/d/viewer?mid=<MID>

Requires:
    pip install playwright
    python3 -m playwright install chromium
"""
import json
import sys
from collections import Counter
from playwright.sync_api import sync_playwright


def extract_features(layers):
    """Parse all layers and return a flat list of GeoJSON Feature dicts."""
    feats = []
    for layer in layers:
        layer_name = layer[2] if layer[2] else "Unknown"
        features = layer[4]
        if not isinstance(features, list):
            continue

        for f in features:
            try:
                gd = f[4]      # geometry data
                attrs = f[5]   # attributes

                # Extract name / description
                name = desc = ""
                if isinstance(attrs, list) and attrs and isinstance(attrs[0], list):
                    name = attrs[0][0] if attrs[0] else ""
                    desc = attrs[0][1] if len(attrs[0]) > 1 else ""

                geom = _parse_geometry(gd)
                if geom:
                    feats.append({
                        "type": "Feature",
                        "properties": {
                            "layer": layer_name,
                            "name": name or "",
                            "description": desc or "",
                        },
                        "geometry": geom,
                    })
            except Exception:
                pass  # skip malformed features

    return feats


def _parse_geometry(gd):
    """Handle two geometry formats used by Google My Maps.

    Format A — Point / LineString:
        geom data = [[null, [lat, lng]], [null, [lat, lng]], ...]
        First item gd[0] is an array of [null, [lat,lng]] pairs.

    Format B — Polygon / bounding box:
        geom data = [[[lng1, lat1, lng2, lat2]], "0", ...]
        gd[0][0] is a 4-element numeric array (bbox).
    """
    if not isinstance(gd, list) or not gd:
        return None

    ga = gd[0]
    if not isinstance(ga, list):
        return None

    # --- Format B: bbox polygon ---
    # Direct: ga = [lng1, lat1, lng2, lat2]
    if len(ga) == 4 and all(isinstance(x, (int, float)) for x in ga):
        return _bbox_to_polygon(*ga)

    # Wrapped: ga = [[lng1, lat1, lng2, lat2]]
    if ga and isinstance(ga[0], list):
        inn = ga[0]
        if len(inn) == 4 and all(isinstance(x, (int, float)) for x in inn):
            return _bbox_to_polygon(*inn)

        # --- Format A: array of [null, [lat, lng]] items ---
        coords = []
        for g in ga:
            if isinstance(g, list) and len(g) > 1 and isinstance(g[1], list) and len(g[1]) >= 2:
                coords.append([g[1][1], g[1][0]])  # swap to [lng, lat]
        if len(coords) == 1:
            return {"type": "Point", "coordinates": coords[0]}
        if len(coords) > 1:
            return {"type": "LineString", "coordinates": coords}

    # --- Format A (flat, no wrapper) ---
    coords = []
    for g in gd:
        if isinstance(g, list) and len(g) > 1 and isinstance(g[1], list) and len(g[1]) >= 2:
            coords.append([g[1][1], g[1][0]])
    if len(coords) == 1:
        return {"type": "Point", "coordinates": coords[0]}
    if len(coords) > 1:
        return {"type": "LineString", "coordinates": coords}

    return None


def _bbox_to_polygon(lng1, lat1, lng2, lat2):
    return {
        "type": "Polygon",
        "coordinates": [[
            [lng1, lat1], [lng2, lat1], [lng2, lat2], [lng1, lat2], [lng1, lat1]
        ]],
    }


def scrape(mid: str, out_path: str):
    url = f"https://www.google.com/maps/d/viewer?mid={mid}"
    print(f"Launching Chromium → {url}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30_000)

        html = page.content()
        print(f"HTML: {len(html):,} bytes", flush=True)

        idx = html.find("_pageData")
        if idx == -1:
            print("ERROR: _pageData not found. Is this map public?", flush=True)
            sys.exit(1)

        start = html.find('"', idx) + 1
        end = html.find('";', start)
        raw = html[start:end]
        print(f"_pageData raw: {len(raw):,} chars", flush=True)

        unescaped = json.loads('"' + raw + '"')
        parsed = json.loads(unescaped)
        browser.close()

    layers = parsed[1][6]
    print(f"Layers ({len(layers)}):", flush=True)
    for i, l in enumerate(layers):
        fc = len(l[4]) if isinstance(l[4], list) else 0
        print(f"  [{i}] {l[2]}  —  {fc} features", flush=True)

    features = extract_features(layers)
    print(f"\nExtracted: {len(features)} features", flush=True)
    stats = Counter(f["properties"]["layer"] for f in features)
    for k, v in stats.items():
        print(f"  {k}: {v}", flush=True)

    geojson = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved → {out_path}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: scrape_my_maps.py <MID> <output.geojson>")
        sys.exit(1)
    scrape(sys.argv[1], sys.argv[2])
