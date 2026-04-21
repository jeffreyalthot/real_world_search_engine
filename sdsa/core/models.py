from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class ProvenanceRef:
    source_id: str
    source_type: str
    version: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class ScientificClaim:
    claim_id: str
    statement: str
    domain: str
    confidence: ConfidenceLevel
    supports: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    provenance: List[ProvenanceRef] = field(default_factory=list)


@dataclass(slots=True)
class Hypothesis:
    hypothesis_id: str
    objective: str
    mechanism: str
    constraints: Dict[str, str]
    novelty_score: float
    testability_score: float


@dataclass(slots=True)
class SimulationSpec:
    simulation_id: str
    hypothesis_id: str
    physics_domains: List[str]
    fidelity: str
    solver: str
    max_steps: int = 1000
    tolerance: float = 1e-6


@dataclass(slots=True)
class SimulationResult:
    simulation_id: str
    status: str
    convergence: bool
    kpis: Dict[str, float]
    uncertainty: Dict[str, float]
    notes: str
