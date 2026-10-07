"""Create optimized website copies; leave the supplied WhatsApp images untouched."""
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "massage-workshop-guidance": "WhatsApp Image 2026-10-03 at 4.02.47 PM (1).jpeg",
    "massage-workshop-practice": "WhatsApp Image 2026-10-03 at 4.02.46 PM.jpeg",
    "massage-workshop-hands-on": "WhatsApp Image 2026-10-03 at 4.02.48 PM.jpeg",
    "garden-massage-event": "WhatsApp Image 2026-10-03 at 4.04.37 PM.jpeg",
    "garden-treatment-tables": "WhatsApp Image 2026-10-03 at 4.04.38 PM (1).jpeg",
    "outdoor-massage-team": "WhatsApp Image 2026-10-03 at 4.04.38 PM.jpeg",
    "seaside-massage-event": "WhatsApp Image 2026-10-03 at 4.04.39 PM.jpeg",
    "workshop-review": "WhatsApp Image 2026-10-03 at 4.04.35 PM (1).jpeg",
    "corporate-event-review": "WhatsApp Image 2026-10-03 at 4.04.35 PM (2).jpeg",
    "garden-workshop-review": "WhatsApp Image 2026-10-03 at 4.04.36 PM (1).jpeg",
}

def main():
    destination = ROOT / "assets" / "gallery"
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, source in SOURCES.items():
        image = ImageOps.exif_transpose(Image.open(ROOT / "images" / source)).convert("RGB")
        image.thumbnail((1600, 2048), Image.Resampling.LANCZOS)
        image.save(destination / f"{name}.webp", "WEBP", quality=85, method=6)
        manifest[name] = {"source": source, "width": image.width, "height": image.height}
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
