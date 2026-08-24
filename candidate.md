Based on recent 2025–2026 studies, here are concrete additions—new shape entries, schema extensions, and methodological reinforcements—that could strengthen the shape-index repository.
1.  New shape entries to populate
The seed entry supply_coupled_draw uses a switch-and-gate signature. Several well-documented cross-domain patterns now have sufficient empirical support to be drafted as new entries.
threshold_gated_switch (or threshold_gated_release)
•  Structural slots: gate_type=THRESHOLD, switch_direction=BIDIRECTIONAL or RELEASE, switch_periodicity=APERIODIC
•  Constraint: boundary-condition / conservation limit
•  Cross-domain instances:
•  Energy economics: South Africa’s energy transition shows a 56.4 % renewable-energy threshold that triggers a regime shift from high-carbon to low-carbon development patterns; below the threshold, emissions rise with GDP, above it they decouple cite🛠web_search:11#1:~:text=The threshold-switching dynamic models...56.4% renewable energy threshold...
•  Biology / medicine: Critical transitions in asthma attacks, epileptic seizures, microbiome dysregulation, and cardiac arrhythmia all share the same threshold-escape structure—abrupt shifts between qualitatively different states once a control parameter crosses a tipping point cite🛠web_search:11#0:~:text=In biology, critical transitions are associated with asthma attacks...epileptic seizures...and cardiac arrhythmia...
•  Physics / materials: Magnetic domain experiments show that discontinuous change in spatially complex systems under stress “represents common generic stress-response behavior” across ecosystems and multidomain magnetic materials, with hysteresis-gated Barkhausen steps acting as the threshold mechanism cite🛠web_search:10#2:~:text=discontinuous change in spatially complex ecosystem models and multidomain magnetic materials represents common generic stress-response behavior...
state_gated_bidirectional (homeostatic regulation)
•  Structural slots: gate_type=STATE, switch_direction=BIDIRECTIONAL, switch_periodicity=APERIODIC or PERIODIC
•  Constraint: set-point maintenance / negative-feedback boundary
•  Cross-domain instances:
•  Neuroscience: A 2021 model of the olivocerebellar loop introduces a gating variable α that turns homeostatic plasticity on when sensor error is large (α → 1) and off when activity converges to target (α → 0), producing bidirectional upbound/downbound regulation cite🛠web_search:10#1:~:text=Our aim was to construct a single feedback signal that can be used to detect whether the activity is within target or not...
•  Engineering: Thermostats and climate-control systems switch bidirectionally (heating vs. cooling) gated on the current temperature state relative to a set point cite🛠web_search:4#2:~:text=bidirectional homeostatic systems regulate deviations from a set point in two directions...
•  Physiology: Blood-glucose regulation switches between insulin release (decrease glucose) and glucagon release (increase glucose) gated on the current glucose state cite🛠web_search:9#5:~:text=Rising glucose triggers insulin release...falling glucose triggers glucagon release...
demand_gated_increase (positive-feedback / runaway amplification)
•  Structural slots: gate_type=DEMAND, switch_direction=INCREASE, switch_periodicity=APERIODIC
•  Constraint: self-reinforcement / amplification
•  Cross-domain instances:
•  Economics / energy: Renewable-energy deployment exhibits positive feedback where “increasing REC creates learning curve benefits that further reduce costs and accelerate adoption” once demand crosses a critical mass cite🛠web_search:11#1:~:text=positive feedback effects where increasing REC creates learning curve benefits...
•  Ecology / evolution: Coevolutionary arms races (e.g., nectarivorous birds and flowers) act as demand-gated increases where each species’ adaptation creates new selection pressure driving further escalation cite🛠web_search:9#5:~:text=Each adaptation by one species creates a new selection pressure on the other—a positive feedback loop...
•  Immunology / oncology: Tumor-immune interactions follow predator-prey dynamics where predator (immune-cell) birth rates increase linearly with prey (tumor-cell) density, a demand-gated increase in effector recruitment cite🛠web_search:4#1:~:text=The functional response is the rate...predator’s birth rate increases linearly with the rate of prey consumption...
hysteresis_gated_switch
•  Structural slots: gate_type=THRESHOLD (but with path-dependent on/off thresholds), switch_direction=BIDIRECTIONAL, switch_periodicity=APERIODIC
•  Constraint: history-dependence / irreversibility
•  Cross-domain instances:
•  Physics / engineering: Ferromagnetic materials, thermostats, Schmitt triggers, and noise gates all use hysteresis to prevent unwanted rapid switching; the on-threshold and off-threshold differ based on history cite🛠web_search:5#5:~:text=Hysteresis occurs in ferromagnetic and ferroelectric materials...thermostats and Schmitt triggers...
•  Phonetics / biomechanics: Vocal-fold voicing exhibits two distinct thresholds—one for stopping oscillation as folds move apart, another for starting oscillation as they come together—creating a quantal jump in devoicing duration cite🛠web_search:5#3:~:text=As the vocal folds move apart...threshold at which the oscillation stops...
•  Environmental economics: The “ratchet effect” shows asymmetric responses to positive vs. negative shocks (renewable-energy expansion reduces emissions more than contraction increases them), indicating path-dependent regime switching cite🛠web_search:11#1:~:text=asymmetric effects identified in this model provide direct support for the ratchet effect theory...
cascading_failure (capacity-load switch)
•  Structural slots: gate_type=THRESHOLD (capacity exceeded), switch_direction=DECREASE, switch_periodicity=APERIODIC
•  Constraint: load/capacity balance
•  Cross-domain instances:
•  Supply-chain / infrastructure: Centralized supply-chain networks show that core node failures “can reduce system efficiency by 30–50% and trigger cross-domain collapses” through exponential decision delays and domino effects cite🛠web_search:6#4:~:text=core failures can reduce system efficiency by 30–50%...trigger cross-domain collapses...
----
2.  Schema and controlled-vocabulary extensions
Recent work suggests fields that would make the index more discriminating without reintroducing vocabulary-based matching.
Add scale and atomic_unit fields
Farzulla’s Replicator-Optimization Mechanism (ROM) formalizes persistence-conditioned dynamics by explicitly parameterizing scale and atomic unit (e.g., molecule, cell, organism, institution) cite🛠web_search:8#0:~:text=scale-relative, kernel-parametric framework...explicitly specifying scale, atomic units, interaction topologies... Adding these to the schema would let entries record whether a threshold_gated_switch at the cellular scale (ion-channel gating) is being matched to one at the institutional scale (energy-policy transition).
Add transition_type (soft vs. hard)
A 2025 magnetic-experiment perspective argues that the classic fold-bifurcation model of tipping points should be “restricted to describing simple systems,” while most real systems show “soft, incremental rather than hard, abrupt change” cite🛠web_search:10#2:~:text=classic fold bifurcation model should be restricted to describing simple systems...soft, incremental rather than hard, abrupt change... A transition_type slot with values {ABRUPT, GRADUAL} would capture this distinction without collapsing into domain-specific vocabulary.
Expand the constraint controlled vocabulary
Zertuche’s Constraint-Based Framework for Cross-Domain Emergence derives four minimal viability-level constraints that make persistence possible across domains: configurational multiplicity, constraint enforcement, information persistence, and irreversibility cite🛠web_search:8#5:~:text=four minimal viability-level generative constraints: configurational multiplicity, constraint enforcement, information persistence, and irreversibility... These could be added as a constraint sub-vocabulary or as tags, strengthening the repository’s premise that “the constraint is a first-class field.”
----
3.  Methodological reinforcements for match.py, FALSIFIER.md, and OPEN.md
Isomorphic Mapping as a falsification protocol
Zertuche introduces Isomorphic Mapping explicitly as “a filter for rejecting unwarranted cross-domain claims” rather than a tool for discovering similarity cite🛠web_search:8#5:~:text=Isomorphic Mapping is not a tool for discovering similarity. It is a filter for rejecting unwarranted cross-domain claims... This aligns with shape-index’s ethos that “a high overlap is a prompt to check, not a finding.” The FALSIFIER.md could incorporate Isomorphic Mapping’s three criteria: abstraction, null-model comparison, and evaluation across multiple dimensions.
ε-tolerant isomorphism for scoring
Hsu’s Tonal Isomorphism methodology defines ≈ε (epsilon-tolerant isomorphism) with explicit deviation functionals and non-transitivity warnings: “a mapping A → B and B → C does not guarantee a valid isomorphism A → C, as deviation can accumulate beyond the tolerance ε” cite🛠web_search:9#2:~:text=≈ε: ε-tolerant isomorphism...a mapping A → B and B → C does not guarantee a valid isomorphism A → C... This provides a formal footing for why match.py keeps structural and lexical layers separate and never blends them into a single headline number.
Cross-domain reasoning primitives as validation evidence
The CrossTrace dataset (1,389 grounded reasoning traces) demonstrates that models trained on balanced biomedical + CS data achieve 99.3 % / 99.7 % of domain-specialist performance in hypothesis generation, suggesting that “the form of scientific reasoning is substantially domain-general” cite🛠web_search:8#1:~:text=a model trained on equal parts biomedical and CS data achieves 99.3%/99.7% of domain-specialist performance... Bouras also annotates eight recurring discovery patterns (gap fill, analogy transfer, mechanistic link, incremental extension, contradiction exploit, data driven, Swanson ABC, replication) cite🛠web_search:8#1:~:text=Eight recurring patterns (gap fill, Swanson ABC, analogy transfer, and others)... These patterns could inform how new shapes are discovered and how CANDIDATES.md is structured.
Structured analogy frameworks as operational precedents
A 2026 survey of cross-domain R&D methods notes that TRIZ, Design-by-Analogy, and biomimicry all follow a four-stage process: (1) problem abstraction into domain-neutral functional language, (2) source-domain identification, (3) analogical mapping of structural correspondences, and (4) solution re-specification cite🛠web_search:9#7:~:text=problem abstraction into domain-neutral functional language...analogical mapping of source-to-target structural correspondences... This validates shape-index’s choice to record shapes in controlled structural terms rather than free text.
----
4.  Suggested implementation priority
Priority	Action	Supporting source
Immediate	Draft threshold_gated_switch entry with climate-energy and biology instances; draft state_gated_bidirectional with neuroscience and engineering instances.
Short-term	Validate hysteresis_gated_switch across physics, phonetics, and economics; validate demand_gated_increase across ecology, immunology, and energy economics.
Methodological	Update FALSIFIER.md with Isomorphic Mapping criteria; add scale and atomic_unit to schema; consider transition_type slot.
Vocabulary	Add Zertuche’s four viability constraints as a constraint sub-vocabulary.
These additions keep the repository’s core rule intact—the searchable unit is the shape, not the vocabulary—while giving it a stronger empirical base and more precise tools for rejecting false matches.
