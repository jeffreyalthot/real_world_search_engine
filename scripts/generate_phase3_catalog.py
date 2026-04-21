"""Générateur déterministe du pack de blueprints SDSA phase 3.

Usage:
    python scripts/generate_phase3_catalog.py --output sdsa/catalog/objective_blueprints_phase3.py --count 1500
"""

from __future__ import annotations

import argparse
from pathlib import Path

DOMAINS: list[tuple[str, str]] = [
    ("energy_storage", "densité énergétique"),
    ("materials", "stabilité structurale"),
    ("climate_tech", "efficacité carbone"),
    ("biotech", "sélectivité biochimique"),
    ("manufacturing", "rendement industriel"),
    ("electronics", "fiabilité électronique"),
    ("quantum", "cohérence quantique"),
    ("aerospace", "fiabilité mission"),
    ("robotics", "autonomie robotique"),
    ("agritech", "productivité agri"),
    ("water_systems", "efficacité hydrique"),
    ("health_ai", "précision clinique"),
]

HORIZONS = ["court_terme", "moyen_terme", "long_terme", "moonshot"]


def build_catalog(count: int, *, start_index: int = 3300) -> str:
    lines: list[str] = [
        '"""Pack massif d\'objectifs R&D SDSA (phase 3).\n\n',
        "Ce module ajoute des programmes transverses orientés résilience,\n",
        "interopérabilité et déploiement global multi-domaines.\n",
        '"""\n',
        "from __future__ import annotations\n\n",
        "from sdsa.catalog.objective_blueprints import ObjectiveBlueprint\n\n",
        "OBJECTIVE_BLUEPRINTS_PHASE3: list[ObjectiveBlueprint] = [\n",
    ]

    for offset in range(count):
        objective_id = start_index + offset
        domain, target_metric = DOMAINS[offset % len(DOMAINS)]
        horizon = HORIZONS[offset % len(HORIZONS)]
        trl = (offset % 9) + 1
        window = 2026 + (offset % 12)

        lines.extend(
            [
                "    {\n",
                f'        "objective_id": "obj-{objective_id}-p3",\n',
                f'        "title": "Programme {objective_id} phase 3: convergence {domain} orientée résilience systémique",\n',
                f'        "domain": "{domain}",\n',
                (
                    '        "mechanism_hint": "Fusionner orchestration multi-agents, '
                    f'preuve formelle et optimisation robuste pour cohorte {objective_id}",\n'
                ),
                f'        "target_metric": "{target_metric} > {190 + (offset % 110)}",\n',
                f'        "risk_guardrail": "Risque opérationnel <= {4 + (offset % 6)}% avec contrôle TRL {trl}",\n',
                f'        "horizon": "{horizon}",\n',
                "        \"keywords\": [\n",
                f'            "phase3_cluster_{offset % 180}",\n',
                f'            "trl_{trl}",\n',
                f'            "interoperability_{offset % 35}",\n',
                f'            "window_{window}",\n',
                f'            "resilience_wave_{offset % 50}",\n',
                f'            "platform_sync_{offset % 22}",\n',
                "        ],\n",
                "    },\n",
            ]
        )

    lines.append("]\n")
    return "".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate SDSA phase 3 objective catalog")
    parser.add_argument("--output", default="sdsa/catalog/objective_blueprints_phase3.py")
    parser.add_argument("--count", type=int, default=1500)
    parser.add_argument("--start-index", type=int, default=3300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    content = build_catalog(args.count, start_index=args.start_index)
    output = Path(args.output)
    output.write_text(content, encoding="utf-8")
    print(f"Generated {args.count} phase 3 blueprints into {output}")


if __name__ == "__main__":
    main()
