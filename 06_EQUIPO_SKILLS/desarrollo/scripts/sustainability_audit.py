#!/usr/bin/env python3
"""
Sustainability audit: Analyze digital footprint of original site.

Analyzes:
  - Total page weight (from network log)
  - Asset breakdown (images, fonts, scripts, etc.)
  - Optimization opportunities
  - Estimated CO₂ per visit
  - Core Web Vitals targets

Outputs:
  - sustainability-audit.json
  - sustainability-audit.md

Usage:
  python sustainability_audit.py ~/captures/linear
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def analyze_network_log(network_log_file: str):
    """Analyze network requests to calculate page weight."""

    try:
        with open(network_log_file, "r") as f:
            network_log = json.load(f)
    except Exception as e:
        print(f"❌ Could not read network log: {e}")
        return None

    breakdown = {
        "fonts": {"count": 0, "bytes": 0, "urls": []},
        "images": {"count": 0, "bytes": 0, "urls": []},
        "scripts": {"count": 0, "bytes": 0, "urls": []},
        "stylesheets": {"count": 0, "bytes": 0, "urls": []},
        "videos": {"count": 0, "bytes": 0, "urls": []},
        "other": {"count": 0, "bytes": 0, "urls": []}
    }

    total_bytes = 0

    for request in network_log:
        url = request.get("url", "")
        size = request.get("size_bytes", 0)
        content_type = request.get("content_type", "").lower()

        if not size:
            continue

        total_bytes += size

        # Categorize
        if "font" in content_type:
            breakdown["fonts"]["count"] += 1
            breakdown["fonts"]["bytes"] += size
            breakdown["fonts"]["urls"].append({"url": url, "size": size})
        elif "image" in content_type:
            breakdown["images"]["count"] += 1
            breakdown["images"]["bytes"] += size
            breakdown["images"]["urls"].append({"url": url, "size": size})
        elif "javascript" in content_type or url.endswith(".js"):
            breakdown["scripts"]["count"] += 1
            breakdown["scripts"]["bytes"] += size
            breakdown["scripts"]["urls"].append({"url": url, "size": size})
        elif "css" in content_type or url.endswith(".css"):
            breakdown["stylesheets"]["count"] += 1
            breakdown["stylesheets"]["bytes"] += size
            breakdown["stylesheets"]["urls"].append({"url": url, "size": size})
        elif "video" in content_type:
            breakdown["videos"]["count"] += 1
            breakdown["videos"]["bytes"] += size
            breakdown["videos"]["urls"].append({"url": url, "size": size})
        else:
            breakdown["other"]["count"] += 1
            breakdown["other"]["bytes"] += size
            breakdown["other"]["urls"].append({"url": url, "size": size})

    return {"total_bytes": total_bytes, "breakdown": breakdown}


def estimate_co2(total_bytes: int):
    """Estimate CO₂ emissions per visit.

    Formula: 0.81g CO₂ per MB (based on websitecarbon.com data)
    """
    mb = total_bytes / (1024 * 1024)
    co2_grams = mb * 0.81
    return co2_grams


def run_audit(capture_dir: str, output_file: str = "sustainability-audit.json"):
    """Run sustainability audit."""

    capture_path = Path(capture_dir)
    network_log_file = capture_path / "network-log.json"

    if not network_log_file.exists():
        print(f"❌ Network log not found: {network_log_file}")
        print(f"   Did you run capture.py first?")
        sys.exit(1)

    print(f"🌱 Running sustainability audit on: {capture_dir}\n")

    # Analyze network
    network_analysis = analyze_network_log(str(network_log_file))

    if not network_analysis:
        print("❌ Audit failed")
        sys.exit(1)

    total_bytes = network_analysis["total_bytes"]
    breakdown = network_analysis["breakdown"]
    co2_grams = estimate_co2(total_bytes)
    total_mb = total_bytes / (1024 * 1024)

    audit = {
        "date": datetime.now().isoformat(),
        "capture_dir": capture_dir,
        "page_weight": {
            "total_bytes": total_bytes,
            "total_mb": round(total_mb, 2),
            "breakdown": {
                "fonts": {"count": breakdown["fonts"]["count"], "bytes": breakdown["fonts"]["bytes"], "mb": round(breakdown["fonts"]["bytes"] / (1024 * 1024), 2)},
                "images": {"count": breakdown["images"]["count"], "bytes": breakdown["images"]["bytes"], "mb": round(breakdown["images"]["bytes"] / (1024 * 1024), 2)},
                "scripts": {"count": breakdown["scripts"]["count"], "bytes": breakdown["scripts"]["bytes"], "mb": round(breakdown["scripts"]["bytes"] / (1024 * 1024), 2)},
                "stylesheets": {"count": breakdown["stylesheets"]["count"], "bytes": breakdown["stylesheets"]["bytes"], "mb": round(breakdown["stylesheets"]["bytes"] / (1024 * 1024), 2)},
                "videos": {"count": breakdown["videos"]["count"], "bytes": breakdown["videos"]["bytes"], "mb": round(breakdown["videos"]["bytes"] / (1024 * 1024), 2)},
                "other": {"count": breakdown["other"]["count"], "bytes": breakdown["other"]["bytes"], "mb": round(breakdown["other"]["bytes"] / (1024 * 1024), 2)}
            }
        },
        "co2_impact": {
            "estimated_co2_per_visit_grams": round(co2_grams, 2),
            "estimated_co2_per_visit_kg": round(co2_grams / 1000, 4),
            "co2_per_month_10k_visitors_kg": round((co2_grams / 1000) * 10000, 2),
            "formula": "Page weight (MB) × 0.81g CO₂/MB"
        },
        "abelha_targets": {
            "page_weight_mb": 1.5,
            "lcp_seconds": 2.5,
            "fid_ms": 100,
            "cls_score": 0.1,
            "estimated_co2_grams": 1.2
        },
        "optimization_opportunities": [],
        "summary": {}
    }

    # Generate optimization suggestions
    if breakdown["fonts"]["mb"] > 0.3:
        audit["optimization_opportunities"].append({
            "category": "Fonts",
            "current": f"{breakdown['fonts']['mb']}MB",
            "opportunity": "Switch to Google Fonts (400, 700 weights only)",
            "potential_savings": f"{breakdown['fonts']['mb'] * 0.9:.2f}MB (90%)"
        })

    if breakdown["images"]["mb"] > 2:
        audit["optimization_opportunities"].append({
            "category": "Images",
            "current": f"{breakdown['images']['mb']}MB",
            "opportunity": "Convert to WebP/AVIF, enable lazy loading, compress",
            "potential_savings": f"{breakdown['images']['mb'] * 0.72:.2f}MB (72%)"
        })

    if breakdown["scripts"]["mb"] > 1:
        audit["optimization_opportunities"].append({
            "category": "Scripts",
            "current": f"{breakdown['scripts']['mb']}MB",
            "opportunity": "Remove unused tracking/analytics, defer non-critical JS",
            "potential_savings": f"{breakdown['scripts']['mb'] * 0.4:.2f}MB (40%)"
        })

    if breakdown["videos"]["mb"] > 2:
        audit["optimization_opportunities"].append({
            "category": "Videos",
            "current": f"{breakdown['videos']['mb']}MB",
            "opportunity": "Reduce duration (max 5s), convert to WebM, compress",
            "potential_savings": f"{breakdown['videos']['mb'] * 0.82:.2f}MB (82%)"
        })

    # Calculate potential savings
    total_potential_savings_mb = sum([
        breakdown["fonts"]["mb"] * 0.9 if breakdown["fonts"]["mb"] > 0.3 else 0,
        breakdown["images"]["mb"] * 0.72 if breakdown["images"]["mb"] > 2 else 0,
        breakdown["scripts"]["mb"] * 0.4 if breakdown["scripts"]["mb"] > 1 else 0,
        breakdown["videos"]["mb"] * 0.82 if breakdown["videos"]["mb"] > 2 else 0,
    ])

    audit["summary"] = {
        "current_page_weight_mb": round(total_mb, 2),
        "current_co2_grams": round(co2_grams, 2),
        "potential_optimized_weight_mb": round(max(total_mb - total_potential_savings_mb, 0.5), 2),
        "potential_co2_reduction_grams": round(estimate_co2(total_bytes - (total_potential_savings_mb * 1024 * 1024)), 2),
        "total_potential_savings_mb": round(total_potential_savings_mb, 2),
        "reduction_percentage": round((total_potential_savings_mb / total_mb * 100) if total_mb > 0 else 0, 1),
        "meets_abelha_target": total_mb < 1.5
    }

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(audit, f, indent=2)

    print(f"✅ Audit saved: {output_file}\n")

    # Generate markdown report
    md_file = output_file.replace(".json", ".md")
    with open(md_file, "w") as f:
        f.write(f"# Sustainability Audit Report\n\n")
        f.write(f"**Date**: {audit['date']}\n")
        f.write(f"**Site**: {capture_dir}\n\n")

        f.write(f"## Page Weight\n\n")
        f.write(f"**Total**: {audit['summary']['current_page_weight_mb']}MB\n\n")
        f.write(f"### Breakdown\n\n")
        for category, data in audit["page_weight"]["breakdown"].items():
            if data["mb"] > 0:
                f.write(f"- **{category.capitalize()}**: {data['mb']}MB ({data['count']} requests)\n")

        f.write(f"\n## CO₂ Impact\n\n")
        f.write(f"- **Per Visit**: {audit['co2_impact']['estimated_co2_per_visit_grams']}g CO₂\n")
        f.write(f"- **Per 10k Visits/Month**: {audit['co2_impact']['co2_per_month_10k_visitors_kg']}kg CO₂\n\n")

        f.write(f"## Abelha Targets\n\n")
        f.write(f"- Page Weight: **< {audit['abelha_targets']['page_weight_mb']}MB** {'✅' if audit['summary']['meets_abelha_target'] else '❌'}\n")
        f.write(f"- LCP: **< {audit['abelha_targets']['lcp_seconds']}s**\n")
        f.write(f"- CLS: **< {audit['abelha_targets']['cls_score']}**\n")
        f.write(f"- CO₂: **< {audit['abelha_targets']['estimated_co2_grams']}g/visit**\n\n")

        f.write(f"## Optimization Opportunities\n\n")
        for opp in audit["optimization_opportunities"]:
            f.write(f"### {opp['category']}\n\n")
            f.write(f"- **Current**: {opp['current']}\n")
            f.write(f"- **Opportunity**: {opp['opportunity']}\n")
            f.write(f"- **Potential Savings**: {opp['potential_savings']}\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- Total Potential Savings: **{audit['summary']['total_potential_savings_mb']}MB ({audit['summary']['reduction_percentage']}% reduction)**\n")
        f.write(f"- Optimized Page Weight: **{audit['summary']['potential_optimized_weight_mb']}MB**\n")
        f.write(f"- CO₂ Reduction: **{audit['summary']['current_co2_grams']}g → {audit['summary']['potential_co2_reduction_grams']}g**\n\n")

    print(f"✅ Report saved: {md_file}\n")

    # Print summary
    print("📊 SUSTAINABILITY SUMMARY")
    print(f"   Current Page Weight: {audit['summary']['current_page_weight_mb']}MB")
    print(f"   Current CO₂: {audit['summary']['current_co2_grams']}g per visit")
    print(f"\n   Potential Optimized Weight: {audit['summary']['potential_optimized_weight_mb']}MB")
    print(f"   Potential CO₂: {audit['summary']['potential_co2_reduction_grams']}g per visit")
    print(f"   Reduction: {audit['summary']['reduction_percentage']}%")
    print(f"\n🎯 Meets Abelha Target (< 1.5MB): {'✅ YES' if audit['summary']['meets_abelha_target'] else '❌ NO'}")
    print(f"\n📋 Full report: {md_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sustainability_audit.py <capture_dir> [output_file]")
        print("Example: python sustainability_audit.py ~/captures/linear sustainability-audit.json")
        sys.exit(1)

    capture_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "sustainability-audit.json"

    try:
        run_audit(capture_dir, output_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
