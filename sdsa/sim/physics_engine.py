from __future__ import annotations

import math
import random

from sdsa.core.models import SimulationResult, SimulationSpec


class PhysicsEngine:
    """Moteur de simulation simplifié multi-physique (prototype)."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)

    def run(self, spec: SimulationSpec) -> SimulationResult:
        base = 0.55
        if "thermal" in spec.physics_domains:
            base += 0.1
        if "electrochemical" in spec.physics_domains:
            base += 0.12
        if "mechanical" in spec.physics_domains:
            base += 0.08

        fidelity_factor = {
            "low": 0.92,
            "medium": 1.0,
            "high": 1.08,
        }.get(spec.fidelity, 1.0)
        noise = self._rng.uniform(-0.03, 0.03)

        performance = max(0.0, min(1.0, base * fidelity_factor + noise))
        risk = max(0.0, min(1.0, 1.0 - performance + self._rng.uniform(0, 0.08)))
        cost_proxy = 100.0 / (0.35 + performance)

        residual = abs(math.sin(performance * math.pi)) * 1e-5
        converged = residual < spec.tolerance * 20

        return SimulationResult(
            simulation_id=spec.simulation_id,
            status="completed" if converged else "warning",
            convergence=converged,
            kpis={
                "performance_index": round(performance, 4),
                "risk_index": round(risk, 4),
                "cost_proxy": round(cost_proxy, 2),
            },
            uncertainty={
                "aleatoric_std": round(0.02 + self._rng.uniform(0.0, 0.02), 4),
                "epistemic_std": round(0.03 + self._rng.uniform(0.0, 0.03), 4),
            },
            notes="Prototype basse fidélité - remplacer par solveurs FEM/FVM/PDE réels.",
        )
