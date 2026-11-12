#!/usr/bin/env python3
"""
Compile all Markdown (.md) documents in burning-house into typographically styled,
searchable, cross-linked web HTML editions under docs/ + docs/index.html + docs/manifest.json.
Preserves all source .md files untouched in place.
"""
import glob
import html
import json
import math
import os
import re
import xml.etree.ElementTree as ET
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(ROOT, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

# Explicit curated metadata & slugs for root & key docs
DOC_META = {
    "Abominable_House_Submission_Draft.md": (
        "abominable-house-submission-draft",
        "Papers & Specifications",
        "Canonical Paper — Minimum Viable Video-Text: Flour Sacks, Swarms & Actuarial Anticombinatorics",
        "The canonical scholarly text for burning-house (plain edition at read.html; claims ledger at CLAIMS.md).",
    ),
    "VTX01_MVVT_Research_Memo_and_Spec.md": (
        "vtx01-mvvt-memo-and-spec",
        "Papers & Specifications",
        "Component Spec (Source) — VTX-0.1 Working Memo & Formal Specification",
        "Source specification for the two-sack VTX-0.1 benchmark (Chance, Memory, Consequence, and Take A vs. Take B).",
    ),
    "Abominable_House_Framing_Notes.md": (
        "abominable-house-framing-notes",
        "Papers & Specifications",
        "Working Source Notes — PAE-04 (The Burning of the Abominable House)",
        "Working framing source feeding the canonical submission draft (flour-sack abstraction, Scion analogy, policies, and Lem's semascope).",
    ),
    "abominable_house_mvvt_research_notes.md": (
        "words-to-world-research-notes",
        "Papers & Specifications",
        "Words to World: Anticombinatorics & Agent-Scale Video-Text",
        "Early foundational working paper on Oulipian anticombinatorics, BDI/LEGOS agents, Geertz, and reading over the machine's shoulder.",
    ),
    "pae04_abominable_house_scion_run.md": (
        "pae04-scion-run",
        "Papers & Specifications",
        "SCION v3.0 Execution — PAE-04 & The DH2025 Spine",
        "Rigorous formal verification run across 12^12 stories, Calvino's 14,000 carry slip, Pierazzo's 27:25 prime ratio, and the 28-state DP quotient.",
    ),
    "Logline_Journal_Entries_and_Existing_Assets.md": (
        "logline-journal-entries",
        "Journals & Inventories",
        "Loglines, Journal Entries 21–38 & Complete Asset Audit",
        "Three register loglines, eighteen dated lab notebook entries bridging PAE-04 to VTX-0.1, and an inventory of existing engines and proofs.",
    ),
    "CLAIMS.md": (
        "claims",
        "Papers & Specifications",
        "Claims Checked: Status, Evidence & Verification Conditions",
        "Fourteen core historical, mathematical, and empirical claims audited across the repository with status (supported, measured, open, conflicting, unsupported) and settlement criteria.",
    ),
    "zettle-past.md": (
        "zettle-past",
        "Zettelkasten Slip-Boxes",
        "Abominable House × DH2025 Methodological Zettels (9 Cards)",
        "Nine precision slip-box cards colliding PAE-04's Film Bank, ledger, and policies with DH2025 philology, network drama, sortes, and constraint theory.",
    ),
    "zettle.md": (
        "zettle",
        "Zettelkasten Slip-Boxes",
        "Master Zettelkasten: Calvino, Six Memos, Blow & Video-Text (26 Cards)",
        "Deduplicated 26-card research slip-box (26 unique IDs, 1:1) spanning Calvino's Six Memos, Jonathan Blow's Braid & The Witness, agent architectures, and formal mechanisms.",
    ),
    "xzet.md": (
        "xzet",
        "Zettelkasten Slip-Boxes",
        "Cross-Zettel Synthesis Deck (xzet)",
        "Five high-density synthesis cards colliding kinetic relays, spatial force-fields, and worldtext mechanics.",
    ),
    "DH2025_Concrete_Papers_and_Works_Cited.md": (
        "dh2025-concrete-papers",
        "Reference Corpora & Prompts",
        "Concrete Papers & Works Cited from DH2025: Book of Abstracts",
        "Full verbatim texts, page citations, thematic spine, and extracted bibliographies for all 19 concrete DH2025 reference papers.",
    ),
    "scion_mvvt_abominable_house_instruction.md": (
        "scion-mvvt-instruction",
        "Reference Corpora & Prompts",
        "Compiled SCION System Instruction & Architectural Rationale",
        "Design rationale and compiled XML contract governing evidence gates, structural/animation/perceptual gates, and counterfactual branching.",
    ),
    "p1.md": (
        "p1-scion-xml-prompt",
        "Reference Corpora & Prompts",
        "SCION v1.1 System Prompt (Source XML Specification)",
        "Structured edition of the SCION v1.1 XML instruction defining Chance, Memory, Consequence, Evidence Seeds C1–L1, and quality gates.",
    ),
    "README.md": (
        "readme",
        "Journals & Inventories",
        "Repository Overview & Architecture (README)",
        "Top-level guide to burning-house, uniting PAE-03, PAE-04, Lab 7, VTX-0.1, Zettelkasten decks, and the complete archive.",
    ),
    "vtx01_build/README.md": (
        "vtx01-build-readme",
        "Journals & Inventories",
        "VTX-0.1 Reproducible Build & Verifier Manual",
        "Step-by-step guide to reproducing Take A (assist) and Take B (arson), verifying the 1-line goal patch, and running the blinded gate.",
    ),
    "paeleo/flour-tower/BRIEF.md": (
        "pae03-brief",
        "PAE-03 Flour Tower & Critic Logs",
        "PAE-03 · The Flour Tower: Brief Every Swarm Receives",
        "Shared 32-second score, ten acting beats, volume conservation rules, and forbidden-tween contract given to all six SCION swarms.",
    ),
    "paeleo/flour-tower/process/README.md": (
        "pae03-process",
        "PAE-03 Flour Tower & Critic Logs",
        "PAE-03 · How the Cuts and Openings Were Made",
        "Production pipeline notes on headless frame capture, audio muxing, and contact-sheet inspection for The Flour Tower.",
    ),
}

SWARM_LIVE = {
    "02": ("02-reiniger.html", "02 · Reiniger Silhouette Cutout"),
    "06": ("06-whitney.html", "06 · Whitney Harmonic Dots"),
    "07": ("07-foldes.html", "07 · Foldes Drawn Metamorphosis"),
    "08": ("08-sutherland.html", "08 · Sutherland Sketchpad"),
    "14": ("14-pose2pose.html", "14 · Pose-to-Pose Pencil"),
    "41": ("41-soft-body.html", "41 · Soft-Body Continuum"),
}

ZETTEL_KEYS = [
    "ID", "TITLE", "SOURCE", "PASSAGE", "RESEARCH OBJECT", "LOCAL MOVE",
    "SOURCE TERMS", "WHAT BECAME STRANGE", "QUESTION", "DEEPER QUESTION",
    "MECHANISM", "FORMAL SHIFT", "SOURCE FORMALISM", "OUR FORMALIZATION",
    "TENSION", "MISSING", "BOUNDARY", "CITATION TRAIL", "TEST",
    "WRITE-UP", "PLATFORM", "LINKS", "BIBTEX"
]
ZETTEL_KEY_RE = re.compile(r"^(" + "|".join(re.escape(k) for k in ZETTEL_KEYS) + r"):\s*(.*)$")


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_]+", "-", s)
    return s[:72].strip("-") or "section"


def discover_md_files():
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True))
    rel_files = [os.path.relpath(f, ROOT).replace("\\", "/") for f in files]
    entries = []
    for rel in rel_files:
        if rel in DOC_META:
            slug, cat, title_override, desc = DOC_META[rel]
        else:
            m = re.match(r"paeleo/flour-tower/critic/(\d+)/round(\d+)\.md$", rel)
            if m:
                sw, rn = m.group(1), m.group(2)
                slug = f"pae03-critic-{sw}-r{rn}"
                cat = "PAE-03 Flour Tower & Critic Logs"
                _, sw_label = SWARM_LIVE.get(sw, ("", f"Swarm {sw}"))
                title_override = f"SCION {sw} · Critic Round {rn}"
                desc = f"Independent visual/kinematic critic inspection for {sw_label}, round {rn}."
            else:
                slug = slugify(rel.replace(".md", ""))
                cat = "Papers & Specifications"
                title_override = None
                desc = f"Web reading edition of {rel}."
        entries.append({
            "rel": rel,
            "slug": slug,
            "category": cat,
            "title_override": title_override,
            "desc": desc,
        })
    return entries


def parse_zettel_cards(raw_text: str):
    """Extract structured ZETTEL blocks whether wrapped in ```text fences or bare."""
    blocks = re.findall(r"```(?:text)?\s*\n(\s*ZETTEL\b.*?)```", raw_text, flags=re.S)
    if not blocks and re.search(r"^\s*ZETTEL\s*$", raw_text, flags=re.M):
        parts = re.split(r"(?=^\s*ZETTEL\s*$)", raw_text, flags=re.M)
        blocks = [p for p in parts if p.strip().startswith("ZETTEL")]

    cards = []
    for blk in blocks:
        fields = {}
        cur_key = None
        buf = []
        for line in blk.splitlines():
            if line.strip() == "ZETTEL":
                continue
            m = ZETTEL_KEY_RE.match(line.strip())
            if m:
                if cur_key:
                    fields[cur_key] = "\n".join(buf).strip()
                cur_key = m.group(1)
                first_val = m.group(2).strip()
                buf = [first_val] if first_val else []
            else:
                if cur_key is not None:
                    buf.append(line)
        if cur_key:
            fields[cur_key] = "\n".join(buf).strip()
        if fields.get("ID") or fields.get("TITLE"):
            zid = fields.get("ID", f"card-{len(cards)+1}").splitlines()[0].strip()
            fields["ID"] = zid
            cards.append(fields)
    return cards


def typeset_math_expr(expr: str, display: bool = False) -> str:
    s = expr.strip("$").strip()
    # Handle \xrightarrow{\text{...}}
    def repl_xarrow(m):
        lbl = m.group(1).replace(r"\_", "_")
        return f'<span class="math-xarrow"><span class="math-xarrow-lbl">{html.escape(lbl)}</span><span class="math-xarrow-line">───▶</span></span>'

    s = re.sub(r"\\xrightarrow\{\\text\{([^}]*)\}\}", repl_xarrow, s)
    s = re.sub(r"\\text\{([^}]*)\}", lambda m: html.escape(m.group(1).replace(r"\_", "_")), s)

    # Escape HTML outside already injected spans
    parts = re.split(r"(<span class=\"math-xarrow\">.*?</span></span>)", s)
    out = []
    for p in parts:
        if p.startswith('<span class="math-xarrow">'):
            out.append(p)
            continue
        t = html.escape(p)
        t = t.replace(r"\times", " × ").replace(r"\cdot", " · ")
        t = t.replace(r"\Rightarrow", " ⇒ ").replace(r"\rightarrow", " → ").replace(r"\to", " → ")
        t = t.replace(r"\approx", " ≈ ").replace(r"\le", " ≤ ").replace(r"\ge", " ≥ ")
        t = t.replace(r"\_", "_")
        t = re.sub(r"\^\{([^}]+)\}", r"<sup>\1</sup>", t)
        t = re.sub(r"\^([0-9a-zA-Z]+)", r"<sup>\1</sup>", t)
        t = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", t)
        t = re.sub(r"_([0-9a-zA-Z]+)", r"<sub>\1</sub>", t)
        out.append(t)
    rendered = "".join(out)
    if display:
        return f'<div class="md-math-block">{rendered}</div>'
    return f'<span class="md-math">{rendered}</span>'


def render_mermaid_block(code: str) -> str:
    """Convert flowchart LR/TD blocks into clean native responsive editorial diagrams."""
    nodes = {}
    edges = []
    for raw_line in code.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("flowchart") or line.startswith("graph"):
            continue
        for nid, lbl in re.findall(r'([A-Za-z0-9_]+)\["([^"]+)"\]', line):
            nodes[nid] = lbl
        m_edge = re.match(r'^([A-Za-z0-9_]+)(?:\["[^"]+"\])?\s*(?:--\s*"([^"]+)"\s*-->|-->)\s*([A-Za-z0-9_]+)', line)
        if m_edge:
            edges.append((m_edge.group(1), m_edge.group(2) or "", m_edge.group(3)))

    if not nodes:
        return f'<div class="md-code-wrap"><div class="md-code-bar"><span>diagram</span></div><pre><code>{html.escape(code)}</code></pre></div>'

    ordered_ids = list(nodes.keys())
    items_html = []
    for idx, nid in enumerate(ordered_ids):
        raw_lbl = nodes[nid].replace("<br/>", "\n").replace("<br>", "\n")
        lines = [html.escape(x.strip()) for x in raw_lbl.splitlines() if x.strip()]
        head = lines[0] if lines else nid
        rest = "<br>".join(lines[1:]) if len(lines) > 1 else ""
        items_html.append(f'<div class="md-flow-node"><strong>{head}</strong>{rest}</div>')
        if idx < len(ordered_ids) - 1:
            edge_lbl = ""
            for a, el, b in edges:
                if a == nid and b == ordered_ids[idx + 1] and el:
                    edge_lbl = f'<span>{html.escape(el)}</span>'
                    break
            items_html.append(f'<div class="md-flow-arrow">{edge_lbl}<span>→</span></div>')

    # List any feedback / branch edges below
    extra_edges = []
    for a, el, b in edges:
        if a in ordered_ids and b in ordered_ids and ordered_ids.index(b) != ordered_ids.index(a) + 1:
            a_name = nodes[a].split("<br")[0]
            b_name = nodes[b].split("<br")[0]
            lbl_part = f" ({html.escape(el)})" if el else ""
            extra_edges.append(f"<code>{html.escape(a_name)} → {html.escape(b_name)}</code>{lbl_part}")

    extra_html = ""
    if extra_edges:
        extra_html = '<div style="margin-top:10px;font-family:var(--font-mono);font-size:11.5px;color:var(--muted);">Feedback &amp; branch edges: ' + " · ".join(extra_edges) + "</div>"

    return (
        '<div class="md-flow">'
        '<div class="md-flow-kicker">Architecture Flow Diagram</div>'
        '<div class="md-flow-track">' + "".join(items_html) + "</div>"
        + extra_html +
        "</div>"
    )


def format_zettel_inline(text: str, zettel_lookup: dict, current_slug: str) -> str:
    """Render inline formatting, epistemic badges, URLs, and [[wiki-links]] inside Zettel fields."""
    if not text:
        return ""
    s = html.escape(text)

    # Epistemic stamps
    def stamp_repl(m):
        return f'<span class="z-epi">{m.group(1)}</span>'

    s = re.sub(
        r"\[(PARAPHRASE|QUOTE|OUR INFERENCE|REPRODUCED IN CODE|OUR FORMALIZATION\s*(?:—|--|-)\s*NOT SOURCE SYNTAX)\]",
        stamp_repl,
        s,
    )

    # Inline code
    code_stash = []
    def save_code(m):
        code_stash.append(f"<code>{m.group(1)}</code>")
        return f"@@ZCODE{len(code_stash)-1}@@"

    s = re.sub(r"`([^`\n]+)`", save_code, s)

    # Wiki links [[...]]
    def repl_wiki(m):
        target = html.unescape(m.group(1)).strip()
        key = target.lower()
        if key in zettel_lookup:
            doc_slug, anchor, _ = zettel_lookup[key]
            href = f"#{anchor}" if doc_slug == current_slug else f"./{doc_slug}.html#{anchor}"
            return f'<a class="wiki-link" href="{href}">⌗ {html.escape(target)}</a>'
        return f'<a class="wiki-link wiki-unresolved" href="#" data-wiki-query="{html.escape(target)}" title="Filter cards mentioning {html.escape(target)}">[[{html.escape(target)}]]</a>'

    s = re.sub(r"\[\[([^\]]+)\]\]", repl_wiki, s)

    # Bold & Italic
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)

    # Bare URLs
    s = re.sub(
        r"(?<![\"'>])(https?://[^\s<)\]]+)",
        r'<a href="\1" target="_blank" rel="noopener">\1</a>',
        s,
    )

    # Arrows
    s = s.replace("-&gt;", "→")

    for i, c in enumerate(code_stash):
        s = s.replace(f"@@ZCODE{i}@@", c)

    paras = [p.strip() for p in re.split(r"\n\s*\n", s) if p.strip()]
    out_p = []
    for p in paras:
        p_br = p.replace("\n", "<br>")
        out_p.append(f"<p>{p_br}</p>")
    return "".join(out_p)


def render_zettel_deck(cards: list, zettel_lookup: dict, current_slug: str):
    platforms = []
    for c in cards:
        raw_p = re.sub(r"^\[\[|\]\]$", "", c.get("PLATFORM", "").strip())
        if raw_p and raw_p not in platforms:
            platforms.append(raw_p)

    plat_chips = "".join(
        f'<button type="button" class="plat-chip" data-plat-filter="{html.escape(p)}">{html.escape(p)}</button>'
        for p in platforms[:18]
    )

    toolbar = f"""
    <div class="zettel-toolbar">
      <input type="search" id="zettelSearch" class="zettel-search" placeholder="Search {len(cards)} Zettel cards by ID, claim, author, mechanism, or [[link]]…" aria-label="Search Zettel cards" />
      <span class="zettel-count-badge" id="zettelCount">{len(cards)} / {len(cards)} cards</span>
      {f'<div class="zettel-plat-bar">{plat_chips}</div>' if plat_chips else ''}
    </div>
    """

    toc_items = []
    card_htmls = []
    total = len(cards)

    for idx, c in enumerate(cards, 1):
        zid = c.get("ID", f"card-{idx}")
        anchor = slugify(zid)
        title = c.get("TITLE", zid)
        raw_plat = re.sub(r"^\[\[|\]\]$", "", c.get("PLATFORM", "").strip())
        toc_items.append((2, anchor, title, zid))

        parts = []
        if c.get("SOURCE"):
            parts.append(f'<div class="z-field"><span class="z-label">Source</span><div class="z-val">{format_zettel_inline(c["SOURCE"], zettel_lookup, current_slug)}</div></div>')

        if c.get("SOURCE TERMS"):
            terms = [t.strip() for t in re.split(r"[;,]|//", c["SOURCE TERMS"]) if t.strip()]
            chips = "".join(f'<span class="z-term">{html.escape(t)}</span>' for t in terms)
            parts.append(f'<div class="z-field"><span class="z-label">Source Terms</span><div class="z-terms">{chips}</div></div>')

        if c.get("PASSAGE"):
            parts.append(f'<div class="z-field z-box"><span class="z-label">Passage &amp; Witness</span><div class="z-val">{format_zettel_inline(c["PASSAGE"], zettel_lookup, current_slug)}</div></div>')

        # 2-col inquiry grid
        grid1 = []
        for k, lbl in [("RESEARCH OBJECT", "Research Object"), ("LOCAL MOVE", "Local Move"), ("QUESTION", "Question"), ("DEEPER QUESTION", "Deeper Question")]:
            if c.get(k):
                grid1.append(f'<div class="z-box"><span class="z-label">{lbl}</span><div class="z-val">{format_zettel_inline(c[k], zettel_lookup, current_slug)}</div></div>')
        if grid1:
            parts.append(f'<div class="z-grid-2">{"".join(grid1)}</div>')

        if c.get("WHAT BECAME STRANGE"):
            parts.append(f'<div class="z-field z-box z-strange"><span class="z-label">What Became Strange</span><div class="z-val">{format_zettel_inline(c["WHAT BECAME STRANGE"], zettel_lookup, current_slug)}</div></div>')

        for k, lbl in [("MECHANISM", "Mechanism"), ("FORMAL SHIFT", "Formal Shift"), ("SOURCE FORMALISM", "Source Formalism"), ("OUR FORMALIZATION", "Our Formalization")]:
            if c.get(k):
                cls = "z-box z-formal" if k in ("FORMAL SHIFT", "OUR FORMALIZATION") else "z-box"
                parts.append(f'<div class="z-field {cls}"><span class="z-label">{lbl}</span><div class="z-val">{format_zettel_inline(c[k], zettel_lookup, current_slug)}</div></div>')

        grid2 = []
        for k, lbl in [("TENSION", "Tension"), ("MISSING", "Missing"), ("BOUNDARY", "Boundary"), ("TEST", "Verification Test")]:
            if c.get(k):
                grid2.append(f'<div class="z-box"><span class="z-label">{lbl}</span><div class="z-val">{format_zettel_inline(c[k], zettel_lookup, current_slug)}</div></div>')
        if grid2:
            parts.append(f'<div class="z-grid-2">{"".join(grid2)}</div>')

        for k, lbl in [("WRITE-UP", "Draft Write-Up"), ("CITATION TRAIL", "Citation Trail"), ("LINKS", "Connected Zettels")]:
            if c.get(k):
                parts.append(f'<div class="z-field"><span class="z-label">{lbl}</span><div class="z-val">{format_zettel_inline(c[k], zettel_lookup, current_slug)}</div></div>')

        if c.get("BIBTEX"):
            bib = c["BIBTEX"].strip()
            entry_cnt = len(re.findall(r"@\w+\s*\{", bib)) or 1
            parts.append(
                f'<details class="z-bib"><summary>BibTeX ({entry_cnt} {"entry" if entry_cnt == 1 else "entries"}) · click to expand</summary>'
                f'<div style="padding:6px 12px 0;text-align:right;"><button type="button" class="code-copy-btn" data-copy-code>Copy BibTeX</button></div>'
                f'<pre>{html.escape(bib)}</pre></details>'
            )

        plat_badge = f'<span class="z-plat">{html.escape(raw_plat)}</span>' if raw_plat else ""
        card_htmls.append(f"""
        <article class="zettel-card" id="{anchor}" data-platform="{html.escape(raw_plat)}">
          <div class="z-head">
            <div class="z-id-group">
              <span class="z-num">CARD {idx:02d}/{total:02d}</span>
              <span class="z-id">{html.escape(zid)}</span>
              {plat_badge}
            </div>
            <button type="button" class="code-copy-btn" data-copy-url="{anchor}"># Copy card link</button>
          </div>
          <h2 class="z-title">{html.escape(title)}</h2>
          {"".join(parts)}
        </article>
        """)

    return toolbar + '<div class="zettel-deck">' + "".join(card_htmls) + "</div>", toc_items


def render_xml_instruction(raw_xml: str):
    """Render pure XML SCION specification (p1.md) as structured readable cards + raw XML tab."""
    toc_items = []
    cards = []
    cleaned = raw_xml.strip()
    try:
        root = ET.fromstring(cleaned)
        spec_name = root.attrib.get("name", "SCION System Instruction")
        spec_ver = root.attrib.get("version", "")
        for idx, child in enumerate(list(root), 1):
            tag = child.tag
            anchor = slugify(tag)
            nice_title = f"{idx}. " + tag.replace("_", " ").title()
            toc_items.append((2, anchor, nice_title, f"<{tag}>"))

            # Extract <source> children if any
            sources = child.findall("source")
            src_rows = []
            for s in sources:
                sid = s.attrib.get("id", "")
                href = s.attrib.get("href", "")
                desc = (s.text or "").strip()
                link_html = f'<a href="{html.escape(href)}" target="_blank" rel="noopener">{html.escape(href)}</a>' if href else ""
                src_rows.append(f"<tr><td><code>{html.escape(sid)}</code></td><td>{html.escape(desc)}<br>{link_html}</td></tr>")

            # Gather plain text paragraphs (excluding <source> tags)
            raw_inner = child.text or ""
            for sub in list(child):
                if sub.tag != "source" and sub.text:
                    raw_inner += "\n\n" + sub.text
                if sub.tail and sub.tail.strip():
                    raw_inner += "\n\n" + sub.tail

            paras_html = []
            for blk in re.split(r"\n\s*\n", raw_inner.strip()):
                lines = [l.strip() for l in blk.splitlines() if l.strip()]
                if not lines:
                    continue
                if all(l.startswith("- ") for l in lines):
                    lis = "".join(f"<li>{html.escape(l[2:])}</li>" for l in lines)
                    paras_html.append(f"<ul>{lis}</ul>")
                elif any(re.match(r"^<[^>]+>\s*\[[^\]]+\]\s*<[^>]+>$", l) for l in lines):
                    # Working olog triples!
                    rows = []
                    for l in lines:
                        if l.endswith(":"):
                            rows.append(f"<p><strong>{html.escape(l)}</strong></p>")
                        else:
                            rows.append(f'<div style="font-family:var(--font-mono);font-size:12.5px;padding:4px 8px;margin:3px 0;background:var(--surface);border-left:2px solid var(--accent);">{html.escape(l)}</div>')
                    paras_html.append("".join(rows))
                else:
                    joined = " ".join(lines)
                    paras_html.append(f"<p>{html.escape(joined)}</p>")

            src_table = ""
            if src_rows:
                src_table = (
                    '<div class="md-table-wrap"><table><thead><tr><th>Seed</th><th>Source &amp; Verification Note</th></tr></thead>'
                    f'<tbody>{"".join(src_rows)}</tbody></table></div>'
                )

            cards.append(f"""
            <section class="xml-card" id="{anchor}">
              <div class="xml-card-tag">&lt;{html.escape(tag)}&gt;</div>
              <h2 style="margin-top:0;border-top:0;padding-top:0;">{html.escape(nice_title)}</h2>
              {"".join(paras_html)}
              {src_table}
            </section>
            """)
    except Exception:
        pass

    raw_pane = (
        '<div id="xmlRawPane" hidden>'
        '<div class="md-code-wrap"><div class="md-code-bar"><span>xml · source specification</span>'
        '<button type="button" class="code-copy-btn" data-copy-code>Copy XML</button></div>'
        f'<pre><code>{html.escape(cleaned)}</code></pre></div></div>'
    )
    tabs = (
        '<div class="xml-tabs">'
        '<button type="button" class="xml-tab active" data-xml-view="structured">Structured Specification</button>'
        '<button type="button" class="xml-tab" data-xml-view="raw">Raw XML Source</button>'
        "</div>"
    )
    return tabs + f'<div id="xmlStructuredPane">{"".join(cards)}</div>' + raw_pane, toc_items


def render_markdown_doc(raw_md: str, rel_to_slug: dict, src_rel_md: str = ""):
    """Render full GFM Markdown with Mermaid, native Math, GitHub Alerts, workspace link rewrites, and TOC."""
    stash = []
    def put_stash(html_fragment: str) -> str:
        stash.append(html_fragment)
        return f"\n\n@@MDSTASH{len(stash)-1}@@\n\n"

    # 1. Extract fenced code blocks first (including mermaid)
    def handle_fence(m):
        lang = (m.group(1) or "text").strip().lower()
        code = m.group(2)
        if lang == "mermaid":
            return put_stash(render_mermaid_block(code))
        return put_stash(
            f'<div class="md-code-wrap"><div class="md-code-bar"><span>{html.escape(lang)}</span>'
            f'<button type="button" class="code-copy-btn" data-copy-code>Copy</button></div>'
            f'<pre><code>{html.escape(code.rstrip())}</code></pre></div>'
        )

    text = re.sub(r"```([^\n`]*)\n(.*?)```", handle_fence, raw_md, flags=re.S)

    # 2. Protect inline `code` spans before math conversion
    inline_codes = []
    def save_inline_code(m):
        inline_codes.append(m.group(0))
        return f"@@INLCODE{len(inline_codes)-1}@@"

    text = re.sub(r"`[^`\n]+`", save_inline_code, text)

    # 3. Convert display $$...$$ and inline $...$ math (ignoring escaped \$)
    text = re.sub(r"\$\$([^$]+)\$\$", lambda m: put_stash(typeset_math_expr(m.group(0), display=True)), text)

    inline_maths = []
    def save_inline_math(m):
        inner = m.group(1)
        if not inner.strip() or inner.startswith(" ") and inner.endswith(" "):
            return m.group(0)
        inline_maths.append(typeset_math_expr(m.group(0), display=False))
        return f"@@INLMATH{len(inline_maths)-1}@@"

    text = re.sub(r"(?<!\\)\$([^$\n]{1,120}?)(?<!\\)\$", save_inline_math, text)
    text = text.replace(r"\$", "$")

    # Restore inline code before Markdown parse
    for idx, c in enumerate(inline_codes):
        text = text.replace(f"@@INLCODE{idx}@@", c)

    # 4. Rewrite workspace file:///Users/gaia/burning%20house/... links to root-relative paths
    def rewrite_ws_uri(m):
        subpath = m.group(1).strip("/")
        return os.path.relpath(os.path.join(ROOT, subpath.replace("%20", " ")), os.path.dirname(os.path.join(ROOT, src_rel_md)) if src_rel_md else ROOT).replace("\\", "/").replace(" ", "%20")

    text = re.sub(r"file:///Users/gaia/burning(?:%20|\s)house/([^\s)\"'>]+)", rewrite_ws_uri, text)

    # 5. Convert GitHub Alerts (> [!NOTE], > [!IMPORTANT], etc.)
    def convert_alerts(src: str) -> str:
        lines = src.splitlines()
        out = []
        i = 0
        while i < len(lines):
            m = re.match(r"^\s*>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", lines[i], re.I)
            if m:
                kind = m.group(1).upper()
                first_rest = m.group(2).strip()
                body_lines = [first_rest] if first_rest else []
                i += 1
                while i < len(lines) and re.match(r"^\s*>\s?", lines[i]):
                    body_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner_md = "\n".join(body_lines)
                inner_html = markdown.markdown(inner_md, extensions=["tables", "sane_lists", "smarty"])
                out.append(put_stash(
                    f'<aside class="md-alert alert-{kind.lower()}">'
                    f'<span class="md-alert-title">{kind}</span>{inner_html}</aside>'
                ))
            else:
                out.append(lines[i])
                i += 1
        return "\n".join(out)

    text = convert_alerts(text)

    # 6. Run Python-Markdown
    md = markdown.Markdown(extensions=["tables", "sane_lists", "smarty"])
    body_html = md.convert(text)

    # Restore stashed blocks and inline math
    for idx, frag in enumerate(stash):
        body_html = body_html.replace(f"<p>@@MDSTASH{idx}@@</p>", frag)
        body_html = body_html.replace(f"@@MDSTASH{idx}@@", frag)
    for idx, mfrag in enumerate(inline_maths):
        body_html = body_html.replace(f"@@INLMATH{idx}@@", mfrag)

    # 7. Wrap tables in .md-table-wrap
    body_html = body_html.replace("<table>", '<div class="md-table-wrap"><table>').replace("</table>", "</table></div>")

    # 8. Add heading IDs + anchor links & collect TOC
    toc_items = []
    used_ids = set()

    def enrich_heading(m):
        lvl = int(m.group(1))
        inner = m.group(2)
        plain = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        base = slugify(plain)
        hid = base
        n = 2
        while hid in used_ids:
            hid = f"{base}-{n}"
            n += 1
        used_ids.add(hid)
        if lvl in (2, 3, 4):
            toc_items.append((lvl, hid, plain, ""))
        anchor_link = f'<a class="h-anchor" href="#{hid}" aria-label="Link to section">#</a>' if lvl >= 2 else ""
        return f'<h{lvl} id="{hid}">{inner}{anchor_link}</h{lvl}>'

    body_html = re.sub(r"<h([1-4])>(.*?)</h\1>", enrich_heading, body_html, flags=re.S)

    # 9. Rewrite internal relative href/src paths (resolved from src_rel_md's folder into docs/)
    src_dir = os.path.dirname(os.path.join(ROOT, src_rel_md)) if src_rel_md else ROOT

    def rewrite_attr(m):
        attr, val = m.group(1), m.group(2).strip()
        if not val or val.startswith(("#", "http://", "https://", "mailto:", "data:", "javascript:")):
            return m.group(0)
        hash_part = ""
        if "#" in val:
            val_path, h = val.split("#", 1)
            hash_part = "#" + h
        else:
            val_path = val
        if not val_path:
            return m.group(0)
        unq = val_path.replace("%20", " ")
        abs_target = os.path.normpath(os.path.join(src_dir, unq))
        repo_rel = os.path.relpath(abs_target, ROOT).replace("\\", "/")
        if repo_rel == "BoA_DH2025.pdf":
            return f'{attr}="https://doi.org/10.5281/zenodo.19494802"'
        if repo_rel == "vtx01_build":
            return f'{attr}="./vtx01-build-readme.html{hash_part}"'
        if repo_rel == "docs/index.html":
            return f'{attr}="./index.html{hash_part}"'
        if repo_rel in rel_to_slug:
            # Keep #hash only if not a raw #L12-L34 line-number fragment
            keep_h = "" if re.match(r"^#L\d+", hash_part) else hash_part
            return f'{attr}="./{rel_to_slug[repo_rel]}.html{keep_h}"'
        rel_from_docs = os.path.relpath(abs_target, DOCS_DIR).replace("\\", "/").replace(" ", "%20")
        if not rel_from_docs.startswith("."):
            rel_from_docs = "./" + rel_from_docs
        return f'{attr}="{rel_from_docs}{hash_part}"'

    body_html = re.sub(r'\b(href|src)="([^"]+)"', rewrite_attr, body_html)

    return body_html, toc_items


def page_shell(
    *,
    title: str,
    subtitle: str,
    category: str,
    rel_md: str,
    words: int,
    read_mins: int,
    unit_label: str,
    toc_items: list,
    body_html: str,
    prev_doc: dict | None,
    next_doc: dict | None,
    extra_banner: str = "",
):
    raw_href = "../" + rel_md.replace(" ", "%20") if rel_md else ""
    toc_lis = []
    for lvl, hid, label, zid in toc_items:
        z_span = f'<span class="toc-zid">{html.escape(zid)}</span>' if zid else ""
        toc_lis.append(
            f'<li class="toc-item lvl-{lvl}"><a href="#{hid}">{z_span}{html.escape(label)}</a></li>'
        )
    toc_html = "\n".join(toc_lis) if toc_lis else '<li class="toc-item"><a href="#top">Top of document</a></li>'

    pager_parts = []
    if prev_doc:
        pager_parts.append(
            f'<a class="pager-card" href="./{prev_doc["slug"]}.html">'
            f'<div class="pager-dir">← Previous Document</div>'
            f'<div class="pager-title">{html.escape(prev_doc["title"])}</div></a>'
        )
    if next_doc:
        pager_parts.append(
            f'<a class="pager-card" href="./{next_doc["slug"]}.html">'
            f'<div class="pager-dir">Next Document →</div>'
            f'<div class="pager-title">{html.escape(next_doc["title"])}</div></a>'
        )
    pager_html = f'<nav class="doc-pager" aria-label="Document pagination">{"".join(pager_parts)}</nav>' if pager_parts else ""

    raw_btn = f'<a class="doc-act-btn" href="{raw_href}">Raw .md</a>' if raw_href else ""
    sub_html = f'<p class="doc-subtitle">{html.escape(subtitle)}</p>' if subtitle else ""

    return f"""<!DOCTYPE html>
<html lang="en" data-plate="paper" data-size="md" data-width="book">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} — burning-house</title>
  <meta name="description" content="{html.escape(subtitle or title)}" />
  <link rel="icon" type="image/svg+xml" href="../favicon.svg" />
  <link rel="icon" type="image/png" sizes="64x64" href="../assets/favicon-64.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png" />
  <link rel="shortcut icon" href="../favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png" />
  <script>
    (function () {{
      try {{
        var qp = new URLSearchParams(location.search).get('plate');
        var p = qp || localStorage.getItem('bh_doc_plate') || localStorage.getItem('bh_plate') || 'paper';
        if (['paper','notebook','ochre','night'].indexOf(p) !== -1) document.documentElement.setAttribute('data-plate', p);
        var s = localStorage.getItem('bh_doc_size') || 'md';
        if (['sm','md','lg'].indexOf(s) !== -1) document.documentElement.setAttribute('data-size', s);
        var w = localStorage.getItem('bh_doc_width') || 'book';
        if (['book','wide'].indexOf(w) !== -1) document.documentElement.setAttribute('data-width', w);
      }} catch (e) {{}}
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IM+Fell+English:ital@0;1&family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./reader.css" />
</head>
<body id="top">
  <div class="read-progress" id="readProgress"></div>

  <header class="reader-topbar">
    <div class="topbar-left">
      <button type="button" class="crumb-link mob-toc-btn" id="mobTocBtn">☰ Contents</button>
      <a class="brand-pill" href="../index.html">burning-house</a>
      <span class="crumb-sep">/</span>
      <a class="crumb-link" href="./index.html">Reading Room</a>
      <a class="crumb-link" href="../paeleo/abominable-house/index.html">PAE-04</a>
    </div>
    <div class="topbar-right">
      <div class="ctrl-group" role="group" aria-label="Reading theme">
        <button type="button" class="ctrl-btn active" data-set-plate="paper">Paper</button>
        <button type="button" class="ctrl-btn" data-set-plate="notebook">Notebook</button>
        <button type="button" class="ctrl-btn" data-set-plate="ochre">Ochre</button>
        <button type="button" class="ctrl-btn" data-set-plate="night">Night</button>
      </div>
      <div class="ctrl-group" role="group" aria-label="Font size">
        <button type="button" class="ctrl-btn" data-set-size="sm">A−</button>
        <button type="button" class="ctrl-btn active" data-set-size="md">A</button>
        <button type="button" class="ctrl-btn" data-set-size="lg">A+</button>
      </div>
      <div class="ctrl-group" role="group" aria-label="Column width and plain prose">
        <button type="button" class="ctrl-btn active" data-set-width="book">Book</button>
        <button type="button" class="ctrl-btn" data-set-width="wide">Wide</button>
        <button type="button" class="ctrl-btn" data-toggle-plain="1" title="Strip inline bold and code styling for continuous plain reading">Plain</button>
      </div>
    </div>
  </header>

  <div class="reader-shell">
    <aside class="reader-rail" id="readerRail" aria-label="Table of contents">
      <div class="rail-meta-box">
        <div class="rail-kicker">{html.escape(category)}</div>
        <div class="rail-stats">
          <span>{words:,} words</span>
          <span>· ~{read_mins} min read</span>
          <span>· {html.escape(unit_label)}</span>
        </div>
      </div>
      <input type="search" id="tocFilter" class="toc-filter" placeholder="Filter contents…" aria-label="Filter table of contents" />
      <div class="toc-heading">Contents</div>
      <ul class="toc-list">
        {toc_html}
      </ul>
    </aside>

    <main class="reader-main">
      <header class="doc-header">
        <div class="doc-kicker">{html.escape(category)} · {html.escape(rel_md or "Anthology")}</div>
        <h1 class="doc-title">{html.escape(title)}</h1>
        {sub_html}
        <div class="doc-byline">
          <span>{words:,} words · ~{read_mins} min read · {html.escape(unit_label)}</span>
          <div class="doc-actions">
            <button type="button" class="doc-act-btn" data-copy-url="">Copy URL</button>
            <button type="button" class="doc-act-btn" onclick="window.print()">Print / PDF</button>
            {raw_btn}
          </div>
        </div>
      </header>

      {extra_banner}

      <div class="md-prose">
        {body_html}
      </div>

      {pager_html}
    </main>
  </div>

  <script src="./reader.js"></script>
</body>
</html>
"""


def main():
    entries = discover_md_files()
    rel_to_slug = {e["rel"]: e["slug"] for e in entries}

    # Pre-scan all Zettel decks to build cross-file Zettel ID lookup
    zettel_lookup = {}
    parsed_zettels = {}
    for e in entries:
        raw = open(os.path.join(ROOT, e["rel"]), encoding="utf-8", errors="ignore").read()
        cards = parse_zettel_cards(raw)
        if cards:
            parsed_zettels[e["rel"]] = cards
            for c in cards:
                zid = c.get("ID", "")
                if zid:
                    zettel_lookup[zid.lower()] = (e["slug"], slugify(zid), c.get("TITLE", zid))

    # Enrich each entry with extracted title, word count, etc.
    for e in entries:
        raw = open(os.path.join(ROOT, e["rel"]), encoding="utf-8", errors="ignore").read()
        e["raw"] = raw
        words = len(re.findall(r"\S+", raw))
        e["words"] = words
        e["read_mins"] = max(1, round(words / 230))
        if e["title_override"]:
            e["title"] = e["title_override"]
        else:
            m_h1 = re.search(r"^#\s+(.+)$", raw, flags=re.M)
            e["title"] = re.sub(r"[`*_]", "", m_h1.group(1)).strip() if m_h1 else e["rel"]

    # Sort entries cleanly by category order for Prev/Next navigation
    cat_order = {
        "Papers & Specifications": 0,
        "Journals & Inventories": 1,
        "Zettelkasten Slip-Boxes": 2,
        "Reference Corpora & Prompts": 3,
        "PAE-03 Flour Tower & Critic Logs": 4,
    }
    entries.sort(key=lambda x: (cat_order.get(x["category"], 9), x["rel"]))

    manifest = {}

    for idx, e in enumerate(entries):
        raw = e["raw"]
        rel = e["rel"]
        slug = e["slug"]
        prev_doc = entries[idx - 1] if idx > 0 else None
        next_doc = entries[idx + 1] if idx + 1 < len(entries) else None

        extra_banner = ""
        if rel in parsed_zettels:
            cards = parsed_zettels[rel]
            body_html, toc_items = render_zettel_deck(cards, zettel_lookup, slug)
            unit_label = f"{len(cards)} Zettel cards"
        elif raw.lstrip().startswith("<?xml") or raw.lstrip().startswith("<scion_system_instruction"):
            body_html, toc_items = render_xml_instruction(raw)
            unit_label = f"{len(toc_items)} XML modules"
        else:
            # Check if this is a PAE-03 critic round
            m_crit = re.match(r"paeleo/flour-tower/critic/(\d+)/round(\d+)\.md$", rel)
            raw_for_md = raw
            if m_crit:
                sw, rn = m_crit.group(1), m_crit.group(2)
                # Bold rubric paragraph leads like "Method.", "Choices.", "Verdict:"
                raw_for_md = re.sub(
                    r"^(Method\.|The world[^.]*\.|Choices\.|Does it read as a flour sack in every frame\?|Mood[^.]*\.|Craft defects\.|PAE_CHECK[^.]*\.|Verdict:)",
                    r"**\1**",
                    raw_for_md,
                    flags=re.M,
                )
                first_line = raw.splitlines()[0] if raw.splitlines() else ""
                if "DOES NOT PASS" in first_line:
                    v_cls, v_txt = "verdict-fail", "DOES NOT PASS (NARROWLY)"
                elif "narrow" in first_line.lower():
                    v_cls, v_txt = "verdict-narrow", "PASS (NARROW)"
                else:
                    v_cls, v_txt = "verdict-pass", "PASS"
                live_file, sw_label = SWARM_LIVE.get(sw, ("", f"Swarm {sw}"))
                round_links = []
                for r_i in (1, 2, 3):
                    cand = f"paeleo/flour-tower/critic/{sw}/round{r_i}.md"
                    if cand in rel_to_slug:
                        act = ' style="background:var(--btn-bg);color:var(--btn-fg);"' if str(r_i) == rn else ""
                        round_links.append(f'<a class="doc-act-btn"{act} href="./{rel_to_slug[cand]}.html">Round {r_i}</a>')
                round_links.append('<a class="doc-act-btn" href="./pae03-critic-all.html">All 17 Rounds</a>')
                if live_file:
                    round_links.append(f'<a class="doc-act-btn" href="../paeleo/flour-tower/films/{live_file}">Open Live Swarm ↗</a>')
                extra_banner = (
                    f'<div class="critic-banner">'
                    f'<div><span class="verdict-stamp {v_cls}">{v_txt}</span>'
                    f'<span style="margin-left:10px;font-family:var(--font-mono);font-size:12px;">{html.escape(sw_label)}</span></div>'
                    f'<div class="doc-actions">{"".join(round_links)}</div></div>'
                )

            body_html, toc_items = render_markdown_doc(raw_for_md, rel_to_slug, rel)
            unit_label = f"{max(1, len(toc_items))} sections"

        out_path = os.path.join(DOCS_DIR, f"{slug}.html")
        html_page = page_shell(
            title=e["title"],
            subtitle=e["desc"],
            category=e["category"],
            rel_md=rel,
            words=e["words"],
            read_mins=e["read_mins"],
            unit_label=unit_label,
            toc_items=toc_items,
            body_html=body_html,
            prev_doc=prev_doc,
            next_doc=next_doc,
            extra_banner=extra_banner,
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_page)

        e["unit_label"] = unit_label
        manifest[rel] = {
            "slug": slug,
            "html": f"docs/{slug}.html",
            "title": e["title"],
            "category": e["category"],
            "desc": e["desc"],
            "words": e["words"],
            "read_mins": e["read_mins"],
            "units": unit_label,
        }

    # Also build docs/pae03-critic-all.html (All 17 Critic Rounds Anthology)
    crit_entries = [e for e in entries if e["rel"].startswith("paeleo/flour-tower/critic/")]
    anth_parts = []
    anth_toc = []
    anth_words = sum(e["words"] for e in crit_entries)
    for e in crit_entries:
        m_crit = re.match(r"paeleo/flour-tower/critic/(\d+)/round(\d+)\.md$", e["rel"])
        sw, rn = m_crit.group(1), m_crit.group(2)
        hid = f"swarm-{sw}-round-{rn}"
        first_line = e["raw"].splitlines()[0].lstrip("# ").strip()
        anth_toc.append((2, hid, first_line, f"SCION {sw} · R{rn}"))
        raw_mod = re.sub(r"^#\s+.+$", "", e["raw"], count=1, flags=re.M).strip()
        raw_mod = re.sub(
            r"^(Method\.|The world[^.]*\.|Choices\.|Does it read as a flour sack in every frame\?|Mood[^.]*\.|Craft defects\.|PAE_CHECK[^.]*\.|Verdict:)",
            r"**\1**",
            raw_mod,
            flags=re.M,
        )
        b_html, _ = render_markdown_doc(raw_mod, rel_to_slug, e["rel"])
        live_file, sw_label = SWARM_LIVE.get(sw, ("", f"Swarm {sw}"))
        anth_parts.append(
            f'<section style="margin-bottom:42px;"><h2 id="{hid}">{html.escape(first_line)}</h2>'
            f'<p style="font-family:var(--font-mono);font-size:11.5px;color:var(--muted);">'
            f'{html.escape(sw_label)} · <a href="../paeleo/flour-tower/films/{live_file}">Live film ↗</a> · '
            f'<a href="./{e["slug"]}.html">Standalone round page</a> · <a href="../{e["rel"]}">Raw .md</a></p>'
            f'{b_html}</section>'
        )

    with open(os.path.join(DOCS_DIR, "pae03-critic-all.html"), "w", encoding="utf-8") as f:
        f.write(page_shell(
            title="PAE-03 · All 17 Independent Critic Rounds (Complete Anthology)",
            subtitle="Every visual and kinematic critique across all six SCION flour-sack swarms (02, 06, 07, 08, 14, 41), rounds 1 through 3.",
            category="PAE-03 Flour Tower & Critic Logs",
            rel_md="",
            words=anth_words,
            read_mins=max(1, round(anth_words / 230)),
            unit_label="17 critic rounds",
            toc_items=anth_toc,
            body_html="".join(anth_parts),
            prev_doc=entries[-1],
            next_doc=entries[0],
        ))

    # Build docs/index.html (The Reading Room)
    grouped = {}
    for e in entries:
        grouped.setdefault(e["category"], []).append(e)

    total_words = sum(e["words"] for e in entries)
    sections_html = []
    for cat in sorted(grouped.keys(), key=lambda c: cat_order.get(c, 9)):
        cards = []
        if cat == "PAE-03 Flour Tower & Critic Logs":
            cards.append(f"""
            <a class="room-card" href="./pae03-critic-all.html">
              <div>
                <div class="room-card-cat">Complete Anthology · 6 Swarms</div>
                <h3 class="room-card-title">All 17 Independent Critic Rounds (02–41)</h3>
                <p class="room-card-desc">Read all 17 blind critic inspections and repair conditions across Swarms 02, 06, 07, 08, 14, and 41 in one continuous scroll.</p>
              </div>
              <div class="room-card-foot">
                <span>{anth_words:,} words · ~{max(1, round(anth_words/230))} min</span>
                <span>17 rounds →</span>
              </div>
            </a>
            """)
        for e in grouped[cat]:
            cards.append(f"""
            <a class="room-card" href="./{e["slug"]}.html">
              <div>
                <div class="room-card-cat">{html.escape(e["rel"])}</div>
                <h3 class="room-card-title">{html.escape(e["title"])}</h3>
                <p class="room-card-desc">{html.escape(e["desc"])}</p>
              </div>
              <div class="room-card-foot">
                <span>{e["words"]:,} words · ~{e["read_mins"]} min</span>
                <span>{html.escape(e["unit_label"])} →</span>
              </div>
            </a>
            """)
        sections_html.append(
            f'<h2 style="font-family:var(--font-display);font-size:26px;margin:32px 0 8px;padding-top:14px;border-top:2px solid var(--ink);">{html.escape(cat)}</h2>'
            f'<div class="room-grid">{"".join(cards)}</div>'
        )

    room_page = f"""<!DOCTYPE html>
<html lang="en" data-plate="paper">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Reading Room — All Styled Markdown Editions · burning-house</title>
  <meta name="description" content="Web-typeset scholarly editions for all 33 Markdown documents, Zettelkasten decks, SCION specifications, and critic logs in burning-house." />
  <link rel="icon" type="image/svg+xml" href="../favicon.svg" />
  <link rel="icon" type="image/png" sizes="64x64" href="../assets/favicon-64.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png" />
  <link rel="shortcut icon" href="../favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png" />
  <script>
    (function () {{
      try {{
        var p = new URLSearchParams(location.search).get('plate') || localStorage.getItem('bh_doc_plate') || localStorage.getItem('bh_plate') || 'paper';
        if (['paper','notebook','ochre','night'].indexOf(p) !== -1) document.documentElement.setAttribute('data-plate', p);
      }} catch (e) {{}}
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IM+Fell+English:ital@0;1&family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./reader.css" />
</head>
<body>
  <header class="reader-topbar">
    <div class="topbar-left">
      <a class="brand-pill" href="../index.html">burning-house</a>
      <span class="crumb-sep">/</span>
      <span style="font-weight:600;">Reading Room ({len(entries)} Styled Editions)</span>
      <a class="crumb-link" href="../paeleo/abominable-house/index.html">PAE-04 Case</a>
      <a class="crumb-link" href="../paeleo/flour-sacks/index.html">Flour Sacks</a>
    </div>
    <div class="topbar-right">
      <div class="ctrl-group" role="group" aria-label="Reading theme">
        <button type="button" class="ctrl-btn active" data-set-plate="paper">Paper</button>
        <button type="button" class="ctrl-btn" data-set-plate="notebook">Notebook</button>
        <button type="button" class="ctrl-btn" data-set-plate="ochre">Ochre</button>
        <button type="button" class="ctrl-btn" data-set-plate="night">Night</button>
      </div>
    </div>
  </header>

  <main class="room-wrap">
    <header class="doc-header" style="max-width:none;">
      <div class="doc-kicker">Editorial Reading Room · Web-Typeset Markdown Library</div>
      <h1 class="doc-title" style="max-width:26ch;">Every note, paper, Zettel deck &amp; critic round, formatted for reading.</h1>
      <p class="doc-subtitle">All {len(entries)} Markdown documents in the repository ({total_words:,} words total, including 82 cross-linked Zettelkasten cards, SCION XML specifications, DH2025 primary papers, and 17 swarm critic logs) with four reading plates, sticky contents, live search, and raw <code>.md</code> source links.</p>
      <div style="margin-top:16px;max-width:520px;">
        <input type="search" id="roomSearch" class="zettel-search" style="width:100%;" placeholder="Filter {len(entries)} documents by title, filename, or topic…" aria-label="Filter documents" />
      </div>
    </header>
    {"".join(sections_html)}
  </main>

  <script src="./reader.js"></script>
</body>
</html>
"""
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(room_page)

    with open(os.path.join(DOCS_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Built {len(entries)} styled document pages + pae03-critic-all.html + docs/index.html ({total_words:,} total words)")


if __name__ == "__main__":
    main()
