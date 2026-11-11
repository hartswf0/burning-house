# VTX-0.1 — Minimum Viable Video-Text (`BUILD` Package)

Source-grounded reference implementation, single-root A/B animation pair, deterministic trace validator, offline HTML5 Canvas workbench + blinded perceptual test harness, and retained revision history for Watson Hartsoe's Flour Test / *The Burning of the Abominable House* research (`SCION v1.1`).

> **Scope & Provenance Note**
> - **Invented Adaptation**: `vtx01_case_a_assist` and `vtx01_case_b_deliberate` are an invented minimal two-actor parlor test, **not** a recovered scene from Italo Calvino's 1973 text.
> - **Synthetic Policies (`P1`–`P4`)**: `cases/policies_synthetic_p1_p4.json` defines explicitly invented demonstration clauses separating **World State** from **Corroborated Visual Evidence** (`authored goal` never counts as visual corroboration).
> - **Human Perceptual Gate (`PENDING`)**: The blinded zero-caption evaluation harness (`viewer/index.html`) and unlabeled `.mp4` exports are ready, but voluntary human respondent testing and narrative-interest judgment have **not** been conducted (`UNTESTED`).

---

## Directory Layout

```text
vtx01_build/
├── README.md
├── cases/
│   ├── case_a_assist.vtx.json              # Canonical Case A (E2.goal = "assist_steadying", rev2)
│   ├── patch_a_to_b_goal.json              # Exact single-root A -> B goal patch
│   ├── case_b_deliberate.vtx.json          # Derived Case B (E2.goal = "tip_lamp_deliberately", rev2)
│   ├── policies_synthetic_p1_p4.json       # Synthetic demonstration policies P1–P4 (v0.1-synthetic)
│   └── protocols_followup_specs.json       # Follow-up Chance, Memory, Policy & Flower transfer specs
├── src/
│   ├── vtx_engine.js                       # Deterministic replay, 2.5D flour-sack rig & display list
│   ├── validate_vtx.js                     # Structural, Kinematic/Attachment & Temporal gate validator
│   ├── export_mp4.py                       # 2x-supersampled (2560x1440 -> 1280x720) MP4 & sheet exporter
│   └── build_viewer_bundle.js              # Offline file:// bundle builder for viewer/index.html
├── viewer/
│   ├── index.html                          # Interactive Workbench, Live JSON Remix & Blinded Test UI
│   └── bundle_data.js                      # Pre-bundled offline case/policy/trace payload
├── traces/
│   ├── chance_trace.json                   # Exogenous keyed Jolt_1 seed/draw invariance across A & B
│   ├── memory_trace.json                   # 3-level separation: World vs Character vs Authorial History
│   ├── consequence_trace.json              # Persistent updates + enabled/blocked downstream actions
│   ├── policy_traces.json                  # P1–P4 World Verdict vs Corroborated Evidence Verdict
│   └── validation_report.json              # Deterministic structural, kinematic & temporal audit
└── revisions/
    ├── rev1_rejected/                      # Retained unsuccessful candidate (failed kinematic gate)
    │   ├── case_a_rev1_rejected.mp4
    │   ├── case_b_rev1_rejected.mp4
    │   ├── ab_focus_comparison_rev1_rejected.png
    │   ├── inspection_sheet_case_a_rev1_rejected.png
    │   ├── inspection_sheet_case_b_rev1_rejected.png
    │   └── validation_report_rev1_failed.json
    └── rev2_accepted/                      # Repaired candidate passing Structural/Animation/Temporal gates
        ├── case_a_rev2_accepted.mp4        # 16.0s, 384f @ 24fps, 1280x720, zero scene captions
        ├── case_b_rev2_accepted.mp4        # 16.0s, 384f @ 24fps, 1280x720, zero scene captions
        ├── ab_paired_clean_rev2_accepted.mp4
        ├── ab_focus_comparison_rev2_accepted.png
        ├── inspection_sheet_case_a_rev2_accepted.png
        ├── inspection_sheet_case_b_rev2_accepted.png
        ├── carry_73frames_case_a_rev2_accepted.png
        ├── carry_73frames_case_b_rev2_accepted.png
        └── verification_record.json        # SHA-256 hashes, tool versions, lineage & gate statuses
```

---

## Reproduction Instructions

Tested on macOS (`arm64`) with:
- Node.js `/opt/homebrew/bin/node` (`v23.6.0`)
- Python `/Users/gaia/anaconda3/bin/python3` (`3.11`, `numpy 1.26.4`, `opencv-python 4.10.0`)
- FFmpeg `/Users/gaia/anaconda3/bin/ffmpeg` (`4.3.2`, `libx264`)

### 1. Derive `Case B` from `Case A + Patch` and Run Gate Validation
```bash
/opt/homebrew/bin/node "/Users/gaia/burning house/vtx01_build/src/validate_vtx.js"
```
This deterministically regenerates `cases/case_b_deliberate.vtx.json` from `cases/case_a_assist.vtx.json` + `cases/patch_a_to_b_goal.json`, verifies identical exogenous `E1` frames (`0..76`), inspects all `384` frames per case (including all `73` frames of the carried `Wedge_1` interval `[10.50, 13.50] s` and the `9.50 s` camera cut), and writes `revisions/validation_report.json` + `revisions/traces_a_and_b.json`.

### 2. Rebuild Offline Viewer Bundle
```bash
/opt/homebrew/bin/node "/Users/gaia/burning house/vtx01_build/src/build_viewer_bundle.js"
```
Open `/Users/gaia/burning house/vtx01_build/viewer/index.html` directly in any modern browser (`file://` compatible, zero server required):
- **Tab 1 — Blinded Perceptual Test (Zero Captions)**: Randomizes Case A and Case B as unlabeled `Clip X` / `Clip Y` with zero captions, state Inspector, or trace spoilers, collects independent viewer judgments + confidence + timestamp cues, and exports a JSON response packet before unblinding.
- **Tab 2 — Synchronized A/B Inspector**: Frame-accurate `24 fps` scrubber (`0..383`), live Chance / Memory / Consequence traces, and side-by-side synthetic policy (`P1`–`P4`) World vs. Corroborated Evidence tables.
- **Tab 3 — Live `VTX-0.1` Remix Editor**: Edit `E2_root_action.goal`, `Jolt_1` impulse, or `Sack_B` initial memory live in JSON, replay causal traces, and inspect immediate visual changes on canvas.

### 3. Re-render `1280x720` Unlabeled `.mp4` Videos & Frame Contact Sheets
```bash
/Users/gaia/anaconda3/bin/python3 "/Users/gaia/burning house/vtx01_build/src/export_mp4.py" rev2_accepted
```

