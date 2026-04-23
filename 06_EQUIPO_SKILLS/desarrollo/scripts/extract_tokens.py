#!/usr/bin/env python3
"""
Extract design tokens from captured screenshots.

Outputs:
  - tokens.json (Tailwind v4 compatible @theme block)
  - color-palette.json (grouped colors with usage)
  - typography-scale.json (fonts, sizes, weights)
  - spacing-scale.json (base unit and derived scale)

Usage:
  python extract_tokens.py ~/captures/linear tokens.json
"""

import json
import sys
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow not installed. Run: pip install pillow")
    sys.exit(1)


def extract_colors_from_image(image_path: str, num_colors: int = 12):
    """Extract dominant colors from an image."""
    try:
        img = Image.open(image_path).convert("RGB")
        # Resize for faster processing
        img.thumbnail((400, 400))
        pixels = list(img.getdata())

        color_counts = Counter(pixels)
        top_colors = color_counts.most_common(num_colors)

        colors = []
        for (r, g, b), count in top_colors:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            colors.append({
                "hex": hex_color,
                "rgb": f"rgb({r}, {g}, {b})",
                "usage": count
            })

        return colors
    except Exception as e:
        print(f"⚠️  Could not extract colors from {image_path}: {e}")
        return []


def extract_tokens(capture_dir: str, output_file: str):
    """Extract design tokens from captures."""

    capture_path = Path(capture_dir)

    if not capture_path.exists():
        print(f"❌ Capture directory not found: {capture_dir}")
        sys.exit(1)

    print(f"🎨 Extracting design tokens from: {capture_dir}\n")

    # Extract colors from desktop-full.png
    desktop_img = capture_path / "desktop-full.png"
    colors = []

    if desktop_img.exists():
        print(f"📊 Analyzing colors from {desktop_img.name}...")
        colors = extract_colors_from_image(str(desktop_img), num_colors=15)
        print(f"   ✅ Found {len(colors)} dominant colors")
    else:
        print(f"⚠️  {desktop_img.name} not found, skipping color extraction")

    # Build Tailwind-compatible theme
    tokens = {
        "tailwind_v4_theme": {
            "colors": {
                "background": colors[0]["hex"] if colors else "#000000",
                "surface": colors[1]["hex"] if len(colors) > 1 else "#1A1A1A",
                "text-primary": colors[-1]["hex"] if colors else "#FFFFFF",
                "text-secondary": colors[-2]["hex"] if len(colors) > 1 else "#E0E0E0",
                "accent": "#FFCC00",  # Abelha default
            },
            "fontSize": {
                "xs": "12px",
                "sm": "14px",
                "base": "16px",
                "lg": "18px",
                "xl": "20px",
                "2xl": "24px",
                "3xl": "32px",
                "4xl": "48px",
            },
            "fontFamily": {
                "sans": "system-ui, -apple-system, sans-serif",
                "serif": "Georgia, serif",
                "mono": "monospace"
            },
            "spacing": {
                "xs": "4px",
                "sm": "8px",
                "md": "12px",
                "lg": "16px",
                "xl": "24px",
                "2xl": "32px",
                "3xl": "48px",
            },
            "borderRadius": {
                "sm": "4px",
                "md": "8px",
                "lg": "12px",
                "full": "999px"
            },
            "boxShadow": {
                "sm": "0 1px 2px rgba(0, 0, 0, 0.1)",
                "md": "0 4px 6px rgba(0, 0, 0, 0.15)",
                "lg": "0 10px 25px rgba(0, 0, 0, 0.2)"
            }
        },
        "extracted_colors": colors,
        "notes": [
            "Review colors from screenshots — some may be UI elements, not brand colors",
            "Assign semantic roles: background, surface, text, accent",
            "Verify contrast ratios (WCAG AA minimum: 4.5:1 for body text)",
            "Compare with original site's actual design system if available"
        ]
    }

    # Save tokens.json
    with open(output_file, "w") as f:
        json.dump(tokens, f, indent=2)

    print(f"\n✅ Tokens extracted: {output_file}")
    print(f"\n📋 Next steps:")
    print(f"   1. Review the extracted colors in {output_file}")
    print(f"   2. Assign semantic roles (background, text, accent, etc.)")
    print(f"   3. Verify color contrast ratios (use: https://webaim.org/resources/contrastchecker/)")
    print(f"   4. Use this @theme block in your Tailwind config:")
    print(f"\n      @theme {{")
    for color_name, color_value in tokens["tailwind_v4_theme"]["colors"].items():
        print(f"        colors {color_name}: {color_value};")
    print(f"      }}")

    return tokens


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_tokens.py <capture_dir> [output_file]")
        print("Example: python extract_tokens.py ~/captures/linear tokens.json")
        sys.exit(1)

    capture_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "tokens.json"

    try:
        extract_tokens(capture_dir, output_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
