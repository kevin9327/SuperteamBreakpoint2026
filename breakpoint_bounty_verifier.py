#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Superteam Earn — Solana Breakpoint 2026 Dual Cash Bounties Verifier ($11,000 USDG Cash Pool / 30 Winner Slots)
  1. Bounty A (EN / Germany): "Travel Boost for Breakpoint 2026!"
     URL: https://earn.superteam.fun/listing/travel-boost-for-bp26
     Cash Pool: $6,000 USDG (15 x $400 USDG Equal-Split Winners)
  2. Bounty B (ES / Spain): "Rumbo a Breakpoint 2026: Gana una entrada y apoyo para tu viaje"
     URL: https://earn.superteam.fun/listing/rumbo-a-breakpoint-2026-gana-una-entrada-y-apoyo-para-tu-viaje
     Cash Pool: $5,000 USDG (10 x $400 USDG + 5 x $200 USDG = 15 Winners; only 11 live submissions!)
"""

import hashlib
import json
import math
import struct
import sys
import zlib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
REPORT_PATH = BASE_DIR / "breakpoint_verification_report.json"
BANNER_PATH = BASE_DIR / "banner.png"


BOUNTY_A_EN_PACK = {
    "slug": "travel-boost-for-bp26",
    "url": "https://earn.superteam.fun/listing/travel-boost-for-bp26",
    "sponsor": "Superteam Germany",
    "reward_pool_cash": "6,000 USDG (15 x 400 USDG)",
    "mandatory_tags": ["@SolanaEvents", "@SuperteamDE"],
    "mandatory_cta_url": "https://luma.com/breakpoint2026?tk=HYnlfc",
    "venue_and_dates": "Olympia London | November 15-17, 2026",
    "x_thread_and_qrt": [
        "1/5 Breakpoint is coming to EUROPE for the first time in 4 years — and @SuperteamDE builders are heading to Olympia London (Nov 15–17, 2026)! 🇩🇪🇬🇧\n\nWhy @SolanaEvents Breakpoint 2026 is the #1 builder summit of the year:\nhttps://luma.com/breakpoint2026?tk=HYnlfc",
        "2/5 Zero fluff, 100% live mainnet engineering: Firedancer production milestones, Alpenglow consensus finality, ZK Compression at scale, and live SVM institutional payment rails unveiled directly on stage.",
        "3/5 For the German Solana ecosystem (@SuperteamDE), London is a 90-minute flight from Berlin, Munich & Frankfurt — turning Breakpoint 2026 into our home-turf European hackathon and founder summit.",
        "4/5 Whether you're shipping DePIN hardware, autonomous AI agent treasuries, or sub-second CLOBs on Solana, 3 days in Olympia London compresses 6 months of partnerships into one weekend.",
        "5/5 Grab your official Breakpoint 2026 pass before the next tier closes and join the @SuperteamDE builder contingent in London with @SolanaEvents:\n👉 https://luma.com/breakpoint2026?tk=HYnlfc",
    ],
    "video_60s_script_and_linkedin": (
        "From Berlin & Munich to Olympia London: Why @SuperteamDE is mobilizing for @SolanaEvents "
        "Breakpoint 2026 (Nov 15–17, 2026). Full 60 FPS motion reel + builder itinerary inside. "
        "Secure your ticket here: https://luma.com/breakpoint2026?tk=HYnlfc"
    ),
}

BOUNTY_B_ES_PACK = {
    "slug": "rumbo-a-breakpoint-2026-gana-una-entrada-y-apoyo-para-tu-viaje",
    "url": "https://earn.superteam.fun/listing/rumbo-a-breakpoint-2026-gana-una-entrada-y-apoyo-para-tu-viaje",
    "sponsor": "La Familia (Spain)",
    "reward_pool_cash": "5,000 USDG (10 x 400 USDG + 5 x 200 USDG = 15 Winners)",
    "mandatory_tags": ["@SolanaEvents", "@LaFamilia_so"],
    "mandatory_cta_url": "https://luma.com/breakpoint2026",
    "mandatory_discount_code": "SUPERTEAM-NH7-BP26",
    "venue_and_dates": "Olympia London | 15-17 de noviembre de 2026",
    "x_thread_es": [
        "1/5 ¡Por primera vez en 4 años, Solana Breakpoint llega a Europa (Olympia London, 15–17 Nov 2026) y @LaFamilia_so va con todo! 🇪🇸🇬🇧\n\nEntradas en @SolanaEvents con 25% DTO usando SUPERTEAM-NH7-BP26:\nhttps://luma.com/breakpoint2026",
        "2/5 ¿Por qué todo builder y creador de España debe estar en Londres? Breakpoint no tiene paneles teóricos: es donde se lanzan en vivo las innovaciones clave de todo el ecosistema Solana.",
        "3/5 De Madrid, Barcelona, Valencia o Málaga a Londres en 2 horas: 3 días conectando cara a cara con equipos core de SVM, inversores globales y los builders de @LaFamilia_so.",
        "4/5 Mi plan en Breakpoint 2026: cubrir en español cada anuncio técnico de Firedancer, Alpenglow y pagos SVM, y conectar proyectos de @LaFamilia_so con liquidez global.",
        "5/5 No te quedes fuera de la cita más importante del año con @SolanaEvents y @LaFamilia_so.\n🎟️ Entradas: https://luma.com/breakpoint2026\n🏷️ Código 25% DTO: SUPERTEAM-NH7-BP26",
    ],
    "video_60s_script_es": (
        "Rumbo a Breakpoint 2026 en Londres (15–17 Nov) con @LaFamilia_so y @SolanaEvents. "
        "Consigue tu entrada con 25% de descuento usando el código SUPERTEAM-NH7-BP26 en https://luma.com/breakpoint2026"
    ),
}


def verify_bounty_a(pack: dict) -> dict:
    combined_text = "\n".join(pack["x_thread_and_qrt"]) + "\n" + pack["video_60s_script_and_linkedin"]
    has_solana_events = "@SolanaEvents" in combined_text
    has_superteam_de = "@SuperteamDE" in combined_text
    has_exact_luma_tk = "https://luma.com/breakpoint2026?tk=HYnlfc" in combined_text
    has_london_dates = "Nov 15" in combined_text and "Olympia London" in combined_text
    tweet_lengths_valid = all(len(t) <= 280 for t in pack["x_thread_and_qrt"])

    passed = all([has_solana_events, has_superteam_de, has_exact_luma_tk, has_london_dates, tweet_lengths_valid])
    return {
        "slug": pack["slug"],
        "reward_pool_cash": pack["reward_pool_cash"],
        "checks": {
            "mentions_SolanaEvents": has_solana_events,
            "mentions_SuperteamDE": has_superteam_de,
            "includes_mandatory_luma_tracking_link": has_exact_luma_tk,
            "includes_london_venue_and_dates": has_london_dates,
            "all_tweets_within_280_chars": tweet_lengths_valid,
            "max_tweet_length": max(len(t) for t in pack["x_thread_and_qrt"]),
        },
        "verified": passed,
    }


def verify_bounty_b(pack: dict) -> dict:
    combined_text = "\n".join(pack["x_thread_es"]) + "\n" + pack["video_60s_script_es"]
    has_solana_events = "@SolanaEvents" in combined_text
    has_la_familia = "@LaFamilia_so" in combined_text
    has_luma_url = "https://luma.com/breakpoint2026" in combined_text
    has_discount_code = "SUPERTEAM-NH7-BP26" in combined_text
    tweet_lengths_valid = all(len(t) <= 280 for t in pack["x_thread_es"])

    passed = all([has_solana_events, has_la_familia, has_luma_url, has_discount_code, tweet_lengths_valid])
    return {
        "slug": pack["slug"],
        "reward_pool_cash": pack["reward_pool_cash"],
        "checks": {
            "mentions_SolanaEvents": has_solana_events,
            "mentions_LaFamilia_so": has_la_familia,
            "includes_mandatory_luma_link": has_luma_url,
            "includes_mandatory_discount_code_SUPERTEAM_NH7_BP26": has_discount_code,
            "all_tweets_within_280_chars": tweet_lengths_valid,
            "max_tweet_length": max(len(t) for t in pack["x_thread_es"]),
        },
        "verified": passed,
    }


def generate_banner(output_path: Path, width: int = 1200, height: int = 630) -> None:
    """Generates a deterministic 1200x630 Solana Breakpoint 2026 London PNG banner."""
    rows = []
    for y in range(height):
        row = bytearray([0])
        ny = y / float(height)
        for x in range(width):
            nx = x / float(width)
            # Solana purple (#9945FF) to Solana green (#14F195) diagonal gradient over dark obsidian
            diag = 0.55 * nx + 0.45 * (1.0 - ny)
            r = int(14 + 115 * (1.0 - diag) + 12 * math.sin(nx * 7.0))
            g = int(16 + 195 * diag + 15 * math.cos(ny * 5.0))
            b = int(38 + 185 * (1.0 - abs(diag - 0.5)))

            # Concentric London radar rings on right
            cx, cy = int(width * 0.76), int(height * 0.50)
            dist = math.hypot(x - cx, y - cy)
            if 155 <= dist <= 163 or 105 <= dist <= 111 or 55 <= dist <= 60:
                r, g, b = 20, 241, 149

            if x % 75 == 0 or y % 75 == 0:
                r = min(255, r + 12)
                g = min(255, g + 16)
                b = min(255, b + 20)

            if y < 8 or y >= height - 8:
                r, g, b = 20, 241, 149

            row.extend((max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))))
        rows.append(bytes(row))

    raw_data = b"".join(rows)

    def make_chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + make_chunk(b"IHDR", ihdr)
        + make_chunk(b"IDAT", zlib.compress(raw_data, level=6))
        + make_chunk(b"IEND", b"")
    )
    output_path.write_bytes(png_bytes)


def main() -> int:
    res_a = verify_bounty_a(BOUNTY_A_EN_PACK)
    res_b = verify_bounty_b(BOUNTY_B_ES_PACK)

    if not (res_a["verified"] and res_b["verified"]):
        print("ERROR: Mandatory Superteam Breakpoint 2026 compliance check failed!", file=sys.stderr)
        return 1

    generate_banner(BANNER_PATH)

    report = {
        "competition_bundle": "Superteam Earn — Solana Breakpoint 2026 Dual Cash Bounties",
        "combined_cash_pool": "$11,000 USDG Cash (30 Total Winner Slots)",
        "bounties": [
            {
                "bounty_a_en_germany": res_a,
                "submission_payload": BOUNTY_A_EN_PACK,
            },
            {
                "bounty_b_es_spain": res_b,
                "submission_payload": BOUNTY_B_ES_PACK,
            },
        ],
        "verification_status": "PASSED_ALL_MANDATORY_CTA_TAGS_AND_DISCOUNT_CODES",
    }
    canonical_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report["sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 78)
    print("Superteam Earn — Solana Breakpoint 2026 Dual Cash Bounties Verifier ($11,000 USDG)")
    print("=" * 78)
    print(f"  [PASS] Bounty A ({res_a['slug']}): {res_a['reward_pool_cash']}")
    print(f"         Mandatory Tags & Link Verified: @SolanaEvents, @SuperteamDE, ?tk=HYnlfc")
    print(f"  [PASS] Bounty B ({res_b['slug']}): {res_b['reward_pool_cash']}")
    print(f"         Mandatory Tags & Code Verified: @SolanaEvents, @LaFamilia_so, SUPERTEAM-NH7-BP26")
    print("-" * 78)
    print(f"  Banner Generated : {BANNER_PATH.name} ({BANNER_PATH.stat().st_size:,} bytes)")
    print(f"  Report Generated : {REPORT_PATH.name}")
    print(f"  Report SHA-256   : {report['sha256']}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
