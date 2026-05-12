# Google My Maps _pageData Structure

Confirmed via datmaps.vn session (May 2026, map mid=1tXE01OUdI6ACJoi3XJpmFzKS4fO6DXg).

## Page Size
HTML ~25–30 MB. All feature data is inline — no XHR needed for features.

## Top-Level Structure

```
_pageData = JSON string (double-JSON-encoded)

parsed = JSON.parse(JSON.parse('"' + raw + '"'))
# parsed is Array(2):
#   parsed[0] = Array(53)  — page config (URLs, locale, etc.)
#   parsed[1] = Array(31)  — map data
```

## Map Data (parsed[1])

```
parsed[1][1]   = map ID (mid)
parsed[1][2]   = map title
parsed[1][4]   = viewport bbox [lng_center, lat_center, ...]
parsed[1][5]   = full extent bbox [lng_min, lat_min, lng_max, lat_max]
parsed[1][6]   = layers array  ← MAIN DATA
```

## Layer Structure (parsed[1][6][i])

```
layer[0]   = null
layer[1]   = layer ID string
layer[2]   = layer NAME string
layer[3]   = ""
layer[4]   = features array  ← features
layer[7]   = true/false (visibility)
```

## Feature Structure (layer[4][j])

```
feature[0] = icon URL array (mt.googleapis.com/vt/icon/...)
feature[1] = null
feature[2] = 1
feature[3] = 1
feature[4] = geometry data  ← coordinates
feature[5] = attributes [[name, description?]]
```

## Geometry Format A — Point or LineString

```python
# feature[4] structure:
geom_data = [
    [null, [lat, lng]],   # first point
    [null, [lat, lng]],   # second point (if LineString)
    ...
    "0",
    null,
    "LAYER_ID",
    [center_lat, center_lng],
    [0, 0],
    "FEATURE_ID"
]
# Access: geom_data[0] = array of [null, [lat,lng]] pairs
# Extract: for g in geom_data[0]: coord = [g[1][1], g[1][0]]  # [lng, lat]
```

## Geometry Format B — Polygon (bounding box)

```python
# Used by KCN (industrial zone) layer and boundary polygons
geom_data = [
    [[lng1, lat1, lng2, lat2]],   # bbox as inner nested array
    "0",
    null,
    "LAYER_ID",
    [center_lat, center_lng],
    [0, 0],
    "FEATURE_ID"
]
# Access: geom_data[0][0] = [lng1, lat1, lng2, lat2]
# Convert to polygon: [[lng1,lat1],[lng2,lat1],[lng2,lat2],[lng1,lat2],[lng1,lat1]]
```

## Datmaps.vn Layer Inventory (May 2026)

| Layer | ID | Features | Geometry |
|---|---|---|---|
| ICON DỮ LIỆU LÕI - CÁC DỰ ÁN | xfRTOTi_Aw8 | 228 | Point + Polygon |
| RANH GIỚI CÁC DỰ ÁN | YRrrz02WuCk | 730 | Point + Polygon |
| TÊN ĐƯỜNG - VÀNH ĐAI - DANH GIỚI DỰ ÁN | eXWsdmoaToQ | 24 | Point + Polygon |
| TONG HOP | IlmFWL7kmGM | 2051 | Point + Polygon |
| TIM ĐƯỜNG | luIMIN1bM8U | 1 | (empty geom) |
| HÈ ĐƯỜNG | jhlw6TUTkuE | 1 | (empty geom) |
| GIAO THÔNG CẦU | iJthrxTyjys | 1 | (empty geom) |
| KHU CÔNG NGHIỆP | XJ3UiIxMYSg | 77 | Polygon bbox |

**Total extracted: 3,110 features**

## KML Export Failure

Attempts made:
- `GET /maps/d/kml?mid=...` → 403
- `GET /maps/d/kml?mid=...&forcekml=1` → 403
- `GET /maps/d/u/0/kml?mid=...&forcekml=1` → 403
- `fetch()` from browser console (google.com origin) → 403
- `fetch('http://localhost:PORT')` from browser console → CORS "Failed to fetch"

All KML endpoints blocked. Playwright server-side approach is the only reliable method.
