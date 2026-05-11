---
name: vietnam-planning-map-research
description: Use this skill when the user asks to identify Vietnamese infrastructure/planning routes (e.g. vành đai, cao tốc, quy hoạch đường, tuyến đi qua xã/huyện nào), extract locality lists from Vietnamese news/infographic sources, or produce map/infographic screenshots for Telegram. It is especially relevant when information is embedded in images rather than page text, or when administrative names may have changed after province/district/commune mergers.
---

# Vietnam Planning Map Research

Use this workflow for Vietnamese route/planning questions such as “Vành đai 5 đi qua xã nào?”, “cao tốc X qua huyện/xã nào?”, “chụp ảnh bản đồ/quy hoạch cho tôi”, especially when sources are local newspapers, government pages, Meey Map, or infographic images.

## Workflow

1. **Clarify current vs old administrative units when needed**
   - Vietnamese infrastructure articles often use old province/district/commune names.
   - If the user says a merged/new province name (e.g. “Bắc Ninh” after Bắc Giang/Bắc Ninh changes), search both the current and historical province names.
   - In the answer, explicitly label old units: “huyện Lục Nam cũ”, “tỉnh Bắc Giang cũ — nay thuộc Bắc Ninh mới” if applicable.

2. **Search broadly, then narrow**
   - Start with web search queries combining route name + province + “xã”, “huyện”, “đi qua”.
   - If province search fails, search historical/neighboring names.
   - Useful patterns:
     - `"Vành đai 5" "Bắc Giang" "xã"`
     - `"đường vành đai 5" "đi qua các xã"`
     - `site:<official-domain> "vành đai" "xã"`

3. **Prefer official/local sources**
   - Government portals (`*.gov.vn`), provincial newspapers/TV sites, and local transport/construction department pages are stronger sources than real-estate reposts.
   - Real-estate/news reposts can be used to discover terms, but verify against official/local sources where possible.

4. **Handle infographic-only pages**
   - Many Vietnamese local news pages embed the actual locality list inside an image. `web_extract` may only return title, metadata, and image URL.
   - Extract the image URL from the page markdown, then use `vision_analyze` to OCR it.
   - Ask vision specifically to read locality names and route metadata:
     - “Đọc OCR nội dung ảnh infographic, đặc biệt danh sách huyện/xã mà tuyến đi qua.”

5. **Download/share the source image**
   - If direct Python/urllib download returns `403 Forbidden`, retry with curl using a browser User-Agent and Referer:
     ```bash
     curl -L -A 'Mozilla/5.0' -e 'https://source-site.vn/' 'IMAGE_URL' -o /tmp/route_infographic.jpg
     file /tmp/route_infographic.jpg
     ```
   - Return Telegram media using `MEDIA:/absolute/path/to/file`.

6. **Answer structure**
   - Start with the concise conclusion.
   - Then list by old district/city and communes/wards.
   - Include route length, start/end point, road scale if available.
   - Add a short caution if source uses old administrative names or if exact GIS alignment cannot be verified.
   - Attach the infographic/map image if the user asked for a screenshot.

## Example output pattern

```markdown
Anh, em tìm được nguồn infographic của [source]. Tuyến [route] đoạn qua [province current] tương ứng địa bàn [old province] cũ.

## Tuyến đi qua các xã nào?

### Huyện A cũ — khoảng X km
- Xã 1
- Xã 2

### Huyện B cũ — khoảng Y km
- Xã 3

## Thông tin chính
- Điểm đầu: ...
- Điểm cuối: ...
- Quy mô: ...

MEDIA:/tmp/route_infographic.jpg
```

## Pitfalls

- Search results and article snippets may mix pre-merger and post-merger administrative names. Do not silently normalize names; preserve source names and explain the relationship.
- `web_extract` often cannot OCR infographic text; use `vision_analyze` on the embedded image URL.
- Image hotlinking may block non-browser requests. Use curl with `-A 'Mozilla/5.0'` and a referer.
- Meey Map and similar planning sites are JavaScript apps; `web_extract` may only show a splash/loading SVG. Use browser interaction if the task requires that exact map, but for locality lists, web/news/official sources may be faster.
