#!/usr/bin/env python3
"""
Sustainability Scorecard: Generate final CO2 reduction report.

Compares original sustainability audit with the build's sustainability metrics.
Generates a formal scorecard suitable for client deliverables.

Usage:
  python sustainability_scorecard.py <original-audit-dir> <build-audit-dir> [output-file]
  python sustainability_scorecard.py ~/captures/linear ~/builds/linear sustainability-scorecard.md
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def generate_scorecard(original_audit_dir, build_audit_dir, output_file="sustainability-scorecard.md"):
    """Generate sustainability scorecard."""

    original_path = Path(original_audit_dir)
    build_path = Path(build_audit_dir)

    # Read original audit
    original_audit_file = original_path / "sustainability-audit.json"
    if not original_audit_file.exists():
        print(f"[ERROR] Original audit not found: {original_audit_file}")
        sys.exit(1)

    # Read build audit
    build_audit_file = build_path / "sustainability-audit.json"
    if not build_audit_file.exists():
        print(f"[ERROR] Build audit not found: {build_audit_file}")
        print(f"   Run sustainability_audit.py on your build directory first.")
        sys.exit(1)

    print(f"[SUSTAINABILITY] Comparing audits\n")

    try:
        with open(original_audit_file, "r") as f:
            original = json.load(f)
        with open(build_audit_file, "r") as f:
            build = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not read audit files: {e}")
        sys.exit(1)

    # Extract metrics
    original_mb = original.get("summary", {}).get("current_page_weight_mb", 0)
    original_co2 = original.get("summary", {}).get("current_co2_grams", 0)

    build_mb = build.get("summary", {}).get("current_page_weight_mb", 0)
    build_co2 = build.get("summary", {}).get("current_co2_grams", 0)

    # Calculate savings
    mb_saved = original_mb - build_mb
    mb_percent = (mb_saved / original_mb * 100) if original_mb > 0 else 0
    co2_saved = original_co2 - build_co2
    co2_percent = (co2_saved / original_co2 * 100) if original_co2 > 0 else 0

    # Generate scorecard
    scorecard = f"""# Sustainability Scorecard

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Project**: Abelha Clone-Study

---

## Summary

| Metric | Original | Recreation | Reduction | % Saved |
|--------|----------|------------|-----------|---------|
| **Page Weight** | {original_mb}MB | {build_mb}MB | {mb_saved:.2f}MB | {mb_percent:.1f}% |
| **CO₂ per Visit** | {original_co2:.2f}g | {build_co2:.2f}g | {co2_saved:.2f}g | {co2_percent:.1f}% |

---

## Detailed Breakdown

### Page Weight Analysis

#### Original Site
"""

    # Original breakdown
    original_breakdown = original.get("page_weight", {}).get("breakdown", {})
    scorecard += "| Asset Type | Size | Count |\n"
    scorecard += "|---|---|---|\n"
    for category, data in original_breakdown.items():
        if data.get("mb", 0) > 0:
            scorecard += f"| {category.capitalize()} | {data.get('mb', 0):.2f}MB | {data.get('count', 0)} |\n"

    scorecard += f"\n**Total**: {original_mb}MB\n\n"

    # Build breakdown
    build_breakdown = build.get("page_weight", {}).get("breakdown", {})
    scorecard += "#### Recreation Site\n"
    scorecard += "| Asset Type | Size | Count |\n"
    scorecard += "|---|---|---|\n"
    for category, data in build_breakdown.items():
        if data.get("mb", 0) > 0:
            scorecard += f"| {category.capitalize()} | {data.get('mb', 0):.2f}MB | {data.get('count', 0)} |\n"

    scorecard += f"\n**Total**: {build_mb}MB\n\n"

    # CO2 Impact
    scorecard += f"""
### CO₂ Impact

**Formula**: Page Weight (MB) × 0.81g CO₂/MB (based on websitecarbon.com data)

#### Original Site
- **Per Visit**: {original_co2:.2f}g CO₂
- **Per 10,000 Visits/Month**: {(original_co2 / 1000) * 10000:.2f}kg CO₂
- **Annual (100k visits/month)**: {(original_co2 / 1000) * 1200:.2f}kg CO₂

#### Recreation Site
- **Per Visit**: {build_co2:.2f}g CO₂
- **Per 10,000 Visits/Month**: {(build_co2 / 1000) * 10000:.2f}kg CO₂
- **Annual (100k visits/month)**: {(build_co2 / 1000) * 1200:.2f}kg CO₂

#### Annual Savings (at 100k visits/month)
- **CO₂ Saved**: {((original_co2 / 1000) * 1200) - ((build_co2 / 1000) * 1200):.2f}kg CO₂/year
- **Equivalent to**: {(((original_co2 / 1000) * 1200) - ((build_co2 / 1000) * 1200)) / 21:.1f} tree seedlings grown for 10 years

---

## Abelha Targets vs. Actual

"""

    # Compare against targets
    abelha_targets = build.get("abelha_targets", {})
    scorecard += f"""| Target | Goal | Achievement | Status |
|--------|------|-------------|--------|
| Page Weight | < {abelha_targets.get('page_weight_mb', 1.5)}MB | {build_mb}MB | {'✓ PASS' if build_mb < abelha_targets.get('page_weight_mb', 1.5) else '✗ REVIEW'} |
| CO₂ per Visit | < {abelha_targets.get('estimated_co2_grams', 1.2)}g | {build_co2:.2f}g | {'✓ PASS' if build_co2 < abelha_targets.get('estimated_co2_grams', 1.2) else '✗ REVIEW'} |
| LCP (Largest Contentful Paint) | < {abelha_targets.get('lcp_seconds', 2.5)}s | [Measure in production] | [Pending] |
| FID (First Input Delay) | < {abelha_targets.get('fid_ms', 100)}ms | [Measure in production] | [Pending] |
| CLS (Cumulative Layout Shift) | < {abelha_targets.get('cls_score', 0.1)} | [Measure in production] | [Pending] |

---

## Optimization Strategy

### Asset Optimizations Applied

"""

    # Optimization opportunities
    opp = original.get("optimization_opportunities", [])
    if opp:
        for opt in opp:
            scorecard += f"""#### {opt.get('category')}
- **Current**: {opt.get('current')}
- **Opportunity**: {opt.get('opportunity')}
- **Potential Savings**: {opt.get('potential_savings')}

"""
    else:
        scorecard += "No major optimization opportunities identified.\n\n"

    scorecard += f"""
---

## Abelha Studio Commitment

**Abelha Studio** leads the industry in sustainable web design. Every project completed through our **Clone-Study** methodology includes:

- ✅ **Digital Carbon Footprint Reduction** — Minimum 30% weight reduction
- ✅ **Optimized Asset Strategy** — WebP/AVIF images, system fonts, lazy loading
- ✅ **Performance-First Architecture** — Core Web Vitals optimization
- ✅ **Sustainability Monitoring** — Monthly reports tracking CO₂ impact

This scorecard represents our commitment to **Sostenibilidad como Velocidad** — sustainable design as a business advantage.

---

## Conclusion

By choosing Abelha Studio's recreation, you're not just getting a beautiful design—you're reducing your digital carbon footprint by **{co2_percent:.1f}%** per visitor.

For a site with 100,000 monthly visitors, this recreation saves:
- **{((original_co2 / 1000) * 1200) - ((build_co2 / 1000) * 1200):.2f}kg of CO₂ annually**
- Equivalent to planting **{(((original_co2 / 1000) * 1200) - ((build_co2 / 1000) * 1200)) / 21:.0f}** tree seedlings

**Sustainability is not a luxury—it's a business imperative.**

---

**Generated by Abelha Clone-Study**
Tecnología Humana • Sostenibilidad • Responsabilidad
"""

    # Save markdown
    with open(output_file, "w") as f:
        f.write(scorecard)

    print(f"[OK] Scorecard saved: {output_file}")
    print(f"\n[RESULTS]")
    print(f"   Original Weight: {original_mb}MB → Recreation: {build_mb}MB")
    print(f"   Saved: {mb_saved:.2f}MB ({mb_percent:.1f}%)")
    print(f"   CO2 Reduction: {co2_saved:.2f}g per visit ({co2_percent:.1f}%)")
    print(f"   Annual Savings (100k visits/month): {((original_co2 / 1000) * 1200) - ((build_co2 / 1000) * 1200):.2f}kg CO2")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sustainability_scorecard.py <original-audit-dir> <build-audit-dir> [output-file]")
        print("Example: python sustainability_scorecard.py ~/captures/linear ~/builds/linear sustainability-scorecard.md")
        sys.exit(1)

    original_audit_dir = sys.argv[1]
    build_audit_dir = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "sustainability-scorecard.md"

    try:
        generate_scorecard(original_audit_dir, build_audit_dir, output_file)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
