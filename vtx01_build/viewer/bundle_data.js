// Auto-generated offline bundle for viewer/index.html (zero-server file:// compatibility)
window.VTX_BUNDLE = {
  "caseA": {
    "vtx_version": "0.1-proposed",
    "case_id": "vtx01_case_a_assist",
    "revision": "rev2",
    "parent_revision": "vtx01_case_a_assist@rev1",
    "adaptation_status": "invented_adaptation_not_recovered_calvino_scene",
    "source_seeds": [
      {
        "id": "C1",
        "locator": "Esther Calvino, Preface to Numbers in the Dark (1995), IBM & 1973 Italian Playboy paratext"
      },
      {
        "id": "C2",
        "locator": "Paul Braffort, L'ordre dans le crime (1995/2002), Oulipo Nov 8 1972 & Atlas constraints"
      },
      {
        "id": "A1",
        "locator": "Walt Disney Family Museum (2020), Animating a Sack Drop: weight, deformation, squash & stretch"
      }
    ],
    "timeline": {
      "fps": 24,
      "duration_s": 16,
      "total_frames": 384,
      "camera_cuts": [
        {
          "shot_id": "shot_1_parlor_wide",
          "start_s": 0,
          "end_s": 9.5,
          "frame_range": [
            0,
            227
          ],
          "camera": {
            "cx": 0,
            "cy": 0.42,
            "zoom": 1
          }
        },
        {
          "shot_id": "shot_2_doorway_medium",
          "start_s": 9.5,
          "end_s": 16,
          "frame_range": [
            228,
            383
          ],
          "camera": {
            "cx": 0.58,
            "cy": 0.44,
            "zoom": 1.24
          }
        }
      ]
    },
    "location_legos": {
      "id": "parlor_01",
      "label": "Boarding-House Parlor (Single Room)",
      "floor_depth_z": [
        0.18,
        0.92
      ],
      "table": {
        "x": -0.05,
        "z": 0.54,
        "width": 0.46,
        "height": 0.34
      },
      "doorway": {
        "x": 1.18,
        "z": 0.48,
        "width": 0.38,
        "height": 0.92
      },
      "wedge_ledge": {
        "x": 0.84,
        "z": 0.46,
        "height": 0.28
      }
    },
    "entities": [
      {
        "id": "Sack_A",
        "kind": "flour_sack",
        "fill_ratio": 0.5,
        "rest_width": 0.23,
        "rest_height": 0.34,
        "color_body": "#c95a49",
        "color_shadow": "#8c372a",
        "color_stitch": "#e8cbb1",
        "initial_pose": {
          "x": -0.66,
          "z": 0.56,
          "facing": 1
        }
      },
      {
        "id": "Sack_B",
        "kind": "flour_sack",
        "fill_ratio": 0.5,
        "rest_width": 0.21,
        "rest_height": 0.32,
        "color_body": "#5b84a3",
        "color_shadow": "#38566e",
        "color_stitch": "#d7e4ee",
        "initial_pose": {
          "x": 0.44,
          "z": 0.55,
          "facing": -1
        }
      },
      {
        "id": "Lamp_1",
        "kind": "oil_lamp",
        "initial_state": {
          "x": -0.02,
          "y_above_floor": 0.34,
          "z": 0.54,
          "tilt_rad": 0,
          "lit": true,
          "tipped": false,
          "broken": false,
          "attachment": "table_top"
        }
      },
      {
        "id": "Wedge_1",
        "kind": "door_wedge",
        "initial_state": {
          "x": 0.84,
          "y_above_floor": 0.28,
          "z": 0.46,
          "attached_to": "wedge_ledge",
          "placement": "on_ledge"
        }
      },
      {
        "id": "Door_1",
        "kind": "room_door",
        "initial_state": {
          "open_fraction": 0.08,
          "wedged_state": "none"
        }
      }
    ],
    "initial_world_state": {
      "lamp_lit": true,
      "lamp_tipped": false,
      "lamp_tip_mode": "none",
      "oil_pool_radius": 0,
      "fire_confirmed": false,
      "fire_intensity": 0,
      "sack_a_mark": "none",
      "relational_stance_b_to_a": "neutral_co_tenant",
      "door_state": "ajar",
      "wedge_placement": "on_ledge",
      "independent_cause_channels": 1
    },
    "configured_chance_inputs": [
      {
        "id": "Jolt_1",
        "event_key": "parlor_01:E1_settling_jolt:Jolt_1",
        "seed": 19730214,
        "distribution": "deterministic_keyed_impulse(mean_N=18.0, sigma_N=0.0, dir='+x')",
        "realized_value": {
          "impulse_N": 18,
          "direction": "+x",
          "onset_s": 1.8,
          "peak_s": 2.05,
          "settle_s": 3.2
        }
      }
    ],
    "initial_character_memory": {
      "Sack_A": [
        {
          "mem_id": "mem_A_init_1",
          "proposition": "co_present_in_parlor_with(Sack_B, Lamp_1)",
          "acquired_via": "initial_scene_copresence",
          "at_s": 0,
          "confidence": 0.95,
          "retention_rule": "persist_full_case",
          "retrieved_by_events": [
            "E2_root_action"
          ]
        }
      ],
      "Sack_B": [
        {
          "mem_id": "mem_B_init_1",
          "proposition": "co_present_in_parlor_with(Sack_A, Lamp_1)",
          "acquired_via": "initial_scene_copresence",
          "at_s": 0,
          "confidence": 0.95,
          "retention_rule": "persist_full_case",
          "retrieved_by_events": [
            "E4_doorway_response"
          ]
        }
      ]
    },
    "events": [
      {
        "id": "E1_settling_jolt",
        "actor": "environment",
        "target": "Sack_B",
        "time_interval_s": [
          0,
          3.2
        ],
        "causal_parents": [],
        "legos": {
          "Location": "parlor_01",
          "Entity": "Sack_B",
          "Goal": "maintain_balance",
          "Obstacle": "Jolt_1_floor_impulse",
          "Shift": "Sack_B_pitches_off_balance_toward_table"
        },
        "goal": "exogenous_disturbance",
        "preconditions": [
          "world.lamp_tipped == false"
        ],
        "chance_inputs_used": [
          "Jolt_1"
        ],
        "memory_reads": [],
        "effects": {
          "world_updates": {
            "b_off_balance": true
          },
          "character_observations": {
            "Sack_A": {
              "channel": "direct_sight_lit_room",
              "mem_id": "mem_A_obs_E1",
              "proposition": "Sack_B_staggering_near_table",
              "confidence": 0.92,
              "retention_rule": "persist_full_case"
            },
            "Sack_B": {
              "channel": "proprioceptive_jolt",
              "mem_id": "mem_B_obs_E1",
              "proposition": "floor_jolted_lost_footing",
              "confidence": 0.96,
              "retention_rule": "persist_full_case"
            }
          }
        },
        "motion_parameters": {
          "jolt_shudder_amp": 0.018,
          "b_stagger_lean_rad": -0.44,
          "lamp_wobble_rad": 0.08
        },
        "contact_intervals": [],
        "carry_intervals": [],
        "evidence_status": {
          "visible_in_camera": true,
          "occluded": false
        },
        "carried_consequences": [
          "b_off_balance",
          "mem_A_obs_E1"
        ]
      },
      {
        "id": "E2_root_action",
        "actor": "Sack_A",
        "target": "Sack_B",
        "time_interval_s": [
          3.2,
          6.8
        ],
        "causal_parents": [
          "E1_settling_jolt"
        ],
        "legos": {
          "Location": "parlor_01_table_zone",
          "Entity": "Sack_A",
          "Goal": "assist_steadying",
          "Obstacle": "narrow_clearance_past_Lamp_1",
          "Shift": "Sack_B_steadied_but_Sack_A_hip_brushes_Lamp_1_over"
        },
        "bdi_state": {
          "beliefs_read": [
            "mem_A_init_1",
            "mem_A_obs_E1"
          ],
          "desires": [
            {
              "name": "steady_neighbor_Sack_B",
              "weight": 0.88
            },
            {
              "name": "keep_distance_from_table",
              "weight": 0.35
            }
          ],
          "committed_intention": "reach_across_to_steady_Sack_B"
        },
        "goal": "assist_steadying",
        "preconditions": [
          "world.lamp_tipped == false",
          "world.b_off_balance == true"
        ],
        "chance_inputs_used": [],
        "memory_reads": [
          "mem_A_init_1",
          "mem_A_obs_E1"
        ],
        "effects": {
          "world_updates": {
            "b_off_balance": false,
            "lamp_tipped": true,
            "lamp_lit": false,
            "lamp_tip_mode": "accidental",
            "oil_pool_radius": 0.28,
            "sack_a_mark": "hem_oil_stain",
            "relational_stance_b_to_a": "cooperative"
          },
          "character_observations": {
            "Sack_A": {
              "channel": "tactile_and_direct_sight",
              "mem_id": "mem_A_obs_E2",
              "proposition": "steadied_B_but_hip_clipped_Lamp_1_accidentally",
              "confidence": 0.94,
              "retention_rule": "persist_full_case"
            },
            "Sack_B": {
              "channel": "direct_sight_plus_tactile_support_in_lit_room",
              "mem_id": "mem_B_obs_E2",
              "proposition": "Sack_A_reached_to_steady_me_and_inadvertently_brushed_Lamp_1",
              "confidence": 0.86,
              "retention_rule": "persist_full_case"
            }
          }
        },
        "motion_parameters": {
          "style": "assist_reach_hip_brush_startled_recoil",
          "anticipation_window_s": [
            3.2,
            3.62
          ],
          "support_touch_window_s": [
            4.45,
            4.95
          ],
          "lamp_contact_window_s": [
            4.9,
            5.15
          ],
          "lamp_fall_window_s": [
            5.05,
            5.72
          ],
          "recoil_window_s": [
            5.32,
            6.8
          ]
        },
        "contact_intervals": [
          {
            "id": "touch_support_AB",
            "actor_part": "Sack_A.ear_R",
            "target_part": "Sack_B.ear_L",
            "interval_s": [
              4.45,
              4.95
            ]
          },
          {
            "id": "brush_lamp_A",
            "actor_part": "Sack_A.waist_R",
            "target_part": "Lamp_1.base",
            "interval_s": [
              4.9,
              5.15
            ]
          }
        ],
        "carry_intervals": [],
        "evidence_status": {
          "visible_in_camera": true,
          "corroborated_second_sensor": false,
          "viewer_blinded_verdict": "PENDING_HUMAN_TEST"
        },
        "carried_consequences": [
          "lamp_tipped",
          "oil_pool_radius",
          "sack_a_mark",
          "relational_stance_b_to_a",
          "mem_B_obs_E2"
        ]
      },
      {
        "id": "E3_oil_ignition",
        "actor": "Lamp_1",
        "target": "parlor_01",
        "time_interval_s": [
          6.8,
          9.5
        ],
        "causal_parents": [
          "E2_root_action"
        ],
        "legos": {
          "Location": "parlor_01_floor",
          "Entity": "Lamp_1",
          "Goal": "none_physical_process",
          "Obstacle": "spilled_oil_contacts_live_wick_ember",
          "Shift": "Fire_1_ignites_and_marks_Sack_A"
        },
        "goal": "physical_consequence_ignition",
        "preconditions": [
          "world.lamp_tipped == true",
          "world.oil_pool_radius > 0.1"
        ],
        "chance_inputs_used": [],
        "memory_reads": [],
        "effects": {
          "world_updates": {
            "fire_confirmed": true,
            "fire_intensity": 1,
            "sack_a_mark": "hem_singed_char"
          },
          "character_observations": {
            "Sack_A": {
              "channel": "direct_sight_and_heat",
              "mem_id": "mem_A_obs_E3",
              "proposition": "oil_pool_ignited_must_exit_door",
              "confidence": 0.99,
              "retention_rule": "persist_full_case"
            },
            "Sack_B": {
              "channel": "direct_sight_and_heat",
              "mem_id": "mem_B_obs_E3",
              "proposition": "oil_pool_ignited_near_door_route",
              "confidence": 0.99,
              "retention_rule": "persist_full_case"
            }
          }
        },
        "motion_parameters": {
          "fire_growth_curve": "smoothstep_6.85_to_9.20"
        },
        "contact_intervals": [],
        "carry_intervals": [],
        "evidence_status": {
          "fire_visible_in_camera": true
        },
        "carried_consequences": [
          "fire_confirmed",
          "fire_intensity",
          "sack_a_mark"
        ]
      },
      {
        "id": "E4_doorway_response",
        "actor": "Sack_B",
        "target": "Wedge_1",
        "time_interval_s": [
          9.5,
          16
        ],
        "causal_parents": [
          "E2_root_action",
          "E3_oil_ignition"
        ],
        "legos": {
          "Location": "parlor_01_doorway",
          "Entity": "Sack_B",
          "Goal": "prop_door_open_and_assist_Sack_A_exit",
          "Obstacle": "heavy_self_closing_door_and_spreading_fire",
          "Shift": "Door_1_wedged_open_cooperative_exit"
        },
        "bdi_state": {
          "beliefs_read": [
            "mem_B_init_1",
            "mem_B_obs_E2",
            "mem_B_obs_E3"
          ],
          "desires": [
            {
              "name": "escape_fire",
              "weight": 0.95
            },
            {
              "name": "aid_cooperative_co_tenant_A",
              "weight": 0.84
            }
          ],
          "committed_intention": "carry_Wedge_1_to_prop_Door_1_open_for_Sack_A"
        },
        "goal": "prop_door_open_for_partner",
        "preconditions": [
          "world.fire_confirmed == true",
          "memory.Sack_B.has('mem_B_obs_E2')"
        ],
        "chance_inputs_used": [],
        "memory_reads": [
          "mem_B_obs_E2",
          "mem_B_obs_E3"
        ],
        "effects": {
          "world_updates": {
            "door_state": "wedged_open_cooperative",
            "wedge_placement": "inner_hinge_prop_open"
          },
          "character_observations": {
            "Sack_A": {
              "channel": "direct_sight_doorway",
              "mem_id": "mem_A_obs_E4",
              "proposition": "Sack_B_propped_door_open_and_reached_back_for_me",
              "confidence": 0.95,
              "retention_rule": "persist_full_case"
            }
          }
        },
        "motion_parameters": {
          "mode": "carry_wedge_prop_open_and_reach_back",
          "pickup_s": 10.5,
          "putdown_s": 13.5
        },
        "contact_intervals": [
          {
            "id": "coop_reach_BA",
            "actor_part": "Sack_B.ear_L",
            "target_part": "Sack_A.ear_R",
            "interval_s": [
              14.4,
              15.8
            ]
          }
        ],
        "carry_intervals": [
          {
            "id": "carry_wedge_B",
            "carrier": "Sack_B",
            "carrier_grip": "ear_R",
            "object": "Wedge_1",
            "object_handle": "grip_notch",
            "interval_s": [
              10.5,
              13.5
            ],
            "max_attachment_px_tolerance": 1.5
          }
        ],
        "evidence_status": {
          "visible_in_camera": true
        },
        "carried_consequences": [
          "door_state",
          "wedge_placement"
        ]
      }
    ]
  },
  "patchAB": {
    "patch_id": "patch_vtx01_goal_assist_to_deliberate",
    "base_case_id": "vtx01_case_a_assist",
    "base_revision": "rev2",
    "derived_case_id": "vtx01_case_b_deliberate",
    "derived_revision": "rev2",
    "root_intervention": {
      "event_id": "E2_root_action",
      "field": "goal",
      "from": "assist_steadying",
      "to": "tip_lamp_deliberately",
      "invariant_held_fixed": [
        "timeline (16.0 s, 24 fps, cut at 9.5 s, identical camera parameters)",
        "entities & initial_world_state",
        "configured_chance_inputs.Jolt_1 (seed 19730214, 18.0 N '+x', onset 1.80 s)",
        "initial_character_memory (Sack_A, Sack_B)",
        "E1_settling_jolt (0.0-3.2 s state and motion identical)",
        "E3_oil_ignition terminal Fire_1 envelope"
      ]
    },
    "declared_causal_descendants": [
      "events[1] (E2_root_action): target, legos, bdi_state, effects, motion_parameters, contact_intervals",
      "events[2] (E3_oil_ignition): effects.world_updates.sack_a_mark (ear_R_soot_char instead of hem_singed_char)",
      "events[3] (E4_doorway_response): legos, bdi_state, goal, effects, motion_parameters, contact_intervals (Sack_B carries Wedge_1 in [10.50, 13.50] s to jam Door_1 shut from outside rather than propping it open)"
    ],
    "operations": [
      {
        "op": "replace",
        "path": "/case_id",
        "value": "vtx01_case_b_deliberate"
      },
      {
        "op": "replace",
        "path": "/parent_revision",
        "value": "vtx01_case_a_assist@rev2"
      },
      {
        "op": "replace",
        "path": "/events/1/target",
        "value": "Lamp_1"
      },
      {
        "op": "replace",
        "path": "/events/1/goal",
        "value": "tip_lamp_deliberately"
      },
      {
        "op": "replace",
        "path": "/events/1/legos",
        "value": {
          "Location": "parlor_01_table_zone",
          "Entity": "Sack_A",
          "Goal": "tip_lamp_deliberately",
          "Obstacle": "table_distance_and_witness_Sack_B",
          "Shift": "Lamp_1_struck_deliberately_onto_floorboards"
        }
      },
      {
        "op": "replace",
        "path": "/events/1/bdi_state",
        "value": {
          "beliefs_read": [
            "mem_A_init_1",
            "mem_A_obs_E1"
          ],
          "desires": [
            {
              "name": "ignite_parlor_lamp",
              "weight": 0.91
            },
            {
              "name": "avoid_oil_splash_on_base",
              "weight": 0.72
            }
          ],
          "committed_intention": "coil_and_strike_Lamp_1_off_table"
        }
      },
      {
        "op": "replace",
        "path": "/events/1/effects",
        "value": {
          "world_updates": {
            "b_off_balance": false,
            "lamp_tipped": true,
            "lamp_lit": false,
            "lamp_tip_mode": "deliberate",
            "oil_pool_radius": 0.28,
            "sack_a_mark": "ear_R_soot_stain",
            "relational_stance_b_to_a": "threatened"
          },
          "character_observations": {
            "Sack_A": {
              "channel": "direct_sight_and_strike_contact",
              "mem_id": "mem_A_obs_E2",
              "proposition": "deliberately_struck_Lamp_1_onto_floor",
              "confidence": 0.97,
              "retention_rule": "persist_full_case"
            },
            "Sack_B": {
              "channel": "direct_sight_lit_room",
              "mem_id": "mem_B_obs_E2",
              "proposition": "Sack_A_coiled_aimed_and_deliberately_shoved_Lamp_1_ignoring_my_stumble",
              "confidence": 0.89,
              "retention_rule": "persist_full_case"
            }
          }
        }
      },
      {
        "op": "replace",
        "path": "/events/1/motion_parameters",
        "value": {
          "style": "planted_coil_aimed_shove_controlled_retreat",
          "anticipation_window_s": [
            3.2,
            4.25
          ],
          "lamp_contact_window_s": [
            4.85,
            5.2
          ],
          "lamp_fall_window_s": [
            5.05,
            5.72
          ],
          "recoil_window_s": [
            5.55,
            6.8
          ]
        }
      },
      {
        "op": "replace",
        "path": "/events/1/contact_intervals",
        "value": [
          {
            "id": "strike_lamp_A",
            "actor_part": "Sack_A.ear_R",
            "target_part": "Lamp_1.chimney_collar",
            "interval_s": [
              4.85,
              5.2
            ]
          }
        ]
      },
      {
        "op": "replace",
        "path": "/events/2/effects/world_updates/sack_a_mark",
        "value": "ear_R_soot_char"
      },
      {
        "op": "replace",
        "path": "/events/3/legos",
        "value": {
          "Location": "parlor_01_doorway",
          "Entity": "Sack_B",
          "Goal": "flee_and_bar_door_against_Sack_A",
          "Obstacle": "approaching_Sack_A_and_spreading_fire",
          "Shift": "Door_1_slammed_and_wedged_shut_from_outside"
        }
      },
      {
        "op": "replace",
        "path": "/events/3/bdi_state",
        "value": {
          "beliefs_read": [
            "mem_B_init_1",
            "mem_B_obs_E2",
            "mem_B_obs_E3"
          ],
          "desires": [
            {
              "name": "escape_fire",
              "weight": 0.95
            },
            {
              "name": "protect_self_from_arsonist_A",
              "weight": 0.92
            }
          ],
          "committed_intention": "carry_Wedge_1_outside_and_jam_Door_1_shut"
        }
      },
      {
        "op": "replace",
        "path": "/events/3/goal",
        "value": "flee_and_wedge_door_shut"
      },
      {
        "op": "replace",
        "path": "/events/3/effects",
        "value": {
          "world_updates": {
            "door_state": "wedged_shut_against_A",
            "wedge_placement": "outer_threshold_jam_shut"
          },
          "character_observations": {
            "Sack_A": {
              "channel": "direct_sight_and_blocked_door",
              "mem_id": "mem_A_obs_E4",
              "proposition": "Sack_B_recoiled_slammed_Door_1_and_wedged_it_shut",
              "confidence": 0.95,
              "retention_rule": "persist_full_case"
            }
          }
        }
      },
      {
        "op": "replace",
        "path": "/events/3/motion_parameters",
        "value": {
          "mode": "carry_wedge_exit_slam_and_jam_shut",
          "pickup_s": 10.5,
          "putdown_s": 13.5
        }
      },
      {
        "op": "replace",
        "path": "/events/3/contact_intervals",
        "value": []
      }
    ]
  },
  "policies": {
    "policy_set_id": "synthetic_demo_policies_v0.1",
    "disclaimer": "Explicitly invented synthetic test rules per SCION v1.1 <delivery_and_stop>; NOT Calvino's original story policies.",
    "evaluation_modes": [
      "world_state",
      "corroborated_evidence"
    ],
    "evidence_rule": "Authored intention/goal in world state NEVER counts as visual corroboration. Missing required evidence yields UNKNOWN; falsified predicate yields NO_PAY.",
    "clauses": [
      {
        "id": "P1",
        "name": "Confirmed Fire Coverage",
        "version": "0.1.0",
        "predicate": "confirmed(Fire_1 == true)",
        "world_evaluator": "world.fire_confirmed === true ? 'PAY' : 'NO_PAY'",
        "evidence_evaluator": "evidence.fire_visible_in_camera === true ? 'PAY' : (evidence.fire_visible_in_camera === false ? 'NO_PAY' : 'UNKNOWN')"
      },
      {
        "id": "P2",
        "name": "Accidental Lamp-Tipping Indemnity",
        "version": "0.1.0",
        "predicate": "confirmed(lamp_tip_cause == 'accidental')",
        "world_evaluator": "world.lamp_tipped && world.lamp_tip_mode === 'accidental' ? 'PAY' : 'NO_PAY'",
        "evidence_evaluator": "evidence.viewer_blinded_verdict === 'accidental' ? 'PAY' : (evidence.viewer_blinded_verdict === 'deliberate' ? 'NO_PAY' : 'UNKNOWN')"
      },
      {
        "id": "P3",
        "name": "Deliberate Lamp-Tipping Liability Rider",
        "version": "0.1.0",
        "predicate": "confirmed(lamp_tip_cause == 'deliberate')",
        "world_evaluator": "world.lamp_tipped && world.lamp_tip_mode === 'deliberate' ? 'PAY' : 'NO_PAY'",
        "evidence_evaluator": "evidence.viewer_blinded_verdict === 'deliberate' ? 'PAY' : (evidence.viewer_blinded_verdict === 'accidental' ? 'NO_PAY' : 'UNKNOWN')"
      },
      {
        "id": "P4",
        "name": "Independently Corroborated Cause Rider",
        "version": "0.1.0",
        "predicate": "confirmed_by_independent_channels(lamp_tip_cause, min_channels=2)",
        "world_evaluator": "world.independent_cause_channels >= 2 ? 'PAY' : 'NO_PAY'",
        "evidence_evaluator": "evidence.independent_corroborated_channels >= 2 ? 'PAY' : 'UNKNOWN'"
      }
    ]
  },
  "validation": {
    "verified_at": "2026-11-10T22:56:53.656Z",
    "node_version": "v23.6.0",
    "hashes": {
      "case_a_sha256": "a683ca02c50aa1fe5820c1a7ffe0efd56fa4eb766bd9a4bb67d965e5976f6f20",
      "patch_sha256": "bc5162da7e358b5bb7f6d625c36cbb12f46eb21e802847d54aa548d4334a46e2",
      "case_b_sha256": "41e06fd3a677b7fa1c451f9239a2e86665db76b2b59185d92a8bf8a50a42b757",
      "policies_sha256": "e954ee53486d17a5bb655c8ca8d2872ea5fbe55f4a9b03d1bf4f148780ef60db"
    },
    "ab_diff_audit": {
      "changed_paths_count": 46,
      "unauthorized_paths": [],
      "e1_identical_frames_0_to_76": 77
    },
    "kinematic_and_attachment_inspection": {
      "case_a": {
        "total_frames_inspected": 384,
        "max_volume_drift_sack_a": 0,
        "max_volume_drift_sack_b": 0,
        "carry_interval_frames_checked": 73,
        "max_carry_attachment_error_px": 0,
        "min_lamp_contact_distance_px": 42.42,
        "max_grounded_slide_px_per_frame_a": 0,
        "max_grounded_slide_px_per_frame_b": 0,
        "cut_persistence_frame_227_to_228_ok": true,
        "pre_cut_frame_227": {
          "fire_intensity": 1,
          "oil_radius": 0.3,
          "sack_a_mark": "hem_singed_char"
        },
        "post_cut_frame_228": {
          "fire_intensity": 1,
          "oil_radius": 0.3,
          "sack_a_mark": "hem_singed_char"
        }
      },
      "case_b": {
        "total_frames_inspected": 384,
        "max_volume_drift_sack_a": 0,
        "max_volume_drift_sack_b": 0,
        "carry_interval_frames_checked": 73,
        "max_carry_attachment_error_px": 0,
        "min_lamp_contact_distance_px": 22.3,
        "max_grounded_slide_px_per_frame_a": 0,
        "max_grounded_slide_px_per_frame_b": 0,
        "cut_persistence_frame_227_to_228_ok": true,
        "pre_cut_frame_227": {
          "fire_intensity": 1,
          "oil_radius": 0.3,
          "sack_a_mark": "ear_R_soot_char"
        },
        "post_cut_frame_228": {
          "fire_intensity": 1,
          "oil_radius": 0.3,
          "sack_a_mark": "ear_R_soot_char"
        }
      }
    },
    "gates": {
      "evidence_gate": {
        "status": "PASS_WITH_NAMED_UNRESOLVED",
        "verifier": "builder_self_check"
      },
      "structural_gate": {
        "status": "PASS",
        "verifier": "validate_vtx.js"
      },
      "animation_kinematic_gate": {
        "status": "PASS_PENDING_VISUAL_FRAME_CHECK",
        "verifier": "validate_vtx.js"
      },
      "temporal_gate": {
        "status": "PASS",
        "verifier": "validate_vtx.js"
      },
      "perceptual_gate": {
        "status": "PENDING",
        "note": "Blinded zero-caption test harness ready; voluntary human respondents UNTESTED."
      }
    }
  }
};
