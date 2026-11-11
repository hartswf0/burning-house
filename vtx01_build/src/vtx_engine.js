/**
 * VTX-0.1 Deterministic Simulation, Kinematic Flour-Sack Rig & 2.5D Display-List Engine (rev2)
 * Runs identically in Node.js (validation & MP4 frame generation) and Browser HTML5 Canvas.
 * Zero captions or labels are drawn inside the scene frame (Perceptual Gate invariant).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.VTXEngine = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const W = 1280;
  const H = 720;

  function hashString(str) {
    let h = 2166136261 >>> 0;
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  function eventKeyedScalar(seed, key, idx) {
    let a = (hashString(String(seed) + ':' + key) + Math.imul(idx + 1, 2654435761)) >>> 0;
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  function lerp(a, b, u) {
    return a + (b - a) * u;
  }

  function smoothstep(t0, t1, t) {
    const u = clamp((t - t0) / Math.max(1e-6, t1 - t0), 0, 1);
    return u * u * (3 - 2 * u);
  }

  function easeOutBack(u) {
    const c1 = 1.55;
    const c3 = c1 + 1;
    const x = clamp(u, 0, 1) - 1;
    return 1 + c3 * x * x * x + c1 * x * x;
  }

  function easeInOutCubic(u) {
    const x = clamp(u, 0, 1);
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  }

  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * Hop-locked locomotion solver: guarantees 0.000 px/frame grounded base skating!
   * Horizontal x/z change ONLY while airborne inside a declared hop [t0, t1].
   */
  function evaluateHopChain(t, startX, startZ, hops) {
    let x = startX;
    let z = startZ;
    let y = 0.0;
    let grounded = true;
    for (const h of hops) {
      if (t >= h.t1) {
        x = h.x1;
        z = h.z1;
      } else if (t > h.t0) {
        const u = clamp((t - h.t0) / (h.t1 - h.t0), 0, 1);
        const uEase = easeInOutCubic(u);
        x = lerp(x, h.x1, uEase);
        z = lerp(z, h.z1, uEase);
        y = h.apex * Math.sin(Math.PI * u);
        grounded = y <= 1e-5;
        break;
      } else {
        break;
      }
    }
    return { x, y, z, grounded };
  }

  function applyPatch(baseCase, patchSpec) {
    const next = deepClone(baseCase);
    for (const op of patchSpec.operations) {
      const parts = op.path.split('/').slice(1).map((p) => p.replace(/~1/g, '/').replace(/~0/g, '~'));
      let cur = next;
      for (let i = 0; i < parts.length - 1; i++) {
        const k = Array.isArray(cur) ? Number(parts[i]) : parts[i];
        cur = cur[k];
      }
      const last = Array.isArray(cur) ? Number(parts[parts.length - 1]) : parts[parts.length - 1];
      if (op.op === 'replace' || op.op === 'add') {
        cur[last] = deepClone(op.value);
      } else if (op.op === 'remove') {
        if (Array.isArray(cur)) cur.splice(last, 1);
        else delete cur[last];
      }
    }
    return next;
  }

  function checkPrecondition(expr, world, charMem) {
    if (expr === 'world.lamp_tipped == false') return world.lamp_tipped === false;
    if (expr === 'world.lamp_tipped == true') return world.lamp_tipped === true;
    if (expr === 'world.b_off_balance == true') return world.b_off_balance === true;
    if (expr === 'world.oil_pool_radius > 0.1') return (world.oil_pool_radius || 0) > 0.1;
    if (expr === 'world.fire_confirmed == true') return world.fire_confirmed === true;
    if (expr === "memory.Sack_B.has('mem_B_obs_E2')") {
      return (charMem.Sack_B || []).some((m) => m.mem_id === 'mem_B_obs_E2');
    }
    return true;
  }

  function replayCase(vtxCase, policiesSpec) {
    const world = deepClone(vtxCase.initial_world_state);
    const charMem = deepClone(vtxCase.initial_character_memory);
    const chanceMap = {};
    for (const c of vtxCase.configured_chance_inputs || []) {
      const checkScalar = eventKeyedScalar(c.seed, c.event_key, 0);
      chanceMap[c.id] = Object.assign({}, c, { deterministic_key_hash_u01: Number(checkScalar.toFixed(6)) });
    }

    const snapshots = [{ after_event: 'INIT', at_s: 0.0, world: deepClone(world), character_memory: deepClone(charMem) }];
    const preconditionLog = [];
    const memoryTrace = [];
    const consequenceTrace = [];

    for (const ev of vtxCase.events) {
      for (const pre of ev.preconditions || []) {
        const ok = checkPrecondition(pre, world, charMem);
        preconditionLog.push({ event_id: ev.id, precondition: pre, satisfied: ok });
        if (!ok) {
          throw new Error(`Precondition failed at ${ev.id}: ${pre}`);
        }
      }

      for (const readId of ev.memory_reads || []) {
        const actorMemList = charMem[ev.actor] || [];
        const found = actorMemList.find((m) => m.mem_id === readId);
        memoryTrace.push({
          phase: 'RETRIEVE',
          at_event: ev.id,
          actor: ev.actor,
          mem_id: readId,
          found: Boolean(found),
          proposition: found ? found.proposition : null
        });
      }

      const wu = (ev.effects && ev.effects.world_updates) || {};
      for (const k of Object.keys(wu)) {
        const prev = world[k];
        world[k] = deepClone(wu[k]);
        consequenceTrace.push({
          from_event: ev.id,
          at_s: ev.time_interval_s[1],
          field: k,
          prev_value: prev,
          new_value: world[k],
          persists_across_cut: ev.time_interval_s[1] <= 9.5
        });
      }

      const obs = (ev.effects && ev.effects.character_observations) || {};
      for (const actorId of Object.keys(obs)) {
        const entry = obs[actorId];
        if (!charMem[actorId]) charMem[actorId] = [];
        const memRecord = {
          mem_id: entry.mem_id,
          source_event: ev.id,
          at_s: ev.time_interval_s[1],
          acquired_via: entry.channel,
          proposition: entry.proposition,
          confidence: entry.confidence,
          retention_rule: entry.retention_rule
        };
        charMem[actorId].push(memRecord);
        memoryTrace.push(Object.assign({ phase: 'WRITE_OBSERVATION', actor: actorId }, memRecord));
      }

      snapshots.push({
        after_event: ev.id,
        at_s: ev.time_interval_s[1],
        world: deepClone(world),
        character_memory: deepClone(charMem)
      });
    }

    const isAssist = vtxCase.events[1].goal === 'assist_steadying';
    const downstreamActionImpact = [
      {
        consequence: 'world.lamp_tipped = true & world.oil_pool_radius = 0.28',
        source_event: 'E2_root_action',
        enables: ['E3_oil_ignition (spilled oil catches live wick)'],
        blocks: ['continued_lit_parlor_lamp'],
        unchanged: ['camera_cut_schedule_at_9.5s', 'Jolt_1_history']
      },
      {
        consequence: isAssist
          ? 'Sack_B.memory.mem_B_obs_E2 = accidental_while_assisting & stance = cooperative'
          : 'Sack_B.memory.mem_B_obs_E2 = deliberate_strike_by_A & stance = threatened',
        source_event: 'E2_root_action',
        enables: isAssist
          ? ['E4: Sack_B props Door_1 open with Wedge_1 and reaches back to pull Sack_A out']
          : ['E4: Sack_B exits Door_1, slams leaf shut, and jams Wedge_1 on outer threshold'],
        blocks: isAssist
          ? ['hostile_door_barring_against_Sack_A']
          : ['cooperative_joint_exit_for_Sack_A'],
        unchanged: ['Wedge_1 pickup time (10.50 s) and carry interval [10.50, 13.50] s', 'Fire_1 growth curve']
      },
      {
        consequence: isAssist ? 'world.sack_a_mark = hem_singed_char' : 'world.sack_a_mark = ear_R_soot_char',
        source_event: 'E2_root_action -> E3_oil_ignition',
        enables: ['persistent visual forensic trace on Sack_A across the 9.5 s camera cut'],
        blocks: ['clean_unmarked_actor_reset_after_cut'],
        unchanged: ['Sack_A rest volume invariant']
      }
    ];

    const evidenceSurface = {
      fire_visible_in_camera: true,
      viewer_blinded_verdict: 'UNKNOWN_UNTESTED_HUMAN_VIEWERS',
      independent_corroborated_channels: 1
    };

    const policyResults = (policiesSpec ? policiesSpec.clauses : []).map((cl) => {
      let worldVerdict = 'UNKNOWN';
      let evidenceVerdict = 'UNKNOWN';
      if (cl.id === 'P1') {
        worldVerdict = world.fire_confirmed === true ? 'PAY' : 'NO_PAY';
        evidenceVerdict = evidenceSurface.fire_visible_in_camera === true ? 'PAY' : 'UNKNOWN';
      } else if (cl.id === 'P2') {
        worldVerdict = world.lamp_tipped && world.lamp_tip_mode === 'accidental' ? 'PAY' : 'NO_PAY';
        evidenceVerdict =
          evidenceSurface.viewer_blinded_verdict === 'accidental'
            ? 'PAY'
            : evidenceSurface.viewer_blinded_verdict === 'deliberate'
            ? 'NO_PAY'
            : 'UNKNOWN';
      } else if (cl.id === 'P3') {
        worldVerdict = world.lamp_tipped && world.lamp_tip_mode === 'deliberate' ? 'PAY' : 'NO_PAY';
        evidenceVerdict =
          evidenceSurface.viewer_blinded_verdict === 'deliberate'
            ? 'PAY'
            : evidenceSurface.viewer_blinded_verdict === 'accidental'
            ? 'NO_PAY'
            : 'UNKNOWN';
      } else if (cl.id === 'P4') {
        worldVerdict = (world.independent_cause_channels || 1) >= 2 ? 'PAY' : 'NO_PAY';
        evidenceVerdict = evidenceSurface.independent_corroborated_channels >= 2 ? 'PAY' : 'UNKNOWN';
      }
      return {
        clause_id: cl.id,
        name: cl.name,
        version: cl.version,
        predicate: cl.predicate,
        world_verdict: worldVerdict,
        evidence_verdict: evidenceVerdict,
        world_facts_used:
          cl.id === 'P1'
            ? { fire_confirmed: world.fire_confirmed }
            : cl.id === 'P4'
            ? { independent_cause_channels: world.independent_cause_channels }
            : { lamp_tipped: world.lamp_tipped, lamp_tip_mode: world.lamp_tip_mode },
        evidence_facts_used:
          cl.id === 'P1'
            ? { fire_visible_in_camera: evidenceSurface.fire_visible_in_camera }
            : cl.id === 'P4'
            ? { independent_corroborated_channels: evidenceSurface.independent_corroborated_channels }
            : { viewer_blinded_verdict: evidenceSurface.viewer_blinded_verdict }
      };
    });

    return {
      case_id: vtxCase.case_id,
      revision: vtxCase.revision,
      terminal_world: world,
      terminal_character_memory: charMem,
      chance_trace: chanceMap,
      precondition_log: preconditionLog,
      snapshots,
      memory_trace: memoryTrace,
      consequence_trace: consequenceTrace,
      downstream_action_impact: downstreamActionImpact,
      policy_results: policyResults
    };
  }

  function getActiveCamera(vtxCase, t, joltShakeX, joltShakeY) {
    const cuts = vtxCase.timeline.camera_cuts;
    const shot = t < 9.5 ? cuts[0] : cuts[1];
    return {
      shot_id: shot.shot_id,
      cx: shot.camera.cx + joltShakeX,
      cy: shot.camera.cy + joltShakeY,
      zoom: shot.camera.zoom
    };
  }

  function project(x, y, z, cam) {
    const depthScale = 1.0 / (0.62 + 0.72 * z);
    const floorHorizonY = H * 0.34;
    const worldScale = 470 * cam.zoom * depthScale;
    const sx = W * 0.5 + (x - cam.cx) * worldScale;
    const floorY = floorHorizonY + (1.0 - z) * 370 * cam.zoom + (cam.cy - 0.42) * 180;
    const sy = floorY - y * worldScale;
    return { x: sx, y: sy, scale: worldScale };
  }

  function polygonArea(pts) {
    let a = 0;
    for (let i = 0; i < pts.length; i++) {
      const p1 = pts[i];
      const p2 = pts[(i + 1) % pts.length];
      a += p1[0] * p2[1] - p2[0] * p1[1];
    }
    return Math.abs(a) * 0.5;
  }

  function cubicPt(p0, p1, p2, p3, u) {
    const v = 1 - u;
    return [
      v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0],
      v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]
    ];
  }

  /**
   * Exact area-preserving, non-self-intersecting articulated flour-sack builder (rev2).
   * Enforces strict ear separation (earR.x > earL.x + minGap) so contours never bowtie,
   * then applies exact base-anchored uniform area normalization (|volumeRatio - 1| < 1e-4).
   */
  function buildFlourSack(spec, pose, cam) {
    const baseProj = project(pose.x, pose.y || 0, pose.z, cam);
    const S = baseProj.scale;
    const restW = spec.rest_width * S;
    const restH = spec.rest_height * S;
    const targetArea = restW * restH * 0.86;

    const squash = clamp(pose.squash || 1.0, 0.70, 1.28);
    const invSquash = 1.0 / Math.sqrt(squash);
    const lean = clamp(pose.lean || 0.0, -0.78, 0.78);
    const twist = clamp(pose.twist || 0.0, -1, 1);

    const hCur = restH * squash;
    const wBase = restW * (0.55 * invSquash);
    const wWaist = restW * (0.42 * invSquash);
    const wShoulder = restW * (0.45 * Math.sqrt(squash));

    const sinL = Math.sin(lean);
    const cosL = Math.cos(lean);

    const crownX = sinL * hCur * 0.88;
    const crownY = -cosL * hCur * 0.88;
    const midX = sinL * hCur * 0.44 + (pose.bellyShiftX || 0) * restW;
    const midY = -cosL * hCur * 0.44;

    // Enforce non-crossing ears relative to crown so contour stays strictly simple (non-bowtie)
    let eLX = crownX - wShoulder + clamp(pose.earL_dx || 0, -0.55, 0.22) * restW;
    let eRX = crownX + wShoulder + clamp(pose.earR_dx || 0, -0.22, 0.88) * restW;
    if (eRX - eLX < restW * 0.36) {
      const midE = 0.5 * (eLX + eRX);
      eLX = midE - restW * 0.18;
      eRX = midE + restW * 0.18;
    }
    const eLY = crownY - restH * 0.13 + clamp(pose.earL_dy || 0, -0.45, 0.36) * restH;
    const eRY = crownY - restH * 0.13 + clamp(pose.earR_dy || 0, -0.45, 0.42) * restH;

    const rawHipL = [-wBase, -restH * 0.02];
    const rawHipR = [wBase, -restH * 0.02];
    const rawBellySag = [0, restH * 0.042 * invSquash];
    const rawWaistL = [midX - wWaist * 1.10, midY];
    const rawWaistR = [midX + wWaist * 1.10, midY];
    const rawEL = [eLX, eLY];
    const rawER = [eRX, eRY];
    const rawSagTop = [crownX, Math.max(eLY, eRY) + restH * 0.06];

    const segs = [
      [rawHipL, [-wBase * 0.45, rawBellySag[1]], [wBase * 0.45, rawBellySag[1]], rawHipR],
      [rawHipR, [lerp(rawHipR[0], rawWaistR[0], 0.45), midY * 0.45], [rawWaistR[0], midY * 1.02], rawER],
      [rawER, [lerp(rawER[0], rawSagTop[0], 0.55), rawSagTop[1]], [lerp(rawEL[0], rawSagTop[0], 0.55), rawSagTop[1]], rawEL],
      [rawEL, [rawWaistL[0], midY * 1.02], [lerp(rawHipL[0], rawWaistL[0], 0.45), midY * 0.45], rawHipL]
    ];

    const rawPts = [];
    for (const seg of segs) {
      for (let k = 0; k < 16; k++) {
        rawPts.push(cubicPt(seg[0], seg[1], seg[2], seg[3], k / 16));
      }
    }

    // Exact base-anchored similarity scale kArea = sqrt(targetArea / rawArea) -> 0.00% volume drift!
    const rawArea = Math.max(1, polygonArea(rawPts));
    const kArea = Math.sqrt(targetArea / rawArea);
    const scalePt = (p) => [baseProj.x + p[0] * kArea, baseProj.y + p[1] * kArea];

    const contour = rawPts.map(scalePt);
    const actualArea = polygonArea(contour);

    const seamOffset = twist * wWaist * 0.48;
    const seamPts = [];
    for (let k = 0; k <= 10; k++) {
      const u = k / 10;
      const p = cubicPt(
        [seamOffset * 0.35, 0],
        [midX + seamOffset, midY * 0.55],
        [midX + seamOffset * 0.85, midY * 1.05],
        [rawSagTop[0] + seamOffset * 0.3, rawSagTop[1]],
        u
      );
      seamPts.push(scalePt(p));
    }

    const creasePts = [];
    for (let k = 0; k <= 8; k++) {
      const u = k / 8;
      const p = cubicPt(
        [rawWaistL[0] * 0.72, midY * 0.68],
        [midX - restW * 0.08, midY * 0.50],
        [midX + restW * 0.08, midY * 0.50],
        [rawWaistR[0] * 0.72, midY * 0.68],
        u
      );
      creasePts.push(scalePt(p));
    }

    return {
      id: spec.id,
      baseScreen: [baseProj.x, baseProj.y],
      contour,
      seamPts,
      creasePts,
      targetArea,
      actualArea,
      volumeRatio: actualArea / targetArea,
      landmarks: {
        hip_L: scalePt(rawHipL),
        hip_R: scalePt(rawHipR),
        ear_L: scalePt(rawEL),
        ear_R: scalePt(rawER),
        crown: scalePt(rawSagTop),
        waist_R: scalePt(rawWaistR),
        waist_L: scalePt(rawWaistL)
      }
    };
  }

  function evaluateFrame(vtxCase, tInput, opts) {
    const options = opts || {};
    const t = clamp(tInput, 0, vtxCase.timeline.duration_s);
    const isAssist = vtxCase.events[1].goal === 'assist_steadying';
    const joltCfg = vtxCase.configured_chance_inputs[0];
    const joltAmp = (joltCfg.realized_value.impulse_N / 18.0) * 0.018;

    // 1. Exogenous floorboard jolt (1.80s - 3.10s) — IDENTICAL across Case A & Case B
    let joltShakeX = 0;
    let joltShakeY = 0;
    if (t >= 1.80 && t <= 3.10) {
      const env = Math.sin(Math.PI * clamp((t - 1.80) / 1.30, 0, 1));
      const decay = Math.exp(-(t - 1.80) * 2.4);
      joltShakeX = Math.sin((t - 1.80) * 34.0) * joltAmp * env * decay;
      joltShakeY = Math.cos((t - 1.80) * 46.0) * joltAmp * 0.65 * env * decay;
    }

    const cam = getActiveCamera(vtxCase, t, joltShakeX, joltShakeY);
    const loc = vtxCase.location_legos;

    // 2. Hop-locked locomotion chains (zero grounded skating!)
    const hopsA = isAssist
      ? [
          // Quick approach hop toward center table to help stumbling Sack_B
          { t0: 3.45, t1: 4.08, x1: -0.36, z1: 0.54, apex: 0.08 },
          // Airborne assist bound reaching high toward Sack_B while waist_R clips Lamp_1 at t=4.90s!
          { t0: 4.20, t1: 5.15, x1: -0.08, z1: 0.53, apex: 0.25 },
          // Startled recoil hop backward upon knocking Lamp_1
          { t0: 5.26, t1: 5.88, x1: -0.36, z1: 0.53, apex: 0.09 },
          // Aborted little step forward trying to catch fallen lamp
          { t0: 6.05, t1: 6.55, x1: -0.28, z1: 0.53, apex: 0.04 },
          // E3 move behind fire toward doorway
          { t0: 8.05, t1: 9.25, x1: 0.06, z1: 0.62, apex: 0.09 },
          // E4 hops across parlor to join Sack_B at wedged-open doorway
          { t0: 9.85, t1: 11.15, x1: 0.34, z1: 0.58, apex: 0.07 },
          { t0: 11.45, t1: 12.85, x1: 0.62, z1: 0.53, apex: 0.07 },
          { t0: 13.20, t1: 14.40, x1: 0.80, z1: 0.49, apex: 0.06 },
          { t0: 14.70, t1: 15.90, x1: 1.02, z1: 0.47, apex: 0.06 }
        ]
      : [
          // Deliberate setup hop into striking stance at x=-0.35
          { t0: 3.22, t1: 3.70, x1: -0.35, z1: 0.54, apex: 0.07 },
          // Composed retreat hop away from spilled oil after deliberate strike
          { t0: 5.60, t1: 6.45, x1: -0.56, z1: 0.55, apex: 0.07 },
          // E3 hops behind fire toward doorway
          { t0: 7.45, t1: 8.35, x1: -0.26, z1: 0.61, apex: 0.07 },
          { t0: 8.50, t1: 9.35, x1: 0.04, z1: 0.62, apex: 0.07 },
          // E4 rushes toward doorway, stopped cold by slammed & wedged Door_1!
          { t0: 9.75, t1: 10.95, x1: 0.38, z1: 0.57, apex: 0.08 },
          { t0: 11.15, t1: 12.35, x1: 0.70, z1: 0.52, apex: 0.08 },
          { t0: 12.50, t1: 13.30, x1: 0.88, z1: 0.49, apex: 0.06 },
          // Blocked recoil hop back from locked door
          { t0: 13.45, t1: 14.20, x1: 0.76, z1: 0.51, apex: 0.05 }
        ];

    const hopsB = isAssist
      ? [
          // E1 Jolt_1 pitches Sack_B leftward in involuntary stumble hop (IDENTICAL in A & B!)
          { t0: 1.88, t1: 2.58, x1: 0.28, z1: 0.55, apex: 0.05 },
          // Startled hop back when Lamp_1 shatters
          { t0: 5.20, t1: 5.88, x1: 0.40, z1: 0.54, apex: 0.07 },
          // E3 hop to doorway / wedge ledge
          { t0: 7.15, t1: 8.45, x1: 0.74, z1: 0.48, apex: 0.09 },
          // E4 carries Wedge_1 [10.50, 13.50]s from ledge (0.74) to base of swung-open Door_1 (x=0.83, z=0.58 -> ear_R at 1.05!)
          { t0: 10.85, t1: 12.35, x1: 0.83, z1: 0.58, apex: 0.07 },
          // Joint exit hop through propped-open doorway with partner Sack_A
          { t0: 14.75, t1: 15.90, x1: 1.18, z1: 0.46, apex: 0.06 }
        ]
      : [
          // E1 Jolt_1 involuntary stumble hop (IDENTICAL in A & B!)
          { t0: 1.88, t1: 2.58, x1: 0.28, z1: 0.55, apex: 0.05 },
          // Recovers footing hop alone
          { t0: 3.45, t1: 4.25, x1: 0.38, z1: 0.55, apex: 0.04 },
          // Alarmed recoil leap away from Sack_A's deliberate strike!
          { t0: 4.95, t1: 5.70, x1: 0.62, z1: 0.52, apex: 0.10 },
          // E3 flees to wedge ledge
          { t0: 6.95, t1: 8.15, x1: 0.74, z1: 0.48, apex: 0.08 },
          // E4 carries Wedge_1 [10.50, 13.50]s THROUGH doorway into hallway behind outer latch (x=1.10, z=0.35 -> ear_R at outer latch base 1.25, 0.31!)
          { t0: 10.70, t1: 12.00, x1: 1.10, z1: 0.35, apex: 0.08 },
          // Steps back deeper into visible cutaway hallway after jamming Wedge_1 at 13.50s
          { t0: 13.75, t1: 15.10, x1: 1.38, z1: 0.42, apex: 0.06 }
        ];

    const locA = evaluateHopChain(t, -0.66, 0.56, hopsA);
    const locB = evaluateHopChain(t, 0.44, 0.55, hopsB);

    const poseA = {
      x: locA.x,
      y: locA.y,
      z: locA.z,
      grounded: locA.grounded,
      squash: 1.0 + 0.015 * Math.sin(t * 2.4),
      lean: 0.04,
      twist: 0.45,
      earL_dx: -0.04,
      earL_dy: 0.02,
      earR_dx: 0.05,
      earR_dy: 0.01
    };

    const poseB = {
      x: locB.x,
      y: locB.y,
      z: locB.z,
      grounded: locB.grounded,
      squash: 1.0 + 0.016 * Math.sin(t * 2.6 + 1.1),
      lean: -0.04,
      twist: -0.45,
      earL_dx: -0.05,
      earL_dy: 0.01,
      earR_dx: 0.04,
      earR_dy: 0.02
    };

    // Phase E1 (0.0 - 3.20s): Identical posture across Case A & Case B
    if (t >= 1.85 && t < 3.20) {
      const uStag = smoothstep(1.85, 2.58, t);
      const wobble = 0.07 * Math.sin((t - 1.85) * 11.0) * smoothstep(1.85, 2.2, t);
      poseB.lean = lerp(-0.04, -0.48, uStag) + wobble;
      poseB.squash = lerp(1.0, 1.08, uStag);
      poseB.earL_dx = lerp(-0.05, -0.36, uStag);
      poseB.earL_dy = lerp(0.01, -0.22, uStag);
      poseB.earR_dx = lerp(0.04, 0.22, uStag);
      poseB.earR_dy = lerp(0.02, -0.14, uStag);

      const uAlert = smoothstep(2.05, 3.15, t);
      poseA.squash = lerp(1.0, 1.05, uAlert);
      poseA.lean = lerp(0.04, 0.12, uAlert);
      poseA.earR_dy = lerp(0.01, -0.12, uAlert);
      poseA.earL_dy = lerp(0.02, -0.10, uAlert);
    }

    // Phase E2 & E3 (3.20 - 9.50s)
    if (t >= 3.20 && t < 9.50) {
      if (isAssist) {
        if (t < 3.62) {
          const u = smoothstep(3.20, 3.62, t);
          poseA.squash = lerp(1.05, 0.82, u);
          poseA.lean = lerp(0.12, 0.24, u);
          poseA.earL_dy = lerp(-0.10, -0.22, u);
          poseA.earR_dx = lerp(0.05, 0.34, u);
          poseA.earR_dy = lerp(-0.12, -0.30, u);
        } else if (t < 5.15) {
          const uMove = smoothstep(3.62, 4.95, t);
          poseA.lean = lerp(0.24, 0.56, uMove);
          poseA.squash = poseA.grounded ? 0.92 : 1.15;
          poseA.twist = 0.70;
          poseA.earR_dx = lerp(0.34, 0.78, uMove);
          poseA.earR_dy = lerp(-0.30, -0.36, uMove);
          poseA.earL_dx = lerp(-0.04, 0.18, uMove);
          poseA.earL_dy = lerp(-0.22, -0.32, uMove);
        } else if (t < 6.80) {
          const uRec = smoothstep(5.15, 5.85, t);
          const uDip = smoothstep(5.95, 6.65, t);
          poseA.lean = lerp(0.56, -0.30, uRec) + uDip * 0.48;
          poseA.squash = lerp(0.92, 1.18, uRec) - uDip * 0.22;
          poseA.earR_dx = lerp(0.78, 0.10, uRec) + uDip * 0.26;
          poseA.earR_dy = lerp(-0.36, -0.44, uRec) + uDip * 0.42;
          poseA.earL_dx = lerp(0.18, -0.18, uRec);
          poseA.earL_dy = lerp(-0.32, -0.42, uRec) + uDip * 0.30;
        } else {
          poseA.lean = 0.24;
          poseA.squash = poseA.grounded ? 0.95 : 1.06;
          poseA.twist = 0.65;
          poseA.earR_dx = 0.24;
          poseA.earR_dy = -0.10;
        }

        if (t < 4.50) {
          poseB.lean = -0.48 + 0.04 * Math.sin(t * 9.0);
          poseB.squash = 1.06;
          poseB.earL_dx = -0.38;
          poseB.earL_dy = -0.24;
        } else if (t < 6.80) {
          const uSteady = smoothstep(4.45, 5.05, t);
          const uStartle = smoothstep(5.20, 5.90, t);
          poseB.lean = lerp(-0.48, -0.05, uSteady) + uStartle * 0.16;
          poseB.squash = lerp(1.06, 0.96, uSteady) + uStartle * 0.12;
          poseB.earL_dx = lerp(-0.38, -0.16, uSteady);
          poseB.earL_dy = lerp(-0.24, -0.34, uStartle);
        } else {
          poseB.lean = 0.22;
          poseB.squash = poseB.grounded ? 0.96 : 1.06;
          poseB.twist = lerp(-0.45, 0.50, smoothstep(7.0, 8.0, t));
          poseB.earL_dx = -0.22;
          poseB.earL_dy = -0.14;
        }
      } else {
        // CASE B: Deliberate planted coil -> horizontal strike -> controlled step-back
        if (t < 4.25) {
          const uCoil = smoothstep(3.65, 4.22, t);
          poseA.squash = lerp(1.05, 0.74, uCoil);
          poseA.lean = lerp(0.12, -0.38, uCoil);
          poseA.twist = lerp(0.45, -0.35, uCoil);
          poseA.earR_dx = lerp(0.05, -0.18, uCoil);
          poseA.earR_dy = lerp(-0.12, 0.08, uCoil);
          poseA.earL_dx = lerp(-0.04, -0.26, uCoil);
          poseA.earL_dy = lerp(-0.10, 0.06, uCoil);
        } else if (t < 5.55) {
          const uStrike = easeOutBack(clamp((t - 4.25) / (5.00 - 4.25), 0, 1));
          poseA.squash = lerp(0.74, 1.05, clamp((t - 4.25) / 0.65, 0, 1));
          poseA.lean = lerp(-0.38, 0.58, clamp(uStrike, 0, 1.10));
          poseA.twist = lerp(-0.35, 0.85, clamp((t - 4.25) / 0.60, 0, 1));
          poseA.earR_dx = lerp(-0.18, 0.86, clamp(uStrike, 0, 1.12));
          poseA.earR_dy = lerp(0.08, -0.04, clamp((t - 4.25) / 0.65, 0, 1));
          poseA.earL_dx = -0.18;
          poseA.earL_dy = 0.04;
        } else if (t < 6.80) {
          const uBack = smoothstep(5.55, 6.50, t);
          poseA.lean = lerp(0.58, 0.06, uBack);
          poseA.squash = lerp(1.05, 0.94, uBack);
          poseA.twist = 0.55;
          poseA.earR_dx = lerp(0.86, 0.14, uBack);
          poseA.earR_dy = lerp(-0.04, 0.04, uBack);
        } else {
          poseA.lean = 0.26;
          poseA.squash = poseA.grounded ? 0.94 : 1.06;
          poseA.twist = 0.70;
          poseA.earR_dx = 0.28;
          poseA.earR_dy = -0.06;
        }

        if (t < 4.75) {
          const uSelfRec = smoothstep(3.20, 4.45, t);
          poseB.lean = lerp(-0.48, -0.06, uSelfRec);
          poseB.squash = lerp(1.08, 0.96, uSelfRec);
          poseB.earL_dx = lerp(-0.36, -0.10, uSelfRec);
          poseB.earL_dy = lerp(-0.22, -0.04, uSelfRec);
        } else if (t < 6.80) {
          const uShock = smoothstep(4.85, 5.65, t);
          poseB.lean = lerp(-0.06, 0.38, uShock);
          poseB.squash = lerp(0.96, 1.18, uShock);
          poseB.earL_dx = -0.24;
          poseB.earL_dy = -0.38;
          poseB.earR_dx = 0.28;
          poseB.earR_dy = -0.36;
        } else {
          poseB.lean = 0.26;
          poseB.squash = poseB.grounded ? 0.96 : 1.06;
          poseB.twist = 0.55;
          poseB.earR_dx = 0.24;
          poseB.earR_dy = -0.10;
        }
      }
    }

    // Phase E4 (9.50 - 16.00s): Doorway Consequence & Carried Wedge_1 [10.50, 13.50]s
    let doorOpenFrac = 0.12;
    if (t >= 9.50) {
      if (isAssist) {
        doorOpenFrac = lerp(0.12, 0.94, smoothstep(9.60, 10.45, t));
        if (t < 10.50) {
          const u = smoothstep(9.50, 10.50, t);
          poseB.lean = lerp(0.18, 0.26, u);
          poseB.squash = lerp(0.98, 0.88, u);
          poseB.twist = 0.55;
          poseB.earR_dx = lerp(0.20, 0.44, u);
          poseB.earR_dy = lerp(-0.10, 0.16, u);
        } else if (t <= 13.50) {
          const uStoop = smoothstep(12.45, 13.50, t);
          poseB.squash = lerp(0.96, 0.74, uStoop) + (poseB.grounded ? 0 : 0.08);
          poseB.lean = lerp(0.26, 0.54, uStoop);
          poseB.twist = 0.65;
          poseB.earR_dx = lerp(0.44, 0.62, uStoop);
          poseB.earR_dy = lerp(0.16, 0.36, uStoop);
        } else {
          const uReachBack = smoothstep(13.50, 14.45, t);
          poseB.squash = lerp(0.74, 1.04, uReachBack);
          poseB.lean = lerp(0.54, -0.28, uReachBack);
          poseB.twist = lerp(0.65, -0.55, uReachBack);
          poseB.earL_dx = lerp(-0.10, -0.50, uReachBack);
          poseB.earL_dy = lerp(-0.04, -0.16, uReachBack);
          poseB.earR_dx = 0.16;
          poseB.earR_dy = -0.06;
        }

        poseA.lean = 0.28;
        poseA.squash = poseA.grounded ? 0.95 : 1.05;
        poseA.twist = 0.65;
        poseA.earR_dx = lerp(0.24, 0.54, smoothstep(13.80, 14.50, t));
        poseA.earR_dy = -0.16;
      } else {
        // CASE B E4: Sack_B carries Wedge_1 out into hallway (x=1.12, z=0.52), slams solid angled Door_1 shut [12.1-12.8s],
        // and leans forward-right (lean=+0.52, earR on +x!) so ear_R cleanly wedges outer door base at (x=1.22, z=0.35) with ZERO bowtie!
        if (t < 11.80) {
          doorOpenFrac = lerp(0.12, 0.88, smoothstep(9.55, 10.35, t));
        } else {
          doorOpenFrac = lerp(0.88, 0.0, smoothstep(12.05, 12.80, t));
        }

        if (t < 10.50) {
          const u = smoothstep(9.50, 10.50, t);
          poseB.lean = 0.24;
          poseB.squash = lerp(0.98, 0.88, u);
          poseB.twist = 0.55;
          poseB.earR_dx = lerp(0.22, 0.44, u);
          poseB.earR_dy = lerp(-0.08, 0.16, u);
        } else if (t <= 13.50) {
          const uStoopJam = smoothstep(12.35, 13.50, t);
          poseB.squash = lerp(0.96, 0.72, uStoopJam) + (poseB.grounded ? 0 : 0.08);
          poseB.lean = lerp(0.28, 0.52, uStoopJam);
          poseB.twist = 0.55;
          poseB.earR_dx = lerp(0.44, 0.56, uStoopJam);
          poseB.earR_dy = lerp(0.16, 0.38, uStoopJam);
          poseB.earL_dx = -0.16;
          poseB.earL_dy = -0.04;
        } else {
          const uStand = smoothstep(13.50, 14.30, t);
          poseB.squash = lerp(0.72, 1.02, uStand);
          poseB.lean = lerp(0.52, -0.14, uStand);
          poseB.twist = lerp(0.55, -0.60, uStand);
          poseB.earR_dx = lerp(0.56, 0.10, uStand);
          poseB.earR_dy = lerp(0.38, 0.02, uStand);
        }

        const uBlocked = smoothstep(13.30, 14.20, t);
        poseA.lean = lerp(0.32, -0.24, uBlocked);
        poseA.squash = lerp(0.95, 0.84, uBlocked) + (poseA.grounded ? 0 : 0.07);
        poseA.twist = 0.70;
        poseA.earR_dx = lerp(0.28, 0.48, smoothstep(12.50, 13.25, t)) - uBlocked * 0.30;
        poseA.earR_dy = lerp(-0.06, -0.24, uBlocked);
      }
    }

    const sackASpec = vtxCase.entities[0];
    const sackBSpec = vtxCase.entities[1];
    const geomA = buildFlourSack(sackASpec, poseA, cam);
    const geomB = buildFlourSack(sackBSpec, poseB, cam);

    // 3. Lamp_1, Oil Pool & Fire_1
    let lampX = -0.02;
    let lampY = 0.34;
    let lampZ = 0.54;
    let lampTilt = 0.0;
    let lampLit = true;
    let oilRadius = 0.0;
    let fireIntensity = 0.0;

    if (t >= 1.85 && t < 3.15) {
      lampTilt = Math.sin((t - 1.85) * 16.0) * 0.075 * Math.exp(-(t - 1.85) * 1.8);
    }
    const contactStart = isAssist ? 4.90 : 4.85;
    if (t >= contactStart) {
      const uTip = clamp((t - contactStart) / (5.38 - contactStart), 0, 1);
      const uFall = clamp((t - 5.22) / (5.72 - 5.22), 0, 1);
      lampTilt = lerp(0.0, Math.PI * 0.52, easeInOutCubic(uTip));
      lampX = lerp(-0.02, 0.24, smoothstep(contactStart, 5.72, t));
      lampY = lerp(0.34, 0.03, uFall * uFall);
      lampZ = lerp(0.54, 0.49, smoothstep(contactStart, 5.72, t));
      lampLit = t < 5.55;
    }
    if (t >= 5.55) {
      oilRadius = lerp(0.04, 0.30, smoothstep(5.55, 6.85, t));
    }
    if (t >= 6.80) {
      fireIntensity = smoothstep(6.80, 9.10, t);
    }

    const lampScreen = project(lampX, lampY, lampZ, cam);

    // 4. Carried Object Wedge_1 Kinematics — Strictly Attached to Sack_B.ear_R in [10.50, 13.50]s!
    let wedgeScreenPos = null;
    let wedgeAngle = 0.0;
    let wedgeAttached = false;
    const ledgeProj = project(loc.wedge_ledge.x, loc.wedge_ledge.height, loc.wedge_ledge.z, cam);
    // Exact release positions match Sack_B.ear_R at t=13.50s so put-down is seamless!
    const releaseSt = t > 13.50 ? buildFlourSack(sackBSpec, {
      x: isAssist ? 0.83 : 1.10,
      y: 0,
      z: isAssist ? 0.58 : 0.35,
      squash: isAssist ? 0.74 : 0.72,
      lean: isAssist ? 0.54 : 0.52,
      twist: isAssist ? 0.65 : 0.55,
      earL_dx: isAssist ? -0.05 : -0.16,
      earL_dy: isAssist ? 0.01 : -0.04,
      earR_dx: isAssist ? 0.62 : 0.56,
      earR_dy: isAssist ? 0.36 : 0.38
    }, cam) : null;

    if (t < 10.50) {
      wedgeScreenPos = [ledgeProj.x, ledgeProj.y];
      wedgeAngle = 0.0;
    } else if (t <= 13.50) {
      wedgeScreenPos = [geomB.landmarks.ear_R[0], geomB.landmarks.ear_R[1]];
      wedgeAngle = isAssist ? 0.18 : -0.18;
      wedgeAttached = true;
    } else {
      wedgeScreenPos = [releaseSt.landmarks.ear_R[0], releaseSt.landmarks.ear_R[1]];
      wedgeAngle = isAssist ? 0.0 : -0.12;
    }

    // 5. Persistent Physical Marks on Sack_A
    let sackAMarkType = 'none';
    if (isAssist) {
      if (t >= 5.65 && t < 7.20) sackAMarkType = 'hem_oil_stain';
      else if (t >= 7.20) sackAMarkType = 'hem_singed_char';
    } else {
      if (t >= 4.95 && t < 7.20) sackAMarkType = 'ear_R_soot_stain';
      else if (t >= 7.20) sackAMarkType = 'ear_R_soot_char';
    }

    // 6. Build 2.5D Display List
    const cmds = [];
    if (!options.skipCommands) {
      const ambientFlicker = fireIntensity > 0 ? 0.06 * Math.sin(t * 21.0) + 0.04 * Math.cos(t * 33.0) : 0;

      cmds.push({ op: 'rect', x: 0, y: 0, w: W, h: H, fill: '#1a1715' });

      // Back parlor wall (ends at doorway hinge x=1.06)
      const wallTL = project(-1.85, 1.35, 0.90, cam);
      const wallTR = project(1.06, 1.35, 0.90, cam);
      const wallBR = project(1.06, 0.0, 0.90, cam);
      const wallBL = project(-1.85, 0.0, 0.90, cam);
      cmds.push({
        op: 'poly',
        pts: [[wallTL.x, wallTL.y], [wallTR.x, wallTR.y], [wallBR.x, wallBR.y], [wallBL.x, wallBL.y]],
        fill: '#2b2420'
      });

      const wainTL = project(-1.85, 0.42, 0.90, cam);
      const wainTR = project(1.06, 0.42, 0.90, cam);
      cmds.push({
        op: 'poly',
        pts: [[wainTL.x, wainTL.y], [wainTR.x, wainTR.y], [wallBR.x, wallBR.y], [wallBL.x, wallBL.y]],
        fill: '#221b17',
        stroke: '#3a2f28',
        lw: 2
      });

      // Night window
      const winTL = project(-1.05, 1.06, 0.89, cam);
      const winBR = project(-0.52, 0.56, 0.89, cam);
      cmds.push({
        op: 'rect',
        x: winTL.x,
        y: winTL.y,
        w: winBR.x - winTL.x,
        h: winBR.y - winTL.y,
        fill: '#1f2d3d',
        stroke: '#40342c',
        lw: 4
      });
      cmds.push({ op: 'line', p1: [(winTL.x + winBR.x) * 0.5, winTL.y], p2: [(winTL.x + winBR.x) * 0.5, winBR.y], stroke: '#352b25', lw: 3 });
      cmds.push({ op: 'line', p1: [winTL.x, (winTL.y + winBR.y) * 0.5], p2: [winBR.x, (winTL.y + winBR.y) * 0.5], stroke: '#352b25', lw: 3 });

      // Right Hallway beyond doorway (cool slate-indigo hallway so outside vs inside reads unmistakably!)
      const hallTL = project(1.06, 1.35, 0.90, cam);
      const hallTR = project(1.98, 1.35, 0.90, cam);
      const hallBR = project(1.98, 0.0, 0.18, cam);
      const hallBL = project(1.06, 0.0, 0.18, cam);
      cmds.push({
        op: 'poly',
        pts: [[hallTL.x, hallTL.y], [hallTR.x, hallTR.y], [hallBR.x, hallBR.y], [hallBL.x, hallBL.y]],
        fill: '#161d26'
      });

      // Floorboards (parlor warm oak + hallway cool slate-wood)
      const floorNearL = project(-1.90, 0.0, 0.16, cam);
      const floorNearDoor = project(1.26, 0.0, 0.16, cam);
      const floorFarDoor = project(1.06, 0.0, 0.90, cam);
      const floorFarL = project(-1.90, 0.0, 0.90, cam);
      cmds.push({
        op: 'poly',
        pts: [[floorFarL.x, floorFarL.y], [floorFarDoor.x, floorFarDoor.y], [floorNearDoor.x, floorNearDoor.y], [floorNearL.x, floorNearL.y]],
        fill: '#382b22'
      });
      const hallFloorFarR = project(1.98, 0.0, 0.90, cam);
      const hallFloorNearR = project(1.98, 0.0, 0.16, cam);
      cmds.push({
        op: 'poly',
        pts: [[floorFarDoor.x, floorFarDoor.y], [hallFloorFarR.x, hallFloorFarR.y], [hallFloorNearR.x, hallFloorNearR.y], [floorNearDoor.x, floorNearDoor.y]],
        fill: '#232830'
      });

      for (let px = -1.6; px <= 1.8; px += 0.24) {
        const pFar = project(px, 0.0, 0.90, cam);
        const pNear = project(px, 0.0, 0.16, cam);
        cmds.push({ op: 'line', p1: [pFar.x, pFar.y], p2: [pNear.x, pNear.y], stroke: 'rgba(20, 15, 12, 0.55)', lw: 1.5 });
      }

      if (lampLit) {
        const glowC = project(lampX, 0.01, lampZ, cam);
        cmds.push({ op: 'glow', x: glowC.x, y: glowC.y - 30 * cam.zoom, r: 290 * cam.zoom, color: 'rgba(255, 194, 102, 0.25)' });
      }
      if (fireIntensity > 0.01) {
        const fGlow = project(0.24, 0.08, 0.49, cam);
        cmds.push({
          op: 'glow',
          x: fGlow.x,
          y: fGlow.y - 25 * cam.zoom,
          r: (340 + 90 * fireIntensity + 180 * ambientFlicker) * cam.zoom,
          color: `rgba(255, 118, 38, ${(0.35 * fireIntensity).toFixed(3)})`
        });
      }

      // Wedge Ledge beside doorway
      const ledgeTopL = project(0.77, 0.28, 0.46, cam);
      const ledgeTopR = project(0.91, 0.28, 0.46, cam);
      const ledgeBotR = project(0.91, 0.0, 0.46, cam);
      const ledgeBotL = project(0.77, 0.0, 0.46, cam);
      cmds.push({
        op: 'poly',
        pts: [[ledgeTopL.x, ledgeTopL.y], [ledgeTopR.x, ledgeTopR.y], [ledgeBotR.x, ledgeBotR.y], [ledgeBotL.x, ledgeBotL.y]],
        fill: '#4a372b',
        stroke: '#241a14',
        lw: 2
      });

      // Parlor Table
      const tb = loc.table;
      const tL = tb.x - tb.width * 0.5;
      const tR = tb.x + tb.width * 0.5;
      const tblShadow = project(tb.x, 0.0, tb.z, cam);
      cmds.push({ op: 'ellipse', x: tblShadow.x, y: tblShadow.y, rx: tb.width * 0.55 * tblShadow.scale, ry: 16 * cam.zoom, fill: 'rgba(10, 8, 6, 0.42)' });
      for (const lx of [tL + 0.04, tR - 0.04]) {
        for (const lz of [tb.z + 0.05, tb.z - 0.05]) {
          const pTop = project(lx, tb.height, lz, cam);
          const pBot = project(lx, 0.0, lz, cam);
          cmds.push({ op: 'line', p1: [pTop.x, pTop.y], p2: [pBot.x, pBot.y], stroke: '#3d2a1d', lw: 7 * cam.zoom });
        }
      }
      const ttFL = project(tL, tb.height, tb.z - 0.07, cam);
      const ttFR = project(tR, tb.height, tb.z - 0.07, cam);
      const ttBR = project(tR, tb.height, tb.z + 0.07, cam);
      const ttBL = project(tL, tb.height, tb.z + 0.07, cam);
      cmds.push({ op: 'poly', pts: [[ttBL.x, ttBL.y], [ttBR.x, ttBR.y], [ttFR.x, ttFR.y], [ttFL.x, ttFL.y]], fill: '#634632', stroke: '#2c1d13', lw: 2.5 });

      // Spilled Oil Pool
      if (oilRadius > 0.005) {
        const oilC = project(0.24, 0.005, 0.49, cam);
        cmds.push({
          op: 'ellipse',
          x: oilC.x,
          y: oilC.y,
          rx: oilRadius * oilC.scale * 1.15,
          ry: oilRadius * oilC.scale * 0.36,
          fill: fireIntensity > 0.2 ? 'rgba(92, 42, 14, 0.82)' : 'rgba(186, 142, 48, 0.72)',
          stroke: 'rgba(40, 24, 10, 0.65)',
          lw: 1.5
        });
      }

      function emitSack(geom, spec, pose, markType) {
        const shProj = project(pose.x, 0.0, pose.z, cam);
        const airShrink = clamp(1.0 - (pose.y || 0) * 2.2, 0.55, 1.0);
        cmds.push({ op: 'ellipse', x: shProj.x, y: shProj.y + 3, rx: spec.rest_width * 0.56 * shProj.scale * airShrink, ry: 13 * cam.zoom * airShrink, fill: 'rgba(8, 6, 5, 0.48)' });
        cmds.push({ op: 'poly', pts: geom.contour, fill: spec.color_body, stroke: '#1e1612', lw: 3.0 });
        cmds.push({ op: 'polyline', pts: geom.creasePts, stroke: spec.color_shadow, lw: 2.4 });
        cmds.push({ op: 'polyline', pts: geom.seamPts, stroke: spec.color_stitch, lw: 1.8, dashed: true });

        if (markType === 'hem_oil_stain' || markType === 'hem_singed_char') {
          const hr = geom.landmarks.hip_R;
          cmds.push({
            op: 'ellipse',
            x: hr[0] - 8 * cam.zoom,
            y: hr[1] - 8 * cam.zoom,
            rx: 16 * cam.zoom,
            ry: 11 * cam.zoom,
            fill: markType === 'hem_singed_char' ? '#1c1410' : '#7a5a1e',
            stroke: markType === 'hem_singed_char' ? '#d96b27' : '#4a3610',
            lw: 1.5
          });
        } else if (markType === 'ear_R_soot_stain' || markType === 'ear_R_soot_char') {
          const er = geom.landmarks.ear_R;
          cmds.push({
            op: 'ellipse',
            x: er[0] - 4 * cam.zoom,
            y: er[1] + 5 * cam.zoom,
            rx: 15 * cam.zoom,
            ry: 12 * cam.zoom,
            fill: '#171311',
            stroke: '#3b302a',
            lw: 1.5
          });
        }
      }

      // Back wall lintel above doorway
      const lintelHingeT = project(1.06, 1.35, 0.64, cam);
      const lintelLatchT = project(1.24, 1.35, 0.30, cam);
      const jambHingeTop = project(1.06, 0.96, 0.64, cam);
      const jambHingeBot = project(1.06, 0.0, 0.64, cam);
      const jambLatchTop = project(1.24, 0.96, 0.30, cam);
      const jambLatchBot = project(1.24, 0.0, 0.30, cam);

      cmds.push({
        op: 'poly',
        pts: [[lintelHingeT.x, lintelHingeT.y], [lintelLatchT.x, lintelLatchT.y], [jambLatchTop.x, jambLatchTop.y], [jambHingeTop.x, jambHingeTop.y]],
        fill: '#29211c',
        stroke: '#1b1512',
        lw: 2
      });

      // Draw actors behind door plane (or inside room far z)
      // Note: When door is CLOSED (doorOpenFrac < 0.25) in Case B, Sack_A (parlor side x<1.05) is behind the near jamb/wall edge only if z>0.5,
      // while Sack_B (hallway side x>=1.12) is to the right of the closed door panel!
      // Let's draw Sack_A first, then Lamp/Fire, then the 3/4 Door Panel if Sack_B is in hallway, or sort cleanly:
      emitSack(geomA, sackASpec, poseA, sackAMarkType);

      // Lamp_1
      const lS = lampScreen.scale;
      const cT = Math.cos(lampTilt);
      const sT = Math.sin(lampTilt);
      const rotLamp = (lx, ly) => [lampScreen.x + (lx * cT - ly * sT) * lS, lampScreen.y + (lx * sT + ly * cT) * lS];
      cmds.push({ op: 'poly', pts: [rotLamp(-0.038, 0), rotLamp(0.038, 0), rotLamp(0.028, -0.045), rotLamp(-0.028, -0.045)], fill: '#b8893a', stroke: '#261b0c', lw: 2 });
      cmds.push({
        op: 'poly',
        pts: [rotLamp(-0.024, -0.045), rotLamp(0.024, -0.045), rotLamp(0.016, -0.135), rotLamp(-0.016, -0.135)],
        fill: lampLit ? 'rgba(255, 232, 170, 0.78)' : 'rgba(155, 168, 178, 0.48)',
        stroke: '#3a352e',
        lw: 1.8
      });
      if (lampLit) {
        const flPt = rotLamp(0, -0.082);
        cmds.push({ op: 'ellipse', x: flPt[0], y: flPt[1], rx: 7 * cam.zoom, ry: 13 * cam.zoom, fill: '#ffd86b' });
      }

      // Fire_1
      if (fireIntensity > 0.01) {
        const fBase = project(0.24, 0.01, 0.49, cam);
        const tongues = [-0.14, -0.06, 0.02, 0.10, 0.17];
        for (let i = 0; i < tongues.length; i++) {
          const phase = t * (9.0 + i * 2.1) + i * 1.7;
          const sway = Math.sin(phase) * 10 * cam.zoom;
          const hFlame = (68 + 44 * Math.sin(phase * 0.7 + i) * 0.3 + (i === 2 ? 38 : 0)) * fireIntensity * cam.zoom;
          const wFlame = (24 + (i === 2 ? 10 : 0)) * fireIntensity * cam.zoom;
          const bx = fBase.x + tongues[i] * fBase.scale;
          const by = fBase.y;
          cmds.push({
            op: 'poly',
            pts: [[bx - wFlame, by], [bx - wFlame * 0.45 + sway * 0.5, by - hFlame * 0.55], [bx + sway, by - hFlame], [bx + wFlame * 0.45 + sway * 0.5, by - hFlame * 0.55], [bx + wFlame, by]],
            fill: i % 2 === 0 ? 'rgba(242, 92, 28, 0.88)' : 'rgba(255, 178, 46, 0.86)'
          });
        }
        for (let s = 0; s < 3; s++) {
          const uSmk = (t * 0.45 + s * 0.33) % 1.0;
          const smkX = fBase.x + Math.sin(t * 2.5 + s * 2) * 22 * cam.zoom;
          const smkY = fBase.y - (95 + uSmk * 170) * cam.zoom * fireIntensity;
          cmds.push({ op: 'ellipse', x: smkX, y: smkY, rx: (18 + uSmk * 26) * cam.zoom, ry: (12 + uSmk * 18) * cam.zoom, fill: `rgba(42, 38, 36, ${(0.32 * (1 - uSmk) * fireIntensity).toFixed(3)})` });
        }
      }

      // 3/4 Perspective Swinging Wooden Door Leaf!
      // Closed (openFrac=0): spans from hinge (1.06, 0.64) to latch (1.24, 0.30) — an unmistakable wide solid panel!
      // Open (openFrac=0.94): swings back into parlor wall to (0.86, 0.74), leaving doorway wide open!
      const closedAng = Math.atan2(0.30 - 0.64, 1.24 - 1.06); // ~ -1.08 rad
      const openAng = 2.65; // swung back toward parlor far wall
      const curDoorAng = lerp(closedAng, openAng, doorOpenFrac);
      const doorLen = Math.hypot(1.24 - 1.06, 0.30 - 0.64);
      const leafTipX = 1.06 + Math.cos(curDoorAng) * doorLen;
      const leafTipZ = 0.64 + Math.sin(curDoorAng) * doorLen;
      const leafFreeTop = project(leafTipX, 0.95, leafTipZ, cam);
      const leafFreeBot = project(leafTipX, 0.01, leafTipZ, cam);
      const brassKnob = project(lerp(1.06, leafTipX, 0.82), 0.44, lerp(0.64, leafTipZ, 0.82), cam);

      // If door is swung open (doorOpenFrac > 0.5), draw swung-back door leaf BEFORE Sack_B so Sack_B stands clearly in front of it!
      const drawDoorLeaf = () => {
        cmds.push({
          op: 'poly',
          pts: [[jambHingeTop.x, jambHingeTop.y], [leafFreeTop.x, leafFreeTop.y], [leafFreeBot.x, leafFreeBot.y], [jambHingeBot.x, jambHingeBot.y]],
          fill: '#664630',
          stroke: '#21150d',
          lw: 3
        });
        cmds.push({ op: 'ellipse', x: brassKnob.x, y: brassKnob.y, rx: 5 * cam.zoom, ry: 5 * cam.zoom, fill: '#dfb14b', stroke: '#291c08', lw: 1.5 });
        cmds.push({ op: 'line', p1: [jambHingeTop.x, jambHingeTop.y], p2: [jambHingeBot.x, jambHingeBot.y], stroke: '#362519', lw: 6 * cam.zoom });
        cmds.push({ op: 'line', p1: [jambLatchTop.x, jambLatchTop.y], p2: [jambLatchBot.x, jambLatchBot.y], stroke: '#2b1d14', lw: 7 * cam.zoom });
      };

      if (poseB.x >= 1.05 && doorOpenFrac <= 0.65) {
        // Sack_B is in hallway (x >= 1.05) behind closing/closed Door_1!
        emitSack(geomB, sackBSpec, poseB, 'none');
        drawDoorLeaf();
      } else {
        // Sack_B is inside parlor or doorway is swung wide open: draw door leaf behind Sack_B!
        drawDoorLeaf();
        emitSack(geomB, sackBSpec, poseB, 'none');
      }

      // Carried / Placed Wooden Door Wedge (Wedge_1)
      const wSize = 25 * cam.zoom;
      const cW = Math.cos(wedgeAngle);
      const sW = Math.sin(wedgeAngle);
      const rotW = (wx, wy) => [wedgeScreenPos[0] + wx * cW - wy * sW, wedgeScreenPos[1] + wx * sW + wy * cW];
      cmds.push({
        op: 'poly',
        pts: [rotW(0, 0), rotW(wSize * 1.25, wSize * 0.48), rotW(-wSize * 0.35, wSize * 0.48)],
        fill: '#e3ac42',
        stroke: '#291c0a',
        lw: 2.2
      });
    }

    const attachmentErrorPx = wedgeAttached
      ? Math.hypot(wedgeScreenPos[0] - geomB.landmarks.ear_R[0], wedgeScreenPos[1] - geomB.landmarks.ear_R[1])
      : 0.0;

    return {
      t: Number(t.toFixed(4)),
      shot_id: cam.shot_id,
      telemetry: {
        sack_a: {
          x: Number(poseA.x.toFixed(4)),
          y: Number(poseA.y.toFixed(4)),
          z: Number(poseA.z.toFixed(4)),
          grounded: poseA.grounded,
          volume_ratio: Number(geomA.volumeRatio.toFixed(5)),
          mark: sackAMarkType,
          landmarks: geomA.landmarks,
          contour: geomA.contour
        },
        sack_b: {
          x: Number(poseB.x.toFixed(4)),
          y: Number(poseB.y.toFixed(4)),
          z: Number(poseB.z.toFixed(4)),
          grounded: poseB.grounded,
          volume_ratio: Number(geomB.volumeRatio.toFixed(5)),
          landmarks: geomB.landmarks,
          contour: geomB.contour
        },
        lamp: {
          x: Number(lampX.toFixed(4)),
          y: Number(lampY.toFixed(4)),
          lit: lampLit,
          tilt_rad: Number(lampTilt.toFixed(4)),
          screen: [lampScreen.x, lampScreen.y]
        },
        fire_intensity: Number(fireIntensity.toFixed(4)),
        oil_radius: Number(oilRadius.toFixed(4)),
        door_open_fraction: Number(doorOpenFrac.toFixed(4)),
        wedge: {
          attached_to_b_ear_r: wedgeAttached,
          grip_notch_screen: wedgeScreenPos,
          attachment_error_px: Number(attachmentErrorPx.toFixed(5))
        }
      },
      commands: cmds
    };
  }

  return {
    W,
    H,
    applyPatch,
    replayCase,
    evaluateFrame,
    eventKeyedScalar
  };
});
