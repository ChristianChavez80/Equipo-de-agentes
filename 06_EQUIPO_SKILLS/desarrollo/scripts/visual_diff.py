#!/usr/bin/env python3
"""
Visual diff: Compare original screenshots against current build screenshots.

Generates side-by-side comparison and structured diff report.

Usage:
  python visual_diff.py <original-dir> <current-dir> [output-file]
  python visual_diff.py ~/captures/linear ~/builds/linear-recreation visual-diff.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageChops
import os

def calculate_diff_score(img1_path, img2_path):
    """Compare two images and return diff score (0-100, where 100 is identical)."""
    try:
        img1 = Image.open(img1_path).convert("RGB")
        img2 = Image.open(img2_path).convert("RGB")

        # Resize to match if different dimensions
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

        # Calculate difference
        diff = ImageChops.difference(img1, img2)
        diff_sum = sum(diff.getdata())
        max_diff = img1.size[0] * img1.size[1] * 3 * 255

        # Score: 100 = identical, 0 = completely different
        score = max(0, 100 - (diff_sum / max_diff * 100))
        return round(score, 1)
    except Exception as e:
        return None

def run_visual_diff(original_dir, current_dir, output_file="visual-diff.json"):
    """Run visual diff comparison."""

    original_path = Path(original_dir)
    current_path = Path(current_dir)

    if not original_path.exists():
        print(f"[ERROR] Original directory not found: {original_dir}")
        sys.exit(1)

    if not current_path.exists():
        print(f"[ERROR] Current directory not found: {current_dir}")
        sys.exit(1)

    print(f"[VISUAL-DIFF] Comparing {original_dir} vs {current_dir}\n")

    # Find screenshots in both directories
    viewports = ["desktop", "tablet", "mobile"]
    comparisons = []

    for viewport in viewports:
        original_file = original_path / f"{viewport}-full.png"
        current_file = current_path / f"{viewport}-full.png"

        if original_file.exists() and current_file.exists():
            score = calculate_diff_score(str(original_file), str(current_file))
            comparisons.append({
                "viewport": viewport,
                "original": str(original_file),
                "current": str(current_file),
                "similarity_score": score
            })
            print(f"  {viewport}: {score}% similar")
        else:
            print(f"  {viewport}: [MISSING] Original={original_file.exists()}, Current={current_file.exists()}")

    # Calculate overall score
    valid_scores = [c["similarity_score"] for c in comparisons if c["similarity_score"] is not None]
    overall_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

    report = {
        "date": datetime.now().isoformat(),
        "original_dir": str(original_dir),
        "current_dir": str(current_dir),
        "comparisons": comparisons,
        "overall_similarity_score": round(overall_score, 1),
        "status": "PASS" if overall_score >= 85 else "REVIEW" if overall_score >= 70 else "NEEDS_WORK"
    }

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[OK] Report saved: {output_file}")
    print(f"[RESULTS] Overall Similarity: {overall_score}% — Status: {report['status']}")

    # Generate markdown report
    md_file = output_file.replace(".json", ".md")
    with open(md_file, "w") as f:
        f.write(f"# Visual Diff Report\n\n")
        f.write(f"**Date**: {report['date']}\n\n")
        f.write(f"## Overall Score: {overall_score}%\n\n")
        f.write(f"**Status**: {report['status']}\n\n")
        f.write(f"## Viewport Comparisons\n\n")
        for comp in comparisons:
            f.write(f"### {comp['viewport'].upper()}\n\n")
            f.write(f"- **Similarity**: {comp['similarity_score']}%\n")
            f.write(f"- **Original**: {comp['original']}\n")
            f.write(f"- **Current**: {comp['current']}\n\n")

        f.write(f"## Interpretation\n\n")
        if overall_score >= 90:
            f.write(f"[EXCELLENT] Visual match is near-pixel-perfect. Minor refinements may remain.\n\n")
        elif overall_score >= 80:
            f.write(f"[GOOD] Visual match is strong. Address remaining differences.\n\n")
        elif overall_score >= 70:
            f.write(f"[REVIEW] Visual match needs work. Compare side-by-side and prioritize high-impact fixes.\n\n")
        else:
            f.write(f"[NEEDS_WORK] Significant visual differences. Return to design phase for substantial revisions.\n\n")

    print(f"[OK] Markdown report: {md_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python visual_diff.py <original-dir> <current-dir> [output-file]")
        print("Example: python visual_diff.py ~/captures/linear ~/builds/linear-rec visual-diff.json")
        sys.exit(1)

    original_dir = sys.argv[1]
    current_dir = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "visual-diff.json"

    try:
        run_visual_diff(original_dir, current_dir, output_file)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
