#!/usr/bin/env python3
"""
Build the unified /Users/gaia/burning house/index.html hub & update README.md:
- Exact color-matched Paper (#fdf8f2) & Ochre (#d78410) hero stage & full-page theme
- 4-Rung Unified System Architecture (1 Sack -> 2 Sacks -> 4 Sacks PAE-04 -> 4 Sacks + Insurer) + Interactive SVG Graph
- Interactive Insights Visualizers (9-Level Combinatorial Sieve + Live Actuarial Policy Simulator + Agent/Critic Charts)
- Visual Page Workbench with Live Embedded Preview Stage
- Synchronized VTX-0.1 A/B Counterfactual Screening + PAE-04 / PAE-03 Film Shelf
- Styled Web Markdown Library (docs/*.html) + Complete Searchable Repository Manifest (two-pass exact sizes)
"""
import glob
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "docs", "manifest.json"), encoding="utf-8") as f:
    DOC_MANIFEST = json.load(f)


def human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


def categorize_file(rel: str) -> tuple[str, str]:
    ext = os.path.splitext(rel)[1].lower()
    if rel in DOC_MANIFEST:
        info = DOC_MANIFEST[rel]
        return "Papers & Notes" if "Zettel" not in info["category"] else "Zettels & Sources", info["desc"]
    if rel.startswith("docs/"):
        if rel == "docs/index.html":
            return "Interactive", "The Reading Room — web-typeset index of all 33 Markdown documents, Zettels, XML prompts, and critic logs."
        if rel == "docs/pae03-critic-all.html":
            return "Papers & Notes", "Complete anthology of all 17 PAE-03 independent critic rounds across Swarms 02–41."
        if rel.endswith(".html"):
            stem = os.path.basename(rel)[:-5]
            for m_rel, info in DOC_MANIFEST.items():
                if info["slug"] == stem:
                    return "Interactive", f"Styled web reading edition of {m_rel} ({info['words']:,} words)."
        return "Cases, Traces & Code", f"Web reader asset ({rel})."
    if rel.startswith("paeleo/abominable-house/"):
        if rel.endswith(".html"):
            descs = {
                "paeleo/abominable-house/index.html": "PAE-04 Main Case File — The Burning of the Abominable House (4 flour-sack tenants, 12 deeds, 12^12 stories, 6,030-film Six Memos Atlas).",
                "paeleo/abominable-house/whole-house.html": "Whole-House Architecture Map — complete inventory of all pages, live engines, Lab 7 links, and open threads.",
                "paeleo/abominable-house/paper.html": "The Flour Sack and the Sieve — scholarly draft paper in PAE-04's IM Fell + Inter notebook register.",
                "paeleo/abominable-house/journal.html": "PAE-04 Working Journal — dated production and mathematical notes.",
                "paeleo/abominable-house/slides.html": "PAE-04 Presentation Deck — slide sequence for The Burning of the Abominable House.",
                "paeleo/abominable-house/live/film.html": "The Film Bank — address, scrub, and screen any of 12^12 = 8,916,100,448,256 combinatorial films.",
                "paeleo/abominable-house/live/player.html": "T ZERO (12×12) — spatial room player staging the four tenants, lamps, traces, and live ledger.",
                "paeleo/abominable-house/live/numbers.html": "The Numbers — interactive derivations of 12^12, Calvino's 14,000 carry slip, 5 rules, and CP-SAT 11/16 proof.",
                "paeleo/abominable-house/live/policies.html": "The Policies — Skiller's four insurance contracts priced exactly over 2,663,172,255,744 five-rule stories.",
                "paeleo/abominable-house/live/abom.html": "Atomic Videotext Bank — 12 deeds + 12 consequences + 4 memories + 13 transitions inspectable individually.",
                "paeleo/abominable-house/live/array.html": "The Array — multi-screen simultaneous combinatorial wall across the Abominable House.",
            }
            return "Interactive", descs.get(rel, f"PAE-04 interactive page ({rel}).")
        if ext in (".mp4", ".jpg", ".png", ".svg"):
            return "Films & Plates", f"PAE-04 Abominable House media plate or rendered film ({os.path.basename(rel)})."
        return "Cases, Traces & Code", f"PAE-04 Abominable House module ({rel})."
    if rel.startswith("paeleo/flour-sacks/"):
        return "Interactive", "Flour Sacks Hub — minimal expressive sack study connecting PAE-03's six handmade swarms to PAE-04."
    if rel.startswith("paeleo/flour-tower/"):
        if rel.endswith(".html"):
            return "Interactive", f"PAE-03 Flour Tower live swarm film or workbench ({os.path.basename(rel)})."
        if ext in (".mp4", ".jpg", ".png", ".wav"):
            return "Films & Plates", f"PAE-03 Flour Tower rendered cut, still, or audio track ({rel})."
        return "Cases, Traces & Code", f"PAE-03 Flour Tower build/process script ({rel})."
    if rel == "paeleo/index.html":
        return "Interactive", "PAELEO Suite Index — gateway to PAE-04 (Abominable House), Flour Sacks, and PAE-03 (Flour Tower)."
    if rel.startswith("lab7/"):
        if rel.endswith(".html"):
            descs = {
                "lab7/index.html": "Lab 7 Companion Trio Index — classroom films 27, 28, and 29.",
                "lab7/abominable-house/index.html": "Lab 7 · 27/32 — The Abominable House (classroom procedural adaptation & interactive ledger).",
                "lab7/house-is-occupied/index.html": "Lab 7 · 28/32 — The House Is Occupied (comparing BDI 0.52, Symbolic 0.35, and Random 0.29 agents).",
                "lab7/by-what-light/index.html": "Lab 7 · 29/32 — By What Light (candle vs. switch focalization sieve collapsing 5.46×10^36 to 524,880).",
            }
            return "Interactive", descs.get(rel, f"Lab 7 interactive film ({rel}).")
        if ext in (".mp4", ".jpg", ".png"):
            return "Films & Plates", f"Lab 7 classroom film or contact still ({rel})."
        return "Cases, Traces & Code", f"Lab 7 runtime script or data ({rel})."
    if rel.startswith("vtx01_build/"):
        if rel.endswith(".html"):
            return "Interactive", f"VTX-0.1 Lamp-Room interactive viewer or blinded perceptual gate ({rel})."
        if ext in (".mp4", ".png", ".jpg"):
            return "Films & Plates", f"VTX-0.1 Lamp-Room rendered take or inspection sheet ({rel})."
        return "Cases, Traces & Code", f"VTX-0.1 case JSON, event trace, policy verdict, or build script ({rel})."
    if rel.startswith("abominable_house_journal/"):
        if rel.endswith(".html"):
            return "Interactive", "Abominable House Journal (Entries 01–20) — standalone visual HTML edition."
        return "Cases, Traces & Code", f"Journal stylesheet or asset ({rel})."
    if rel.startswith("assets/"):
        return "Films & Plates", f"Visual plate, color-matched hero illustration, favicon, or thumbnail ({rel})."
    if ext == ".zip":
        return "Bundles", f"Downloadable archive bundle ({rel})."
    if ext == ".pdf":
        if "DH2027" in rel:
            return "Papers & Notes", "Reading Over the Machine's Shoulder (DH2027 Short Paper PDF) — typeset scholarly PDF edition."
        return "Zettels & Sources", f"Extracted 19-paper DH2025 primary reference packet ({rel})."
    if rel in ("index.html", "reader.html"):
        return "Interactive", "Primary burning-house system hub & universal Markdown web reader."
    return "Cases, Traces & Code", f"Repository file ({rel})."


def collect_manifest() -> list[dict]:
    ignore_prefixes = (".git/", "__pycache__/")
    ignore_names = {".DS_Store", "BoA_DH2025.pdf"}
    rows = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in sorted(dirnames) if d not in (".git", "__pycache__")]
        for fn in sorted(filenames):
            if fn in ignore_names or fn.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            if any(rel.startswith(p) for p in ignore_prefixes):
                continue
            sz = os.path.getsize(full)
            ext = os.path.splitext(fn)[1].lstrip(".").upper() or "FILE"
            cat, desc = categorize_file(rel)
            styled_url = DOC_MANIFEST[rel]["html"] if rel in DOC_MANIFEST else ""
            inline_code = ext in ("JSON", "JSONL", "PY", "XML", "CSS") and sz < 250_000
            rows.append({
                "path": rel,
                "url": "./" + rel.replace(" ", "%20"),
                "styledUrl": ("./" + styled_url) if styled_url else "",
                "size": human_size(sz),
                "bytes": sz,
                "ext": ext,
                "cat": cat,
                "desc": desc,
                "inlineCode": inline_code,
            })
    return rows


VISUAL_PLATES = [
    {
        "group": "PAE-04 · Main Case",
        "title": "The Burning of the Abominable House (12¹²)",
        "meta": "paeleo/abominable-house/index.html",
        "img": "./paeleo/abominable-house/sheets/thumb.jpg",
        "href": "./paeleo/abominable-house/index.html",
    },
    {
        "group": "PAE-04 · System Map",
        "title": "Whole-House Inventory & Open Threads",
        "meta": "paeleo/abominable-house/whole-house.html",
        "img": "./assets/thumbs/sys-whole-house.jpg",
        "href": "./paeleo/abominable-house/whole-house.html",
    },
    {
        "group": "PAE-04 · Actuarial Engine",
        "title": "The Policies · Skiller's Four Contracts",
        "meta": "84.0% → 79.4% (−4.6 pp) Widow Life confound",
        "img": "./assets/thumbs/sys-policies.jpg",
        "href": "./paeleo/abominable-house/live/policies.html",
    },
    {
        "group": "PAE-04 · Combinatorial Sieve",
        "title": "The Numbers · 12¹² to Zero",
        "meta": "8.92T → 2.66T → 5.11B → CP-SAT 0",
        "img": "./assets/thumbs/sys-numbers.jpg",
        "href": "./paeleo/abominable-house/live/numbers.html",
    },
    {
        "group": "PAE-04 · Atomic Bank",
        "title": "41 Videotext Modules (Deeds · Conseq · Memory)",
        "meta": "paeleo/abominable-house/live/abom.html",
        "img": "./assets/thumbs/sys-deed-bank.jpg",
        "href": "./paeleo/abominable-house/live/abom.html",
    },
    {
        "group": "PAE-04 · Multi-Screen Wall",
        "title": "The Array · Simultaneous Permutations",
        "meta": "paeleo/abominable-house/live/array.html",
        "img": "./assets/thumbs/sys-array.jpg",
        "href": "./paeleo/abominable-house/live/array.html",
    },
    {
        "group": "DH2027 · Short Paper PDF",
        "title": "Reading Over the Machine's Shoulder",
        "meta": "Reading_Over_the_Machines_Shoulder_DH2027.pdf",
        "img": "./assets/thumbs/thumb-dh2027-short-paper.jpg",
        "href": "./Reading_Over_the_Machines_Shoulder_DH2027.pdf",
    },
    {
        "group": "PAE-04 · Draft Paper",
        "title": "The Flour Sack and the Sieve",
        "meta": "paeleo/abominable-house/paper.html",
        "img": "./assets/thumbs/sys-paper.jpg",
        "href": "./paeleo/abominable-house/paper.html",
    },
    {
        "group": "PAE-03 · 1-Sack Rung",
        "title": "Flour Sacks & The Flour Tower (6 Swarms)",
        "meta": "paeleo/flour-sacks/index.html",
        "img": "./paeleo/flour-tower/film/thumbnail.jpg",
        "href": "./paeleo/flour-sacks/index.html",
    },
    {
        "group": "PAE-03 · Swarm 14",
        "title": "Pose-to-Pose Pencil Flour Sack",
        "meta": "paeleo/flour-tower/films/14-pose2pose.html",
        "img": "./paeleo/flour-tower/stills/14-22.5.jpg",
        "href": "./paeleo/flour-tower/films/14-pose2pose.html",
    },
    {
        "group": "PAE-03 · Swarm 41",
        "title": "Soft-Body Continuum Flour Sack",
        "meta": "paeleo/flour-tower/films/41-soft-body.html",
        "img": "./paeleo/flour-tower/stills/41-29.0.jpg",
        "href": "./paeleo/flour-tower/films/41-soft-body.html",
    },
    {
        "group": "VTX-0.1 · 2-Sack Counterfactual",
        "title": "Take A (Assist) vs. Take B (Arson) · Accepted",
        "meta": "1-line goal patch · 77 shared frames",
        "img": "./Abominable_House_Journal_38/journal-img/25-rev2-pair.jpg",
        "href": "./vtx01_build/viewer/index.html",
    },
    {
        "group": "VTX-0.1 · Critic Rejection",
        "title": "Rev 1 Rejected · 163px Lamp Gap & Bow-Tie",
        "meta": "vtx01_build/revisions/rev1_rejected/",
        "img": "./Abominable_House_Journal_38/journal-img/24-rev1-bowtie.jpg",
        "href": "#compare",
    },
    {
        "group": "Lab 7 · 27 / 32",
        "title": "Classroom Adaptation · Abominable House",
        "meta": "lab7/abominable-house/index.html",
        "img": "./lab7/abominable-house/abominable-house.jpg",
        "href": "./lab7/abominable-house/index.html",
    },
    {
        "group": "Lab 7 · 28 / 32",
        "title": "The House Is Occupied · BDI vs. Symbolic Agents",
        "meta": "Coherence: 0.52 BDI · 0.35 Symbolic · 0.29 Random",
        "img": "./lab7/house-is-occupied/house-is-occupied.jpg",
        "href": "./lab7/house-is-occupied/index.html",
    },
    {
        "group": "Lab 7 · 29 / 32",
        "title": "By What Light · Focalization Sieve",
        "meta": "5.46×10³⁶ → 3.79×10²⁴ → 524,880 legal stories",
        "img": "./lab7/by-what-light/by-what-light.jpg",
        "href": "./lab7/by-what-light/index.html",
    },
    {
        "group": "Reading Room · 33 Editions",
        "title": "Styled Web Papers, Zettels & Critic Logs",
        "meta": "docs/index.html · 193k words · 82 Zettel cards",
        "img": "./assets/thumbs/thumb-dh2025-packet.jpg",
        "href": "./docs/index.html",
    },
]

WORKBENCH_PAGES = [
    {
        "id": "pae04-main",
        "rung": "Main · 4 Sacks",
        "title": "PAE-04 · The Abominable House",
        "sub": "Case file, 3 rendered films, 6,030-film Six Memos Atlas, and complete entry hub.",
        "url": "./paeleo/abominable-house/index.html",
        "img": "./paeleo/abominable-house/sheets/thumb.jpg",
    },
    {
        "id": "pae04-whole",
        "rung": "Architecture",
        "title": "Whole-House System Map",
        "sub": "Every room, live tool, Lab 7 backlink, and open verification question on one board.",
        "url": "./paeleo/abominable-house/whole-house.html",
        "img": "./assets/thumbs/sys-whole-house.jpg",
    },
    {
        "id": "pae04-film",
        "rung": "12¹² Engine",
        "title": "The Film Bank",
        "sub": "Dial any 12-digit base-12 number to play its exact 74-second flour-sack film live.",
        "url": "./paeleo/abominable-house/live/film.html",
        "img": "./paeleo/abominable-house/sheets/sheetA.jpg",
    },
    {
        "id": "pae04-player",
        "rung": "Spatial Stage",
        "title": "T ZERO · 12×12 Room",
        "sub": "Watch Roessler, Belindo, Inigo, and Ogiva move across rooms, light, and material traces.",
        "url": "./paeleo/abominable-house/live/player.html",
        "img": "./paeleo/abominable-house/sheets/sheetB.jpg",
    },
    {
        "id": "pae04-policies",
        "rung": "Actuarial",
        "title": "The Policies",
        "sub": "Skiller's four insurance contracts priced exactly across 2.66 trillion five-rule stories.",
        "url": "./paeleo/abominable-house/live/policies.html",
        "img": "./assets/thumbs/sys-policies.jpg",
    },
    {
        "id": "pae04-numbers",
        "rung": "Combinatorics",
        "title": "The Numbers",
        "sub": "Exact counts from 12¹² through Calvino's 14,000 carry slip down to CP-SAT's 0.",
        "url": "./paeleo/abominable-house/live/numbers.html",
        "img": "./assets/thumbs/sys-numbers.jpg",
    },
    {
        "id": "pae04-abom",
        "rung": "41 Modules",
        "title": "Atomic Videotext Bank",
        "sub": "Inspect all 12 deeds, 12 consequences, 4 tenant memories, and 13 transitions.",
        "url": "./paeleo/abominable-house/live/abom.html",
        "img": "./assets/thumbs/sys-deed-bank.jpg",
    },
    {
        "id": "pae04-array",
        "rung": "Multi-Channel",
        "title": "The Array",
        "sub": "Simultaneous grid of parallel house permutations running in lockstep.",
        "url": "./paeleo/abominable-house/live/array.html",
        "img": "./assets/thumbs/sys-array.jpg",
    },
    {
        "id": "flour-sacks",
        "rung": "1 Sack · Study",
        "title": "Flour Sacks",
        "sub": "Why a half-filled sack is the minimal acting body for words-to-world video-text.",
        "url": "./paeleo/flour-sacks/index.html",
        "img": "./paeleo/flour-tower/stills/02-22.5.jpg",
    },
    {
        "id": "flour-tower",
        "rung": "PAE-03 · 6 Swarms",
        "title": "The Flour Tower, Handmade",
        "sub": "Six SCION swarms, zero tween libraries, 17 blind critic rounds, and workbench.",
        "url": "./paeleo/flour-tower/index.html",
        "img": "./paeleo/flour-tower/stills/07-22.5.jpg",
    },
    {
        "id": "vtx01-viewer",
        "rung": "2 Sacks · Patch",
        "title": "VTX-0.1 Counterfactual Viewer",
        "sub": "1-line goal patch (assist vs. arson), event graph diff, and policy verdict flip.",
        "url": "./vtx01_build/viewer/index.html",
        "img": "./Abominable_House_Journal_38/journal-img/25-rev2-pair.jpg",
    },
    {
        "id": "lab7-28",
        "rung": "Lab 7 · 28/32",
        "title": "The House Is Occupied",
        "sub": "BDI (0.52) vs. Symbolic (0.35) vs. Random (0.29) tenant reasoning architectures.",
        "url": "./lab7/house-is-occupied/index.html",
        "img": "./lab7/house-is-occupied/house-is-occupied.jpg",
    },
    {
        "id": "lab7-29",
        "rung": "Lab 7 · 29/32",
        "title": "By What Light",
        "sub": "Candle vs. light-switch visibility collapsing 5.46×10³⁶ open states to 524,880.",
        "url": "./lab7/by-what-light/index.html",
        "img": "./lab7/by-what-light/by-what-light.jpg",
    },
    {
        "id": "reading-room",
        "rung": "33 Styled Docs",
        "title": "The Reading Room",
        "sub": "Editorial web editions for zettle-past, zettle, papers, specs, XML prompts, and critics.",
        "url": "./docs/index.html",
        "img": "./assets/thumbs/sys-paper.jpg",
    },
]

FEATURED_DOCS = [
    ("CLAIMS.md", "14 Claims Audited"),
    ("zettle-past.md", "9 Cards · New"),
    ("Abominable_House_Submission_Draft.md", "Canonical Paper"),
    ("VTX01_MVVT_Research_Memo_and_Spec.md", "VTX-0.1 Spec"),
    ("Abominable_House_Framing_Notes.md", "Framing Notes"),
    ("pae04_abominable_house_scion_run.md", "Formal Proofs"),
    ("Logline_Journal_Entries_and_Existing_Assets.md", "Entries 21–38"),
    ("zettle.md", "28 Zettels"),
    ("xzet.md", "5 Cross-Zettels"),
    ("DH2025_Concrete_Papers_and_Works_Cited.md", "19 DH2025 Papers"),
    ("abominable_house_mvvt_research_notes.md", "Words to World"),
    ("p1.md", "XML v1.1 Spec"),
]


def build_html(manifest_rows: list[dict]) -> str:
    featured_cards = []
    for rel, badge in FEATURED_DOCS:
        info = DOC_MANIFEST[rel]
        featured_cards.append(f"""
        <article class="doc-shelf-card">
          <div>
            <div class="doc-shelf-top">
              <span class="doc-shelf-cat">{html.escape(info["category"])}</span>
              <span class="doc-shelf-badge">{html.escape(badge)}</span>
            </div>
            <h3 class="doc-shelf-title"><a href="./{info["html"]}">{html.escape(info["title"])}</a></h3>
            <p class="doc-shelf-desc">{html.escape(info["desc"])}</p>
          </div>
          <div class="doc-shelf-foot">
            <span>{info["words"]:,} words · ~{info["read_mins"]} min · {html.escape(info["units"])}</span>
            <span class="doc-shelf-links">
              <a class="mini-cta" href="./{info["html"]}">Read web edition →</a>
              <a class="mini-raw" href="./{rel}">.md</a>
            </span>
          </div>
        </article>
        """)

    wb_cards = []
    for i, w in enumerate(WORKBENCH_PAGES):
        act = " active" if i == 0 else ""
        wb_cards.append(f"""
        <div class="wb-card{act}" data-wb-card="{w["id"]}">
          <div class="wb-thumb" onclick="loadStage('{w["id"]}')">
            <img src="{w["img"]}" alt="{html.escape(w["title"])}" loading="lazy" />
            <span class="wb-rung">{html.escape(w["rung"])}</span>
          </div>
          <div class="wb-body">
            <h3 class="wb-title">{html.escape(w["title"])}</h3>
            <p class="wb-sub">{html.escape(w["sub"])}</p>
            <div class="wb-actions">
              <button type="button" class="read-btn" onclick="loadStage('{w["id"]}')">Preview on stage</button>
              <a class="mini-cta" href="{w["url"]}">Open page ↗</a>
            </div>
          </div>
        </div>
        """)

    return f"""<!DOCTYPE html>
<html lang="en" data-plate="paper">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>burning-house — Flour Sacks, Abominable House (12¹²) &amp; Minimum Viable Video-Text</title>
  <meta name="description" content="Unified system uniting PAE-03 (Flour Sacks &amp; Flour Tower), VTX-0.1 (Lamp-Room Counterfactual), PAE-04 (The Burning of the Abominable House, 12^12 stories), Lab 7 (27–29), Skiller's Policies, and 33 web-typeset research editions." />
  <meta name="theme-color" id="themeColorMeta" content="#fdf8f2" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="icon" type="image/png" sizes="64x64" href="./assets/favicon-64.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="./assets/favicon-32.png" />
  <link rel="shortcut icon" href="./favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="./assets/apple-touch-icon.png" />
  <script>
    (function () {{
      var p = 'paper';
      try {{
        var q = new URLSearchParams(location.search).get('plate');
        if (q === 'ochre' || q === 'paper') {{
          p = q;
        }} else {{
          var s = localStorage.getItem('bh_plate');
          if (s === 'ochre' || s === 'paper') p = s;
        }}
      }} catch (e) {{}}
      document.documentElement.setAttribute('data-plate', p);
      var m = document.getElementById('themeColorMeta');
      if (m) m.setAttribute('content', p === 'ochre' ? '#d78410' : '#fdf8f2');
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet" />
  <style>
    :root,
    html[data-plate="paper"] {{
      --bg: #fdf8f2;
      --surface: #f6efe5;
      --surface-elev: #ede4d6;
      --ink: #131311;
      --ink-body: #28241f;
      --muted: #6b6156;
      --accent: #9e331e;
      --rule: rgba(19, 19, 17, 0.14);
      --rule-strong: rgba(19, 19, 17, 0.34);
      --btn-bg: #131311;
      --btn-hover: #27231e;
      --btn-fg: #f8f6f3;
      --pill-fg: #fdf8f2;
      --row-hover: rgba(19, 19, 17, 0.045);
      --ghost-hover: rgba(19, 19, 17, 0.06);
      --hero-divider: rgba(19, 19, 17, 0.14);
      --backdrop: rgba(19, 17, 14, 0.52);
      --serif: 'Newsreader', 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
      --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
      color-scheme: light;
    }}

    html[data-plate="ochre"] {{
      --bg: #d78410;
      --surface: #cc790d;
      --surface-elev: #ba6c0a;
      --ink: #0e0b05;
      --ink-body: #1c1408;
      --muted: #3d280b;
      --accent: #681707;
      --rule: rgba(14, 11, 5, 0.22);
      --rule-strong: rgba(14, 11, 5, 0.48);
      --btn-bg: #0a0a0a;
      --btn-hover: #1d160f;
      --btn-fg: #ecddb9;
      --pill-fg: #ecddb9;
      --row-hover: rgba(14, 11, 5, 0.075);
      --ghost-hover: rgba(14, 11, 5, 0.09);
      --hero-divider: #291f15;
      --backdrop: rgba(14, 11, 5, 0.65);
      color-scheme: light;
    }}

    * {{ box-sizing: border-box; }}
    html {{
      scroll-behavior: smooth;
      background: var(--bg);
      color: var(--ink);
      transition: background-color 0.24s ease, color 0.24s ease;
    }}
    body {{
      margin: 0;
      font-family: var(--serif);
      background: var(--bg);
      color: var(--ink);
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.24s ease, color 0.24s ease;
    }}

    /* ── HERO STAGE (100dvh, exact color-matched Paper & Ochre plates) ── */
    .hero {{
      position: relative;
      min-height: 100dvh;
      width: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      background: var(--bg);
      border-bottom: 1px solid var(--hero-divider);
      transition: background-color 0.24s ease, border-color 0.24s ease;
    }}
    html[data-plate="ochre"] .hero {{ border-bottom-width: 2px; }}

    .hero-bar {{
      position: relative;
      z-index: 4;
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 14px 20px;
      padding: clamp(20px, 3.8vw, 42px) clamp(20px, 4.8vw, 60px);
    }}

    .brand {{
      font-family: var(--serif);
      font-weight: 500;
      font-size: clamp(30px, 3.8vw, 52px);
      line-height: 1;
      letter-spacing: -0.028em;
      color: var(--ink);
      text-decoration: none;
    }}
    html[data-plate="ochre"] .brand {{ font-weight: 600; letter-spacing: -0.032em; }}

    .hero-nav {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: clamp(12px, 1.8vw, 22px);
    }}

    .mode-pair {{
      display: inline-flex;
      align-items: baseline;
      gap: 6px;
      font-family: var(--serif);
      font-size: clamp(14px, 1.15vw, 17px);
      color: var(--muted);
    }}
    .mode-opt {{
      appearance: none;
      background: none;
      border: 0;
      padding: 2px 0;
      font: inherit;
      color: var(--muted);
      cursor: pointer;
      opacity: 0.8;
    }}
    .mode-opt:hover {{ color: var(--ink); opacity: 1; }}
    .mode-opt.active {{
      color: var(--ink);
      font-weight: 500;
      opacity: 1;
      text-decoration: underline;
      text-underline-offset: 4px;
      text-decoration-thickness: 1.25px;
    }}
    .mode-dot {{ user-select: none; opacity: 0.55; }}

    .nav-link {{
      font-family: var(--serif);
      font-size: clamp(16px, 1.35vw, 20px);
      color: var(--ink);
      text-decoration: none;
      opacity: 0.9;
    }}
    .nav-link:hover {{
      text-decoration: underline;
      text-underline-offset: 4px;
      opacity: 1;
    }}
    .archive-link {{
      font-family: var(--serif);
      font-size: clamp(17px, 1.5vw, 23px);
      color: var(--ink);
      text-decoration: underline;
      text-underline-offset: 5px;
      text-decoration-thickness: 1.6px;
    }}

    .paper-stage {{
      position: relative;
      z-index: 2;
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0 clamp(18px, 5vw, 64px) clamp(38px, 6.5vh, 72px);
      gap: clamp(20px, 3.6vh, 34px);
    }}
    .paper-art {{
      width: min(760px, 88vw);
      max-height: 52dvh;
      object-fit: contain;
      mix-blend-mode: multiply;
      user-select: none;
      pointer-events: none;
    }}
    .ochre-bg {{
      display: none;
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: right bottom;
      z-index: 1;
      user-select: none;
      pointer-events: none;
    }}
    @media (max-width: 720px) {{ .ochre-bg {{ object-position: 86% bottom; }} }}
    html[data-plate="ochre"] .ochre-bg {{ display: block; }}
    html[data-plate="ochre"] .paper-art {{ display: none; }}
    html[data-plate="ochre"] .paper-stage {{
      align-items: flex-start;
      justify-content: flex-end;
      padding: 0 clamp(22px, 5vw, 64px) clamp(28px, 5.2vh, 52px);
    }}

    .hero-cta-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 12px;
    }}
    html[data-plate="ochre"] .hero-cta-row {{ justify-content: flex-start; }}

    .cta-btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--btn-bg);
      color: var(--btn-fg);
      font-family: var(--serif);
      font-size: clamp(17px, 1.45vw, 21px);
      padding: 12px 28px 13px;
      border: 1px solid var(--btn-bg);
      text-decoration: none;
      cursor: pointer;
      transition: background-color 0.14s ease, color 0.14s ease;
    }}
    .cta-btn:hover {{ background: var(--btn-hover); }}
    .cta-btn.ghost {{
      background: rgba(253, 248, 242, 0.72);
      color: var(--ink);
      border-color: var(--rule-strong);
      font-size: clamp(16px, 1.3vw, 19px);
      padding: 11px 22px 12px;
    }}
    html[data-plate="ochre"] .cta-btn.ghost {{
      background: rgba(215, 132, 16, 0.82);
    }}
    .cta-btn.ghost:hover {{ background: var(--ghost-hover); }}

    /* ── SECTIONS ── */
    .wrap {{
      max-width: 1260px;
      margin: 0 auto;
      padding: clamp(46px, 6.5vw, 84px) clamp(20px, 4.8vw, 60px);
      border-top: 1px solid var(--rule);
    }}
    .wrap:first-of-type {{ border-top: 0; }}

    .sec-kicker {{
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.11em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 6px;
    }}
    .sec-head {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px 24px;
      margin-bottom: 26px;
      padding-bottom: 14px;
      border-bottom: 1.5px solid var(--rule-strong);
    }}
    .sec-head h2 {{
      margin: 0;
      font-size: clamp(26px, 2.7vw, 37px);
      font-weight: 500;
      letter-spacing: -0.022em;
      color: var(--ink);
    }}
    .sec-note {{
      margin: 0;
      color: var(--muted);
      font-size: 16.5px;
      line-height: 1.45;
      max-width: 64ch;
    }}

    .pill {{
      appearance: none;
      background: transparent;
      color: var(--ink);
      border: 1px solid var(--rule-strong);
      padding: 7px 14px 8px;
      font-family: var(--serif);
      font-size: 15px;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background-color 0.14s ease, color 0.14s ease;
    }}
    .pill.active, .pill:hover {{
      background: var(--ink);
      color: var(--pill-fg);
      border-color: var(--ink);
    }}

    /* ── SECTION 1: 4-RUNG SCALE LADDER + ARCHITECTURE GRAPH ── */
    .rungs-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
      margin-bottom: 26px;
    }}
    @media (max-width: 1020px) {{ .rungs-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 600px) {{ .rungs-grid {{ grid-template-columns: 1fr; }} }}

    .rung-card {{
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      border-top: 3px solid var(--ink);
      padding: 18px 18px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }}
    .rung-card.main-rung {{
      border-top-width: 5px;
      border-top-color: var(--accent);
      background: var(--surface-elev);
    }}
    .rung-num {{
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 6px;
    }}
    .rung-title {{
      font-size: 21px;
      font-weight: 600;
      line-height: 1.2;
      margin: 0 0 8px;
    }}
    .rung-desc {{
      font-size: 15.5px;
      line-height: 1.48;
      color: var(--ink-body);
      margin: 0 0 10px;
    }}
    .rung-stat {{
      font-family: var(--mono);
      font-size: 11.5px;
      color: var(--muted);
      padding-top: 10px;
      border-top: 1px solid var(--rule);
    }}
    .rung-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }}
    .mini-cta {{
      font-family: var(--mono);
      font-size: 11px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--rule-strong);
      padding: 3px 8px;
      background: var(--bg);
    }}
    .mini-cta:hover {{
      background: var(--ink);
      color: var(--pill-fg);
    }}

    .arch-diagram {{
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      padding: 18px 20px;
      overflow-x: auto;
    }}
    .arch-diagram svg {{
      width: 100%;
      min-width: 780px;
      height: auto;
      display: block;
    }}
    .arch-node {{ cursor: pointer; transition: opacity 0.15s ease; }}
    .arch-node:hover rect {{ stroke-width: 2.4px; }}

    /* ── SECTION 2: INTERACTIVE INSIGHTS (SIEVE + POLICIES + AGENTS) ── */
    .insights-grid {{
      display: grid;
      grid-template-columns: 1.12fr 0.88fr;
      gap: 22px;
      margin-bottom: 22px;
    }}
    @media (max-width: 960px) {{ .insights-grid {{ grid-template-columns: 1fr; }} }}

    .insight-box {{
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      padding: 20px 22px;
    }}
    .insight-box h3 {{
      margin: 0 0 6px;
      font-size: 22px;
      font-weight: 600;
      letter-spacing: -0.015em;
    }}
    .insight-sub {{
      margin: 0 0 16px;
      font-size: 15px;
      color: var(--muted);
      line-height: 1.42;
    }}

    .sieve-list {{
      display: flex;
      flex-direction: column;
      gap: 7px;
      margin-bottom: 14px;
    }}
    .sieve-row {{
      appearance: none;
      width: 100%;
      text-align: left;
      background: var(--bg);
      border: 1px solid var(--rule);
      padding: 8px 10px;
      cursor: pointer;
      color: var(--ink);
      font-family: inherit;
      transition: border-color 0.14s ease;
    }}
    .sieve-row:hover, .sieve-row.active {{
      border-color: var(--ink);
      border-width: 1.5px;
    }}
    .sieve-row-top {{
      display: flex;
      justify-content: space-between;
      gap: 8px;
      font-family: var(--mono);
      font-size: 11.5px;
      margin-bottom: 5px;
    }}
    .sieve-track {{
      height: 8px;
      width: 100%;
      background: var(--surface-elev);
      overflow: hidden;
    }}
    .sieve-fill {{
      height: 100%;
      background: var(--ink);
      transition: width 0.25s ease;
    }}
    .sieve-row.main-bar .sieve-fill {{ background: var(--accent); }}
    .sieve-detail {{
      background: var(--bg);
      border-left: 3px solid var(--accent);
      padding: 12px 14px;
      font-size: 15px;
      line-height: 1.48;
    }}
    .sieve-detail code {{
      font-family: var(--mono);
      font-size: 12px;
    }}

    .pol-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 14px;
    }}
    .pol-btn {{
      appearance: none;
      background: var(--bg);
      color: var(--ink);
      border: 1px solid var(--rule-strong);
      font-family: var(--mono);
      font-size: 11px;
      padding: 5px 9px;
      cursor: pointer;
    }}
    .pol-btn.active {{
      background: var(--ink);
      color: var(--pill-fg);
    }}
    .pol-bars {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin: 14px 0;
    }}
    .pol-item-top {{
      display: flex;
      justify-content: space-between;
      font-family: var(--mono);
      font-size: 12px;
      margin-bottom: 4px;
    }}
    .pol-track {{
      position: relative;
      height: 16px;
      background: var(--bg);
      border: 1px solid var(--rule-strong);
    }}
    .pol-fill {{
      height: 100%;
      background: var(--ink);
      transition: width 0.25s ease;
    }}
    .pol-fill.confound {{ background: var(--accent); }}
    .pol-ref-tick {{
      position: absolute;
      top: -3px;
      bottom: -3px;
      width: 2px;
      background: var(--ink);
    }}

    .metrics-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}
    .metric-card {{
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      padding: 16px 18px;
    }}
    .metric-card h4 {{
      margin: 0 0 8px;
      font-size: 18px;
      font-weight: 600;
    }}

    /* ── SECTION 3: LIVE SYSTEM WORKBENCH & INLINE PREVIEW STAGE ── */
    .stage-shell {{
      background: var(--surface);
      border: 1.5px solid var(--rule-strong);
      margin-bottom: 24px;
    }}
    .stage-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 10px 14px;
      border-bottom: 1px solid var(--rule-strong);
      font-family: var(--mono);
      font-size: 12px;
    }}
    .stage-frame {{
      width: 100%;
      height: clamp(460px, 68dvh, 720px);
      border: 0;
      display: block;
      background: #141310;
    }}

    .wb-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(268px, 1fr));
      gap: 18px;
    }}
    .wb-card {{
      background: var(--surface);
      border: 1px solid var(--rule);
      display: flex;
      flex-direction: column;
      transition: border-color 0.15s ease, transform 0.15s ease;
    }}
    .wb-card.active, .wb-card:hover {{
      border-color: var(--ink);
      transform: translateY(-1px);
    }}
    .wb-thumb {{
      position: relative;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      background: #141310;
      cursor: pointer;
      border-bottom: 1px solid var(--rule);
    }}
    .wb-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .wb-rung {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(19, 19, 17, 0.86);
      color: #fdf8f2;
      font-family: var(--mono);
      font-size: 10px;
      padding: 2px 7px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .wb-body {{
      padding: 12px 14px 14px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }}
    .wb-title {{
      margin: 0 0 5px;
      font-size: 18px;
      font-weight: 600;
      line-height: 1.24;
    }}
    .wb-sub {{
      margin: 0 0 12px;
      font-size: 14.5px;
      line-height: 1.42;
      color: var(--ink-body);
    }}
    .wb-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    /* ── SECTION 4: COMPARE TAKES ── */
    .takes-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px 16px;
      margin-bottom: 18px;
    }}
    .takes-controls {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}
    .takes-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
      margin-bottom: 22px;
    }}
    @media (max-width: 820px) {{ .takes-grid {{ grid-template-columns: 1fr; }} }}
    .take-figure {{
      margin: 0;
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      padding: 14px;
    }}
    .take-figure video {{
      width: 100%;
      aspect-ratio: 16 / 9;
      background: #12100e;
      display: block;
    }}
    .take-cap {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 12px;
      margin-top: 10px;
      font-size: 15.5px;
    }}
    .take-cap span.mono {{
      font-family: var(--mono);
      font-size: 11.5px;
      color: var(--muted);
    }}

    /* ── SECTION 5: STYLED WEB MARKDOWN LIBRARY ── */
    .doc-shelf-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }}
    .doc-shelf-card {{
      background: var(--surface);
      border: 1px solid var(--rule-strong);
      border-left: 3.5px solid var(--ink);
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }}
    .doc-shelf-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .doc-shelf-cat {{
      font-family: var(--mono);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .doc-shelf-badge {{
      font-family: var(--mono);
      font-size: 10px;
      padding: 2px 6px;
      background: var(--bg);
      border: 1px solid var(--rule-strong);
    }}
    .doc-shelf-title {{
      margin: 0 0 6px;
      font-size: 19.5px;
      font-weight: 600;
      line-height: 1.24;
    }}
    .doc-shelf-title a {{
      color: var(--ink);
      text-decoration: none;
    }}
    .doc-shelf-title a:hover {{ text-decoration: underline; }}
    .doc-shelf-desc {{
      margin: 0;
      font-size: 14.8px;
      line-height: 1.45;
      color: var(--ink-body);
    }}
    .doc-shelf-foot {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid var(--rule);
      font-family: var(--mono);
      font-size: 10.5px;
      color: var(--muted);
    }}
    .doc-shelf-links {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .mini-raw {{
      color: var(--muted);
      text-decoration: underline;
      font-family: var(--mono);
      font-size: 10.5px;
    }}

    /* ── SECTION 6: PLATES GALLERY & COMPLETE FILE MANIFEST ── */
    .plates-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(265px, 1fr));
      gap: 20px 18px;
      margin-bottom: 52px;
    }}
    .plate-card {{
      display: flex;
      flex-direction: column;
      text-decoration: none;
      color: inherit;
      border: 1px solid var(--rule);
      background: var(--surface);
      transition: border-color 0.16s ease, transform 0.16s ease;
    }}
    .plate-card:hover {{
      border-color: var(--ink);
      transform: translateY(-1px);
    }}
    .plate-thumb {{
      aspect-ratio: 16 / 10;
      width: 100%;
      overflow: hidden;
      background: var(--surface-elev);
      border-bottom: 1px solid var(--rule);
    }}
    .plate-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .plate-meta {{ padding: 12px 14px 14px; }}
    .plate-group {{
      font-family: var(--mono);
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      margin-bottom: 4px;
    }}
    .plate-title {{
      font-size: 17px;
      font-weight: 500;
      line-height: 1.28;
      margin: 0 0 5px;
    }}
    .plate-path {{
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      word-break: break-all;
    }}

    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 18px;
    }}
    .cat-tabs {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .search-input {{
      font-family: var(--serif);
      font-size: 16px;
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--rule-strong);
      padding: 7px 12px;
      min-width: 250px;
    }}
    .manifest-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 15px;
    }}
    .manifest-table th {{
      text-align: left;
      font-weight: 500;
      font-size: 12.5px;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
      padding: 9px 10px;
      border-bottom: 1.5px solid var(--rule-strong);
    }}
    .manifest-table td {{
      padding: 10px;
      border-bottom: 1px solid var(--rule);
      vertical-align: top;
    }}
    .manifest-table tr:hover td {{ background: var(--row-hover); }}
    .file-link {{
      font-family: var(--mono);
      font-size: 12px;
      color: var(--ink);
      text-decoration: underline;
      text-underline-offset: 3px;
      word-break: break-all;
    }}
    .file-desc {{ color: var(--ink-body); line-height: 1.42; }}
    .file-cat, .file-size {{
      font-family: var(--mono);
      font-size: 11.5px;
      color: var(--muted);
      white-space: nowrap;
    }}
    .read-btn {{
      appearance: none;
      background: var(--bg);
      border: 1px solid var(--rule-strong);
      font-family: var(--mono);
      font-size: 11px;
      padding: 3px 8px;
      color: var(--ink);
      cursor: pointer;
      margin-right: 6px;
      text-decoration: none;
      display: inline-block;
    }}
    .read-btn:hover {{
      background: var(--ink);
      color: var(--pill-fg);
    }}

    /* ── CODE / JSON DRAWER ── */
    .drawer-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 60;
      background: var(--backdrop);
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .drawer-backdrop.open {{ display: flex; }}
    .drawer {{
      width: min(980px, 100%);
      max-height: 88dvh;
      background: var(--bg);
      border: 1.5px solid var(--ink);
      display: flex;
      flex-direction: column;
    }}
    .drawer-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 18px;
      border-bottom: 1px solid var(--rule-strong);
      background: var(--surface);
    }}
    .drawer-title {{ font-family: var(--mono); font-size: 12.5px; }}
    .drawer-body {{ padding: 20px; overflow: auto; }}
    .drawer-body pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: var(--mono);
      font-size: 12.5px;
      line-height: 1.58;
    }}

    footer {{
      max-width: 1260px;
      margin: 0 auto;
      padding: 26px clamp(20px, 4.8vw, 60px) 54px;
      border-top: 1px solid var(--rule);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 12px;
      font-size: 14.5px;
      color: var(--muted);
    }}
    footer a {{ color: var(--ink); }}
  </style>
</head>
<body>

  <!-- 100dvh HERO STAGE: Paper (#fdf8f2) & Ochre (#d78410) -->
  <section class="hero" id="top">
    <img class="ochre-bg" src="./assets/hero-ochre-wide.jpg" alt="Flour sack beside a tipped kerosene lamp on warm ochre ground" />

    <header class="hero-bar">
      <a class="brand" href="#top">burning-house</a>
      <nav class="hero-nav" aria-label="Primary">
        <span class="mode-pair" role="group" aria-label="Color mode">
          <button type="button" class="mode-opt active" data-mode-btn="paper" onclick="setPlate('paper')">Paper</button>
          <span class="mode-dot" aria-hidden="true">·</span>
          <button type="button" class="mode-opt" data-mode-btn="ochre" onclick="setPlate('ochre')">Ochre</button>
        </span>
        <a class="nav-link" href="#system">System</a>
        <a class="nav-link" href="#insights">Insights</a>
        <a class="nav-link" href="#pages">Workbench</a>
        <a class="nav-link" href="./find.html">Find</a>
        <a class="nav-link" href="./read.html">Read</a>
        <a class="nav-link" href="./docs/index.html">Reading Room</a>
        <a class="archive-link" href="#archive">Archive</a>
      </nav>
    </header>

    <div class="paper-stage">
      <img class="paper-art" src="./assets/hero-paper-sacks.jpg" alt="Two half-filled flour sacks and a fallen brass lamp in graphite and wash" />
      <div class="hero-cta-row">
        <a class="cta-btn" href="./paeleo/abominable-house/index.html">Enter Abominable House (12¹²)</a>
        <a class="cta-btn ghost" href="#system">Explore unified system ↓</a>
      </div>
    </div>
  </section>

  <!-- SECTION 1: UNIFIED SYSTEM ARCHITECTURE -->
  <section class="wrap" id="system">
    <div class="sec-kicker">Unified System Architecture · Words to World</div>
    <div class="sec-head">
      <h2>From one flour sack to 8,916,100,448,256 films</h2>
      <p class="sec-note">Disney's 1930s flour-sack acting test scaled across four experimental rungs into a complete anticombinatorial cinema and actuarial engine after Italo Calvino's 1973 <em>“The Burning of the Abominable House.”</em></p>
    </div>

    <div class="rungs-grid">
      <article class="rung-card">
        <div>
          <div class="rung-num">Rung I · 1 Flour Sack</div>
          <h3 class="rung-title">PAE-03 · Flour Sacks &amp; The Flour Tower</h3>
          <p class="rung-desc">Six independent SCION swarms build a single half-filled sack on a shared 32-second score with zero tween libraries, conserving volume and surviving 17 blind visual critic rounds.</p>
        </div>
        <div>
          <div class="rung-stat">6 swarms · 10 acting beats · 17 critic logs</div>
          <div class="rung-links">
            <a class="mini-cta" href="./paeleo/flour-sacks/index.html">Flour Sacks →</a>
            <a class="mini-cta" href="./paeleo/flour-tower/index.html">PAE-03 Tower →</a>
            <a class="mini-cta" href="./docs/pae03-critic-all.html">17 Critics</a>
          </div>
        </div>
      </article>

      <article class="rung-card">
        <div>
          <div class="rung-num">Rung II · 2 Flour Sacks</div>
          <h3 class="rung-title">VTX-0.1 · Lamp-Room Counterfactual</h3>
          <p class="rung-desc">Two faceless sacks, one kerosene lamp, and a <strong>1-line goal patch</strong> (<code>assist_neighbor</code> vs. <code>knock_over_lamp</code>). Frame-locked through <code>f=77</code>; persistent door trace flips policy payout.</p>
        </div>
        <div>
          <div class="rung-stat">77 shared frames · 0.00px carry err · blinded gate</div>
          <div class="rung-links">
            <a class="mini-cta" href="./vtx01_build/viewer/index.html">VTX-0.1 Viewer →</a>
            <a class="mini-cta" href="#compare">Compare A/B ↓</a>
            <a class="mini-cta" href="./docs/vtx01-mvvt-memo-and-spec.html">Spec</a>
          </div>
        </div>
      </article>

      <article class="rung-card main-rung">
        <div>
          <div class="rung-num">Rung III · 4 Sacks · Main System</div>
          <h3 class="rung-title">PAE-04 · The Abominable House</h3>
          <p class="rung-desc">Roessler, Belindo, Inigo, and Ogiva across 12 alphabetical deeds: <strong>41 atomic JS modules</strong> (12 deeds, 12 consequences, 13 transitions, 4 memories) addressing every film in base 12.</p>
        </div>
        <div>
          <div class="rung-stat">12¹² = 8.92T films · 6,030 Six Memos Atlas</div>
          <div class="rung-links">
            <a class="mini-cta" href="./paeleo/abominable-house/index.html">Main Case →</a>
            <a class="mini-cta" href="./paeleo/abominable-house/live/film.html">Film Bank →</a>
            <a class="mini-cta" href="./paeleo/abominable-house/whole-house.html">Whole House</a>
          </div>
        </div>
      </article>

      <article class="rung-card">
        <div>
          <div class="rung-num">Rung IV · 4 Sacks + Observer / Insurer</div>
          <h3 class="rung-title">Lab 7 (27–29) &amp; Skiller's Policies</h3>
          <p class="rung-desc">BDI vs. Symbolic agent reasoning (<em>Occupied</em>), candle vs. light-switch focalization (<em>By What Light</em>), and exact DP pricing of Skiller's four insurance riders (<em>The Policies</em>).</p>
        </div>
        <div>
          <div class="rung-stat">−4.6 pp Widow Life confound · 524,880 lit histories</div>
          <div class="rung-links">
            <a class="mini-cta" href="./paeleo/abominable-house/live/policies.html">Policies →</a>
            <a class="mini-cta" href="./paeleo/abominable-house/live/numbers.html">Numbers →</a>
            <a class="mini-cta" href="./lab7/index.html">Lab 7 Trio</a>
          </div>
        </div>
      </article>
    </div>

    <div class="arch-diagram" aria-label="Interactive system map">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-family:var(--mono);font-size:11px;color:var(--muted);">
        <span>SYSTEM DATAFLOW · CLICK ANY NODE TO OPEN ITS LIVE ENGINE OR EDITION</span>
        <span>PEO: PROMPT → EKPHRASIS → OPERATION</span>
      </div>
      <svg viewBox="0 0 1120 250" role="img" aria-label="Architecture diagram connecting PAE-03, VTX-0.1, PAE-04, Lab 7, Policies, and Reading Room">
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="currentColor" />
          </marker>
        </defs>
        <g stroke="currentColor" stroke-opacity="0.45" stroke-width="1.5" fill="none" marker-end="url(#arr)">
          <path d="M 200 72 L 248 72" />
          <path d="M 200 178 L 248 178" />
          <path d="M 442 72 L 492 108" />
          <path d="M 442 178 L 492 142" />
          <path d="M 718 105 L 770 68" />
          <path d="M 718 125 L 770 125" />
          <path d="M 718 145 L 770 185" />
          <path d="M 940 68 L 976 105" />
          <path d="M 940 125 L 976 125" />
          <path d="M 940 185 L 976 145" />
        </g>

        <a href="./paeleo/flour-sacks/index.html" class="arch-node">
          <rect x="14" y="34" width="186" height="76" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="26" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">1 SACK · PAE-03</text>
          <text x="26" y="76" font-family="Newsreader, Georgia, serif" font-size="16" font-weight="600" fill="currentColor">Flour Sacks &amp; Tower</text>
          <text x="26" y="95" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.75">6 swarms · 17 critic rounds</text>
        </a>

        <a href="./vtx01_build/viewer/index.html" class="arch-node">
          <rect x="14" y="140" width="186" height="76" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="26" y="161" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">2 SACKS · VTX-0.1</text>
          <text x="26" y="182" font-family="Newsreader, Georgia, serif" font-size="16" font-weight="600" fill="currentColor">Lamp-Room Patch</text>
          <text x="26" y="201" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.75">1-line diff · door trace</text>
        </a>

        <a href="./paeleo/abominable-house/live/abom.html" class="arch-node">
          <rect x="252" y="34" width="190" height="76" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="264" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">ATOMIC VIDEOTEXT BANK</text>
          <text x="264" y="76" font-family="Newsreader, Georgia, serif" font-size="16" font-weight="600" fill="currentColor">41 JS Scene Modules</text>
          <text x="264" y="95" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.75">12 deeds · conseq · memory</text>
        </a>

        <a href="./lab7/index.html" class="arch-node">
          <rect x="252" y="140" width="190" height="76" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="264" y="161" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">LAB 7 · FILMS 27–29</text>
          <text x="264" y="182" font-family="Newsreader, Georgia, serif" font-size="16" font-weight="600" fill="currentColor">Agents &amp; Focalization</text>
          <text x="264" y="201" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.75">BDI 0.52 · By What Light</text>
        </a>

        <a href="./paeleo/abominable-house/index.html" class="arch-node">
          <rect x="496" y="68" width="222" height="114" rx="4" fill="var(--bg)" stroke="var(--accent)" stroke-width="2.5" />
          <text x="512" y="92" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="600" fill="var(--accent)">MAIN HUB · PAE-04</text>
          <text x="512" y="118" font-family="Newsreader, Georgia, serif" font-size="20" font-weight="600" fill="currentColor">The Abominable House</text>
          <text x="512" y="140" font-family="JetBrains Mono, monospace" font-size="11" fill="currentColor">12¹² = 8,916,100,448,256</text>
          <text x="512" y="160" font-family="JetBrains Mono, monospace" font-size="10.5" fill="currentColor" opacity="0.75">R · B · I · O + T ZERO + Atlas</text>
        </a>

        <a href="./paeleo/abominable-house/live/film.html" class="arch-node">
          <rect x="774" y="32" width="166" height="62" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="786" y="53" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">WATCH REGISTER</text>
          <text x="786" y="74" font-family="Newsreader, Georgia, serif" font-size="15.5" font-weight="600" fill="currentColor">Film Bank &amp; Array</text>
        </a>

        <a href="./paeleo/abominable-house/live/numbers.html" class="arch-node">
          <rect x="774" y="98" width="166" height="56" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="786" y="118" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">ANTICOMBINATORICS</text>
          <text x="786" y="138" font-family="Newsreader, Georgia, serif" font-size="15.5" font-weight="600" fill="currentColor">The Numbers Sieve</text>
        </a>

        <a href="./paeleo/abominable-house/live/policies.html" class="arch-node">
          <rect x="774" y="160" width="166" height="62" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="786" y="181" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">SKILLER'S LEDGER</text>
          <text x="786" y="202" font-family="Newsreader, Georgia, serif" font-size="15.5" font-weight="600" fill="currentColor">The Policies (DP)</text>
        </a>

        <a href="./docs/index.html" class="arch-node">
          <rect x="980" y="76" width="128" height="98" rx="3" fill="var(--bg)" stroke="currentColor" stroke-width="1.5" />
          <text x="992" y="99" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.7">READ REGISTER</text>
          <text x="992" y="121" font-family="Newsreader, Georgia, serif" font-size="16" font-weight="600" fill="currentColor">Reading Room</text>
          <text x="992" y="140" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.78">33 Web Docs</text>
          <text x="992" y="156" font-family="JetBrains Mono, monospace" font-size="10" fill="currentColor" opacity="0.78">82 Zettels</text>
        </a>
      </svg>
    </div>
  </section>

  <!-- SECTION 2: VISUALIZED INSIGHTS -->
  <section class="wrap" id="insights">
    <div class="sec-kicker">Visualized System Insights · Sieves, Actuaries &amp; Critics</div>
    <div class="sec-head">
      <h2>What the numbers, policies &amp; critics prove</h2>
      <p class="sec-note">Interactive explorers for the two core mathematical discoveries in <code>PAE-04</code>—the combinatorial sieve from <code>10³⁶</code> to <code>0</code> and Skiller's <code>−4.6 pp</code> insurance confound—plus agent and critic telemetry.</p>
    </div>

    <div class="insights-grid">
      <!-- Insight A: Log-Scale Sieve Explorer -->
      <div class="insight-box">
        <h3>1. The Anticombinatorial Sieve (Log₁₀ Scale)</h3>
        <p class="insight-sub">Click any constraint tier to inspect its exact integer, mathematical rule, and live verification page.</p>
        <div class="sieve-list" id="sieveList"></div>
        <div class="sieve-detail" id="sieveDetail"></div>
      </div>

      <!-- Insight B: Interactive Actuarial Policy Simulator -->
      <div class="insight-box">
        <h3>2. Skiller's Four Policies · Live Confound Simulator</h3>
        <p class="insight-sub">Toggle narrative plausibility rules, arsonist pool, tour clause, and planted-notebook probability to watch payouts shift.</p>

        <div class="pol-controls">
          <button type="button" class="pol-btn active" id="polRule5" onclick="setPolState('five', true)">Film's 5 Rules (2.66T)</button>
          <button type="button" class="pol-btn" id="polRule0" onclick="setPolState('five', false)">Unconstrained (12¹²)</button>
          <button type="button" class="pol-btn" id="polSkiller" onclick="setPolState('skiller', 'toggle')">+ Skiller 1/5 Arsonist</button>
          <button type="button" class="pol-btn" id="polWider" onclick="setPolState('wider', 'toggle')">Wider Tour Clause</button>
        </div>

        <div style="display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:11.5px;margin-bottom:8px;">
          <label for="plantedSlider">Planted copybook weight:</label>
          <input type="range" id="plantedSlider" min="0" max="50" value="0" oninput="setPolState('planted', this.value)" style="flex:1;" />
          <span id="plantedVal">0%</span>
        </div>

        <div class="pol-bars" id="polBars"></div>

        <div class="sieve-detail" id="polNote"></div>
      </div>
    </div>

    <!-- Insight C: Agent Reasoning & Critic Telemetry -->
    <div class="metrics-strip">
      <div class="metric-card">
        <div class="sec-kicker">Lab 7 · 28 · The House Is Occupied</div>
        <h4>Agent Reasoning Coherence</h4>
        <p style="font-size:14.5px;color:var(--ink-body);margin:0 0 12px;">Holding room geometry fixed while swapping only how tenants choose actions:</p>
        <div style="font-family:var(--mono);font-size:11.5px;display:flex;flex-direction:column;gap:8px;">
          <div>
            <div style="display:flex;justify-content:space-between;"><span>BDI (Belief–Desire–Intention)</span><strong>0.52</strong></div>
            <div class="sieve-track"><div class="sieve-fill" style="width:100%;background:var(--accent);"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;"><span>Symbolic Rule Engine</span><strong>0.35</strong></div>
            <div class="sieve-track"><div class="sieve-fill" style="width:67.3%;"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;"><span>Random Walk Baseline</span><strong>0.29</strong></div>
            <div class="sieve-track"><div class="sieve-fill" style="width:55.8%;opacity:0.65;"></div></div>
          </div>
        </div>
      </div>

      <div class="metric-card">
        <div class="sec-kicker">PAE-03 &amp; VTX-0.1 · Self-Critical Loops</div>
        <h4>Why Independent Critics Catch Blind Spots</h4>
        <p style="font-size:14.5px;color:var(--ink-body);margin:0 0 10px;">Generator assertions (<code>PAE_CHECK</code>) passed while visual frames failed—caught only by fresh-context frame inspection:</p>
        <ul style="margin:0;padding-left:18px;font-size:14.5px;line-height:1.48;color:var(--ink-body);">
          <li><strong>SCION 06 (R1 → R3):</strong> Top-heavy heart silhouette &amp; 1-frame stipple flicker repaired into pooled flour sack (<a href="./docs/pae03-critic-06-r1.html">read R1</a>).</li>
          <li><strong>SCION 08 (R1 → R3):</strong> Flipbook registration drift repaired by Round 2 (<a href="./docs/pae03-critic-08-r1.html">read R1</a>).</li>
          <li><strong>VTX-0.1 (Rev 1 → Rev 2):</strong> <code>163 px</code> lamp miss &amp; <code>f=324</code> bow-tie self-intersection repaired to <code>0.00</code> drift.</li>
        </ul>
      </div>

      <div class="metric-card">
        <div class="sec-kicker">DH2025 Philological Collision</div>
        <h4>The Exact 27 : 25 Prime Lock</h4>
        <p style="font-size:14.5px;color:var(--ink-body);margin:0 0 10px;">Pierazzo's genetic edition of <em>Il Capitolo dei Frati</em> counts <code>8,255,648,563,200</code> variants against PAE-04's <code>8,916,100,448,256</code>:</p>
        <div style="font-family:var(--mono);font-size:12px;background:var(--bg);padding:10px;border:1px solid var(--rule);">
          PAE-04: 2²⁴ · 3¹² = 8,916,100,448,256<br/>
          Pierazzo: 2²⁴ · 3⁹ · 5² = 8,255,648,563,200<br/>
          Ratio: 3³ / 5² = <strong>27 : 25 (1.08×)</strong>
        </div>
        <div style="margin-top:8px;"><a class="mini-cta" href="./docs/zettle-past.html#house-what-the-count-counts">Read Zettel Card 01 →</a></div>
      </div>
    </div>
  </section>

  <!-- SECTION 3: VISUAL SYSTEM WORKBENCH & LIVE PREVIEW STAGE -->
  <section class="wrap" id="pages">
    <div class="sec-kicker">Visual System Workbench · 14 Interactive Rooms</div>
    <div class="sec-head">
      <h2>Inspect every live page &amp; engine</h2>
      <p class="sec-note">Preview any live canvas film, combinatorial calculator, classroom piece, or reading room directly on the stage below, or launch it full-screen.</p>
    </div>

    <div class="stage-shell">
      <div class="stage-bar">
        <div>
          <strong id="stageTitle">PAE-04 · The Abominable House</strong>
          <span id="stageUrlLabel" style="color:var(--muted);margin-left:8px;">./paeleo/abominable-house/index.html</span>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <a class="mini-cta" id="stageOpenLink" href="./paeleo/abominable-house/index.html" target="_blank" rel="noopener">Open full screen ↗</a>
        </div>
      </div>
      <iframe class="stage-frame" id="stageIframe" src="./paeleo/abominable-house/index.html" title="Live system workbench preview" loading="lazy"></iframe>
    </div>

    <div class="wb-grid">
      {"".join(wb_cards)}
    </div>
  </section>

  <!-- SECTION 4: SYNCHRONIZED COUNTERFACTUAL TAKES -->
  <section class="wrap" id="compare">
    <div class="sec-kicker">VTX-0.1 &amp; PAE-04 · Counterfactual Screenings</div>
    <div class="sec-head">
      <h2>Compare takes</h2>
      <p class="sec-note">Two 16-second flour-sack takes from one world state. Identical through frame 77; a single root goal patch changes approach, lamp contact, and the persistent door trace.</p>
    </div>

    <div class="takes-bar">
      <div class="takes-controls">
        <button type="button" class="pill active" id="btnRev2" onclick="setTakeRev('rev2')">Accepted pair (Rev 2)</button>
        <button type="button" class="pill" id="btnRev1" onclick="setTakeRev('rev1')">Critic-rejected pair (Rev 1)</button>
      </div>
      <div class="takes-controls">
        <button type="button" class="pill" onclick="syncPlay(true)">Play both</button>
        <button type="button" class="pill" onclick="syncPlay(false)">Pause</button>
        <button type="button" class="pill" onclick="syncRestart()">Frame 0</button>
        <a class="pill" href="./vtx01_build/viewer/index.html">Interactive diff &amp; blinded gate →</a>
      </div>
    </div>

    <div class="takes-grid">
      <figure class="take-figure">
        <video id="vidA" controls playsinline preload="metadata" poster="./vtx01_build/revisions/rev2_accepted/inspection_sheet_case_a_rev2_accepted.png">
          <source id="srcA" src="./vtx01_build/revisions/rev2_accepted/case_a_rev2_accepted.mp4" type="video/mp4" />
        </video>
        <figcaption class="take-cap">
          <span id="capA">Take A · Steady reach, accidental brush, door propped from inside</span>
          <span class="mono" id="metaA">384f · 0.00 vol drift</span>
        </figcaption>
      </figure>

      <figure class="take-figure">
        <video id="vidB" controls playsinline preload="metadata" poster="./vtx01_build/revisions/rev2_accepted/inspection_sheet_case_b_rev2_accepted.png">
          <source id="srcB" src="./vtx01_build/revisions/rev2_accepted/case_b_rev2_accepted.mp4" type="video/mp4" />
        </video>
        <figcaption class="take-cap">
          <span id="capB">Take B · Single-line patch: deliberate strike, door wedged from hall</span>
          <span class="mono" id="metaB">46 paths · 0.00px carry err</span>
        </figcaption>
      </figure>
    </div>
  </section>

  <!-- SECTION 5: STYLED WEB MARKDOWN LIBRARY -->
  <section class="wrap" id="reading">
    <div class="sec-kicker">Editorial Reading Room · 33 Web-Typeset Markdown Editions</div>
    <div class="sec-head">
      <h2>Read the papers, Zettelkasten &amp; specs on the web</h2>
      <p class="sec-note">Every <code>.md</code> document in this repository now compiles into a book-grade HTML reading edition with four reading plates (<em>Paper, Notebook, Ochre, Night</em>), sticky table of contents, live Zettel card search, cross-linked <code>[[wiki-links]]</code>, formatted tables, and math.</p>
    </div>

    <div style="margin-bottom:18px;display:flex;flex-wrap:wrap;gap:10px;">
      <a class="cta-btn" style="font-size:16px;padding:9px 20px;" href="./docs/index.html">Open Full Reading Room (All 34 Editions) →</a>
      <a class="pill" href="./find.html">Find (Search Claims, Cards &amp; Citations) →</a>
      <a class="pill" href="./docs/claims.html">Claims Checked (14 Claims) →</a>
      <a class="pill" href="./docs/zettle-past.html">Abominable House Zettels (zettle-past) →</a>
      <a class="pill" href="./docs/zettle.html">Master Zettelkasten (28 Cards) →</a>
    </div>

    <div class="doc-shelf-grid">
      {"".join(featured_cards)}
    </div>
  </section>

  <!-- SECTION 6: VISUAL PLATES & COMPLETE REPOSITORY ARCHIVE -->
  <section class="wrap" id="archive">
    <div class="sec-kicker">Complete Archive · Plates, Films, Modules &amp; Sources</div>
    <div class="sec-head">
      <h2>Archive &amp; complete file manifest</h2>
      <p class="sec-note"><span id="totalCount">0</span> repository files indexed across <code>PAE-04</code>, <code>PAE-03</code>, <code>Flour Sacks</code>, <code>Lab 7</code>, <code>VTX-0.1</code>, and the <code>Reading Room</code>. Every Markdown file opens in its styled web edition.</p>
    </div>

    <div class="plates-grid" id="platesGrid"></div>

    <div class="filter-bar">
      <div class="cat-tabs" id="catTabs"></div>
      <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
        <button type="button" class="pill" onclick="togglePlate()" id="archiveModeBtn">Switch to Ochre mode</button>
        <input type="search" class="search-input" id="fileSearch" placeholder="Filter all files…" aria-label="Filter files" oninput="renderManifest()" />
      </div>
    </div>

    <div style="overflow-x:auto;">
      <table class="manifest-table">
        <thead>
          <tr>
            <th style="width:36%;">File</th>
            <th style="width:43%;">Description</th>
            <th style="width:13%;">Group</th>
            <th style="width:8%;">Size</th>
          </tr>
        </thead>
        <tbody id="manifestBody"></tbody>
      </table>
    </div>
  </section>

  <footer>
    <span>burning-house · Flour Sacks, PAE-03, VTX-0.1, PAE-04 (12¹²) &amp; Lab 7</span>
    <span>
      <a href="#top">Top</a> ·
      <a href="./paeleo/abominable-house/index.html">Abominable House</a> ·
      <a href="./paeleo/flour-sacks/index.html">Flour Sacks</a> ·
      <a href="./docs/index.html">Reading Room</a> ·
      <a href="https://github.com/hartswf0/burning-house">GitHub</a>
    </span>
  </footer>

  <!-- Code / JSON Inspector Drawer -->
  <div class="drawer-backdrop" id="drawerBackdrop" onclick="if(event.target===this)closeDrawer()">
    <div class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawerTitle">
      <div class="drawer-head">
        <span class="drawer-title" id="drawerTitle">file</span>
        <div style="display:flex; gap:8px; align-items:center;">
          <a class="pill" id="drawerRawLink" href="#" target="_blank" rel="noopener" style="font-size:13px; padding:4px 10px;">Open raw</a>
          <button type="button" class="pill" onclick="closeDrawer()" style="font-size:13px; padding:4px 10px;">Close</button>
        </div>
      </div>
      <div class="drawer-body"><pre id="drawerPre">Loading…</pre></div>
    </div>
  </div>

  <script>
    const PLATES = {json.dumps(VISUAL_PLATES, indent=2)};
    const WORKBENCH = {json.dumps(WORKBENCH_PAGES, indent=2)};
    const MANIFEST = {json.dumps(manifest_rows, indent=2)};
    const EXTERNAL_SOURCES = [
      {{
        path: "BoA_DH2025.pdf (Zenodo source)",
        url: "https://doi.org/10.5281/zenodo.19494802",
        styledUrl: "./docs/dh2025-concrete-papers.html",
        size: "507.4 MB",
        ext: "DOI",
        cat: "Zettels & Sources",
        desc: "Full DH2025 Lisbon Book of Abstracts source volume (38.1 MB extracted 19-paper packet & styled web edition hosted directly in repo).",
        inlineCode: false
      }}
    ];

    // ── Theme Switcher (Paper #fdf8f2 <-> Ochre #d78410) ──
    function syncPlateUI(p) {{
      document.querySelectorAll('[data-mode-btn]').forEach(btn => {{
        const active = btn.getAttribute('data-mode-btn') === p;
        btn.classList.toggle('active', active);
      }});
      const archBtn = document.getElementById('archiveModeBtn');
      if (archBtn) archBtn.textContent = p === 'paper' ? 'Switch to Ochre mode' : 'Switch to Paper mode';
      const meta = document.getElementById('themeColorMeta');
      if (meta) meta.setAttribute('content', p === 'ochre' ? '#d78410' : '#fdf8f2');
    }}

    function setPlate(mode) {{
      const p = mode === 'ochre' ? 'ochre' : 'paper';
      document.documentElement.setAttribute('data-plate', p);
      syncPlateUI(p);
      try {{ localStorage.setItem('bh_plate', p); }} catch (e) {{}}
      if (window.history && window.history.replaceState) {{
        try {{
          const u = new URL(window.location.href);
          if (p === 'ochre') u.searchParams.set('plate', 'ochre');
          else u.searchParams.delete('plate');
          window.history.replaceState(null, '', u.pathname + u.search + u.hash);
        }} catch (e) {{}}
      }}
    }}
    function togglePlate() {{
      setPlate(document.documentElement.getAttribute('data-plate') === 'paper' ? 'ochre' : 'paper');
    }}
    syncPlateUI(document.documentElement.getAttribute('data-plate') === 'ochre' ? 'ochre' : 'paper');

    // ── Insight 1: Combinatorial Sieve Explorer ──
    const SIEVE_TIERS = [
      {{ label: "By What Light · Open World", count: "5.46 × 10³⁶", log: 36.74, main: false, formula: "(12 pairs × rooms × light)^12", note: "Unconstrained spatial + lighting + deed assignment space in Lab 7 · 29 (By What Light).", link: "./lab7/by-what-light/index.html" }},
      {{ label: "By What Light · Legal Room Histories", count: "3.79 × 10²⁴", log: 24.58, main: false, formula: "3.79 × 10²⁴ histories", note: "Surviving histories once co-presence and room-transition legality are enforced before focalization.", link: "./lab7/by-what-light/index.html" }},
      {{ label: "PAE-04 · Raw Film Bank (12¹²)", count: "8,916,100,448,256", log: 12.95, main: true, formula: "12¹² = 2²⁴ · 3¹²", note: "Every ordered pair of 4 tenants (12 directed pairs) assigned independently across Calvino's 12 alphabetical deeds. Every film is addressable and playable in the Film Bank.", link: "./paeleo/abominable-house/live/film.html" }},
      {{ label: "Calvino 1973 · Hand-Multiplied Slip", count: "8,874,296,672,256", log: 12.948, main: false, formula: "12⁶ × (12⁶ − 14,000)", note: "Exact diagnosis of Calvino's 1973 prose figure: squaring 12⁶ = 2,985,984 by hand dropped 14,000 in the second factor.", link: "./paeleo/abominable-house/live/numbers.html" }},
      {{ label: "Ledger · Objective Consistency", count: "3,316,025,558,016", log: 12.52, main: false, formula: "37.19% of 12¹²", note: "Eliminates stories where a dead or immobilized tenant acts later in the sequence.", link: "./paeleo/abominable-house/live/numbers.html" }},
      {{ label: "PAE-04 · Film's Five Rules (DP Exact)", count: "2,663,172,255,744", log: 12.425, main: true, formula: "29.87% of 12¹² · 28-state quotient", note: "Enforces dead-cannot-act (#4, #6, #12), suicide (#3) kills victim, bound (#7) immobilized, 4-pair cap, and asymmetric partition—the exact denominator of Skiller's Policies.", link: "./paeleo/abominable-house/live/policies.html" }},
      {{ label: "Balanced 3-Done / 3-Suffered Symmetry", count: "5,112,676,800", log: 9.71, main: false, formula: "5.11B (vs. Pair-Once 12! = 479,001,600)", note: "Requiring each tenant to perform 3 deeds and suffer 3 deeds yields 5.11B; requiring each directed pair once gives 12! = 479M.", link: "./docs/zettle-past.html#house-what-the-count-counts" }},
      {{ label: "By What Light · Candle/Switch Sieve", count: "524,880", log: 5.72, main: false, formula: "524,880 observable stories", note: "Adding candle vs. switch visibility and unrepeatable deeds collapses trillions to half a million.", link: "./lab7/by-what-light/index.html" }},
      {{ label: "CP-SAT · Waldemar's 11/16 Notebook Clues", count: "0 (Unsatisfiable)", log: 0.4, main: true, formula: "UNSAT at >11 of 16 clues", note: "Constraint solver proof that no story satisfies more than 11 of Roessler's 16 notebook clues simultaneously—proving the surviving index is itself suspect.", link: "./paeleo/abominable-house/live/numbers.html" }}
    ];

    function selectSieve(idx) {{
      const maxLog = 37;
      document.getElementById('sieveList').innerHTML = SIEVE_TIERS.map((t, i) => {{
        const w = Math.max(2, (t.log / maxLog) * 100).toFixed(1);
        return `<button type="button" class="sieve-row ${{i === idx ? 'active' : ''}} ${{t.main ? 'main-bar' : ''}}" onclick="selectSieve(${{i}})">
          <div class="sieve-row-top"><span>${{t.label}}</span><strong>${{t.count}}</strong></div>
          <div class="sieve-track"><div class="sieve-fill" style="width:${{w}}%;"></div></div>
        </button>`;
      }}).join('');
      const cur = SIEVE_TIERS[idx];
      document.getElementById('sieveDetail').innerHTML =
        `<strong>${{cur.label}}</strong> · <code>${{cur.formula}}</code><br/>${{cur.note}} ` +
        `<a href="${{cur.link}}" style="color:var(--ink);font-family:var(--mono);font-size:11.5px;">Verify live →</a>`;
    }}
    selectSieve(2);

    // ── Insight 2: Live Actuarial Policy Simulator ──
    const polState = {{ five: true, skiller: false, wider: false, planted: 0 }};

    function setPolState(key, val) {{
      if (key === 'five') polState.five = val;
      else if (key === 'skiller') polState.skiller = !polState.skiller;
      else if (key === 'wider') polState.wider = !polState.wider;
      else if (key === 'planted') polState.planted = Number(val) || 0;

      document.getElementById('polRule5').classList.toggle('active', polState.five);
      document.getElementById('polRule0').classList.toggle('active', !polState.five);
      document.getElementById('polSkiller').classList.toggle('active', polState.skiller);
      document.getElementById('polWider').classList.toggle('active', polState.wider);
      document.getElementById('plantedVal').textContent = polState.planted + '%';
      renderPolicies();
    }}

    function renderPolicies() {{
      const p = polState.planted / 100;
      const fireBase = polState.skiller ? 80.0 : 75.0;
      const wigsBase = polState.skiller ? 80.0 : 75.0;
      const widowBase = polState.five ? 79.4 : 84.0;
      const tourBase = polState.wider ? (polState.five ? 70.0 : 75.0) : (polState.five ? 91.7 : 91.7);

      // Blend toward 50% uninformative prior if copybook is planted with weight p
      const blend = v => ((1 - p) * v + p * 50.0);
      const rows = [
        {{ name: "Inigo · Fire Cover", val: blend(fireBase), ref: 75.0, confound: false, tag: polState.skiller ? "80.0% w/ Skiller 1/5" : "3/4 non-Inigo arson" }},
        {{ name: "Widow · Life on Ogiva", val: blend(widowBase), ref: 84.0, confound: polState.five, tag: polState.five ? "84.0% → 79.4% (−4.6 pp confound)" : "84.0% unconstrained baseline" }},
        {{ name: "Ogiva · 100 Wigs", val: blend(wigsBase), ref: 75.0, confound: false, tag: polState.skiller ? "80.0% w/ Skiller 1/5" : "Mirrors non-policyholder arson" }},
        {{ name: "Widow · Belindo Tour", val: blend(tourBase), ref: 91.7, confound: polState.wider, tag: polState.wider ? "70.0% under wider clause" : "91.7% narrow clause" }}
      ];

      document.getElementById('polBars').innerHTML = rows.map(r => `
        <div>
          <div class="pol-item-top">
            <span><strong>${{r.name}}</strong></span>
            <span><strong>${{r.val.toFixed(1)}}%</strong> <span style="color:var(--muted);">[${{r.tag}}]</span></span>
          </div>
          <div class="pol-track">
            <div class="pol-fill ${{r.confound ? 'confound' : ''}}" style="width:${{r.val.toFixed(1)}}%;"></div>
            <div class="pol-ref-tick" style="left:${{r.ref}}%;" title="Baseline ${{r.ref}}%"></div>
          </div>
        </div>
      `).join('');

      document.getElementById('polNote').innerHTML =
        `<strong>Actuarial takeaway:</strong> Imposing “neutral” narrative plausibility rules (<em>Five Rules</em>) silently lowers Skiller's expected payout on Widow Roessler's life policy by <strong>4.6 percentage points</strong> (<code>84.0% → 79.4%</code>). ` +
        `<a href="./paeleo/abominable-house/live/policies.html" style="color:var(--ink);font-family:var(--mono);font-size:11.5px;">Open full DP engine →</a>`;
    }}
    renderPolicies();

    // ── Section 3: Workbench Preview Stage ──
    function loadStage(id) {{
      const item = WORKBENCH.find(w => w.id === id);
      if (!item) return;
      document.getElementById('stageTitle').textContent = item.title;
      document.getElementById('stageUrlLabel').textContent = item.url;
      document.getElementById('stageOpenLink').href = item.url;
      document.getElementById('stageIframe').src = item.url;
      document.querySelectorAll('[data-wb-card]').forEach(el => {{
        el.classList.toggle('active', el.getAttribute('data-wb-card') === id);
      }});
      document.getElementById('pages').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}

    // ── Section 4: Synchronized VTX-0.1 Takes ──
    const vidA = document.getElementById('vidA');
    const vidB = document.getElementById('vidB');
    function syncPlay(play) {{
      if (play) {{
        const t = Math.min(vidA.currentTime || 0, vidB.currentTime || 0);
        vidA.currentTime = t; vidB.currentTime = t;
        vidA.play(); vidB.play();
      }} else {{
        vidA.pause(); vidB.pause();
      }}
    }}
    function syncRestart() {{
      vidA.pause(); vidB.pause();
      vidA.currentTime = 0; vidB.currentTime = 0;
    }}
    function setTakeRev(rev) {{
      const isRev2 = rev === 'rev2';
      document.getElementById('btnRev2').classList.toggle('active', isRev2);
      document.getElementById('btnRev1').classList.toggle('active', !isRev2);
      if (isRev2) {{
        vidA.poster = './vtx01_build/revisions/rev2_accepted/inspection_sheet_case_a_rev2_accepted.png';
        vidB.poster = './vtx01_build/revisions/rev2_accepted/inspection_sheet_case_b_rev2_accepted.png';
        document.getElementById('srcA').src = './vtx01_build/revisions/rev2_accepted/case_a_rev2_accepted.mp4';
        document.getElementById('srcB').src = './vtx01_build/revisions/rev2_accepted/case_b_rev2_accepted.mp4';
        document.getElementById('capA').textContent = 'Take A · Steady reach, accidental brush, door propped from inside';
        document.getElementById('capB').textContent = 'Take B · Single-line patch: deliberate strike, door wedged from hall';
        document.getElementById('metaA').textContent = '384f · 0.00 vol drift';
        document.getElementById('metaB').textContent = '46 paths · 0.00px carry err';
      }} else {{
        vidA.poster = './vtx01_build/revisions/rev1_rejected/inspection_sheet_case_a_rev1_rejected.png';
        vidB.poster = './vtx01_build/revisions/rev1_rejected/inspection_sheet_case_b_rev1_rejected.png';
        document.getElementById('srcA').src = './vtx01_build/revisions/rev1_rejected/case_a_rev1_rejected.mp4';
        document.getElementById('srcB').src = './vtx01_build/revisions/rev1_rejected/case_b_rev1_rejected.mp4';
        document.getElementById('capA').textContent = 'Rejected Take A (Rev 1) · Leaping sack misses lamp by 163 px';
        document.getElementById('capB').textContent = 'Rejected Take B (Rev 1) · Ear corners cross spine into bow-tie at f=324';
        document.getElementById('metaA').textContent = 'FAIL · 163px lamp gap';
        document.getElementById('metaB').textContent = 'FAIL · 37% area loss';
      }}
      vidA.load(); vidB.load();
    }}

    // ── Section 6: Plates & Complete Manifest ──
    document.getElementById('platesGrid').innerHTML = PLATES.map(p => `
      <a class="plate-card" href="${{p.href}}">
        <div class="plate-thumb"><img src="${{p.img}}" alt="${{p.title}}" loading="lazy" /></div>
        <div class="plate-meta">
          <div class="plate-group">${{p.group}}</div>
          <div class="plate-title">${{p.title}}</div>
          <div class="plate-path">${{p.meta}}</div>
        </div>
      </a>
    `).join('');

    const ALL_ROWS = MANIFEST.concat(EXTERNAL_SOURCES);
    document.getElementById('totalCount').textContent = MANIFEST.length;
    const CATS = ['All', 'Interactive', 'Papers & Notes', 'Zettels & Sources', 'Films & Plates', 'Cases, Traces & Code', 'Bundles'];
    let activeCat = 'All';

    function setCat(c) {{
      activeCat = c;
      renderTabs();
      renderManifest();
    }}

    function renderTabs() {{
      document.getElementById('catTabs').innerHTML = CATS.map(c => {{
        const n = c === 'All' ? ALL_ROWS.length : ALL_ROWS.filter(r => r.cat === c).length;
        return `<button type="button" class="pill ${{activeCat === c ? 'active' : ''}}" onclick="setCat('${{c.replace(/'/g, "\\\\'")}}')">${{c}} (${{n}})</button>`;
      }}).join('');
    }}

    function renderManifest() {{
      const q = (document.getElementById('fileSearch').value || '').trim().toLowerCase();
      const rows = ALL_ROWS.filter(r => {{
        if (activeCat !== 'All' && r.cat !== activeCat) return false;
        if (!q) return true;
        return r.path.toLowerCase().includes(q) || r.desc.toLowerCase().includes(q) || r.cat.toLowerCase().includes(q);
      }});
      document.getElementById('manifestBody').innerHTML = rows.map(r => {{
        let actionBtn = '';
        if (r.styledUrl) {{
          actionBtn = `<a class="read-btn" href="${{r.styledUrl}}">Read Web</a>`;
        }} else if (r.inlineCode) {{
          actionBtn = `<button type="button" class="read-btn" onclick="openDrawer('${{r.url}}', '${{r.path.replace(/'/g, "\\\\'")}}')">Inspect</button>`;
        }}
        const primaryHref = r.styledUrl ? r.styledUrl : r.url;
        const rawSuffix = r.styledUrl ? ` <a href="${{r.url}}" style="font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-left:4px;">[raw]</a>` : '';
        return `<tr>
          <td>${{actionBtn}}<a class="file-link" href="${{primaryHref}}">${{r.path}}</a>${{rawSuffix}}</td>
          <td class="file-desc">${{r.desc}}</td>
          <td class="file-cat">${{r.cat}}</td>
          <td class="file-size">${{r.size}}</td>
        </tr>`;
      }}).join('');
    }}

    async function openDrawer(url, path) {{
      document.getElementById('drawerTitle').textContent = path;
      document.getElementById('drawerRawLink').href = url;
      document.getElementById('drawerPre').textContent = 'Loading ' + path + '…';
      document.getElementById('drawerBackdrop').classList.add('open');
      try {{
        const res = await fetch(url);
        const txt = await res.text();
        document.getElementById('drawerPre').textContent = txt;
      }} catch (err) {{
        document.getElementById('drawerPre').textContent = 'Open directly via "Open raw" above (' + err.message + ').';
      }}
    }}
    function closeDrawer() {{ document.getElementById('drawerBackdrop').classList.remove('open'); }}
    window.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeDrawer(); }});

    renderTabs();
    renderManifest();
  </script>
</body>
</html>
"""


def main():
    out_index = os.path.join(ROOT, "index.html")
    # Pass 1: collect manifest and write index.html
    rows = collect_manifest()
    with open(out_index, "w", encoding="utf-8") as f:
        f.write(build_html(rows))
    # Pass 2: re-collect so index.html's own exact byte size is recorded
    rows = collect_manifest()
    with open(out_index, "w", encoding="utf-8") as f:
        f.write(build_html(rows))
    print(f"Built unified index.html with {len(rows)} tracked repository files.")


if __name__ == "__main__":
    main()
