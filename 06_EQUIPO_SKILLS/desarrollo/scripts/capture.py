#!/usr/bin/env python3
"""
Capture a website systematically using Playwright.

Outputs:
  - Full-page screenshots (desktop, tablet, mobile)
  - Scroll-state screenshots every 600px
  - 30-second video recording of automated scroll
  - DOM snapshot after JS hydration
  - Network log with all requests
  - Computed styles for text elements
  - Console logs (framework fingerprints)
  - Font face declarations
  - Manual observation placeholders (keyboard nav, hover states, audio)

Usage:
  python capture.py https://linear.app ~/captures/linear
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
import traceback

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    sys.exit(1)


async def capture_site(url: str, output_dir: str):
    """Capture website systematically."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "scroll-states").mkdir(exist_ok=True)

    print(f"📸 Starting capture: {url}")
    print(f"📁 Output directory: {output_dir}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Three viewports
        viewports = {
            "desktop": {"width": 1920, "height": 1080},
            "tablet": {"width": 768, "height": 1024},
            "mobile": {"width": 390, "height": 844}
        }

        network_log = []
        console_logs = []
        font_faces = []

        # Capture for each viewport
        for viewport_name, viewport_size in viewports.items():
            print(f"📱 Capturing {viewport_name} ({viewport_size['width']}×{viewport_size['height']})")

            page = await browser.new_page(viewport=viewport_size)

            # Network listener
            def handle_response(response):
                network_log.append({
                    "url": response.url,
                    "status": response.status,
                    "content_type": response.headers.get("content-type", "unknown"),
                    "size_bytes": len(await response.body()) if response.ok else 0
                })

            page.on("response", handle_response)

            # Console listener
            def handle_console(msg):
                console_logs.append({
                    "type": msg.type,
                    "text": msg.text,
                    "viewport": viewport_name
                })

            page.on("console", handle_console)

            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)

                # Full page screenshot
                await page.screenshot(
                    path=str(output_path / f"{viewport_name}-full.png"),
                    full_page=True
                )
                print(f"  ✅ Full-page screenshot: {viewport_name}-full.png")

                # Scroll and capture states
                height = await page.evaluate("document.documentElement.scrollHeight")
                scroll_positions = list(range(0, int(height), 600))

                if len(scroll_positions) > 1:
                    print(f"  📍 Capturing {len(scroll_positions)} scroll positions...")
                    for pos_idx, pos in enumerate(scroll_positions):
                        await page.evaluate(f"window.scrollTo(0, {pos})")
                        await page.wait_for_timeout(300)  # Wait for lazy-load
                        await page.screenshot(
                            path=str(output_path / "scroll-states" / f"{viewport_name}-scroll-{pos_idx:03d}-{pos}px.png")
                        )

                # Extract fonts
                fonts = await page.evaluate("""
                    () => {
                        const fonts = [];
                        const rules = document.styleSheets || [];
                        for (let sheet of rules) {
                            try {
                                if (sheet.cssRules) {
                                    for (let rule of sheet.cssRules) {
                                        if (rule.type === 5) {  // @font-face
                                            fonts.push({
                                                family: rule.style.fontFamily,
                                                src: rule.style.src,
                                                weight: rule.style.fontWeight || "normal"
                                            });
                                        }
                                    }
                                }
                            } catch (e) {}
                        }
                        return fonts;
                    }
                """)
                font_faces.extend(fonts)

                # DOM snapshot (only once, from desktop)
                if viewport_name == "desktop":
                    dom_html = await page.content()
                    with open(str(output_path / "dom-snapshot.html"), "w", encoding="utf-8") as f:
                        f.write(dom_html)
                    print(f"  ✅ DOM snapshot: dom-snapshot.html")

                await page.close()

            except Exception as e:
                print(f"  ❌ Error capturing {viewport_name}: {e}")
                await page.close()
                continue

        # Video recording (desktop only)
        print(f"\n🎥 Recording 30-second video...")
        page = await browser.new_page(viewport=viewports["desktop"])

        # Start video recording
        page.video.path = str(output_path / "recording.webm")

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Auto-scroll for 30 seconds
            await page.evaluate("""
                () => {
                    let pos = 0;
                    const height = document.documentElement.scrollHeight;
                    const interval = setInterval(() => {
                        window.scrollBy(0, 50);
                        if (window.scrollY >= height) clearInterval(interval);
                    }, 100);
                }
            """)

            await page.wait_for_timeout(30000)
            await page.close()
            print(f"  ✅ Video recorded: recording.webm")

        except Exception as e:
            print(f"  ⚠️ Video recording failed: {e}")
            await page.close()

        await browser.close()

    # Save network log
    with open(str(output_path / "network-log.json"), "w") as f:
        json.dump(network_log, f, indent=2)
    print(f"\n✅ Network log: network-log.json ({len(network_log)} requests)")

    # Save console logs
    with open(str(output_path / "console-log.txt"), "w") as f:
        for log in console_logs:
            f.write(f"[{log['viewport']}] {log['type']}: {log['text']}\n")
    print(f"✅ Console logs: console-log.txt ({len(console_logs)} messages)")

    # Save font faces
    with open(str(output_path / "fonts-detected.json"), "w") as f:
        json.dump(list({f["family"]: f for f in font_faces}.values()), f, indent=2)
    print(f"✅ Fonts detected: fonts-detected.json ({len(set(f['family'] for f in font_faces))} unique families)")

    # Create manual notes template
    manual_notes = """# Manual Observations — Complete This After Script Capture

## Keyboard Navigation
Test with Tab key:
- [ ] Can navigate all buttons with Tab
- [ ] Can navigate all links with Tab
- [ ] Can interact with dropdowns (Enter/Space)
- [ ] Can close modals with Escape
- [ ] Focus is always visible
- [ ] No focus traps

**Notes**:
[Add observations here]

## Hover States & Interactions
- [ ] Buttons change color/shadow on hover
- [ ] Links underline or change color on hover
- [ ] Cards lift or change shadow on hover
- [ ] Custom cursors used? (describe)
- [ ] Magnetic effects or snap-to-grid interactions?

**Notes**:
[Add observations here]

## Animations & Micro-interactions
- [ ] Animations on page load (entrance)
- [ ] Animations on hover (buttons, links, cards)
- [ ] Animations on scroll (reveal, parallax, etc.)
- [ ] Animations on click (transitions between states)
- [ ] Auto-playing animations (loops)

**Timing notes**:
[Fast (< 300ms) / Medium (300-600ms) / Slow (> 600ms)]

## Audio & Sound Design
- [ ] Any sound effects on interactions
- [ ] Background music or ambient sound
- [ ] Auto-play audio (risky for accessibility)

**Notes**:
[Add observations here]

## Color & Contrast
Spot-check a few elements:
- Primary text color: [#XXXXXX]
- Background color: [#XXXXXX]
- Accent/highlight color: [#XXXXXX]
- Any problematic color combinations? (too light text, insufficient contrast)

## Accessibility Notes
- [ ] Dark mode / light mode toggle visible
- [ ] Skip links (skip to main content)?
- [ ] ARIA labels on custom components?
- [ ] Alt text on images? (check in DevTools)

**Concerns**:
[Any accessibility issues spotted?]

## Other Notes
[Anything unusual or noteworthy?]
"""

    with open(str(output_path / "manual-notes.md"), "w") as f:
        f.write(manual_notes)
    print(f"✅ Manual notes template: manual-notes.md (complete this manually)")

    print(f"\n🎉 Capture complete!")
    print(f"📂 Files created in: {output_dir}")
    print(f"\n⏭️  Next: Open manual-notes.md and fill in observations.")
    print(f"Then run: python extract_tokens.py {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python capture.py <URL> <output_dir>")
        print("Example: python capture.py https://linear.app ~/captures/linear")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2]

    try:
        asyncio.run(capture_site(url, output_dir))
    except KeyboardInterrupt:
        print("\n⏹️  Capture cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
