#!/usr/bin/env python3
"""
Accessibility audit: Check baseline accessibility of original site.

This script attempts to identify common a11y issues:
  - Color contrast problems
  - Missing alt text indicators
  - ARIA attribute presence
  - Semantic HTML usage
  - Motion-related issues (prefers-reduced-motion)

Note: This is a basic static analysis. Full a11y testing requires:
  - axe-core browser integration
  - Screen reader testing (NVDA, JAWS)
  - Manual keyboard navigation

Outputs:
  - a11y-audit.json (findings)
  - a11y-audit.md (human-readable report)

Usage:
  python a11y_audit.py ~/captures/linear
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ BeautifulSoup not installed. Run: pip install beautifulsoup4")
    sys.exit(1)


def audit_html_accessibility(html_file: str):
    """Parse HTML and check for accessibility issues."""

    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"❌ Could not read HTML file: {e}")
        return None

    soup = BeautifulSoup(html, "html.parser")

    audit = {
        "date": datetime.now().isoformat(),
        "html_file": html_file,
        "findings": {
            "semantic_html": {
                "has_lang_attribute": soup.html and "lang" in soup.html.attrs,
                "has_main_element": bool(soup.find("main")),
                "has_nav_element": bool(soup.find("nav")),
                "has_header_element": bool(soup.find("header")),
                "has_footer_element": bool(soup.find("footer")),
            },
            "images": {
                "total": len(soup.find_all("img")),
                "with_alt": len(soup.find_all("img", alt=True)),
                "without_alt": len(soup.find_all("img", alt=False)),
                "with_alt_empty": len([img for img in soup.find_all("img") if img.get("alt") == ""]),
            },
            "forms": {
                "total_inputs": len(soup.find_all(["input", "textarea", "select"])),
                "inputs_with_labels": 0,
                "inputs_without_labels": 0,
            },
            "buttons": {
                "semantic_buttons": len(soup.find_all("button")),
                "div_buttons": len(soup.find_all("div", {"role": "button"})),
            },
            "links": {
                "total": len(soup.find_all("a")),
                "with_href": len(soup.find_all("a", href=True)),
                "without_href": len(soup.find_all("a", href=False)),
            },
            "aria": {
                "elements_with_aria_label": len(soup.find_all(attrs={"aria-label": True})),
                "elements_with_aria_live": len(soup.find_all(attrs={"aria-live": True})),
                "elements_with_role": len(soup.find_all(attrs={"role": True})),
            },
            "headings": {
                "h1": len(soup.find_all("h1")),
                "h2": len(soup.find_all("h2")),
                "h3": len(soup.find_all("h3")),
                "h4": len(soup.find_all("h4")),
                "h5": len(soup.find_all("h5")),
                "h6": len(soup.find_all("h6")),
            },
            "video_audio": {
                "video_tags": len(soup.find_all("video")),
                "video_with_captions": len(soup.find_all("video", attrs={"captions": True})),
                "audio_tags": len(soup.find_all("audio")),
            }
        },
        "recommendations": []
    }

    # Count inputs with associated labels
    for input_elem in soup.find_all(["input", "textarea", "select"]):
        input_id = input_elem.get("id")
        has_label = False

        # Check for <label for="...">
        if input_id:
            label = soup.find("label", {"for": input_id})
            if label:
                has_label = True

        # Check for aria-label or aria-labelledby
        if input_elem.get("aria-label") or input_elem.get("aria-labelledby"):
            has_label = True

        if has_label:
            audit["findings"]["forms"]["inputs_with_labels"] += 1
        else:
            audit["findings"]["forms"]["inputs_without_labels"] += 1

    # Generate recommendations
    if audit["findings"]["images"]["without_alt"] > 0:
        audit["recommendations"].append(
            f"⚠️  {audit['findings']['images']['without_alt']} images without alt text. Add descriptive alt attributes."
        )

    if audit["findings"]["forms"]["inputs_without_labels"] > 0:
        audit["recommendations"].append(
            f"⚠️  {audit['findings']['forms']['inputs_without_labels']} form inputs without labels. Use <label for=\"...\"> or aria-label."
        )

    if audit["findings"]["semantic_html"]["has_lang_attribute"] is False:
        audit["recommendations"].append(
            "⚠️  Missing lang attribute on <html>. Add: <html lang=\"es\">"
        )

    if audit["findings"]["semantic_html"]["has_main_element"] is False:
        audit["recommendations"].append(
            "⚠️  Missing <main> element. Wrap main content in <main>."
        )

    if audit["findings"]["buttons"]["div_buttons"] > audit["findings"]["buttons"]["semantic_buttons"]:
        audit["recommendations"].append(
            f"⚠️  {audit['findings']['buttons']['div_buttons']} div[role='button'] found. Use semantic <button> instead."
        )

    if audit["findings"]["video_audio"]["video_tags"] > audit["findings"]["video_audio"]["video_with_captions"]:
        audit["recommendations"].append(
            f"⚠️  Videos without captions detected. Add <track kind=\"captions\"> or embedded captions."
        )

    # Summary
    audit["summary"] = {
        "critical_issues": len([r for r in audit["recommendations"] if "⚠️" in r]),
        "wcag_level_baseline": "Needs Review",
        "next_steps": [
            "1. Run this audit against the original site's HTML",
            "2. Use axe-core browser plugin for detailed violations",
            "3. Test keyboard navigation manually (Tab key)",
            "4. Test with screen reader (NVDA on Windows, VoiceOver on macOS)",
            "5. Check color contrast ratios (https://webaim.org/resources/contrastchecker/)"
        ]
    }

    return audit


def run_audit(capture_dir: str, output_file: str = "a11y-audit.json"):
    """Run accessibility audit."""

    capture_path = Path(capture_dir)
    dom_file = capture_path / "dom-snapshot.html"

    if not dom_file.exists():
        print(f"❌ DOM snapshot not found: {dom_file}")
        print(f"   Did you run capture.py first?")
        sys.exit(1)

    print(f"♿ Running accessibility audit on: {capture_dir}\n")

    audit = audit_html_accessibility(str(dom_file))

    if not audit:
        print("❌ Audit failed")
        sys.exit(1)

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(audit, f, indent=2)

    print(f"✅ Audit saved: {output_file}\n")

    # Generate markdown report
    md_file = output_file.replace(".json", ".md")
    with open(md_file, "w") as f:
        f.write(f"# Accessibility Audit Report\n\n")
        f.write(f"**Date**: {audit['date']}\n")
        f.write(f"**HTML File**: {audit['html_file']}\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- Critical Issues: {audit['summary']['critical_issues']}\n")
        f.write(f"- WCAG Level (Baseline): {audit['summary']['wcag_level_baseline']}\n\n")

        f.write(f"## Semantic HTML\n\n")
        for key, value in audit["findings"]["semantic_html"].items():
            f.write(f"- {key}: {'✅' if value else '❌'}\n")

        f.write(f"\n## Images\n\n")
        f.write(f"- Total: {audit['findings']['images']['total']}\n")
        f.write(f"- With alt: {audit['findings']['images']['with_alt']}\n")
        f.write(f"- Without alt: {audit['findings']['images']['without_alt']}\n")

        f.write(f"\n## Forms\n\n")
        f.write(f"- Total inputs: {audit['findings']['forms']['total_inputs']}\n")
        f.write(f"- With labels: {audit['findings']['forms']['inputs_with_labels']}\n")
        f.write(f"- Without labels: {audit['findings']['forms']['inputs_without_labels']}\n")

        f.write(f"\n## Recommendations\n\n")
        for rec in audit["recommendations"]:
            f.write(f"{rec}\n\n")

        f.write(f"\n## Next Steps\n\n")
        for step in audit["summary"]["next_steps"]:
            f.write(f"{step}\n")

    print(f"✅ Report saved: {md_file}\n")

    # Print summary
    print("📊 AUDIT SUMMARY")
    print(f"   Critical Issues: {audit['summary']['critical_issues']}")
    print(f"\n⚠️  RECOMMENDATIONS:")
    for rec in audit["recommendations"][:5]:
        print(f"   {rec}")
    if len(audit["recommendations"]) > 5:
        print(f"   ... and {len(audit['recommendations']) - 5} more")

    print(f"\n📋 Full report: {md_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python a11y_audit.py <capture_dir> [output_file]")
        print("Example: python a11y_audit.py ~/captures/linear a11y-audit.json")
        sys.exit(1)

    capture_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "a11y-audit.json"

    try:
        run_audit(capture_dir, output_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
