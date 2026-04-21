from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from sdsa.cli import build_orchestrator


class SdsaGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SDSA - Scientific Discovery Copilot")
        self.geometry("920x620")
        self.orchestrator = build_orchestrator()
        self._build_layout()

    def _build_layout(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)

        ttk.Label(root, text="Objectif technique", font=("Arial", 12, "bold")).pack(anchor="w")
        self.objective_var = tk.StringVar(value="Nouveau matériau de stockage énergie sûr et abordable")
        ttk.Entry(root, textvariable=self.objective_var).pack(fill=tk.X, pady=(4, 12))

        ttk.Label(root, text="Budget d'hypothèses", font=("Arial", 12, "bold")).pack(anchor="w")
        self.budget_var = tk.IntVar(value=5)
        ttk.Spinbox(root, from_=1, to=100, textvariable=self.budget_var).pack(anchor="w", pady=(4, 12))

        ttk.Button(root, text="Lancer pipeline", command=self._run_pipeline).pack(anchor="w")

        ttk.Label(root, text="Classement des concepts", font=("Arial", 12, "bold")).pack(anchor="w", pady=(16, 4))
        self.table = ttk.Treeview(root, columns=("id", "performance", "risk", "cost"), show="headings", height=18)
        for col in ("id", "performance", "risk", "cost"):
            self.table.heading(col, text=col)
            self.table.column(col, width=200 if col == "id" else 120)
        self.table.pack(fill=tk.BOTH, expand=True)

    def _run_pipeline(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        output = self.orchestrator.run(
            objective=self.objective_var.get(),
            budget=max(1, int(self.budget_var.get())),
        )
        for item in output.ranking:
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


def main() -> None:
    app = SdsaGui()
    app.mainloop()


if __name__ == "__main__":
    main()
