#!/usr/bin/env python3
"""
VTX-0.1 Deterministic 2x-Supersampled Frame Renderer, Contact-Sheet Builder & FFmpeg MP4 Exporter.
Consumes the exact declarative display list emitted by src/vtx_engine.js so HTML5 Canvas and MP4
are driven by identical geometry, timing, and state transitions. Zero captions inside scene frames.
"""
import json
import math
import os
import re
import subprocess
import sys
import hashlib
import numpy as np
import cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NODE_BIN = '/opt/homebrew/bin/node'
FFMPEG_BIN = '/Users/gaia/anaconda3/bin/ffmpeg'

SS = 2  # 2x supersampling: render 2560x1440 -> downsample AREA to 1280x720
W, H = 1280, 720
SW, SH = W * SS, H * SS


def parse_color(c_str):
    if not c_str:
        return None, 0.0
    c_str = c_str.strip()
    if c_str.startswith('#'):
        hx = c_str[1:]
        if len(hx) == 3:
            hx = ''.join(ch * 2 for ch in hx)
        r = int(hx[0:2], 16)
        g = int(hx[2:4], 16)
        b = int(hx[4:6], 16)
        return (b, g, r), 1.0
    m = re.match(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)', c_str)
    if m:
        r, g, b = int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3)))
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (b, g, r), max(0.0, min(1.0, a))
    return (255, 255, 255), 1.0


# Precompute unit radial glow mask for fast alpha-blended lighting
_yy, _xx = np.ogrid[-128:128, -128:128]
_GLOW_MASK = np.clip(1.0 - np.sqrt((_xx / 128.0) ** 2 + (_yy / 128.0) ** 2), 0.0, 1.0) ** 1.8


def blend_glow(img, cx, cy, radius, bgr, alpha):
    if alpha <= 0.002 or radius < 2:
        return
    r = int(radius)
    x0, y0 = int(cx - r), int(cy - r)
    x1, y1 = int(cx + r), int(cy + r)
    if x1 <= 0 or y1 <= 0 or x0 >= SW or y0 >= SH:
        return
    mask = cv2.resize(_GLOW_MASK, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    ix0, iy0 = max(0, x0), max(0, y0)
    ix1, iy1 = min(SW, x1), min(SH, y1)
    mx0, my0 = ix0 - x0, iy0 - y0
    mx1, my1 = mx0 + (ix1 - ix0), my0 + (iy1 - iy0)
    sub_mask = (mask[my0:my1, mx0:mx1] * alpha)[..., None]
    roi = img[iy0:iy1, ix0:ix1].astype(np.float32)
    color_arr = np.array(bgr, dtype=np.float32)
    img[iy0:iy1, ix0:ix1] = np.clip(roi * (1.0 - sub_mask) + color_arr * sub_mask, 0, 255).astype(np.uint8)


def render_commands_bgr(cmds):
    img = np.zeros((SH, SW, 3), dtype=np.uint8)
    for cmd in cmds:
        op = cmd.get('op')
        if op == 'rect':
            x = int(round(cmd['x'] * SS))
            y = int(round(cmd['y'] * SS))
            w = int(round(cmd['w'] * SS))
            h = int(round(cmd['h'] * SS))
            fill, fa = parse_color(cmd.get('fill'))
            if fill and fa >= 0.995:
                cv2.rectangle(img, (x, y), (x + w, y + h), fill, -1, lineType=cv2.LINE_AA)
            elif fill and fa > 0:
                ov = img.copy()
                cv2.rectangle(ov, (x, y), (x + w, y + h), fill, -1, lineType=cv2.LINE_AA)
                cv2.addWeighted(ov, fa, img, 1.0 - fa, 0, dst=img)
            stroke, sa = parse_color(cmd.get('stroke'))
            if stroke and sa > 0:
                lw = max(1, int(round(cmd.get('lw', 1) * SS)))
                cv2.rectangle(img, (x, y), (x + w, y + h), stroke, lw, lineType=cv2.LINE_AA)

        elif op == 'glow':
            bgr, a = parse_color(cmd.get('color'))
            blend_glow(img, cmd['x'] * SS, cmd['y'] * SS, cmd['r'] * SS, bgr, a)

        elif op == 'ellipse':
            cx = int(round(cmd['x'] * SS))
            cy = int(round(cmd['y'] * SS))
            rx = max(1, int(round(cmd['rx'] * SS)))
            ry = max(1, int(round(cmd['ry'] * SS)))
            fill, fa = parse_color(cmd.get('fill'))
            if fill and fa >= 0.995:
                cv2.ellipse(img, (cx, cy), (rx, ry), 0, 0, 360, fill, -1, lineType=cv2.LINE_AA)
            elif fill and fa > 0:
                x0, y0 = max(0, cx - rx - 4), max(0, cy - ry - 4)
                x1, y1 = min(SW, cx + rx + 4), min(SH, cy + ry + 4)
                if x1 > x0 and y1 > y0:
                    roi = img[y0:y1, x0:x1].copy()
                    cv2.ellipse(roi, (cx - x0, cy - y0), (rx, ry), 0, 0, 360, fill, -1, lineType=cv2.LINE_AA)
                    cv2.addWeighted(roi, fa, img[y0:y1, x0:x1], 1.0 - fa, 0, dst=img[y0:y1, x0:x1])
            stroke, sa = parse_color(cmd.get('stroke'))
            if stroke and sa > 0:
                lw = max(1, int(round(cmd.get('lw', 1) * SS)))
                cv2.ellipse(img, (cx, cy), (rx, ry), 0, 0, 360, stroke, lw, lineType=cv2.LINE_AA)

        elif op == 'poly':
            pts = np.array([[int(round(p[0] * SS)), int(round(p[1] * SS))] for p in cmd['pts']], dtype=np.int32)
            fill, fa = parse_color(cmd.get('fill'))
            if fill and fa >= 0.995:
                cv2.fillPoly(img, [pts], fill, lineType=cv2.LINE_AA)
            elif fill and fa > 0:
                x0, y0 = max(0, int(pts[:, 0].min()) - 4), max(0, int(pts[:, 1].min()) - 4)
                x1, y1 = min(SW, int(pts[:, 0].max()) + 4), min(SH, int(pts[:, 1].max()) + 4)
                if x1 > x0 and y1 > y0:
                    roi = img[y0:y1, x0:x1].copy()
                    shifted = pts - np.array([[x0, y0]], dtype=np.int32)
                    cv2.fillPoly(roi, [shifted], fill, lineType=cv2.LINE_AA)
                    cv2.addWeighted(roi, fa, img[y0:y1, x0:x1], 1.0 - fa, 0, dst=img[y0:y1, x0:x1])
            stroke, sa = parse_color(cmd.get('stroke'))
            if stroke and sa > 0:
                lw = max(1, int(round(cmd.get('lw', 1) * SS)))
                cv2.polylines(img, [pts], True, stroke, lw, lineType=cv2.LINE_AA)

        elif op == 'polyline':
            pts = np.array([[int(round(p[0] * SS)), int(round(p[1] * SS))] for p in cmd['pts']], dtype=np.int32)
            stroke, sa = parse_color(cmd.get('stroke'))
            if stroke and sa > 0:
                lw = max(1, int(round(cmd.get('lw', 1) * SS)))
                if cmd.get('dashed'):
                    for i in range(0, len(pts) - 1, 2):
                        cv2.line(img, tuple(pts[i]), tuple(pts[i + 1]), stroke, lw, lineType=cv2.LINE_AA)
                else:
                    cv2.polylines(img, [pts], False, stroke, lw, lineType=cv2.LINE_AA)

        elif op == 'line':
            p1 = (int(round(cmd['p1'][0] * SS)), int(round(cmd['p1'][1] * SS)))
            p2 = (int(round(cmd['p2'][0] * SS)), int(round(cmd['p2'][1] * SS)))
            stroke, sa = parse_color(cmd.get('stroke'))
            if stroke and sa > 0:
                lw = max(1, int(round(cmd.get('lw', 1) * SS)))
                cv2.line(img, p1, p2, stroke, lw, lineType=cv2.LINE_AA)

    return cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)


def dump_case_frames_json(case_path):
    js_code = f"""
    const fs = require('fs');
    const eng = require({json.dumps(os.path.join(ROOT, 'src', 'vtx_engine.js'))});
    const c = JSON.parse(fs.readFileSync({json.dumps(case_path)}, 'utf8'));
    const fps = c.timeline.fps;
    const total = c.timeline.total_frames;
    for (let f = 0; f < total; f++) {{
      const st = eng.evaluateFrame(c, f / fps);
      process.stdout.write(JSON.stringify({{ f, t: st.t, commands: st.commands }}) + '\\n');
    }}
    """
    proc = subprocess.Popen([NODE_BIN, '-e', js_code], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        if line.strip():
            yield json.loads(line)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f'Node frame dump failed for {case_path}')


def render_case_to_mp4_and_keyframes(case_path, mp4_out_path, key_frames_indices):
    os.makedirs(os.path.dirname(mp4_out_path), exist_ok=True)
    ffmpeg_cmd = [
        FFMPEG_BIN, '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}',
        '-pix_fmt', 'bgr24',
        '-r', '24',
        '-i', '-',
        '-an',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        mp4_out_path
    ]
    ff = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    saved_keyframes = {}
    for item in dump_case_frames_json(case_path):
        f = item['f']
        frame_bgr = render_commands_bgr(item['commands'])
        ff.stdin.write(frame_bgr.tobytes())
        if f in key_frames_indices:
            saved_keyframes[f] = (item['t'], frame_bgr.copy())
    ff.stdin.close()
    err = ff.stderr.read()
    ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(f'FFmpeg failed: {err.decode("utf8", errors="ignore")}')
    return saved_keyframes


def build_contact_sheet(kf_dict, indices, out_png_path, cols=4):
    thumbs = []
    tw, th = 420, 236
    for idx in indices:
        t, img = kf_dict[idx]
        th_img = cv2.resize(img, (tw, th), interpolation=cv2.INTER_AREA)
        # Note: Diagnostic border timecode ONLY on builder inspection sheet, NEVER in MP4 or perceptual test!
        cv2.rectangle(th_img, (4, 4), (174, 28), (18, 16, 15), -1)
        cv2.putText(th_img, f'f={idx:03d} t={t:05.2f}s', (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (235, 220, 195), 1, cv2.LINE_AA)
        thumbs.append(th_img)
    rows = math.ceil(len(thumbs) / cols)
    sheet = np.zeros((rows * th, cols * tw, 3), dtype=np.uint8)
    for i, im in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet[r * th:(r + 1) * th, c * tw:(c + 1) * tw] = im
    cv2.imwrite(out_png_path, sheet)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fp:
        while True:
            b = fp.read(65536)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


if __name__ == '__main__':
    rev_tag = sys.argv[1] if len(sys.argv) > 1 else 'rev1'
    out_dir = os.path.join(ROOT, 'revisions', rev_tag)
    os.makedirs(out_dir, exist_ok=True)

    key_indices = [
        48,   # 2.00s Jolt_1
        86,   # 3.58s Anticipation A vs Coil B
        98,   # 4.08s Mid-reach A vs Held coil B
        118,  # 4.92s Contact with Lamp_1!
        125,  # 5.21s Tipping & Follow-through
        138,  # 5.75s Startled recoil A vs Composed retreat B
        204,  # 8.50s Fire_1 full in Shot 1
        227,  # 9.46s Pre-cut frame
        228,  # 9.50s Post-cut frame (Shot 2 doorway)
        252,  # 10.50s Carry start (Wedge_1 pickup)
        288,  # 12.00s Mid-carry (Wedge_1 attached to Sack_B.ear_R)
        324,  # 13.50s Carry end (Wedge_1 prop open vs jam shut)
        360   # 15.00s Final consequence (Cooperative exit vs Blocked door)
    ]

    carry_indices = list(range(252, 325))  # All 73 frames of carried Wedge_1 interval [10.50, 13.50]s
    capture_set = set(key_indices) | set(carry_indices)

    case_a = os.path.join(ROOT, 'cases', 'case_a_assist.vtx.json')
    case_b = os.path.join(ROOT, 'cases', 'case_b_deliberate.vtx.json')
    mp4_a = os.path.join(out_dir, f'case_a_{rev_tag}.mp4')
    mp4_b = os.path.join(out_dir, f'case_b_{rev_tag}.mp4')

    print(f'Rendering {rev_tag} Case A -> {mp4_a} ...')
    kf_a = render_case_to_mp4_and_keyframes(case_a, mp4_a, capture_set)
    sheet_a = os.path.join(out_dir, f'inspection_sheet_case_a_{rev_tag}.png')
    build_contact_sheet(kf_a, key_indices[:12], sheet_a, cols=4)

    print(f'Rendering {rev_tag} Case B -> {mp4_b} ...')
    kf_b = render_case_to_mp4_and_keyframes(case_b, mp4_b, capture_set)
    sheet_b = os.path.join(out_dir, f'inspection_sheet_case_b_{rev_tag}.png')
    build_contact_sheet(kf_b, key_indices[:12], sheet_b, cols=4)

    # Build 73-frame carried-object inspection grids (cropped to doorway carry region x=[560:1240], y=[220:660])
    def build_carry_grid(kf_dict, out_path):
        cells = []
        cw, ch = 220, 142
        for idx in carry_indices:
            t, img = kf_dict[idx]
            crop = img[220:660, 560:1240]
            cell = cv2.resize(crop, (cw, ch), interpolation=cv2.INTER_AREA)
            cv2.rectangle(cell, (2, 2), (108, 20), (18, 16, 15), -1)
            cv2.putText(cell, f'f{idx} {t:.2f}s', (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (235, 220, 195), 1, cv2.LINE_AA)
            cells.append(cell)
        cols = 9
        rows = math.ceil(len(cells) / cols)
        grid = np.zeros((rows * ch, cols * cw, 3), dtype=np.uint8)
        for i, im in enumerate(cells):
            r, c = divmod(i, cols)
            grid[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = im
        cv2.imwrite(out_path, grid)

    carry_png_a = os.path.join(out_dir, f'carry_73frames_case_a_{rev_tag}.png')
    carry_png_b = os.path.join(out_dir, f'carry_73frames_case_b_{rev_tag}.png')
    build_carry_grid(kf_a, carry_png_a)
    build_carry_grid(kf_b, carry_png_b)

    # Also mux clean unlabeled side-by-side A/B MP4 (1920x540, zero text/captions in frames)
    mp4_pair = os.path.join(out_dir, f'ab_paired_clean_{rev_tag}.mp4')
    subprocess.run([
        FFMPEG_BIN, '-y',
        '-i', mp4_a,
        '-i', mp4_b,
        '-filter_complex', '[0:v]scale=960:540[l];[1:v]scale=960:540[r];[l][r]hstack=inputs=2[v]',
        '-map', '[v]',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
        mp4_pair
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Also build focused contact/carry zoom sheet (frames 98, 118, 138, 228, 252, 288, 324, 360)
    pair_focus = []
    for idx in [98, 118, 138, 228, 252, 288, 324, 360]:
        ta, ima = kf_a[idx]
        tb, imb = kf_b[idx]
        row_img = np.hstack([
            cv2.resize(ima, (560, 315), interpolation=cv2.INTER_AREA),
            cv2.resize(imb, (560, 315), interpolation=cv2.INTER_AREA)
        ])
        cv2.rectangle(row_img, (6, 6), (260, 32), (18, 16, 15), -1)
        cv2.putText(row_img, f'A vs B | f={idx:03d} t={ta:05.2f}s', (12, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 225, 200), 1, cv2.LINE_AA)
        pair_focus.append(row_img)
    focus_png = os.path.join(out_dir, f'ab_focus_comparison_{rev_tag}.png')
    cv2.imwrite(focus_png, np.vstack(pair_focus))

    print(json.dumps({
        'mp4_a_sha256': sha256_file(mp4_a),
        'mp4_b_sha256': sha256_file(mp4_b),
        'mp4_pair_sha256': sha256_file(mp4_pair),
        'sheet_a': sheet_a,
        'sheet_b': sheet_b,
        'focus_png': focus_png,
        'carry_png_a': carry_png_a,
        'carry_png_b': carry_png_b
    }, indent=2))
