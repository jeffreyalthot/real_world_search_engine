# Système de Découverte Scientifique Assistée (SDSA)

## 1) Vision, périmètre et principes de conception

Le SDSA est une **infrastructure computationnelle distribuée** destinée à assister la recherche scientifique et l'ingénierie d'innovation. Il ne vise pas la vérité absolue : il agit comme un moteur probabiliste d'exploration, de simulation et de priorisation des hypothèses.

### 1.1 Objectifs opérationnels
- Agréger la littérature scientifique, les jeux de données, les brevets, les protocoles expérimentaux et les résultats de simulation.
- Structurer ces contenus dans un socle de connaissance formel interopérable (RDF/OWL + graphes de propriétés + index vectoriels).
- Générer des hypothèses testables en respectant les contraintes physiques et les invariants connus.
- Simuler numériquement des scénarios multi-physiques et multi-échelles.
- Transformer des hypothèses en concepts technologiques plausibles et scorés.

### 1.2 Principes non-fonctionnels
- **Traçabilité totale** : chaque assertion, équation, simulation et recommandation doit être explicable et versionnée.
- **Incertitude explicite** : tout résultat est associé à des intervalles de confiance, distributions et conditions de validité.
- **Modularité forte** : couches découplées via contrats API et schémas d'échange stables.
- **Évolutivité** : architecture orientée événements + microservices + calcul distribué CPU/GPU/HPC.
- **Sécurité scientifique** : garde-fous contre les extrapolations non physiques, données frauduleuses et dérives automatiques.

---

## 2) Architecture globale en couches

Le système suit 4 couches principales interconnectées :
1. **Knowledge Layer** (représentation de la connaissance scientifique)
2. **Physics Engine Layer** (simulation numérique)
3. **AI & Inference Layer** (raisonnement, génération, apprentissage)
4. **Invention Engine** (synthèse de concepts techniques exploitables)

### 2.1 Vue logique (pipeline)
1. Ingestion de sources hétérogènes
2. Extraction sémantique et normalisation
3. Construction du graphe de connaissance + index associés
4. Génération d'hypothèses sous contraintes
5. Compilation des hypothèses en modèles simulables
6. Simulations multi-fidélité
7. Évaluation multi-objectifs
8. Production de dossiers d'innovation (concept, preuves, limites, protocole expérimental)

### 2.2 Contrats inter-couches (interfaces)
- `Knowledge API`: requêtes SPARQL/GraphQL + retrieval vectoriel + requêtes causales.
- `Model API`: soumission de modèles physiques abstraits (DSL), maillage, solveurs, conditions limites.
- `Inference API`: génération/validation d'hypothèses, détection d'incohérences, plans d'expériences.
- `Innovation API`: optimisation de concept, scoring techno-éco-physique, export CAO conceptuel.

---

## 3) Couche de connaissance (Knowledge Layer)

## 3.1 Structure interne
Sous-modules :
1. **Connecteurs d'ingestion** (journaux, arXiv, PubMed, Crossref, USPTO/EPO, datasets publics, LIMS internes)
2. **NLP scientifique** (parsing PDF/LaTeX, NER scientifique, extraction d'équations, tableaux, unités)
3. **Normalisation** (entités, unités SI, taxonomies disciplinaires, résolution d'identité)
4. **Store de connaissance** :
   - Triple store RDF pour faits formels
   - Graphe de propriétés pour navigation performante
   - Index vectoriel pour similarité sémantique
   - Document store pour artefacts bruts (PDF, notebooks, protocoles)
5. **Moteur de qualité et contradiction** (détection de conflit, niveau de preuve, provenance)

## 3.2 Types de données manipulées
- Concepts scientifiques : `Entity(concept_id, label, domain, aliases)`
- Relations : causalité, composition, dépendance, corrélation, contradiction
- Lois et équations : forme symbolique + domaine de validité + hypothèses implicites
- Expériences : protocole, setup, métriques, incertitudes, répétabilité
- Observations : mesures horodatées avec unités et distribution d'erreur
- Sources : DOI, auteurs, date, revue, niveau de preuve

## 3.3 Schémas RDF / OWL (exemple minimal)
Préfixes : `sdsa:`, `prov:`, `qudt:`, `owl:`, `rdf:`, `xsd:`.

Classes OWL principales :
- `sdsa:ScientificConcept`
- `sdsa:PhysicalLaw`
- `sdsa:Equation`
- `sdsa:Experiment`
- `sdsa:Observation`
- `sdsa:Measurement`
- `sdsa:Hypothesis`
- `sdsa:SimulationRun`

Propriétés objet :
- `sdsa:explains(PhysicalLaw -> Observation)`
- `sdsa:testedBy(Hypothesis -> Experiment)`
- `sdsa:contradicts(Claim -> Claim)`
- `sdsa:hasAssumption(Model -> Assumption)`
- `sdsa:validIn(Equation -> Regime)`

Propriétés datatype :
- `sdsa:confidenceScore` (xsd:decimal)
- `sdsa:uncertaintyStd` (xsd:decimal)
- `sdsa:equationLatex` (xsd:string)
- `sdsa:doi` (xsd:string)
- `sdsa:timestamp` (xsd:dateTime)

## 3.4 Représentation d'une loi physique
Structure canonique :
- Identifiant unique
- Forme symbolique (AST mathématique + LaTeX)
- Variables, dimensions, unités
- Hypothèses (linéarité, isotropie, équilibre, etc.)
- Domaine de validité (échelles, température, pression, précision)
- Sources de preuve + score de robustesse

Exemple abstrait :
```json
{
  "law_id": "law:maxwell_faraday_v1",
  "equation_ast": "curl(E) + dB/dt = 0",
  "assumptions": ["milieu continu", "régime classique"],
  "validity_domain": {
    "scale": "macro",
    "frequency_hz": [0, 1e12]
  },
  "evidence": {
    "citations": ["doi:..."],
    "replication_score": 0.92
  }
}
```

## 3.5 Représentation d'une expérience
Champs requis :
- `protocol_id`, `materials`, `instrumentation`, `control_variables`, `noise_model`, `sample_size`, `statistics_plan`, `reproducibility_index`
- Lien bidirectionnel avec hypothèse et loi
- Encodage des métadonnées FAIR

## 3.6 Relier théorie et observation
- Un nœud `sdsa:Equation` prédit une variable observable.
- Un mapping `ObservationModel` relie grandeurs théoriques et capteurs réels.
- Un `LikelihoodModel` quantifie P(observation | modèle, paramètres).
- Le système met à jour la croyance (Bayes) sur les hypothèses.

## 3.7 Gestion des niveaux d'abstraction
- Niveau 0 : faits expérimentaux bruts
- Niveau 1 : relations empiriques
- Niveau 2 : modèles mécanistes
- Niveau 3 : principes unificateurs
- Niveau 4 : méta-théories / analogies inter-domaines

Passerelles entre niveaux via opérateurs : agrégation, réduction de modèle, homogénéisation, dimensionnalité réduite.

## 3.8 Gestion des contradictions scientifiques
- Graphe de revendications contradictoires avec pondération par qualité de preuve.
- Reconciliation par contexte (plage de paramètres différente).
- Détection automatique des contradictions logiques et dimensionnelles.
- Statut de claim : `supported`, `contested`, `deprecated`, `contextual`.

## 3.9 Ingestion automatique et NLP
Pipeline :
1. OCR/parse PDF + LaTeX equation extraction
2. Segmentation sectionnelle (méthodes, résultats, limites)
3. NER scientifique (matériaux, équations, constantes, protocoles)
4. Extraction relationnelle et causalité
5. Normalisation unités (SI) et résolution d'entités
6. Insertion transactionnelle versionnée dans le graphe

---

## 4) Couche de simulation physique (Physics Engine Layer)

## 4.1 Structure interne
- **Model Compiler** : convertit les modèles abstraits en problèmes numériques.
- **Mesh & Discretization Service** : maillage adaptatif, raffinement local.
- **Solver Runtime** : solveurs PDE/ODE/DAE, linéaires/non-linéaires, explicites/implicites.
- **Coupling Orchestrator** : co-simulation multi-physique.
- **Uncertainty Engine** : propagation Monte Carlo, Polynomial Chaos, intervalles.
- **Result Store** : champs simulés, métriques, diagnostics de convergence.

## 4.2 Modèles mathématiques et algorithmes
- PDE : Navier-Stokes, Maxwell, diffusion-chaleur, élasticité, réaction-diffusion.
- Discrétisation :
  - FEM pour géométries complexes
  - FDM pour grilles structurées
  - FVM pour conservation robuste
  - Méthodes spectrales pour haute précision
- Intégration temporelle : Runge-Kutta, BDF, Crank-Nicolson
- Solveurs : GMRES, CG, multigrille, Newton-Krylov
- Réduction de modèle : POD, ROM, surrogate models (PINN/GP)

## 4.3 Modules de simulation requis
- Électromagnétique : ondes, induction, couplage EM-matière
- Thermique : conduction, convection, rayonnement
- Mécanique : statique/dynamique, fatigue, rupture probabiliste
- Quantique approximative : DFT simplifiée, tight-binding, Monte Carlo quantique approximatif
- Chimie réactionnelle : cinétique, bilans matière/énergie, réseaux réactionnels

## 4.4 Entrées/sorties standardisées
Entrée (`SimulationSpec` JSON/Protobuf) :
- géométrie (CAD simplifié / maillage)
- propriétés matériaux (fonction de T, P, champ)
- conditions initiales et limites
- paramètres solveur (tolérance, pas de temps, schéma)
- budget de calcul et niveau de fidélité

Sortie (`SimulationResult`) :
- champs spatio-temporels (ex. température, contrainte, potentiel)
- KPI extraits (rendement, stabilité, coût énergétique)
- diagnostics (résidu, convergence, sensibilité)
- incertitude (IC, distributions)
- verdict de validité numérique

## 4.5 Gestion des erreurs et incertitudes
- Contrôles de stabilité (CFL, conditionnement)
- Détection de divergence et fallback vers solveur robuste
- Quantification d'incertitude (UQ) systématique
- Journal d'audit numérique (seed, version solveur, précision flottante)

## 4.6 Performance et scalabilité
- Décomposition de domaine MPI
- Accélération GPU (CUDA/ROCm) pour kernels de solveur
- Scheduling adaptatif selon coût/valeur d'information
- Hiérarchie multi-fidélité : rapide (surrogate) -> intermédiaire -> haute fidélité HPC

---

## 5) Couche d'intelligence et d'inférence (AI & Inference)

## 5.1 Architecture hybride neuro-symbolique
Composants :
- **LLM scientifique** : lecture/raisonnement textuel, génération de candidates hypotheses.
- **Moteur symbolique** : logique du 1er ordre, solveurs SAT/SMT, vérification dimensionnelle.
- **Systèmes experts** : règles métier par domaine (matériaux, énergie, bio, etc.).
- **Réseaux profonds spécialisés** : prédiction de propriétés, surrogate physics-informed.
- **Meta-Learner** : sélection adaptative de modèles et stratégies d'exploration.

## 5.2 A) Génération d'hypothèses
Algorithme proposé :
1. Sélection de frontière de connaissance (zones à forte incertitude + fort impact).
2. Recherche de combinaisons conceptuelles via graphe (motifs causaux, analogies inter-domaines).
3. Génération contrainte : invariants physiques, unités, bornes de stabilité.
4. Scoring initial : nouveauté, plausibilité, testabilité, coût expérimental.

Techniques :
- Beam search sur graphe conceptuel
- Program synthesis d'équations candidates
- Génération par contraintes (SMT) + LLM conditionné

## 5.3 B) Raisonnement scientifique
- Vérification logique de cohérence interne
- Validation dimensionnelle automatique
- Vérification contre lois non violables (conservation, causalité)
- Détection d'incompatibilités entre hypothèses et littérature de référence
- Production de preuves structurées (proof traces)

## 5.4 C) Apprentissage
- Supervisé : classification qualité d'hypothèse, régression de métriques physiques.
- Non supervisé : clustering de mécanismes, détection d'anomalies dans résultats de simulation.
- Renforcement : agent d'orchestration qui choisit prochaines simulations pour maximiser information utile.
- Active learning : demande ciblée d'expériences réelles minimisant l'incertitude globale.

## 5.5 Auto-amélioration
- Boucle continue : résultats -> recalibrage des modèles -> mise à jour des politiques d'exploration.
- Évaluation hors-ligne avant déploiement de nouveaux modèles.
- Gating de sûreté : un modèle ne peut influencer la production sans seuil de fiabilité.

---

## 6) Couche d'innovation (Invention Engine)

## 6.1 Pipeline obligatoire (implémentation)
1. **Définition d'objectif** (ex. stocker 2x plus d'énergie à coût constant)
2. **Extraction de contraintes** (physiques, matériaux, fabrication, réglementaires)
3. **Phénomènes exploitables** (effets physiques pertinents)
4. **Génération de concepts** (architectures, matériaux, topologies)
5. **Simulation** multi-fidélité
6. **Évaluation** multi-critères
7. **Optimisation** itérative
8. **Design conceptuel** (dossier technique + plan expérimental)

## 6.2 Algorithmes clés
- Évolutionnaires : NSGA-II/III, CMA-ES
- Optimisation bayésienne sous contraintes
- Recherche multi-objectifs (Pareto coût/performance/sécurité/durabilité)
- Topology optimization (SIMP, level-set)
- Scoring robuste sous incertitude

## 6.3 Fonction de scoring (exemple)
`Score = w1*PlausibilitePhysique + w2*Performance + w3*Fabricabilite + w4*Securite + w5*ImpactEco - w6*Cout - w7*Risque`

Chaque terme est normalisé et accompagné d'un intervalle de confiance.

## 6.4 Sortie attendue
- Concept d'invention classé
- Hypothèses et mécanismes explicatifs
- Résultats de simulation reproductibles
- Analyse risques/limites
- Plan d'expérimentation réel (protocole, capteurs, critères d'acceptation)

---

## 7) Modélisation de l'énergie

## 7.1 Types d'énergie et modèles
- Mécanique, thermique, électromagnétique, chimique, nucléaire, rayonnante.
- Représentation commune par bilans et potentiels :
  - Conservation énergie/masse
  - Rendements de conversion
  - Pertes dissipatives (Joule, frottements, rayonnement non utile)

## 7.2 Conversions et systèmes hybrides
- Graphe de conversion énergétique avec arcs pondérés (rendement, coût, maturité technologique).
- Détection de chaînes hybrides optimales (ex. thermoélectrique + stockage électrochimique).
- Optimisation dynamique selon usage, climat, profil de charge.

## 7.3 Détection d'opportunités
- Analyse exergétique pour localiser pertes irréversibles.
- Sensibilité globale (Sobol) pour identifier leviers dominants.
- Suggestion de reconfiguration topologique des systèmes énergétiques.

---

## 8) Paramètres fondamentaux et scénarios hypothétiques

## 8.1 Constantes physiques intégrées
Exemples : `c`, `G`, `h`, `k_B`, `e`, `epsilon_0`, `mu_0`, masses fondamentales.

Chaque constante est stockée avec :
- valeur SI
- incertitude
- source de référence
- dépendances de modèle

## 8.2 Simulation réaliste vs hypothétique
- **Mode réaliste** : constantes verrouillées aux valeurs de référence.
- **Mode hypothétique** : variations paramétriques contrôlées avec avertissement épistémique.

## 8.3 Propagation des variations
- Analyse locale : dérivées de sensibilité.
- Analyse globale : plans d'expériences + UQ.
- Cartographie des ruptures de validité de modèle quand les constantes sont perturbées.

---

## 9) Limites et contraintes du système

## 9.1 Limites épistémiques
- Qualité inégale des publications
- Biais de publication
- Corrélations confondues avec causalité

## 9.2 Limites computationnelles
- Coût prohibitif des simulations haute fidélité
- Explosions combinatoires dans l'espace des hypothèses
- Besoin de compromis latence/précision

## 9.3 Dépendance aux données
- Couverture incomplète de certains domaines
- Données propriétaires non accessibles
- Reproductibilité variable

## 9.4 Gouvernance de l'incertitude
- Toutes les sorties incluent probabilité de validité et conditions d'application.
- Validation externe obligatoire pour toute décision critique.
- Protocoles de revue humaine et de red-team scientifique.

---

## 10) Stack technologique recommandée

## 10.1 Langages et runtimes
- Python (orchestration IA/science)
- Rust/C++ (noyaux performance, solveurs, sécurité mémoire)
- Julia (prototypage scientifique rapide)
- SQL + SPARQL + GraphQL

## 10.2 Données et stockage
- RDF triple store : GraphDB / Blazegraph / Stardog
- Graphe de propriétés : Neo4j / JanusGraph
- Vector DB : Milvus / Weaviate / pgvector
- Data lake objet : S3-compatible + format Parquet/Iceberg
- Metadata catalog : OpenMetadata / DataHub

## 10.3 IA et raisonnement
- LLM serving : vLLM/TGI
- Frameworks DL : PyTorch + JAX
- Symbolique : Z3/SMT, Prolog, moteur de règles Drools-like
- Orchestration ML : Ray + MLflow + Feast

## 10.4 Simulation et calcul
- Solveurs : PETSc, Trilinos, FEniCS, OpenFOAM, MOOSE
- HPC orchestration : Slurm + Kubernetes hybride
- MPI + NCCL + CUDA/ROCm

## 10.5 Architecture microservices
- Event bus : Kafka / NATS
- Workflow : Temporal / Argo Workflows
- API Gateway + service mesh (Istio/Linkerd)
- Observabilité : OpenTelemetry + Prometheus + Grafana
- Sécurité : IAM, secrets manager, chiffrement au repos/en transit

---

## 11) Flux de fonctionnement complet (de bout en bout)

## 11.1 Entrée
Entrée type : « Concevoir un matériau de stockage d'énergie plus sûr et à haute densité ».

## 11.2 Traitement
1. `Problem Formalizer` convertit l'objectif en contraintes quantitatives.
2. `Knowledge Retriever` extrait lois, matériaux, échecs connus, régimes opératoires.
3. `Hypothesis Generator` produit N hypothèses mécanistes.
4. `Scientific Verifier` élimine celles qui violent invariants et dimensions.
5. `Simulation Planner` assigne budgets compute et niveaux de fidélité.
6. `Physics Engine` exécute simulations + UQ.
7. `Innovation Optimizer` construit front de Pareto.
8. `Report Builder` génère design conceptuel et protocole expérimental.

## 11.3 Décisions prises par le système
- Prioriser hypothèses à fort gain d'information attendu.
- Escalader vers haute fidélité uniquement si signal prometteur.
- Rejeter toute solution non robuste à l'incertitude.

## 11.4 Critères d'évaluation
- Validité physique
- Performance cible
- Coût et fabricabilité
- Sécurité/réglementaire
- Durabilité et impact environnemental
- Niveau de preuve expérimental

---

## 12) Stratégie d'implémentation progressive

## Phase 1 (6-9 mois)
- Knowledge Layer minimal + ingestion automatisée + graphe scientifique initial.
- Génération d'hypothèses bornée à 1-2 domaines.
- Couplage avec 2 solveurs physiques existants.

## Phase 2 (9-18 mois)
- Orchestration multi-physique, UQ systématique, optimisation multi-objectifs.
- Boucle active learning avec premiers retours expérimentaux réels.

## Phase 3 (18-36 mois)
- Extension multi-domaines à grande échelle.
- Standardisation des protocoles d'innovation.
- Gouvernance scientifique complète (audit, conformité, éthique, sûreté).

---

## 13) Résultat attendu (objectif final)

Le SDSA permet :
- une exploration systématique, traçable et probabiliste de l'espace scientifique des possibles ;
- la proposition d'innovations techniquement crédibles et hiérarchisées ;
- une accélération mesurable du cycle « idée -> simulation -> test -> apprentissage » au service des équipes humaines de R&D.

Il reste explicitement borné par la qualité des données, les limites de calcul et la validation expérimentale externe.

---

## 14) Structures de données de référence (implémentables)

## 14.1 Modèle canonique d'hypothèse (`HypothesisRecord`)
```protobuf
message HypothesisRecord {
  string hypothesis_id = 1;
  string objective_id = 2;
  repeated string related_concept_ids = 3;
  string mechanistic_statement = 4;   // texte structuré
  string equation_program = 5;        // DSL compilable
  repeated Constraint constraints = 6;
  EvidenceProfile evidence = 7;
  PlausibilityProfile plausibility = 8;
  repeated string required_simulators = 9;
  map<string, double> priors = 10;
  string status = 11; // drafted|verified|simulated|rejected|promoted
}
```

## 14.2 Modèle de contrainte (`Constraint`)
- `type`: `physical|regulatory|manufacturing|cost|safety`
- `expression`: formule logique/algébrique (SMT-LIB ou DSL interne)
- `hardness`: `hard` (inviolable) vs `soft` (pénalisable)
- `context`: domaine de validité (température, échelle, environnement)

## 14.3 Modèle d'observation instrumentale
```json
{
  "observation_id": "obs:2026-04-21:lab17:0012",
  "instrument": {
    "type": "calorimeter",
    "calibration_curve_id": "cal:Q3-2026-17",
    "measurement_range": [0.0, 500.0]
  },
  "quantity": "specific_heat_capacity",
  "value": 1420.3,
  "unit": "J/(kg*K)",
  "uncertainty": {
    "type": "gaussian",
    "sigma": 11.6
  },
  "conditions": {
    "temperature_K": 298.15,
    "pressure_Pa": 101325
  },
  "provenance": {
    "operator": "lab_bot_3",
    "timestamp": "2026-04-21T10:15:00Z"
  }
}
```

## 14.4 Indexation multi-niveaux
- **Index sémantique**: `(entity_id -> embedding)` pour retrieval conceptuel.
- **Index équationnel**: hash canonique AST pour détecter équivalences algébriques.
- **Index dimensionnel**: signature `[M, L, T, I, Θ, N, J]` pour vérification d'unités.
- **Index causal**: motifs DAG annotés pour requêtes « mécanisme similaire ». 

---

## 15) Algorithmes centraux (pseudo-code opérationnel)

## 15.1 Génération d'hypothèses sous contraintes
```text
Input: Objective O, KnowledgeGraph K, ConstraintSet C, Budget B
Output: RankedHypotheses H*

1. frontier <- detect_unknown_frontier(K, O)
2. motifs <- mine_cross_domain_motifs(K, frontier)
3. candidates <- constrained_llm_generate(motifs, C)
4. candidates <- symbolic_filter(candidates, invariants=[conservation, causality, dimensions])
5. candidates <- novelty_filter(candidates, K)
6. for h in candidates:
       h.score_prior <- score_plausibility_testability(h)
7. H* <- top_k(candidates, k=B.initial_batch)
8. return H*
```

## 15.2 Orchestration multi-fidélité guidée par valeur d'information
```text
for each hypothesis h in active_set:
  run surrogate_sim(h)
  if uncertainty(h) > tau_u and expected_information_gain(h) > tau_eig:
      run medium_fidelity_sim(h)
  if passes_gate(h, robustness, safety, feasibility):
      run high_fidelity_hpc(h)
  update posterior(h)
```

## 15.3 Résolution de contradictions scientifiques
```text
Given claims c1..cn on same phenomenon:
  cluster by context regime (scale, material, T, P)
  for each cluster:
    compute evidence_weight = f(reproducibility, sample_size, bias_risk, recency)
    infer compatibility graph
    if incompatible:
      mark contested + propose discriminative experiment
```

---

## 16) Gouvernance, sûreté et auditabilité scientifique

## 16.1 Niveaux de validation avant promotion d'une innovation
- **V0 (formel)**: cohérence logique + dimensionnelle.
- **V1 (numérique)**: convergence solveur + stabilité paramétrique.
- **V2 (robustesse)**: sensibilité globale + stress tests scénarios extrêmes.
- **V3 (réalité)**: protocole expérimental externe pré-enregistré.
- **V4 (transfert)**: étude de fabricabilité + sécurité + conformité normative.

Aucune proposition ne passe au niveau supérieur sans artefacts de preuve signés et versionnés.

## 16.2 Traçabilité (ledger scientifique)
Chaque étape écrit un événement immuable:
- `event_id`, `parent_event_id`, `artifact_hash`, `model_version`, `dataset_snapshot`, `operator`.
- Permet replay complet d'un résultat et audit par tiers.

## 16.3 Politique anti-dérive
- Détection de data drift (population stability index, KL divergence).
- Détection de model drift (dégradation sur benchmarks gelés).
- Circuit de rollback automatique vers version stable certifiée.

---

## 17) SLO/SLA techniques et scalabilité cible

## 17.1 Objectifs de performance
- Latence requête connaissance P95 < 800 ms (hors batch lourd).
- Génération d'un lot de 100 hypothèses contraintes < 10 min.
- Planification + lancement de 10k simulations/jour en cluster mixte.
- Taux de reproductibilité simulation (re-run hash-identique) > 99.5%.

## 17.2 Scalabilité
- Partitionnement par domaine + sharding temporel pour données expérimentales.
- Exécution asynchrone orientée événements pour absorber des pics d'ingestion.
- Autoscaling séparé pour services NLP, inferencing LLM et solveurs HPC.

## 17.3 Coût de calcul (FinOps scientifique)
- Attribution coût par hypothèse (`cost_per_information_gain`).
- Arrêt anticipé des branches peu prometteuses (bandits / pruning).
- Priorisation green compute (fenêtres énergétiques bas carbone).

---

## 18) Exemple de déroulé complet (cas énergétique)

### Problème
« Concevoir un module de stockage stationnaire plus sûr que Li-ion, densité volumique > 450 Wh/L, coût < 90 €/kWh. »

### Exécution système
1. Formalisation en contraintes mathématiques et réglementaires.
2. Recherche dans le graphe de mécanismes alternatifs (sodium solide, redox organique, hybride thermo-électrochimique).
3. Génération de 320 hypothèses mécanistes, filtrage à 41 candidates physiquement valides.
4. Simulation surrogate sur 41 candidates, puis haute fidélité sur 7.
5. Optimisation multi-objectifs -> front de Pareto de 3 concepts.
6. Production du design conceptuel gagnant + protocole de validation labo + risques.

### Sortie
- Dossier technique versionné.
- Liste d'expériences discriminantes priorisées par gain d'information.
- Score de confiance explicite et limites d'applicabilité.

