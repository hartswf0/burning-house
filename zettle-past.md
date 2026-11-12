```text
ZETTEL

ID: house-what-the-count-counts

TITLE: The film number fixes a casting of the index

SOURCE: Elena Pierazzo — What Do You Do with 8 Thousand Billion Variants? — DH2025, p. 1014 and continuation. Italo Calvino — Prose and Anticombinatorics — “Order in Crime” and “Esthetic Constraints.” Abominable House — Twelve to the Twelfth.

PASSAGE: [PARAPHRASE] Pierazzo computes 8,255,648,563,200 possible combinations of selected readings in Il Capitolo dei Frati. Canto lengths and stanza reorderings introduce further variation. Calvino’s burnt index supplies twelve deeds but leaves their order unknown. The Film Bank plays a fixed deed sequence and varies who does each deed to whom.

RESEARCH OBJECT: What an exact count commits the project to treating as a variable.

LOCAL MOVE: Pierazzo counts combinations in a model of surviving witnesses. The Film Bank counts combinations it can address and stage.

SOURCE TERMS: loci critici, canonical versions, anticombinatorics, esthetic constraints.

WHAT BECAME STRANGE: [OUR INFERENCE] The same arithmetic exposes a distinction inside the project’s own count. Giving every tenant three deeds done and three suffered permits repeated pairs and yields 5,112,676,800 assignments. Calvino’s additional requirement that each tenant act once on each of the other three gives 12! = 479,001,600 assignments before applying his other aesthetic constraints.

QUESTION: Which absences in the copybook does the adaptation open to variation, and which does it settle in advance?

MECHANISM: Twelve fixed deed slots each take one of twelve ordered pairs. The symmetry count changes when the rule changes from equal row and column totals to exactly one use of each directed pair.

FORMAL SHIFT:
<burnt index> → <fixed deed slots with variable actor–recipient pairs> → [enumerate or filter] → <addressable assignments>

SOURCE FORMALISM: Pierazzo’s product over selected reading types. The Film Bank’s base-12 index. Calvino’s pair-once condition.

OUR FORMALIZATION:
[OUR FORMALIZATION — NOT SOURCE SYNTAX]
Balanced totals allow a 4 × 4 zero-diagonal count matrix with each row and column summing to 3. Pair-once fixes every off-diagonal entry to 1. Assigning the twelve distinct pairs to the twelve slots then gives 12!.

TENSION: The interface makes a precise promise about which films can be retrieved. The fiction asks a broader question about what can be reconstructed from an index.

MISSING: A write-up that names the separately counted rule sets and states where deed order is fixed.

BOUNDARY: The 12! figure isolates the pair-once condition. It leaves Calvino’s action-class rules and the project’s ledger constraints open.

CITATION TRAIL: Calvino’s “Esthetic Constraints,” especially the parenthetical requirement that each tenant act on each of the others. Compare the “Three kinds of constraint” section on the project’s numbers page.

TEST: Take a balanced assignment that repeats one ordered pair. It should pass the project’s equal-totals condition and fail pair-once.

WRITE-UP: “The Film Bank indexes 12¹² cast assignments to a fixed sequence of twelve deeds. Its exact counts describe which assignments survive each stated constraint.”

PLATFORM: [[Abominable House methods]]

LINKS:
[[house-opening-representatives]]
[[house-film-citation]]

BIBTEX:
@inproceedings{pierazzo2025variants,
  author = {Pierazzo, Elena},
  title = {What Do You Do with 8 Thousand Billion Variants? Toward Structural and Quantitative Philology},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  url = {https://zenodo.org/records/19494802}
}
@incollection{calvino2003anticombinatorics,
  author = {Calvino, Italo},
  title = {Prose and Anticombinatorics},
  booktitle = {The New Media Reader},
  editor = {Wardrip-Fruin, Noah and Montfort, Nick},
  publisher = {MIT Press},
  year = {2003},
  url = {https://rednoise.org/teaching/pdal/uploads/OULIPO.pdf}
}
```

```text
ZETTEL

ID: house-presence-and-witnessing

TITLE: Turning out the light changes who knows while leaving the cast in place

SOURCE: Jan Niklas Jokisch and Antonio Rojas Castro — Revisiting Network Analysis in Drama — DH2025, pp. 798–799. Abominable House — Film Bank, film 1541585241617, deed IX, and ledger.js.

PASSAGE: [PARAPHRASE] Jokisch and Rojas Castro distinguish scenic copresence, speech-based interaction, and presence inferred from entrances and exits. Their proposed comparison uses fully encoded stage directions as a reference for the last of these.

RESEARCH OBJECT: A fixed scene in which light changes the transfer of information.

LOCAL MOVE: The question of what counts as an interaction becomes a question the adaptation can stage under controlled conditions.

SOURCE TERMS: scenic copresence, speech-based presence, gold standard, inhabitants, trace.

WHAT BECAME STRANGE: [REPRODUCED IN CODE] In deed IX of film 1541585241617, Inigo is in the bedroom and learns of the current deed. Roessler finds the curtain left by deed VIII. I reran the same assignment with the bedroom dark only during deed IX. Inigo stayed in the room, and both knowledge updates disappeared.

QUESTION: Which relationship matters for the interpretation at hand: doing the deed, being there, seeing it, or finding what it left?

MECHANISM: The ledger updates direct witnesses and discoveries through a light threshold. Participants can know through participation. Public slander and snooping provide further routes.

FORMAL SHIFT:
<deed and room state> → <participants, inhabitants, light, surviving traces> → [apply observation rules] → <who learns what, and when>

SOURCE FORMALISM: ledger.js records inhabitants and discoveries separately in each frame. The implemented threshold for both checks is light ≥ 1.

OUR FORMALIZATION: NONE. The result comes from changing one lighting condition in a local copy of the published ledger.

TENSION: An entrance–exit record could correctly put Inigo in the bedroom and still leave open whether he saw the deed. A knowledge graph can also link Roessler to an event she did not attend.

MISSING: An explicit relation type wherever the write-up uses “witness” or “visibility.”

BOUNDARY: The intervention establishes how the simulation behaves. It does not measure what viewers notice in the rendered film.

CITATION TRAIL: Compare the deed IX quatrain and discovery line with the frame record. For the artistic lineage, follow the four lists in Knowles and Tenney’s The House of Dust.

TEST: Build three records for the same beat: who was present, who saw it, and who learned of an earlier deed. Show which records change when the lamp goes out.

WRITE-UP: “The House of Dust supplies four compositional variables. The adaptation makes them consequential by letting light and material traces govern access to a deed.”

PLATFORM: [[Evidence in the Abominable House]]

LINKS:
[[house-trace-attribution]]
[[drama-segmentation]]

BIBTEX:
@inproceedings{jokischrojascastro2025drama,
  author = {Jokisch, Jan Niklas and Rojas Castro, Antonio},
  title = {Revisiting Network Analysis in Drama: Operational Challenges and Methodological Insights},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  pages = {798--799},
  url = {https://zenodo.org/records/19494802}
}
@misc{hartsoe2026houseledger,
  author = {Hartsoe, Watson},
  title = {Abominable House Film Bank Ledger},
  year = {2026},
  url = {https://github.com/hartswf0/bolas/blob/0ef3a04103f4f16d96ab9684a0bfc73e101225e9/paeleo/abominable-house/live/ledger.js}
}
```

```text
ZETTEL

ID: house-trace-attribution

TITLE: A curtain can disclose that something happened without disclosing who did it

SOURCE: Federico Pianzola, Franziska Pannach, Luotong Cheng, and Xiaoyan Yang — The GOLEM Ontology for Narrative and Fiction — DH2025, pp. 201–202, “Inference module.” Abominable House — ledger.js, step and memories.

PASSAGE: [PARAPHRASE] GOLEM models an attribution as a statement with a source and a method. One attribution can become a premise for another.

RESEARCH OBJECT: The inference the Film Bank makes when a character finds a material trace.

LOCAL MOVE: GOLEM gives evidence and attribution separate identities. The ledger stores the discovery as knowledge of the deed’s index.

SOURCE TERMS: Attribute Assignment, provenance, source, method, trace, knowledge.

WHAT BECAME STRANGE: [OUR INFERENCE] The film can say Roessler finds a curtain while the code gives her the index of deed VIII. The memory reader can use that index to look up the recorded deed and its participants. The material clue is narrower than the information the engine can retrieve from it.

QUESTION: When should finding a trace entitle a tenant to identify an actor?

MECHANISM: A trace has a material and the index of its originating event. Discovery adds that index to the tenant’s knowledge list. Later code dereferences it to the event.

FORMAL SHIFT:
<material trace> → <observation with source and time> → [attribute a deed or actor] → <claim a character can act on>

SOURCE FORMALISM: GOLEM uses CIDOC CRM E13_Attribute_Assignment. The Film Bank records deed indices in per-tenant knowledge lists and records the material found in the frame.

OUR FORMALIZATION:
[OUR FORMALIZATION — NOT SOURCE SYNTAX]
Preserve three assertions separately: Roessler saw a curtain, Roessler inferred a deed, Roessler attributed it to a tenant. Give each assertion its own grounds.

TENSION: A fixed trace-to-event lookup keeps the simulation legible. Calvino’s investigation draws force from the possibility that a surviving object supports more than one account.

MISSING: A representation of partial, uncertain, or false attribution inside the live ledger.

BOUNDARY: This concerns how the present code stores knowledge. It leaves open how much the spectator infers from the visual clue.

CITATION TRAIL: GOLEM’s inference module and ledger.js. Read alongside the classroom film By What Light, where the difference between seeing an act and seeing its trace can carry the scene.

TEST: Give Roessler the same curtain after two different possible actor assignments. Ask which claims the prop itself supports in both versions and which claims require further evidence.

WRITE-UP: “Finding a trace currently makes its originating deed available to a tenant. This lets the simulation propagate evidence and also marks where its account of inference is strongest and most compressed.”

PLATFORM: [[Evidence in the Abominable House]]

LINKS:
[[house-presence-and-witnessing]]
[[house-observer-enters]]

BIBTEX:
@inproceedings{pianzolaEtAl2025golem,
  author = {Pianzola, Federico and Pannach, Franziska and Cheng, Luotong and Yang, Xiaoyan},
  title = {The {GOLEM} Ontology for Narrative and Fiction},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  pages = {200--202},
  url = {https://zenodo.org/records/19494802}
}
```

```text
ZETTEL

ID: house-most-likely

TITLE: The best film found by a search depends on what that search rewards

SOURCE: Abominable House — “The most likely story,” Film Bank, story.js, crossed.js, and published Atlas data. Kartik Chandra et al. — Storytelling as Inverse Inverse Planning — 2024.

PASSAGE: [PARAPHRASE] The landing page presents a film selected by Monte Carlo tree search. The live engine uses the geometric mean of deed-level believability as that search’s reward and reports a separate sequence log probability. The author search rewards selected responses from a modeled watcher.

RESEARCH OBJECT: The scope of the claim made by “most likely.”

LOCAL MOVE: Separate a search result, its objective function, and the audience response it might or might not elicit.

SOURCE TERMS: believability, log P, Monte Carlo tree search, inverse inverse planning.

WHAT BECAME STRANGE: [REPRODUCED IN CODE] The featured film 1541585241617 scored 0.59635 in the published engine. Atlas film 1974948683979, generated by the irony search, scored 0.90214 under the same scorer. The Atlas case had zero ledger contradictions.

QUESTION: What can the featured screening demonstrate once its claim is limited to the search that produced it?

MECHANISM: Believability aggregates authored deed ratings. Sequence log probability sums the logs of normalized conditional pair scores. The browser’s MOST LIKELY button makes a seeded search with 400 iterations and sorts the films it finds by believability.

FORMAL SHIFT:
<cast assignment> → <deed ratings and conditional pair probabilities> → [aggregate and rank under a stated objective] → <selected film>

SOURCE FORMALISM: story.js calculates both quantities. crossed.js separately defines the watcher and the irony, suspense, and twist objectives.

OUR FORMALIZATION: NONE. Both scores above were recalculated with the published scorer.

TENSION: The selected film can illustrate what one search produces. Its label can also suggest an exhaustive result or a human judgment, neither of which the selection procedure supplies.

MISSING: The featured render’s search seed, budget, and original score table.

BOUNDARY: The higher Atlas score refutes a global maximum claim under the inspected scorer. It leaves the result of the featured film’s original search open.

CITATION TRAIL: story.js, score and mcts. film.html, the MOST LIKELY handler. Chandra et al., DOI 10.1111/tops.12710, for the audience model as a design target.

TEST: Put the two film numbers in the Film Bank and record believability, log probability, and the objective that originally selected each one. Give human judgments a separate column if collected.

WRITE-UP: “We screened one film selected by a believability-directed search. The score expresses the engine’s authored rules, and other search objectives expose different parts of the film space.”

PLATFORM: [[Abominable House methods]]

LINKS:
[[house-disclosure-clock]]
[[house-opening-representatives]]

BIBTEX:
@misc{hartsoe2026housestory,
  author = {Hartsoe, Watson},
  title = {Abominable House Film Bank Scoring and Search},
  year = {2026},
  url = {https://github.com/hartswf0/bolas/blob/0ef3a04103f4f16d96ab9684a0bfc73e101225e9/paeleo/abominable-house/live/story.js}
}
@article{chandraEtAl2024storytelling,
  author = {Chandra, Kartik and Li, Tzu-Mao and Tenenbaum, Joshua B. and Ragan-Kelley, Jonathan},
  title = {Storytelling as Inverse Inverse Planning},
  journal = {Topics in Cognitive Science},
  year = {2024},
  volume = {16},
  number = {1},
  pages = {54--70},
  doi = {10.1111/tops.12710}
}
```

```text
ZETTEL

ID: house-disclosure-clock

TITLE: Two cuts can share every deed and disclose different evidence

SOURCE: Sean A. Yeager — Postclassical Time Maps: Theory and Interpretation — DH2025, pp. 558–559. Abominable House — Film Bank, FAST / WATCH / CUT, and crossed.js.

PASSAGE: [PARAPHRASE] Yeager treats presentation as the route by which the audience accesses story time. His time maps allow the same segment to be interpreted differently from different temporal viewpoints.

RESEARCH OBJECT: A change in a cut that the current audience model cannot register.

LOCAL MOVE: Apply the fabula–syuzhet distinction to two presentations of the same Film Bank assignment.

SOURCE TERMS: fabula, syuzhet, narrative velocity, memory, consequence, watcher.

WHAT BECAME STRANGE: [CODE INSPECTION] Changing the pace rebuilds the screening timeline and changes such things as chapter cards, standalone memory beats, and which consequences appear. The watcher still computes its curves from the same twelve cast assignments. It receives each deed as a complete event in the same order.

QUESTION: When does a viewer learn the identity of an actor: from the deed, a chapter card, a memory, or a later consequence?

MECHANISM: The renderer can repeat, foreshadow, or omit a disclosure. The watcher takes one update per ledger deed and does not consume the timed presentation segments.

FORMAL SHIFT:
<ledger events> → <timed presentation segments with disclosures> → [map each disclosure to its originating event] → <time map of what the cut makes available>

SOURCE FORMALISM: Yeager maps presentation time against story time. The Film Bank maintains a timed segment list and a separate deed-indexed watcher.

OUR FORMALIZATION:
[OUR FORMALIZATION — NOT SOURCE SYNTAX]
For each clue, record when the deed occurred, when a tenant learned of it, and when the cut first gave the viewer grounds to identify it.

TENSION: A curve can describe what a model infers from a complete deed sequence. A film cut can make the same sequence read differently by changing when the audience gets the evidence.

MISSING: A watcher that takes the cues available in a particular cut as its input.

BOUNDARY: Inspection establishes that the pace buttons do not change the modeled curves. Whether they change viewers’ readings remains a testable question.

CITATION TRAIL: Yeager’s Time Maps: Theory and Method, DOI 10.22148/001c.87937. Compare film.html’s build function with crossed.js’s audience function.

TEST: Use the same film number in WATCH and CUT. Timestamp the first evidence for one prior deed in each. At matched checkpoints, ask viewers what they know and which cue gave it away.

WRITE-UP: “The Film Bank can vary the disclosure of a history while keeping its deed sequence fixed. Its current watcher measures inference over the sequence of deeds.”

PLATFORM: [[Cinematic time in the Abominable House]]

LINKS:
[[house-most-likely]]
[[house-film-citation]]

BIBTEX:
@inproceedings{yeager2025postclassical,
  author = {Yeager, Sean A.},
  title = {Postclassical Time Maps: Theory and Interpretation},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  pages = {558--559},
  url = {https://zenodo.org/records/19494802}
}
```

```text
ZETTEL

ID: house-opening-representatives

TITLE: Two openings grouped as the same house can leave different people informed

SOURCE: Elena Pierazzo — What Do You Do with 8 Thousand Billion Variants? — DH2025. Abominable House — OPENINGS and crossed.js.

PASSAGE: [PARAPHRASE] Pierazzo groups manuscript witnesses using selected textual, paratextual, or codicological features and chooses a central witness as a reference copy. The Film Bank groups three-deed openings by a signature and selects the highest-scoring prefix within each group.

RESEARCH OBJECT: What a chosen representative lets the reader infer about other members of its group.

LOCAL MOVE: Compare a representative chosen for centrality with one chosen for believability.

SOURCE TERMS: average manuscript, reference copy, opening, signature, different houses.

WHAT BECAME STRANGE: [REPRODUCED IN CODE] The default run grouped 1,728 openings into 589 signatures. Two openings in the same group differ only in who acts in deed III: Ogiva in one, Roessler in the other, both toward Belindo. Their third-deed knowledge and room records differ. Their generated cuts stop before VII and IX, respectively.

QUESTION: What remains equivalent after two openings receive the same signature?

MECHANISM: The signature includes survival, body marks, dominant archetype, and current intention. It omits location and knowledge. The continuation still runs from the fuller state. The displayed representative is selected by prefix believability.

FORMAL SHIFT:
<three-deed history> → <selected post-opening attributes> → [group and select] → <one displayed opening per signature>

SOURCE FORMALISM: crossed.js defines the signature, the continuation, and the choice of representative. Pierazzo describes choosing the manuscript nearest the middle of a cluster.

OUR FORMALIZATION: NONE. The paired result comes from the shipped default opening run.

TENSION: The label “different houses” makes the grouping easy to read. The continuation can depend on details the signature deliberately omits.

MISSING: A measure of how much knowledge, location, or cut position varies inside a group.

BOUNDARY: The 589 figure counts observed signatures under the implemented rule. It does not count full ledger states or classes of interchangeable continuations.

CITATION TRAIL: In crossed.js, compare signature, agentStep, and openings. The two continued assignments are 1232343590237 and 1176469771756. Jacomy et al.’s Grounded AI Map offers a related question about keeping individual cases accessible after grouping.

TEST: Reopen both prefixes and inspect deed III. Compare the rooms, who learns what, and the next-deed distributions before judging whether one opening can stand for both.

WRITE-UP: “We grouped openings by a compact description of the tenants. A group can contain histories with different evidence and continuations, so its representative serves as a way into the group.”

PLATFORM: [[Abominable House methods]]

LINKS:
[[house-what-the-count-counts]]
[[house-trace-attribution]]

BIBTEX:
@inproceedings{pierazzo2025variants,
  author = {Pierazzo, Elena},
  title = {What Do You Do with 8 Thousand Billion Variants? Toward Structural and Quantitative Philology},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  url = {https://zenodo.org/records/19494802}
}
@misc{hartsoe2026houseopenings,
  author = {Hartsoe, Watson},
  title = {Abominable House Film Bank Opening Analysis},
  year = {2026},
  url = {https://github.com/hartswf0/bolas/blob/0ef3a04103f4f16d96ab9684a0bfc73e101225e9/paeleo/abominable-house/live/crossed.js}
}
```

```text
ZETTEL

ID: house-observer-enters

TITLE: The forecast gets the fire right and contains the intervention that follows it

SOURCE: Italo Calvino — The Burning of the Abominable House — closing sequence. Abominable House — The House Is Occupied, script and “How It Is Made.”

PASSAGE: [PARAPHRASE] Calvino’s Waldemar discovers that Skiller supplied evidence and noise to a second programmer to test whether the insurer’s involvement could be reconstructed. In The House Is Occupied, Skiller asks for an observer who stays outside. Waldemar reports the forecast and enters anyway. The fire occurs at the predicted time, and the printed image turns out to depict the rescue.

RESEARCH OBJECT: A forecast whose evidence includes the observer becoming a participant.

LOCAL MOVE: The follow-up takes Calvino’s implicated investigator from retrospective reconstruction to an intervention before the event.

SOURCE TERMS: second programmer, noise, observer, participant, forecast, rescue.

WHAT BECAME STRANGE: [OUR INFERENCE] The follow-up gives the audience a concrete reason to distinguish a correct forecast from an independent test. The forecaster’s image travels into the chain of action that the image depicts.

QUESTION: What does a correct prediction establish when people can act on the prediction before the event occurs?

MECHANISM: The forecast names a time and supplies an image. Waldemar reports it, crosses the yard, and enters. The later scene reveals what the earlier image depicts. The production notes state that the dot-matrix image is derived from the film’s own rescue frame.

FORMAL SHIFT:
<forecast at 21:06> → <evidence received by a character> → [report and enter] → <21:17 event with an intervening observer>

SOURCE FORMALISM: The production notes describe sampling the rescue frame into a dot grid for the forecast image.

OUR FORMALIZATION: NONE. A causal account of the fire and a causal account of the rescue should be drawn separately if the scene is diagrammed.

TENSION: The film confirms the fire and the image in the same sequence. It leaves the audience to decide what kind of success each confirmation represents.

MISSING: The counterfactual history in which Waldemar stays outside.

BOUNDARY: The screenplay establishes the sequence of disclosure, action, and rescue. It does not establish that reading the forecast caused the fire.

CITATION TRAIL: Put Calvino’s closing paragraphs beside the follow-up’s 21:06 forecast, 21:16 shutter order, and 21:17 fire.

TEST: Ask two readers to identify what the forecast correctly predicts before and after the image is identified as the rescue. Record which inferences depend on the later reveal.

WRITE-UP: “The House Is Occupied moves Calvino’s second programmer upstream. Its most consequential forecast is an image that the observer helps bring about by acting on it.”

PLATFORM: [[Calvino adaptation argument]]

LINKS:
[[house-trace-attribution]]
[[house-disclosure-clock]]

BIBTEX:
@incollection{calvino1995abominable,
  author = {Calvino, Italo},
  title = {The Burning of the Abominable House},
  booktitle = {Numbers in the Dark and Other Stories},
  translator = {Parks, Tim},
  publisher = {Pantheon Books},
  year = {1995}
}
@misc{hartsoe2026occupied,
  author = {Hartsoe, Watson},
  title = {The House Is Occupied},
  year = {2026},
  url = {https://hartswf0.github.io/2700-fa26/LAB%207%20-%20CLASSES/house-is-occupied/index.html}
}
```

```text
ZETTEL

ID: house-film-citation

TITLE: A film number lets the reader recover the casting, while the cut needs its own citation

SOURCE: Sebastian Enns, Maximilian Michel, and Andreas Kuczera — Algorithmic Edition — DH2025, pp. 231–233. Abominable House — film.html and player.html, film-number encoding.

PASSAGE: [PARAPHRASE] Enns and colleagues distinguish references tied to page offsets from citations that identify a passage, check its integrity, and can recover an earlier state. The Film Bank and Deed Bank use the same film number to recover the same sequence of pairs.

RESEARCH OBJECT: The smallest reference that lets a reader inspect a particular claim about a generated film.

LOCAL MOVE: Apply versioned passage citation to a film whose presentation is assembled from code.

SOURCE TERMS: Explicitly Notated Citations, UUID, hash, film number, pace, cut.

WHAT BECAME STRANGE: [CODE INSPECTION] The number survives a move between the Film Bank and the Deed Bank. Their presentations differ. The Film Bank’s `n` URL carries the twelve pairs, while its opening stop and pace are separate state. A link can recover the right assignment and still miss the cited beat.

QUESTION: Which object is a sentence in the paper citing: a deed assignment, a ledger transition, a rendered cut, or an interaction with the interface?

MECHANISM: Both banks decode the same base-12 number. The renderer separately applies a pace, builds timed segments, and may stop a generated opening before all twelve deeds play.

FORMAL SHIFT:
<claim about a beat> → <film ID, deed or segment, presentation settings, code version> → [reopen the cited state] → <inspectable evidence>

SOURCE FORMALISM: Enns et al. use persistent character IDs and a hash, with a versioned representation for earlier states. The Film Bank’s existing cross-links encode the assignment in `n`.

OUR FORMALIZATION:
[OUR FORMALIZATION — NOT SOURCE SYNTAX]
Cite an assignment by film number. Cite a particular disclosure by film number, deed or segment, pace or named render, and revision. Include the stopping point when it matters.

TENSION: A compact identifier is ideal for browsing possibilities. A critical claim needs enough information to recover the exact thing the author saw.

MISSING: A public permalink that captures a complete screening state in one address.

BOUNDARY: The proposed citation fields are a write-up convention. The deployed `n` parameter itself does not encode them.

CITATION TRAIL: Enns et al., “Explicitly Notated Citations.” For the live artifact, compare the `setFilm` functions in the two banks.

TEST: Cite the stopped opening for assignment 1232343590237. Open the ordinary `n` URL in a fresh tab. Record what it recovers, then supply the stopping point separately and check that the argument can be inspected.

WRITE-UP: “Film numbers identify cast assignments across the two banks. References to a shot, disclosure, or stopping point also specify the presentation and revision.”

PLATFORM: [[Abominable House methods]]

LINKS:
[[house-disclosure-clock]]
[[house-opening-representatives]]

BIBTEX:
@inproceedings{ennsEtAl2025algorithmic,
  author = {Enns, Sebastian and Michel, Maximilian and Kuczera, Andreas},
  title = {Algorithmic Edition},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  pages = {231--233},
  url = {https://zenodo.org/records/19494802}
}
```

```text
ZETTEL

ID: house-gesture-as-evidence

TITLE: A change in the sack’s movement can change who looks responsible

SOURCE: Peter Broadwell et al. — The Director’s Signature — DH2025, pp. 173–175. Ugur Onal et al. — Comparing Human and AI Performance in Visual Storytelling through Creation of Comic Strips — DH2025, pp. 120–123. Abominable House — Film Bank, LEVERS.

PASSAGE: [PARAPHRASE] Broadwell and colleagues distinguish classifying performances by pose features from explaining the gestures behind the classification. Onal and colleagues show how a small change in drawn eyes can shift a reader’s inference from accidental discovery to deliberate intrusion.

RESEARCH OBJECT: A viewer’s attribution of intention when the same deed is staged with different movement cues.

LOCAL MOVE: Shift the question from whether the flour sacks look expressive to what the viewer infers from one controlled change in the performance.

SOURCE TERMS: pose embeddings, movelets, choreography, expressive cues, levers.

WHAT BECAME STRANGE: [OUR INFERENCE] The ledger can fix who acted and what happened while the rendered performance changes whether the act looks calculated, reluctant, or forced. The difference matters in a film about reconstructing responsibility from appearances.

QUESTION: Which movement or lighting cue first makes viewers attribute intent to one sack?

MECHANISM: The renderer can apply state-dependent compositing to the sack layers, including apparent size, greying, halo, and shadow. The LEVERS control lets the same assignment be viewed with or without that compositing.

FORMAL SHIFT:
<same recorded deed> → <two presentations with different cues> → [compare attributions and cited moments] → <evidence about the performance>

SOURCE FORMALISM: The Film Bank implements the rendering toggle. The two studies supply methods and examples for examining expressive cues. They did not study these films.

OUR FORMALIZATION: NONE. Start with one shot and a matched pair of presentations.

TENSION: A visual cue can communicate the ledger’s current characterization. It can also make a character look guilty before the deed gives the viewer grounds to say so.

MISSING: Viewer accounts tied to particular frames or sounds.

BOUNDARY: The toggle provides a controlled rendering comparison. A difference in how the audience reads it still needs observation.

CITATION TRAIL: Broadwell et al., “Results,” on retrieving examples behind aggregate pose scores. Onal et al., Figures 1–2, for minimal expressive changes.

TEST: Show deed XI, Snooping, from the same assignment with LEVERS on and off. Keep the crop and sound fixed. Ask viewers whether the act looks deliberate and which visible moment informed their answer.

WRITE-UP: “The flour sacks make responsibility a question of performance. The same recorded deed can be staged with different visual cues, allowing us to test what makes an intention legible.”

PLATFORM: [[Flour-sack performance as evidence]]

LINKS:
[[house-disclosure-clock]]
[[house-presence-and-witnessing]]

BIBTEX:
@inproceedings{broadwellEtAl2025signature,
  author = {Broadwell, Peter and Rau, Michael and Wiles, Simon and Abraham, Vijoy},
  title = {The Director's Signature: Stylometry of Theater Choreography via Pose and Action Estimation},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  url = {https://zenodo.org/records/19494802}
}
@inproceedings{onalEtAl2025comics,
  author = {Onal, Ugur and Sariel, Sanem and Sezgin, Metin and Akleman, Ergun},
  title = {Comparing Human and {AI} Performance in Visual Storytelling through Creation of Comic Strips: A Case Study},
  booktitle = {Digital Humanities 2025: Book of Abstracts},
  year = {2025},
  url = {https://zenodo.org/records/19494802}
}
```