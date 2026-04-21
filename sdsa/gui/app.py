from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from sdsa.cli import build_orchestrator
from sdsa.services.autonomous_creator import AutonomousCreator, DetailedBlueprint


class SdsaGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SDSA - Infinite Real-World Invention Studio")
        self.geometry("1340x860")

        self.creator = AutonomousCreator(build_orchestrator())
        self._loop_job: str | None = None

        self.objective_var = tk.StringVar(
            value="Créer des technologies inédites et réutiliser les créations précédentes pour inventer des systèmes plus complexes"
        )
        self.budget_var = tk.IntVar(value=6)
        self.status_var = tk.StringVar(value="Prêt")

        self._build_layout()

    def _build_layout(self) -> None:
        root = ttk.Frame(self, padding=10)
        root.pack(fill=tk.BOTH, expand=True)

        controls = ttk.LabelFrame(root, text="Contrôle moteur autonome", padding=8)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="Objectif d'amorçage").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.objective_var, width=140).grid(row=1, column=0, columnspan=6, sticky="ew", pady=4)

        ttk.Label(controls, text="Budget hypothèses").grid(row=0, column=6, sticky="w", padx=(8, 0))
        ttk.Spinbox(controls, from_=1, to=100, textvariable=self.budget_var, width=8).grid(row=1, column=6, sticky="w", padx=(8, 0))

        ttk.Button(controls, text="Exécuter 1 cycle", command=self._run_one_cycle).grid(row=1, column=7, padx=(8, 0))
        ttk.Button(controls, text="Démarrer boucle infinie", command=self._start_infinite_loop).grid(row=1, column=8, padx=(8, 0))
        ttk.Button(controls, text="Arrêter", command=self._stop_infinite_loop).grid(row=1, column=9, padx=(8, 0))

        ttk.Label(controls, textvariable=self.status_var).grid(row=1, column=10, sticky="e", padx=(12, 0))
        controls.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self._build_main_pages()
        self._build_specialized_pages(page_count=150)

    def _build_main_pages(self) -> None:
        self.dashboard_page = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_page, text="Dashboard")

        self.table = ttk.Treeview(
            self.dashboard_page,
            columns=("id", "performance", "risk", "cost"),
            show="headings",
            height=20,
        )
        for col in ("id", "performance", "risk", "cost"):
            self.table.heading(col, text=col)
            self.table.column(col, width=280 if col == "id" else 120)
        self.table.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.blueprint_page = ttk.Frame(self.notebook)
        self.notebook.add(self.blueprint_page, text="Blueprint détaillé")
        self.blueprint_text = tk.Text(self.blueprint_page, wrap="word")
        self.blueprint_text.pack(fill=tk.BOTH, expand=True)

        self.visual_page = ttk.Frame(self.notebook)
        self.notebook.add(self.visual_page, text="Visualisation")
        self.canvas = tk.Canvas(self.visual_page, bg="#0f172a")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.constraints_page = ttk.Frame(self.notebook)
        self.notebook.add(self.constraints_page, text="Contraintes monde réel")
        self.constraints_text = tk.Text(self.constraints_page, wrap="word")
        self.constraints_text.pack(fill=tk.BOTH, expand=True)

    def _build_specialized_pages(self, page_count: int) -> None:
        for page_idx in range(1, page_count + 1):
            frame = ttk.Frame(self.notebook)
            ttk.Label(
                frame,
                text=(
                    f"Page Spécification {page_idx} / {page_count}\n"
                    "Réservée à la décomposition détaillée: exigences, architecture, validation, risques, industrialisation."
                ),
                justify="left",
            ).pack(anchor="w", padx=10, pady=10)

            text = tk.Text(frame, height=16, wrap="word")
            text.insert(
                "1.0",
                (
                    f"[Template Page {page_idx}]\n"
                    "- Objectif local\n"
                    "- Contraintes physiques et réglementaires\n"
                    "- Métriques de succès\n"
                    "- Procédure expérimentale\n"
                    "- Conditions de passage à l'échelle\n"
                ),
            )
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            self.notebook.add(frame, text=f"Spec {page_idx}")

    def _run_one_cycle(self) -> None:
        output, blueprint = self.creator.run_cycle(
            objective_seed=self.objective_var.get(),
            budget=max(1, int(self.budget_var.get())),
        )
        self._render_results(output.ranking)
        self._render_blueprint(blueprint)
        self._render_visual(blueprint)
        self._render_constraints(blueprint)
        self.status_var.set(f"Cycle {self.creator.cycle_count} terminé | Concepts mémorisés: {len(self.creator.known_concepts)}")

    def _render_results(self, ranking: list[dict[str, float | str]]) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
        for item in ranking:
            self.table.insert(
                "",
                tk.END,
                values=(
                    item["hypothesis_id"],
                    item["performance"],
                    item["risk"],
                    item["cost"],
                ),
            )

    def _render_blueprint(self, blueprint: DetailedBlueprint) -> None:
        self.blueprint_text.delete("1.0", tk.END)
        self.blueprint_text.insert(tk.END, blueprint.human_readable_plan)

    def _render_constraints(self, blueprint: DetailedBlueprint) -> None:
        self.constraints_text.delete("1.0", tk.END)
        self.constraints_text.insert(tk.END, "CONTRAINTES MONDE RÉEL (obligatoires)\n\n")
        for key, value in blueprint.real_world_constraints.items():
            self.constraints_text.insert(tk.END, f"- {key.upper()}: {value}\n")
        self.constraints_text.insert(tk.END, "\nPROCESSUS REQUIS\n")
        for process in blueprint.required_processes:
            self.constraints_text.insert(tk.END, f"- {process}\n")

    def _render_visual(self, blueprint: DetailedBlueprint) -> None:
        self.canvas.delete("all")
        width = self.canvas.winfo_width() or 1200
        height = self.canvas.winfo_height() or 700

        self.canvas.create_text(20, 20, anchor="nw", fill="#f8fafc", text=blueprint.title, font=("Arial", 16, "bold"))
        self.canvas.create_text(20, 48, anchor="nw", fill="#93c5fd", text=blueprint.objective[:170], width=width - 40)

        # mini graphe visuel du pipeline
        x0, y0 = 100, 150
        node_w, node_h = 250, 80
        stages = ["Objective", "Hypothesis", "Simulation", "Blueprint", "Recursive Upgrade"]
        for idx, stage in enumerate(stages):
            x = x0 + idx * (node_w + 20)
            color = "#1d4ed8" if idx < 3 else "#0f766e"
            self.canvas.create_rectangle(x, y0, x + node_w, y0 + node_h, fill=color, outline="#e2e8f0", width=2)
            self.canvas.create_text(x + 16, y0 + 24, anchor="w", fill="white", text=stage, font=("Arial", 12, "bold"))
            self.canvas.create_text(
                x + 16,
                y0 + 52,
                anchor="w",
                fill="#dbeafe",
                text=f"Cycle={self.creator.cycle_count}",
                font=("Arial", 10),
            )
            if idx < len(stages) - 1:
                ax = x + node_w
                self.canvas.create_line(ax, y0 + node_h / 2, ax + 20, y0 + node_h / 2, fill="#cbd5e1", width=3, arrow=tk.LAST)

    def _start_infinite_loop(self) -> None:
        if self._loop_job is not None:
            return
        self.status_var.set("Boucle infinie en cours...")
        self._loop_forever()

    def _loop_forever(self) -> None:
        self._run_one_cycle()
        self._loop_job = self.after(1200, self._loop_forever)

    def _stop_infinite_loop(self) -> None:
        if self._loop_job is not None:
            self.after_cancel(self._loop_job)
            self._loop_job = None
        self.status_var.set(f"Boucle arrêtée à cycle {self.creator.cycle_count}")


def main() -> None:
    app = SdsaGui()
    app.mainloop()


if __name__ == "__main__":
    main()
