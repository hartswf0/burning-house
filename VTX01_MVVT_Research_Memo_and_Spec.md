# Minimum Viable Video-Text (`VTX-0.1`): Chance, Memory, and Consequence in the Flour-Sack *Abominable House*

**Mode:** `NOTES` (Working Research Memo + Falsifiable Experiment Specification; `BUILD` and empirical viewer/swarm evaluations `NOT_RUN`)  
**Decision Owner:** Watson Hartsoe  
**Status:** `MILESTONE` (Source-audited memo and `VTX-0.1` baseline specification ready for review or live `BUILD` authorization)

---

## Part I — Research Memo (Connected Prose)

### 1. Opening Argument: Calvino's Burned House, the Flour Sack, and Three Temporal Primitives

Italo Calvino's *"The Burning of the Abominable House"* (1973) begins where a police investigation gives up: a boarding house has burned to ashes with all four inhabitants inside, leaving behind a charred notebook whose surviving index names twelve categories of abominable deeds without recording who committed them, against whom, or in what order (`C1`; `C2`). What turns this combinatorial puzzle from parlor arithmetic into a parable of modern calculation is its commissioning frame. An insurance investigator hires a computer programmer to reconstruct which histories remain possible because overlapping claims ride on how the dead behaved before the fire. Beneath its playful Oulipian surface, the story asks a deadly serious question about numerification, responsibility, and value: when human conduct is compressed into discrete slots and exclusion rules, who authorizes the rules, what evidence survives the flames, and who profits when one reconstruction is accepted as official truth?

To investigate that question inside contemporary generative media without losing causal accountability, we turn to a deliberately stripped-down performer: the half-filled canvas flour sack popularized in Walt Disney Studios animation training (`A1`; Johnston and Thomas 1981). A flour sack has no face, hands, or spoken dialogue. Weight shift, squash and stretch, corner drag, hesitation, contact, and recoil must carry the entire burden of visible intention. Paired with Calvino's house, the flour sack serves two research purposes at once. Expressively, it isolates the minimal movement threshold at which an audience can tell an accidental brush from a deliberate shove. Methodologically, abstracting conflict onto faceless canvas sacks keeps our experimental cases non-graphic while letting us document—rather than evade—what generative tools accept, distort, or refuse when staging transgressive literary structures.

We organize both the literary analysis and the technical design around a testable temporal triad: **chance**, **memory**, and **consequence**. In our proposed model, **chance** names an explicit contingent disturbance inside the fictional world—kept strictly distinct from audience uncertainty, authored counterfactual branches, and stochastic noise during model sampling. **Memory** operates across three separated layers: persistent physical traces left in the room, a character's selective and potentially mistaken recollections acquired only through permitted observations or inferences, and the external production archive. **Consequence** names a state change that persists across cuts—altering physical affordances, social relations, character knowledge, viewer interpretation, and contractual liability—so that earlier outcomes become the preconditions for later acts and future memories.

Our candidate contribution is a **Minimum Viable Video-Text** representation, **`VTX-0.1`**: a small, inspectable, editable format linking textual propositions, executable event logic, timed movement scores, and counterfactual patches. Rather than claiming that "anything can become video-text" in general, we test a falsifiable proposition on a controlled first case (*all empirical results currently unmeasured*). In one room with a shared fixed camera, two faceless flour sacks (`Sack_A`, `Sack_B`), and one lit oil lamp (`Lamp_1`), both scenes end in the same fire (`16.0` seconds). Prior history, initial character memories, and a named exogenous floorboard jolt (`Jolt_1`) are held identical. Only one root variable changes: in **Case A**, `Sack_A` reaches to steady `Sack_B` during the jolt and inadvertently tips the lamp; in **Case B**, `Sack_A` plants its base during the same jolt and deliberately shoves the lamp over. Because consequences persist across cuts, the oil spill, singed fabric, and `Sack_B`'s permitted observation govern `Sack_B`'s next action at the doorway—cooperating with `Sack_A` in Case A versus recoiling to bar `Sack_A` in Case B—and yield divergent verdicts under synthetic insurance clauses evaluated separately against world state and visible camera evidence.

### 2. Historical Evidence: IBM, *Playboy*, and Oulipian Anticombinatorics

A rigorous framing must separate Calvino's 1973 story from the later computer experiments it inspired (`C1`; `C2`). In her preface to *Numbers in the Dark*, Esther Calvino writes that the story answered *"a somewhat vague request from IBM: how far was it possible to write a story using the computer?"*—noting that in Paris, where access to data-processing machines was difficult, Calvino carried out all the combinatorial operations by hand before publishing the story in the Italian edition of *Playboy* in 1973 (`C1`). Paul Braffort's first-person memoir *"L'ordre dans le crime"* (`C2`) complicates and enriches Esther Calvino's paratext on two fronts while introducing one discrepancy of its own. Citing Marcel Benabou and Mario Barenghi's *Meridiani* critical apparatus (*Romanzi e racconti*, vol. III, 1994, p. 1242), Braffort documents that Calvino already presented the project—conceived as the seed of a full novel—at his first Oulipo luncheon on **8 November 1972**, prior to his formal election on 14 February 1973 (`C2`). Braffort and Jacques Roubaud then visited Calvino in Paris, Calvino observed early program tests at Braffort's Université Paris XI (Orsay) laboratory, and Braffort later built the formal constraint-filtering software presented at the 1977 Centre Pompidou A.R.T.A. showcase and codified in *"Prose et anticombinatoire"* (*Atlas de littérature potentielle*, 1981; `C2`). Conversely, Braffort parenthetically calls the initial publication *"l'édition américaine de Playboy"* (`C2`), contradicting Esther Calvino and bibliographic records identifying the 1973 Italian *Playboy*; until the physical 1973 issue and the Pantheon/Mondadori story pages are inspected directly, we preserve that disagreement and refrain from claiming a verbatim transcription of the story's twelve English deed labels or policy wording.

Recomputing the baseline possibility space exposes how Oulipian constraints generate alternatives while **anticombinatorial** filters eliminate them. Under the simplifying assumption of four inhabitants ($4 \times 3 = 12$ non-reflexive directed pairs) independently assigned across twelve fixed deed slots, the unconstrained space contains exactly $12^{12} = 8,916,100,448,256$ assignments (printed editions and secondary summaries variously give `8,874,296,672,256`—equal to $12^6 \times (12^6 - 14,000)$, consistent with a hand-squaring slip—or `874,296,672,256`). In the French synopsis preserved by Braffort (`C2`), Calvino eliminates alternatives through explicit objective filters: narrative-economy caps (one actor per deed role per permutation), irreversibility and non-redundancy within **murder** (*étrangler, poignarder, induire au suicide*) and **sexual** classes (*séduction, argent, viol*), transitive prerequisites for **appropriation of a secret** and **appropriation of will**, and chronological mortality (a murdered victim can neither act nor be acted upon afterward, forcing lethal acts toward the end of valid sequences). As Dennis Duncan (2012) argues, Oulipian method pairs exhaustive structural pruning with the Lucretian *clinamen*—the intentional swerve that restores narrative surprise once mechanical absurdities fall away.

### 3. Insurance, *Double Indemnity*, and the Politics of Reconstruction

Insurance transforms uncertain conduct into discrete categories, evidentiary burdens, and binary payouts. In Calvino's frame, the reconstruction is commissioned not by neutral historians, but by an insurer whose financial exposure depends on which exclusions hold—and in Braffort's quotation of the story's ending (`C2`), the analyst realizes as fire sirens approach that his client has come to kill him and burn his laboratory to destroy incriminating cards. We propose pairing Calvino's frame with James M. Cain's *Double Indemnity* (1943) and Billy Wilder and Raymond Chandler's 1944 film adaptation—treated here as a **proposed comparative close reading** rather than an established equivalence—where claims manager Barton Keyes translates desire and staged accident into actuarial probability tables. In our experiment, keeping **world-state evaluation** separate from **evidence-based evaluation** exposes the core institutional tension: a movement that was genuinely accidental in authored reality (`Case A`) may still yield `UNKNOWN` or `NO_PAY` under a corroboration clause if camera framing or smoke occludes the contact interval.

### 4. Related Work and the Proposed Bridge from `LEGOS` to `VTX-0.1`

`VTX-0.1` bridges four distinct technical lineages while maintaining strict boundaries around what each source establishes:

- **From `LEGOS` Assembly to Timed Action:** In prior project work (*Can a Language Model Build With LEGO?*), editable text lines place discrete spatial bricks so a misplaced element can be traced to its source line and repaired locally, alongside the `LEGOS` narrative grammar (**Location, Entity, Goal, Obstacle, Shift/Solution**). Because we have not inspected LDraw/MPD code interoperability in this run, we claim no direct file-level compatibility. Instead, the exact bridge proposed is mapping `LEGOS` narrative slots onto timed state transitions (`Location → room/camera`, `Entity → sack rig + state`, `Goal → committed action target`, `Obstacle → precondition/disturbance`, `Shift → persistent consequence`) where trajectory, contact intervals, and weight deformation must unfold continuously across frames.
- **Agent Commitments, Memory, and Unresolved Cognitive Citations:** For character action selection, we separate Michael Bratman's (1987) philosophical account of intention stability from Anand Rao and Michael Georgeff's (1995; `B1`) computational **BDI** architecture—continuing the author's earlier `PIE`/BDI modeling of competing historical interpretations—so beliefs, desires, and intentions denote explicit public data structures rather than post-hoc LLM rationalizations. For language-mediated memory, reflection, and planning, Joon Sung Park et al.'s *Generative Agents* ("Smallville", 2023; `G1`) provides the primary research precedent, kept distinct from the `a16z-infra/ai-town` open-source web starter kit it inspired. An intended reference to **Demis Hassabis** from project brainstorming remains **visibly unresolved** pending authorial confirmation (candidates include Hassabis et al.'s 2014 personality-simulation neuroimaging study *Imagine All the People* vs. early *Black & White* creature AI); we do not attribute BDI to Hassabis.
- **Creative Swarms and Iterative Video Critique:** Anthropic's October 2026 engineering report on **Scion** (`S1`)—built when internal coding merges rose from ~2,500 to >30,000/day—serves solely as an **architectural analogy** (sharing its name by coincidence with the user's `SCION` instruction compiler, with no affiliation or animation-productivity evidence implied): changing generation scale exposes human-paced review bottlenecks. While robotics-oriented pipelines such as *VideoAgent* (Soni et al. 2024/2025) refine generated pixel clips via external feedback, and DH2025 studies document persistent sequential-storytelling failures in diffusion models (Onal et al. 2025) and focalization blind spots in LLMs (Pichler and Pagel 2025), our proposed wedge is **local causal-and-kinematic repair** over an explicit event contract rather than regenerating opaque video clips from scratch.
- **Reading Over the Machine's Shoulder and Lem's *Bitistics*:** Extending Clifford Geertz's (1972/1973; `H1`) ethnographic metaphor of reading cultural texts *"over the shoulders"* of participants, our method inspects **public model state**—snapshots, memory updates, motion scores, critic verdicts, and revision diffs—without claiming access to hidden neural cognition or equating simulated agents with a human culture. Stanisław Lem's *"A History of Bitic Literature"* in *Imaginary Magnitude* (`L1`) frames critical reception of machine-authored works: verified passages in Heine's 1984 translation describe **`semascope`** projections and geometric **`sematures`** woven of *"burning threads"*, whereas the brainstormed **"semaphore"** reference remains **unresolved** in Lem's text and is treated strictly as our own state-signaling design term unless another passage is identified.

### 5. Method, Competing Explanations, Limitations, and Next Actions

To test whether `VTX-0.1` earns its complexity, our experimental design isolates single-root interventions before testing production architectures. After validating the baseline **Goal Comparison** (`Case A` assist vs. `Case B` deliberate tip), follow-on protocols vary **Chance** alone (changing the realized magnitude of `Jolt_1` while holding goals and initial memories fixed) and **Memory** alone (changing whether `Sack_B` retains an earlier boundary-intrusion recollection after identical observed events, paired with an irrelevant-memory control), before testing embodiment transfer onto **Flower** (the project's plant performer). When authorized for `BUILD`, we will compare a single-pass baseline, a single builder with a critique loop, and a role-separated swarm under matched budgets (*all comparative speedups and quality gains currently unmeasured hypotheses*).

Several competing explanations could challenge or falsify our approach: viewers may prove unable to distinguish accidental from deliberate sack motion without facial cues or captions; critique, constraint repair, and merge overhead may consume more effort than regenerating whole clips; strict formalization may flatten the productive literary ambiguity that makes Calvino's story compelling; or industry resistance to editable video-text may stem from seat-licensing and billing incentives around opaque clips rather than technical feasibility. Our immediate next actions are: (1) inspect the Pantheon/Mondadori story edition to close the twelve-act and policy-wording audit; (2) confirm the intended Hassabis and Lem locators with Watson; and (3) upon live `BUILD` request, implement and verify the `Case A / Case B` HTML5 Canvas pair and blinded perceptual test.

*(Connected prose count: ~1,860 words)*

---

## Part II — Claim & Source Verification Ledger

Every material historical, literary, and technical claim is categorized below (`FACT`, `INTERPRETATION`, `DESIGN_CHOICE`, `HYPOTHESIS`, `UNRESOLVED`):

| ID | Claim / Concept | Epistemic Type | Source & Locator | Verification Status & Disagreements Preserved |
| :--- | :--- | :--- | :--- | :--- |
| **CL-01** | Calvino's story responded to a vague IBM inquiry on computer story-writing; lacking easy computer access in Paris, Calvino executed the operations manually. | `FACT` (Paratext) | `C1` (Esther Calvino, Preface to *Numbers in the Dark*, Pantheon 1995) | **VERIFIED** via `C1` transcription and quoted French parallel in `C2` (note 6, *La grande bonace des Antilles*, p. 8). |
| **CL-02** | Chronology & *Playboy* venue: presented to Oulipo on **8 Nov 1972**; published 1973 in *Playboy*; algorithmic filtering built later with Braffort (Orsay / 1977 Pompidou A.R.T.A. / 1981 *Atlas*). | `FACT` with **Source Conflict** | `C1` vs. `C2` (Braffort 1995/2002, citing Benabou 1990 & Barenghi *Meridiani* 1994, III: 1242) | **DISAGREEMENT PRESERVED**: `C1` specifies **Italian *Playboy*** (1973); `C2` (§1) parenthetically says **American *Playboy***. Original 1973 physical issue uninspected here. Story ≠ 1977 program. |
| **CL-03** | Exact transcription of all 12 source deed labels and Calvino's 4 original insurance clauses. | `UNRESOLVED` | Story edition (*Numbers in the Dark*, trans. Parks, 1995 / *Prima che tu dica «Pronto»*, 1993) | **`UNRESOLVED_PENDING_EDITION`**: Full story edition not in workspace. `C2` verifies 4 French *Atlas* constraint classes (*meurtre, sexuelles, secret, volonté*) and 6 named acts (*étrangler, poignarder, induire au suicide, séduction, argent, viol*). Full 12-act coverage matrix deferred per `<delivery_and_stop>`. |
| **CL-04** | Unconstrained dyadic assignment count is $12^{12} = 8,916,100,448,256$. | `FACT` (Recomputed) | Exact arithmetic (`12 ** 12`) | **VERIFIED** under stated assumptions: 4 actors $\Rightarrow 12$ ordered non-reflexive pairs independently assigned to 12 fixed deed slots. Contrasts with `8,874,296,672,256` and `874,296,672,256` in print/web summaries. |
| **CL-05** | Sack drop teaches weight, organic deformation, and squash-and-stretch; used here as minimal non-graphic expressive testbed. | `FACT` + `DESIGN_CHOICE` | `A1` (Walt Disney Family Museum 2020); Johnston & Thomas (1981) | **VERIFIED** (`A1` documents pedagogical lineage; does **not** establish the exercise's individual inventor). **Flower** (plant performer) kept distinct for later embodiment transfer. |
| **CL-06** | Anthropic's *Scion* (13 Oct 2026, updated 15 Oct 2026) replaced Git after merges grew from ~2,500 to >30,000/day. | `FACT` (Analogy Only) | `S1` (Anthropic Engineering 2026) | **VERIFIED** as **infrastructure analogy only**—not animation productivity evidence; zero affiliation with Watson's `SCION` compiler. |
| **CL-07** | BDI separates beliefs, desires, and committed intentions; Generative Agents models memory/reflection/planning. | `FACT` | `B1` (Rao & Georgeff 1995); Bratman (1987); `G1` (Park et al. 2023); `a16z-infra/ai-town` | **VERIFIED**: Bratman's philosophy kept distinct from `B1` implementation; `G1` Smallville kept distinct from `a16z-infra/ai-town`. |
| **CL-08** | Intended **Demis Hassabis** citation from initial research brainstorm. | `UNRESOLVED` | Candidate: Hassabis et al. (2014) *Cerebral Cortex* vs. *Black & White* (2001) | **`UNRESOLVED`**: BDI is **not** attributed to Hassabis; candidate reference flagged pending Watson's confirmation. |
| **CL-09** | "Reading over the machine's shoulder" inspects public state/revisions, not hidden LLM cognition. | `INTERPRETATION` / `METHOD` | `H1` (Geertz, *Daedalus* 1972 / *Interpretation of Cultures* 1973, p. 452) | **VERIFIED** as our methodological extension of Geertz's ethnographic metaphor. |
| **CL-10** | Lem's *Bitistics* (`L1`) and the brainstormed "semaphore" concept. | `FACT` + `UNRESOLVED` | `L1` (Lem, *Imaginary Magnitude*, 1973 / trans. Heine 1984) | **PARTIALLY VERIFIED / `UNRESOLVED`**: *Bitistics*, *semascope*, and *semature* verified in *"A History of Bitic Literature"*; **no "semaphore" passage verified in Lem**—kept unresolved and separated from our own design terminology. |
| **CL-11** | *Double Indemnity* illuminates actuarial categorization of accident vs. murder/arson. | `HYPOTHESIS` (Comparative) | Cain (1943); Wilder & Chandler (1944) | Marked as a **proposed literary/cinematic comparison** requiring dedicated close reading. |
| **CL-12** | Local `VTX-0.1` event editing + critique loop outperforms full-clip regeneration and single-pass authoring. | `HYPOTHESIS` (`UNMEASURED`) | Proposed `BUILD` study | **`NOT_RUN` / `UNMEASURED`**: Zero empirical speedup, viewer accuracy, or swarm advantage claimed. |

---

## Part III — Domain Theory, Working Olog, and `VTX-0.1` Schema

### 3.1 Formal Definitions of the Three Primitives
1. **Chance (`ConfiguredDisturbance`):** An explicit exogenous perturbation inside the storyworld `(disturbance_id, target_scope, rule_or_distribution, seed_key, realized_value)`. Never inferred post-hoc merely because a stochastic generator produced a different clip; separated from (a) viewer epistemic uncertainty, (b) authored counterfactual branches, and (c) renderer/LLM sampling variance.
2. **Memory (Three Strict Levels):**
   - *Level 1 — Persistent World Traces (`world_traces`):* Physical marks remaining in the environment (`oil_spill_polygon`, `lamp_broken`, `char_mark_on_sack_A_hem`).
   - *Level 2 — Character Account (`character_memory[actor_id]`):* Selective, potentially mistaken propositions `(mem_id, source_event_id, acquisition_mode ∈ {direct_sight, sound_cue, communication, inference}, proposition, confidence, retention_rule, retrieved_at_events[])`. An actor's account updates **if and only if** a permitted observation channel (line-of-sight, light state, room co-presence, audible cue) is satisfied at event execution.
   - *Level 3 — Production Archive (`archive_log`):* Revision history, prompts, hashes, critic logs, and rejected branches. Production logs **never** leak into Level 2 character knowledge.
3. **Consequence (`PersistentConsequence`):** A durable mutation across five tracked registers—`(1) physical_state`, `(2) relational_stance`, `(3) character_knowledge`, `(4) viewer_evidence_surface`, and `(5) policy_verdict`—that persists across shot cuts unless undone by a named `REWIND(branch_id, target_snapshot)` branch operation.

### 3.2 Working Olog (Typed Test Diagram)
```text
<source passage>                     [supports or complicates]  <research claim>
<prior world state and character memory> [condition]            <next event>
<configured chance input>            [perturbs]                 <event>
<event>                              [changes]                  <world state and possible continuations>
<permitted observation of an event>  [updates]                  <character memory>
<world state>                        [permits]                  <event with preconditions and effects>
<event>                              [receives]                 <performance score>
<score>                              [renders as]               <time-addressable movement>
<observation>                        [supports or contests]     <interpretation>
<interpretation plus fictional clause> [yields]                 <conditional verdict>
<counterfactual patch>               [revises]                  <case revision>
```
*Commutativity Check as Falsifiable Test:* Event-graph replay predicts observable contact, posture, and consequence facts (`Path 1: Event → World State → Verdict`); blinded inspection of rendered frames checks what is visibly legible on screen (`Path 2: Event → Score → Movement → Viewer/Critic Observation → Verdict`). Disagreement between `Path 1` and `Path 2` is recorded explicitly: **a planned `Goal` in state is not automatically a perceived intention on screen**.

### 3.3 `VTX-0.1` Proposed Case Representation (JSON Skeleton)
```json
{
  "vtx_version": "0.1-proposed",
  "case_id": "pae04_flour_lamp_ab_v1",
  "adaptation_note": "Invented 2-sack room adaptation testing intention, consequence persistence, and synthetic policies; not a recovered Calvino scene.",
  "source_links": ["C1", "C2", "A1"],
  "location_legos": {
    "room_id": "parlor_01",
    "bounds_m": [4.0, 3.0],
    "camera": { "id": "cam_shared_01", "mode": "locked_three_quarter", "fov_deg": 42, "cut_at_s": 9.5 }
  },
  "entities": [
    { "id": "Sack_A", "kind": "flour_sack", "fill_ratio": 0.5, "mass_kg": 12.0, "rest_volume": 1.0, "tint": "#c95a49" },
    { "id": "Sack_B", "kind": "flour_sack", "fill_ratio": 0.5, "mass_kg": 10.5, "rest_volume": 1.0, "tint": "#6089a8" },
    { "id": "Lamp_1", "kind": "oil_lamp", "pos_m": [2.0, 0.75], "lit": true, "tipped": false, "attachment": "table_top" },
    { "id": "Door_1", "kind": "exit_door", "pos_m": [3.6, 0.0], "open": false, "blocked_by": null }
  ],
  "configured_chance_inputs": [
    {
      "id": "Jolt_1",
      "at_event": "E1_settling_jolt",
      "distribution": "fixed_deterministic_test_draw(lateral_impulse_N=18.0, dir='+x')",
      "realized_value": { "impulse_N": 18.0, "dir": "+x" }
    }
  ],
  "initial_character_memory": {
    "Sack_A": [{ "mem_id": "mA0", "prop": "co_tenant(Sack_B)", "confidence": 0.9, "retention_rule": "persist_scene" }],
    "Sack_B": [{ "mem_id": "mB0", "prop": "co_tenant(Sack_A)", "confidence": 0.9, "retention_rule": "persist_scene" }]
  },
  "events": [
    {
      "id": "E2_root_action",
      "actor": "Sack_A",
      "target": "Sack_B | Lamp_1 (patched)",
      "time_interval_s": [3.2, 6.8],
      "legos_slot": { "Goal": "assist_steadying", "Obstacle": "Jolt_1_off_balance", "Shift": "inadvertent_elbow_brush_on_Lamp_1" },
      "bdi_commitment": { "belief_read": ["mA0", "obs_B_stagger"], "desire": "stabilize_B", "intention": "reach_support_B" },
      "preconditions": ["Lamp_1.tipped == false", "distance(Sack_A, Table) <= 0.85"],
      "chance_reads": ["Jolt_1"],
      "motion_score": {
        "anticipation_s": [3.2, 3.6],
        "pose_arc": "open_both_top_ears_toward_Sack_B_center_of_mass_off_axis",
        "contact_interval_s": [4.9, 5.15],
        "contact_pair": ["Sack_A.hip_R", "Lamp_1.base"],
        "weight_curve": "stagger_forward_recover_recoil_back",
        "easing": "cubic_out_overshoot"
      },
      "effects_world": ["Lamp_1.tipped = true", "world_traces.oil_pool = true", "Sack_A.hem_oil_stain = true"],
      "permitted_observations": {
        "Sack_B": { "channel": "direct_sight_lit_room", "observed_cue": "A_ears_oriented_to_B_off_balance_hip_brush", "memory_update": "believe(accident_by_A, conf=0.80)" }
      },
      "evidence_status": { "camera_clear_line_of_sight": true, "corroborated_independent_sensor": false },
      "carried_consequences": ["Lamp_1.tipped", "world_traces.oil_pool", "Sack_B.memory.believe(accident_by_A)"]
    }
  ]
}
```

---

## Part IV — Concrete First Experiment Specification (`Case A` vs. `Case B`)

### 4.1 Baseline Single-Root Goal Comparison (16.0 s, Shared Camera, Same Final Fire)
- **Fixed Across `Case A` and `Case B`:** Room geometry (`parlor_01`), locked camera (`0.0–9.5 s` wide three-quarter shot; `9.5–16.0 s` medium doorway angle after cut, **carrying all physical and memory consequences across the cut**), `Sack_A` and `Sack_B` initial positions and `initial_character_memory`, exogenous disturbance `Jolt_1` (`t = 1.8–3.2 s`, causing `Sack_B` to wobble near the lamp table), ignition time (`E3_ignition`, `t = 6.8–9.5 s`, oil catches flame into identical final fire envelope), and zero captions/narration during perceptual testing.
- **Single Root Patch (`patch_root_goal_A_to_B.json`):** Changes **only** `E2_root_action.goal / bdi_commitment.intention` and its causally required downstream motion, character observation update, subsequent action `E4`, and policy verdicts:

| Stage / Register | **Case A — Assist / Accidental Tip (Baseline)** | **Case B — Deliberate Lamp Tip (Counterfactual Patch)** |
| :--- | :--- | :--- |
| **`E1` (`0.0–3.2 s`) Setup & `Jolt_1`** | `Jolt_1` shakes floor; `Sack_B` tilts toward table edge. *(Identical)* | `Jolt_1` shakes floor; `Sack_B` tilts toward table edge. *(Identical)* |
| **`E2` (`3.2–6.8 s`) Root Goal & Acting Score** | **`goal: assist_steadying`**. `Sack_A` leans quickly toward `Sack_B` with upper corners ("ears") reaching to catch `Sack_B`; off-balance `hip_R` brushes `Lamp_1` (`4.9–5.15 s`), followed by immediate startled recoil toward `Lamp_1` trying vainly to catch it. | **`goal: tip_lamp_deliberately`**. `Sack_A` widens basal stance (settling weight low, `3.2–4.1 s` anticipation), orients torso directly at `Lamp_1` (ignoring `Sack_B`), drives upper-right corner cleanly through `Lamp_1` (`4.9–5.25 s` sustained follow-through), and steps back before flame rises. |
| **`E3` (`6.8–9.5 s`) Consequence & Memory Update** | `Lamp_1` shatters; oil ignites (`Fire_1`); `Sack_A` hem singed. `Sack_B` (facing table in lit room) records `mem_B1: accidental_brush_by_A`, `stance(B→A) = cooperative`. | `Lamp_1` shatters; oil ignites (`Fire_1`); `Sack_A` right corner soot-marked. `Sack_B` (facing table in lit room) records `mem_B1: deliberate_shove_by_A`, `stance(B→A) = threatened`. |
| **`Cut` (`9.5 s`) → `E4` (`9.5–16.0 s`) Required Persistent Downstream Action** | **Traces persist across cut** (fire glow, `Sack_A` singed hem). Reading `mem_B1`, `Sack_B` pulls `Door_1` open and **holds jamb open waiting to pull `Sack_A` through**. | **Traces persist across cut** (fire glow, `Sack_A` soot corner). Reading `mem_B1`, `Sack_B` bolts to `Door_1`, **recoils from `Sack_A`'s approach, and wedges `Door_1` shut from outside**. |

### 4.2 Synthetic Demonstration Policy Verdicts (World State vs. Corroborated Evidence)
Per `<delivery_and_stop>`, because Calvino's story edition is not yet inspected, we evaluate four **explicitly invented synthetic test rules**—separating omniscient **World-State Truth** from **Evidence-Based Adjudication** (where authored `goal` is **forbidden** from counting as visual corroboration):

| Synthetic Clause (Invented Test Rule) | Predicate Definition | `Case A` (World State) | `Case A` (Evidence Only, 1 Uncorroborated Camera / Blinded Viewer) | `Case B` (World State) | `Case B` (Evidence Only, 1 Uncorroborated Camera / Blinded Viewer) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`P1` (Fire Occurrence)** | Pays iff `confirmed(Fire_1 == true)` | `PAY` | `PAY` *(if flame visible in frame)* | `PAY` | `PAY` *(if flame visible in frame)* |
| **`P2` (Accidental Tip)** | Pays iff `confirmed(lamp_tip == accidental)` | `PAY` | `PAY` *iff Perceptual Gate passes; else* `UNKNOWN` | `NO_PAY` | `NO_PAY` *iff deliberate cue clear; else* `UNKNOWN` |
| **`P3` (Deliberate Arson Rider)** | Pays iff `confirmed(lamp_tip == deliberate)` | `NO_PAY` | `NO_PAY` *iff accidental cue clear; else* `UNKNOWN` | `PAY` | `PAY` *iff Perceptual Gate passes; else* `UNKNOWN` |
| **`P4` (Independent Corroboration)** | Pays iff cause corroborated by $\ge 2$ independent evidence channels (e.g., camera + physical trace / second witness) | `NO_PAY` *(if 1 channel)* | **`UNKNOWN`** *(single camera without independent second witness/forensic sensor)* | `NO_PAY` *(if 1 channel)* | **`UNKNOWN`** *(demonstrates evidentiary gap despite known authored state)* |

### 4.3 Follow-On Orthogonal Comparisons (Held Separate; Never Varied Together)
1. **Protocol 2 — Chance Comparison (Goals & Memories Fixed):** Hold `Sack_A.goal = assist_steadying` and `initial_character_memory` fixed; vary **only** `Jolt_1.realized_value` (`18.0 N` strong jolt causing elbow-lamp collision vs. `4.0 N` mild tremor where `Sack_A` steadies `Sack_B` cleanly without contacting `Lamp_1`, blocking `E3_ignition`).
2. **Protocol 3 — Memory Comparison (Observed Scene & Chance Fixed, Plus Control):** Hold `E1` observed physical motion ambiguous (partial smoke/back-turned contact); vary **only** `Sack_B`'s prior retained recollection (`mem_B0_threat: A previously hid lamp oil` vs. `mem_B0_neutral` vs. **`mem_B0_control_irrelevant: wallpaper pattern is striped`**). Predeclared test: `mem_B0_threat` shifts `E4` to flight/barring, whereas `mem_B0_control_irrelevant` must produce **zero change** in `E4`.
3. **Protocol 4 — Embodiment Transfer (`Flower`):** Replay the exact `Case A / Case B` `VTX-0.1` event contract on **Flower** (plant stem/petals rig) to measure what body morphology contributes to intention legibility without changing event logic.
4. **Stress Scenario Model (`100×` Candidate Volume — Analytical Model Only, Not Generated):** At `100×` candidate changesets, four queues saturate in sequence: (1) **Perceptual/Critic Review Queue** (1x playback human bottleneck; saturation signal: rising queue age and rubber-stamp agreement $>95\%$); (2) **Attachment/Frame Inspection Queue** (frame-by-frame carry-contact checks); (3) **Causal Merge Queue** (conflicting patches on shared `world_traces` or exogenous RNG consumption drift—mitigated by event-keyed draws); and (4) **Recovery/Rollback Queue** when a shared rig update invalidates downstream cached checks.

---

## Part V — Frozen Quality Contract & Run-Gate Status (`NOTES` Mode)

| Gate | Frozen Acceptance Bar | Current Status | Verifier & Evidence Note |
| :--- | :--- | :---: | :--- |
| **1. Evidence Gate** | Every historical/technical claim has a verified source locator or is visibly marked `UNRESOLVED`; counts recomputed with stated assumptions; story ≠ 1977 code. | **`PASS` (with 3 named `UNRESOLVED` items)** | Self-checked against fetched `C1`, `C2`, `A1`, `S1`, `B1`, `G1`, `H1`, `L1` + workspace `.docx`. `CL-03` (story edition), `CL-08` (Hassabis), `CL-10` (Lem semaphore) explicitly held open. |
| **2. Structural Gate** | Replay reaches terminal state without precondition violations; A/B diff has 1 root intervention; policies output `PAY`/`NO_PAY`/`UNKNOWN` from versioned clauses. | **`NOT_RUN`** | Specification frozen in Part III–IV; validator execution awaits live `BUILD` request. |
| **3. Animation Gate** | Real squash-and-stretch, anticipation, weight, follow-through, silhouette clarity, depth, and frame-by-frame attachment continuity across carry/contact intervals. | **`NOT_RUN`** | Score intervals (`3.2–6.8 s`, contact `4.9–5.15 s`) specified; Canvas render awaits `BUILD`. |
| **4. Perceptual Gate** | Blinded human/independent viewer distinguishes accidental (`Case A`) vs. deliberate (`Case B`) tipping with **zero captions/narration**, citing visible cues; ambiguous readings preserved. *(Provisional pilot bar to agree with Watson before data collection.)* | **`NOT_RUN` / `PENDING`** | Independent viewer review `PENDING`; no perceptual accuracy claimed. |
| **5. Temporal Gate** | Physical/relational effects persist across `9.5 s` cut into `E4`; character knowledge has explicit observation path; memory comparison includes irrelevant-memory control. | **`NOT_RUN`** | Acquisition path and `E4` persistence specified; runtime trace awaits `BUILD`. |
| **Separate Judgment: Narrative Interest** | Assessed independently of technical validity on consequential alternatives, uncertainty, and motivated surprise. | **`PENDING`** | Reserved for human critical evaluation after baseline pair renders. |

---

## References

- **Anthropic.** (2026). *Redesigning source control at Anthropic* [Scion engineering post, 13 October 2026; updated 15 October 2026]. `https://www.anthropic.com/research/redesigning-source-control` [`S1`]
- **Braffort, P.** (1995 [2002]). *L'ordre dans le crime : une expérience cybernétique avec Italo Calvino* [Expanded from 17 October 1995 lecture at Librairie La Tour de Babel, Paris; quotes Calvino's *Atlas de littérature potentielle* (1981) constraints and Barenghi's *Meridiani* (1994) notes]. `https://www.paulbraffort.net/litterature/critique/calvino_crime.html` [`C2`]
- **Bratman, M. E.** (1987). *Intention, Plans, and Practical Reason*. Cambridge, MA: Harvard University Press.
- **Cain, J. M.** (1943 [1936]). *Double Indemnity*. In *Three of a Kind*. New York: Alfred A. Knopf. *(Proposed close-reading comparator.)*
- **Calvino, E.** (1995 [1993]). Preface to *Numbers in the Dark and Other Stories*, trans. T. Parks. New York: Pantheon Books. Transcription consulted at `https://www.ruanyifeng.com/calvino/2008/11/numbers_in_the_dark_preface_en.html` [`C1`]
- **Calvino, I.** (1973 [1995]). L'incendio della casa abominevole [*Playboy*, 1973; collected in *Prima che tu dica «Pronto»*, Mondadori, 1993; English trans. T. Parks, "The Burning of the Abominable House," in *Numbers in the Dark*, Pantheon, 1995]. *(Direct page inspection of story edition pending for verbatim 12-act and policy audit.)*
- **Duncan, D.** (2012). Calvino, Llull, Lucretius: Two models of literary combinatorics. *Comparative Literature*, 64(1): 93–109.
- **Geertz, C.** (1972 [1973]). Deep play: Notes on the Balinese cockfight. *Dædalus*, 101(1): 1–37; reprinted in *The Interpretation of Cultures* (1973), New York: Basic Books, pp. 412–453 (reading metaphor at p. 452). `https://www.amacad.org/publication/daedalus/deep-play-notes-balinese-cockfight-1972` [`H1`]
- **Hartsoe, W.** (2026). *Can a Language Model Build With LEGO?* and *Video text and the flour sack test: Research notes for the Abominable House project* [Working archive artifacts, 10 November 2026].
- **Hassabis, D., Spreng, R. N., Rusu, A. A., Robbins, C. A., Mar, R. A. and Schacter, D. L.** (2014 [2013]). Imagine all the people: How the brain creates and uses personality models to predict behavior. *Cerebral Cortex*, 24(8): 1979–1987. *(Candidate citation only; intended Hassabis reference held `UNRESOLVED` pending author confirmation.)*
- **Johnston, O. and Thomas, F.** (1981). *Disney Animation: The Illusion of Life*. New York: Abbeville Press.
- **Lem, S.** (1973 [1984]). A history of bitic literature. In *Imaginary Magnitude*, trans. M. E. Heine. San Diego: Harcourt Brace Jovanovich. `https://www.everand.com/book/709063337/Imaginary-Magnitude` [`L1`] *(Bitistics, semascope, and semature verified; brainstormed "semaphore" passage held `UNRESOLVED`.)*
- **Onal, E., Uren, Z. and Güngör, T.** (2025). Evaluating visual storytelling in generative AI. *Digital Humanities 2025: Book of Abstracts*, Lisbon, pp. 120–125.
- **Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. and Bernstein, M. S.** (2023). Generative agents: Interactive simulacra of human behavior. *UIST '23*, Article 2; `https://arxiv.org/abs/2304.03442` [`G1`]. *(Kept distinct from `a16z-infra/ai-town`, `https://github.com/a16z-infra/ai-town`.)*
- **Pichler, A. and Pagel, J.** (2025). Operationalizing focalization in literary texts. *Digital Humanities 2025: Book of Abstracts*, Lisbon, pp. 1011–1013.
- **Rao, A. S. and Georgeff, M. P.** (1995). BDI agents: From theory to practice. *Proceedings of ICMAS-95*, pp. 312–319. `https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf` [`B1`]
- **Soni, A., et al.** (2024 [2025]). VideoAgent: Self-improving video generation. *arXiv preprint* arXiv:2410.10076.
- **Walt Disney Family Museum.** (2020). *Studio Series | Animating a Sack Drop (Youth Session)*. `https://www.waltdisney.org/education/workshops/studio-series-animating-sack-drop-youth-session` [`A1`]
- **Wilder, B. (dir.), Wilder, B. and Chandler, R. (screenplay).** (1944). *Double Indemnity*. Paramount Pictures.

---

## Handoff State (`MILESTONE`)

- **Accepted Revision:** `vtx01_mvvt_notes_and_spec` (`rev-0.1-notes`, saved in artifact directory and workspace `/Users/gaia/burning house/VTX01_MVVT_Research_Memo_and_Spec.md`).
- **Key Assumptions Held:** `NOTES` mode enforced (zero unexecuted renders, studies, or swarm speedups claimed); $12^{12}$ recomputed under explicit dyadic slot assumptions; synthetic demonstration contracts `P1`–`P4` separated across world-state vs. corroborated visual evidence.
- **Outstanding Gates:** `CL-03` (inspect primary *Numbers in the Dark* / *Meridiani* story pages before building the 12-act coverage matrix), `CL-08` & `CL-10` (Watson to confirm intended Hassabis citation and Lem semaphore vs. semascope/semature usage), and Gates 2–5 (`Structural`, `Animation`, `Perceptual`, `Temporal`) `NOT_RUN` pending `BUILD`.
- **Budget Spent / Remaining:** 1 single-worker `NOTES` pass completed within local read/write scope; `BUILD` budget (`max 3 candidate pairs`, `2 repair cycles/gate`, `25% reserved for verification`) `100%` unspent.
- **Single Next Operation:** Either (a) supply/confirm the primary story edition pages and Hassabis/Lem locators to close the three open `Evidence Gate` items, or (b) issue a live **`BUILD`** request to implement, validate, render, and inspect the baseline `Case A / Case B` (`assist_steadying` vs. `tip_lamp_deliberately`) HTML5 Canvas + `VTX-0.1` JSON pair.
