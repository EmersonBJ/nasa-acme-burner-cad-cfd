from PIL import Image, ImageDraw, ImageFont
import os

assets = r"D:\NASA_CAD_Reverse_Engineering\assets"

img_insert = Image.open(os.path.join(assets, "render_chamber_insert_iso.png"))
img_ems = Image.open(os.path.join(assets, "render_ems_structure_iso.png"))
img_igniter = Image.open(os.path.join(assets, "render_igniter_assembly_iso.png"))
img_burner = Image.open(os.path.join(assets, "render_burner_collar_iso.png"))

# Target size for each quadrant
quad_w, quad_h = 1280, 820

def prep(im):
    return im.resize((quad_w, quad_h), Image.Resampling.LANCZOS)

q1 = prep(img_insert)
q2 = prep(img_ems)
q3 = prep(img_igniter)
q4 = prep(img_burner)

# Create 2x2 collage canvas with sleek dividers
border = 8
header_h = 90
total_w = quad_w * 2 + border * 3
total_h = quad_h * 2 + border * 3 + header_h

banner = Image.new("RGB", (total_w, total_h), "#070a12")
draw = ImageDraw.Draw(banner)

# Header
draw.rectangle([(0, 0), (total_w, header_h)], fill="#0b1120")
# Accent line
draw.line([(0, header_h - 2), (total_w, header_h - 2)], fill="#0284c7", width=3)

# Fonts
try:
    font_title = ImageFont.truetype("arial.ttf", 34)
    font_sub = ImageFont.truetype("arial.ttf", 16)
    font_badge = ImageFont.truetype("consolas.ttf", 15)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_badge = ImageFont.load_default()

draw.text((36, 18), "NASA ACME FLIGHT HARDWARE  •  3D CAD REVERSE ENGINEERING PORTFOLIO", fill="#f8fafc", font=font_title)
draw.text((38, 58), "International Space Station (ISS) Combustion Integrated Rack (CIR)  |  Lead Engineer: Emerson B. J.", fill="#38bdf8", font=font_sub)

# Paste quadrants
x1 = border
x2 = border * 2 + quad_w
y1 = header_h + border
y2 = header_h + border * 2 + quad_h

banner.paste(q1, (x1, y1))
banner.paste(q2, (x2, y1))
banner.paste(q3, (x1, y2))
banner.paste(q4, (x2, y2))

out_path = os.path.join(assets, "cad_master_showcase.png")
banner.save(out_path, quality=95)
print("Saved master showcase banner:", out_path)

