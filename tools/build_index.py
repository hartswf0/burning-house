#!/usr/bin/env python3
"""Build the finding aids for this repository. Standard library only.

  python3 tools/build_index.py            rebuild data/index.js, read.html, CLAIMS.md
  python3 tools/build_index.py --dedupe   also rewrite zettle.md without repeated identical cards

Reads: zettle.md, Abominable_House_Journal_38/index.html, the long markdown
documents, tools/claims.json, and the tracked file list.
"""
import collections, hashlib, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CANON = 'Abominable_House_Submission_Draft.md'
DOCS = [
    (CANON, 'Submission draft', 'the paper'),
    ('Abominable_House_Framing_Notes.md', 'Framing notes', 'source for the paper'),
    ('VTX01_MVVT_Research_Memo_and_Spec.md', 'VTX-0.1 memo and spec', 'source for the paper'),
    ('Logline_Journal_Entries_and_Existing_Assets.md', 'Loglines, entries 21–38, existing assets', 'working notes'),
    ('abominable_house_mvvt_research_notes.md', 'MVVT research notes', 'working notes'),
    ('pae04_abominable_house_scion_run.md', 'PAE-04 SCION run', 'process record'),
    ('scion_mvvt_abominable_house_instruction.md', 'SCION instruction for MVVT', 'process record'),
    ('DH2025_Concrete_Papers_and_Works_Cited.md', 'DH2025 papers and works cited', 'reference'),
    ('p1.md', 'p1', 'working notes'),
    ('xzet.md', 'xzet', 'working notes'),
]

def read(p):
    with open(p, encoding='utf8') as f:
        return f.read()

def plain(s):
    """Markdown emphasis and code marks removed; text kept."""
    s = re.sub(r'\[\[([^\]]+)\]\]', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    s = s.replace('`', '')
    return s

def label(s):
    return re.sub(r'\s+', ' ', plain(s).replace('*', '')).strip()

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', plain(s).lower()).strip('-')[:70]

# ---------------------------------------------------------------- cards
def cards():
    src = read('zettle.md')
    blocks = re.split(r'(?m)^ZETTEL[ \t]*$', src)
    seen, out, order = {}, [], []
    for b in blocks[1:]:
        m = re.search(r'ID:\s*\n\s*(ZTL-[A-Z0-9-]+)', b)
        if not m:
            continue
        cid = m.group(1)
        norm = re.sub(r'\s+', ' ', b).strip('` \n')
        h = hashlib.md5(norm.encode()).hexdigest()
        key = (cid, h)
        if key in seen:
            seen[key]['copies'] += 1
            continue
        fields = collections.OrderedDict()
        cur = None
        for line in b.strip('`\n ').split('\n'):
            fm = re.match(r'^([A-Z][A-Z /&\-]{1,40}):\s*$', line)
            if fm:
                cur = fm.group(1); fields[cur] = []
            elif cur:
                fields[cur].append(line)
        f = {k: plain('\n'.join(v).strip()) for k, v in fields.items() if k != 'ID'}
        c = {'id': cid, 'short': short(cid), 'title': f.pop('TITLE', ''), 'fields': f,
             'copies': 1, 'words': len(norm.split()), 'raw': b}
        seen[key] = c; out.append(c)
    # mark variants of one ID
    n = collections.Counter(c['id'] for c in out)
    v = collections.Counter()
    for c in out:
        if n[c['id']] > 1:
            v[c['id']] += 1; c['variant'] = v[c['id']]
    return out, len(blocks) - 1

def short(cid):
    m = re.search(r'-(\d{4}-\d{2})$', cid)
    return m.group(1) if m else cid.rsplit('-', 1)[-1]

def dedupe(cs):
    body = ''.join('ZETTEL' + c['raw'] for c in cs)
    if not body.lstrip().startswith('```'):
        body = '```text\n' + body
    with open('zettle.md', 'w', encoding='utf8') as f:
        f.write(body)

# ---------------------------------------------------------------- journal entries
def entries():
    p = 'Abominable_House_Journal_38/index.html'
    s = read(p)
    out = []
    for m in re.finditer(r'<article class="en" id="(e\d+)">(.*?)</article>', s, flags=re.S):
        a = m.group(2)
        def txt(x):
            return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
        h = re.search(r'<h3>(.*?)</h3>', a, flags=re.S)
        mg = re.search(r'<div class="mg">(.*?)</div>', a, flags=re.S)
        kp = re.search(r'<p class="kp">(.*?)</p>', a, flags=re.S)
        tg = re.search(r'<p class="tg">(.*?)</p>', a, flags=re.S)
        un = re.search(r'<p class="un">(.*?)</p>', a, flags=re.S)
        body = re.sub(r'<figure.*?</figure>', ' ', a, flags=re.S)
        body = re.sub(r'<div class="mg">.*?</div>|<h3>.*?</h3>|<p class="(kp|tg|un)">.*?</p>', ' ', body, flags=re.S)
        out.append({'n': int(m.group(1)[1:]), 'anchor': m.group(1), 'title': txt(h.group(1)) if h else '',
                    'when': txt(mg.group(1)) if mg else '', 'text': txt(body), 'kept': txt(kp.group(1)) if kp else '',
                    'source': txt(tg.group(1)) if tg else '', 'unchecked': txt(un.group(1)) if un else '',
                    'exhibit': txt(' '.join(re.findall(r'<figure.*?</figure>', a, flags=re.S)))[:1200],
                    'href': p + '#' + m.group(1)})
    return out

# ---------------------------------------------------------------- document sections
def sections():
    out = []
    for path, name, role in DOCS:
        if not os.path.exists(path):
            continue
        lines = read(path).split('\n')
        cur = {'doc': path, 'docname': name, 'role': role, 'heading': name, 'level': 1, 'buf': []}
        used = collections.Counter()
        def close(c):
            t = plain('\n'.join(c['buf'])).strip()
            if len(t) < 40:
                return
            a = slug(c['heading']); used[a] += 1
            if used[a] > 1:
                a += '-' + str(used[a])
            cap = 1800 if c['doc'].startswith('DH2025') else 9000
            out.append({'doc': c['doc'], 'docname': c['docname'], 'role': c['role'], 'heading': label(c['heading']),
                        'anchor': a, 'text': re.sub(r'\s+', ' ', t)[:cap],
                        'href': ('read.html#' + a) if c['doc'] == CANON else c['doc']})
        fence = False
        for ln in lines:
            if ln.startswith('```'):
                fence = not fence
            m = None if fence else re.match(r'^(#{1,3})\s+(.*)$', ln)
            if m:
                close(cur)
                cur = {'doc': path, 'docname': name, 'role': role, 'heading': m.group(2), 'level': len(m.group(1)), 'buf': []}
            else:
                cur['buf'].append(ln)
        close(cur)
    return out

# ---------------------------------------------------------------- files
def files():
    try:
        names = subprocess.check_output(['git', 'ls-files'], text=True).split('\n')
    except Exception:
        names = []
    out = []
    for n in names:
        if not n or not os.path.exists(n):
            continue
        ext = n.rsplit('.', 1)[-1].lower() if '.' in n else ''
        kind = ('page' if ext == 'html' else 'film' if ext in ('mp4', 'webm') else 'image' if ext in ('jpg', 'png', 'svg', 'ico')
                else 'data' if ext == 'json' else 'code' if ext in ('js', 'py') else 'text' if ext in ('md', 'txt') else 'document')
        out.append({'path': n, 'size': os.path.getsize(n), 'kind': kind})
    return out

# ---------------------------------------------------------------- reading edition
def reading_edition():
    src = read(CANON).split('\n')
    out, para, lst, used, toc, tbl = [], [], [], collections.Counter(), [], []
    def inline(s):
        s = html.escape(plain(s))
        s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', s)
        return s
    def flush():
        nonlocal para, lst, tbl
        if tbl:
            rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in tbl if not re.match(r'^\s*\|?[\s:|-]+\|?\s*$', r)]
            out.append('<div class="tw"><table>' + ''.join('<tr>' + ''.join(('<th>' if i == 0 else '<td>') + inline(c) + ('</th>' if i == 0 else '</td>') for c in r) + '</tr>' for i, r in enumerate(rows)) + '</table></div>'); tbl = []
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
        if lst:
            out.append('<ol>' if lst[0][0] else '<ul>')
            out.extend('<li>' + inline(t) + '</li>' for _, t in lst)
            out.append('</ol>' if lst[0][0] else '</ul>'); lst = []
    title = ''
    for ln in src:
        h = re.match(r'^(#{1,3})\s+(.*)$', ln)
        if h:
            flush(); lvl = len(h.group(1)); text = h.group(2)
            a = slug(text); used[a] += 1
            if used[a] > 1:
                a += '-' + str(used[a])
            if lvl == 1 and not title:
                title = label(text); out.append(f'<h1 id="{a}">{inline(text)}</h1>')
            else:
                out.append(f'<h{lvl} id="{a}">{inline(text)}</h{lvl}>')
                if lvl == 2:
                    toc.append((a, label(text)))
            continue
        if re.match(r'^\s*(---+|\*\*\*+)\s*$', ln):
            flush(); continue
        li = re.match(r'^\s*(\d+\.|[-*])\s+(.*)$', ln)
        if li:
            if para:
                flush()
            lst.append((li.group(1)[0].isdigit(), li.group(2))); continue
        if ln.strip().startswith('|'):
            if para or lst:
                flush()
            tbl.append(ln); continue
        if ln.startswith('>'):
            flush()
            if not re.match(r'^>\s*\[!\w+\]\s*$', ln):
                out.append('<blockquote>' + inline(ln.lstrip('> ')) + '</blockquote>')
            continue
        if not ln.strip():
            flush(); continue
        if lst and ln.startswith(' '):
            lst[-1] = (lst[-1][0], lst[-1][1] + ' ' + ln.strip())
        else:
            para.append(ln.strip())
    flush()
    nav = ''.join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in toc)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Reading Edition</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="The submission draft set for reading: one column, no bold or code marks. Generated from {CANON}.">
<link rel="icon" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
<style>
/* Layout: one reading column of about 66 characters; a contents strip that stays at the top. */
:root{{--bg:#fdf8f2;--surface:#f6efe5;--ink:#131311;--body:#28241f;--muted:#6b6156;--line:#e0d5c4;--acc:#a85f08;
 --serif:'Newsreader','Iowan Old Style','Palatino Linotype',Georgia,serif;--mono:'JetBrains Mono',ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16130f;--surface:#1f1b16;--ink:#f1e9dc;--body:#ddd3c3;--muted:#a3978a;--line:#39322a;--acc:#e8a244;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#16130f;--surface:#1f1b16;--ink:#f1e9dc;--body:#ddd3c3;--muted:#a3978a;--line:#39322a;--acc:#e8a244;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--body);font:19px/1.6 var(--serif)}}
.top{{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;gap:6px 14px;flex-wrap:wrap;font:12px var(--mono);z-index:2}}
.top a{{color:var(--muted);text-decoration:none;white-space:nowrap}}.top a:hover,.top a:focus-visible{{color:var(--ink);text-decoration:underline}}
.top b{{color:var(--ink);font-weight:500}}
main{{max-width:36em;margin:0 auto;padding:28px 16px 90px}}
h1{{font:600 clamp(28px,5vw,40px)/1.12 var(--serif);color:var(--ink);margin:0 0 14px;text-wrap:balance}}
h2{{font:600 25px/1.2 var(--serif);color:var(--ink);margin:44px 0 10px;text-wrap:balance;scroll-margin-top:70px}}
h3{{font:italic 400 21px/1.25 var(--serif);color:var(--ink);margin:26px 0 6px;scroll-margin-top:70px}}
p{{margin:0 0 14px}}li{{margin-bottom:8px}}ol,ul{{padding-left:1.3em;margin:0 0 14px}}
.tw{{overflow-x:auto;margin:0 0 16px}}table{{border-collapse:collapse;font:14px/1.4 var(--serif);min-width:100%}}th,td{{border-bottom:1px solid var(--line);padding:6px 10px 6px 0;text-align:left;vertical-align:top}}th{{font:500 11px var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}}
blockquote{{margin:0 0 14px;padding-left:14px;border-left:3px solid var(--line);color:var(--muted)}}
.note{{font:13px/1.5 var(--mono);color:var(--muted);border:1px solid var(--line);background:var(--surface);padding:10px 12px;margin:0 0 26px}}
.note a{{color:var(--acc)}}
</style></head><body>
<nav class="top" aria-label="Contents"><b>Reading edition</b><a href="./">Home</a><a href="find.html">Find</a><a href="find.html#claims">Claims</a>{nav}</nav>
<main>
<p class="note">Generated from <a href="{CANON}">{CANON}</a> by tools/build_index.py. The words are the draft's; bold and code marks are removed. Claims in this text that have been checked are in <a href="find.html#claims">the claims list</a>.</p>
{chr(10).join(out)}
</main></body></html>'''
    with open('read.html', 'w', encoding='utf8') as f:
        f.write(page)
    return len(out)

# ---------------------------------------------------------------- claims
def claims():
    cs = json.loads(read('tools/claims.json'))
    order = ['unsupported', 'conflicting', 'open', 'supported', 'measured', 'resolved']
    md = ['# Claims checked', '',
          'Each row is one claim made somewhere in this repository or in the pages it points to, how it stands, and what would settle it.',
          'Edit `tools/claims.json` and run `python3 tools/build_index.py`. The same list is searchable in [find.html](./find.html#claims).', '',
          '| | Claim | Status | Evidence | What would settle it |', '|:--|:--|:--|:--|:--|']
    for c in sorted(cs, key=lambda c: (order.index(c['status']), c['id'])):
        md.append(f"| {c['id']} | {c['claim']} *{c['where']}* | **{c['status']}** | {c['evidence']} | {c['next']} |")
    with open('CLAIMS.md', 'w', encoding='utf8') as f:
        f.write('\n'.join(md) + '\n')
    return cs

# ---------------------------------------------------------------- main
def main():
    cs, nblocks = cards()
    if '--dedupe' in sys.argv:
        dedupe(cs); cs, nblocks = cards()
    es, ss, fs, cl = entries(), sections(), files(), claims()
    # backlinks: full card IDs anywhere; short codes only where the text is about the zettels
    for c in cs:
        full = re.compile(re.escape(c['id']))
        sh = re.compile(r'(?<![\w-])' + re.escape(c['short']) + r'(?![\w-])')
        refs = []
        for e in es:
            t = ' '.join([e['title'], e['text'], e['kept'], e['source'], e['when'], e['exhibit']])
            if full.search(t) or sh.search(e['when'] + ' ' + e['source']):
                refs.append({'k': 'entry', 'label': f"Journal {e['n']:02d} · {e['title']}", 'href': e['href']})
        for s in ss:
            if full.search(s['text']) or (('ZTL' in s['text'] or 'zettle' in s['text']) and sh.search(s['text'])):
                refs.append({'k': 'section', 'label': f"{s['docname']} · {s['heading']}", 'href': s['href']})
        c['refs'] = refs
        del c['raw']
    idx = {'built': subprocess.check_output(['git', 'log', '-1', '--format=%h %ad', '--date=short'], text=True).strip(),
           'counts': {'card_blocks_in_file': nblocks, 'cards': len(cs), 'card_ids': len({c['id'] for c in cs}),
                      'entries': len(es), 'sections': len(ss), 'files': len(fs), 'claims': len(cl)},
           'cards': cs, 'entries': es, 'sections': ss, 'files': fs, 'claims': cl}
    os.makedirs('data', exist_ok=True)
    with open('data/index.js', 'w', encoding='utf8') as f:
        f.write('window.BH_INDEX=' + json.dumps(idx, ensure_ascii=False, separators=(',', ':')) + ';\n')
    n = reading_edition()
    print(json.dumps(idx['counts']), 'reading blocks', n, 'index bytes', os.path.getsize('data/index.js'))

if __name__ == '__main__':
    main()
