# Generating Handwritten-Style PDFs with PIL

Use this pattern when the user asks for a "viết tay" (handwritten) version of a document — attendance sheets, sign-in sheets, reports, etc.

## Core Technique

Use **PIL/Pillow** to render pages as images with handwriting fonts, then save as multi-page PDF via `Image.save(path, 'PDF', save_all=True, append_images=[...])`.

## Fonts

Download Google Fonts that support Vietnamese and have a handwriting style:

```bash
# Patrick Hand — clean, legible handwriting, good Vietnamese support
wget -q 'https://github.com/google/fonts/raw/main/ofl/patrickhand/PatrickHand-Regular.ttf' -O /tmp/PatrickHand.ttf

# Caveat — bolder, more casual handwriting
wget -q 'https://github.com/google/fonts/raw/main/ofl/caveat/Caveat%5Bwght%5D.ttf' -O /tmp/Caveat.ttf
```

Always verify fonts render Vietnamese diacritics correctly after download (test with "Nguyễn Văn An ăâđêôơư").

## Key Functions

### Jittered Text (handwritten feel)
```python
from PIL import Image, ImageDraw, ImageFont
import random

def jitter_text(draw, x, y, text, font, fill='#333', j=1.0):
    dx = random.gauss(0, j * 0.5)
    dy = random.gauss(0, j * 0.5)
    draw.text((x + dx, y + dy), text, font=font, fill=fill)
```

### Wobbly Lines (hand-drawn grid)
```python
import math

def wobbly_line(draw, x1, y1, x2, y2, fill='#999', width=1, wobble=0.4):
    dist = math.hypot(x2 - x1, y2 - y1)
    n = max(int(dist / 25), 2)
    pts = []
    for i in range(n + 1):
        t = i / n
        px = x1 + (x2 - x1) * t + random.gauss(0, wobble)
        py = y1 + (y2 - y1) * t + random.gauss(0, wobble)
        pts.append((px, py))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=fill, width=width)
```

### Paper Texture
```python
# Cream paper background
img = Image.new('RGB', (W, H), '#FFFBF3')
draw = ImageDraw.Draw(img)

# Grain noise
for _ in range(8000):
    px, py = random.randint(0, W - 1), random.randint(0, H - 1)
    v = random.randint(245, 255)
    draw.point((px, py), fill=(v, v, max(v - 5, 0)))
```

## Page Layout Guidelines

- Use landscape dimensions (e.g. 3600×2600) for wide tables with 30+ day columns
- Typical fit: **10 employees per page** with dual rows (N + OT) and 30 day columns
- Column width for days: ~35px minimum with 15px font
- Leave room for: STT (45px), Name (260px), 30×day columns, Total (55px), Thuong/CN/Le (~35px each), Notes (100px), signature area at bottom

## Multi-Page PDF Output

```python
all_images = []
for page_data in pages:
    img = render_page(page_data)
    all_images.append(img)

all_images[0].save(
    'output.pdf', 'PDF',
    save_all=True,
    append_images=all_images[1:],
    resolution=150
)
```

## Visual Conventions for Attendance Sheets

- **Red text** (#CC0000): Sunday/holiday attendance, OT > 4 hours
- **Blue text** (#0055CC): "P" (phép / approved leave)
- **Alternating row backgrounds**: subtle cream tones (#FFFEF8 / #FEF9F0)
- **Header row**: light blue (#D6E4F0)
- **N/OT separator**: light gray line between the two sub-rows
- **Signature lines** at bottom: "Người lập bảng" / "Trưởng ca" / "Giám đốc"

## Reading Goertek Attendance Excel Files

These files use a specific layout:
- Each employee occupies **2 rows**: N (cong) and OT (overtime)
- Columns 1-6: STT, MaNV, Name, Role, HireDate, N/OT label
- Columns 7-36: daily values for the period (30 days)
- Column 37: Total, 38: Thuong (weekday), 39: CN (Sunday), 40: Le (holiday)
- Merged cells across N+OT rows for STT, name, code, role, hire date
- Read with `step of 2` through rows, using `data_only=True` for calculated values
